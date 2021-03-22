import pandas as pd
import numpy as np
import sklearn.preprocessing
from sklearn.model_selection import train_test_split
import os

from env import host, user, password

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_zillow_data():
    '''
    This function reads the zillow data from the Codeup db into a df,
    write it to a csv file, and returns the df.
    '''
    # Create SQL query.
    sql_query = ''' select parcelid, 
                        bathroomcnt, 
                        bedroomcnt,
                        calculatedfinishedsquarefeet,
                        fips,
                        latitude,
                        longitude,
                        lotsizesquarefeet,
                        regionidzip,
                        yearbuilt,
                        taxvaluedollarcnt,
                        taxamount,
                        transactiondate 
      from properties_2017
      join predictions_2017 using(parcelid)
      where transactiondate between "2017-05-01" and "2017-08-31"
      AND (unitcnt = 1 OR propertylandusetypeid IN (261, 279, 262, 263, 264, 266, 275));
                    '''
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df

def get_zillow_data(cached=False):
    '''
    This function reads in zillow data from Codeup database and writes data to
    a csv file if cached == False or if cached == True reads in telco df from
    a csv file, returns df.
    '''
    if cached == False or os.path.isfile('zillow.csv') == False:
        
        # Read fresh data from db into a DataFrame.
        df = new_zillow_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('zillow.csv')
        
    else:
        
        # If csv file exists or cached == True, read in data from csv.
        df = pd.read_csv('zillow.csv', index_col=1)
        
    return df

def clean_zillow(df):
    '''Takes in a df of zillow data and cleans the data by dropping null values, renaming columns, creating age column, and dealing with             outliers using 1.5x IQR    
    
    return: df, a cleaned pandas dataframe'''
    
    df = df.set_index('parcelid')  

    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df = df.dropna()
    df = df.rename(columns={"bedroomcnt": "bedrooms", "bathroomcnt": "bathrooms", "calculatedfinishedsquarefeet":    
                                    "square_feet","taxamount": "taxes", "taxvaluedollarcnt": "tax_value"})
    
    df['age_in_years'] = 2021 - df.yearbuilt
    df['Bathrooms'] = df.bathrooms.apply(lambda x: "4+" if x >= 4 else x)
    df['Bedrooms'] = df.bathrooms.apply(lambda x: "4+" if x >= 4 else x)
    df['tax_rate'] = round(((df.taxes / df.tax_value) * 100), 2)
    df = df.drop(columns=['yearbuilt','bathrooms','bedrooms']) 
    
    q1 = df.tax_value.quantile(.25)
    q3 = df.tax_value.quantile(.75)
    iqr = q3 - q1
    multiplier = 1.5
    upper_bound = q3 + (multiplier * iqr)
    lower_bound = q1 - (multiplier * iqr)
    df = df[df.tax_value > lower_bound]
    df = df[df.tax_value < upper_bound]
    
    return df

def split_zillow(df, stratify_by=None):
    """
    train, validate, test split
    To stratify, send in a column name
    """
    
    if stratify_by == None:
        train, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(df, test_size=.3, random_state=123)
    else:
        train_validate, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[stratify_by])
        train, validate = train_test_split(train_validate, test_size=.3, random_state=123, stratify=train_validate[stratify_by])
    
    return train, validate, test

def wrangle_zillow(split=False):
    '''
    wrangle_zillow will read zillow.csv as a pandas dataframe,
    clean the data
    split the data
    return: train, validate, test sets of pandas dataframes from zilow if split = True
    '''
    df = clean_zillow(get_zillow_data())
    if split == True:
        return split_zillow(df)
    else:
        return df

def scale_data(train,validate,test):
    '''Accepts train, validate, test data frames and applies min-max scaler
    return: train, validate, test scaled pandas dataframe'''
    
    scaler = sklearn.preprocessing.MinMaxScaler()
    scaler.fit(train)
    
    train_scaled = scaler.transform(train)
    validate_scaled = scaler.transform(validate)
    test_scaled = scaler.transform(test)
    
    train_scaled = pd.DataFrame(train_scaled, columns=train.columns)
    validate_scaled = pd.DataFrame(validate_scaled, columns=train.columns)
    test_scaled = pd.DataFrame(test_scaled, columns=train.columns)
    
    return train_scaled, validate_scaled, test_scaled