# <font color ='cyan'>Zillow Regression Project</font>



<p align="center">
  <img src="https://www.underconsideration.com/brandnew/archives/zillow_logo.png" width="500" height="200" >
</p> 


All appliciable files, modules, and references for my regrssion project will be uploaded into this repository.

##  <font color ="blue">This repository will contain:</font>
    * One clearly labeled final Jupyter Notebook that walks through the pipeline for my project.
    * `.py `files necessary to reproduce my work, and your work must be reproducible by someone with their own `env.py` file.
    * A `README.md `file documenting the project planning with instructions on how someone could clone and reproduce this project on their own machine. 
        - `README` will include :
            - My goals for the project
            - A data dictionary
            - Key findings and takeaways

<font color ="darkgreen"><a href="https://trello.com/b/C5zkPkLB/regression-project">This link will direct you to my project board which details individual tasks I'll be working on for this project</a>

    ### Data for Predicting Tax Value of Property
---
| Attribute | Definition | Data Type |
| ----- | ----- | ----- |
| parcelid | Unique identifier for parcels (lots) | Index/int | 
| bathroomcnt | Number of bathrooms in home including fractional bathrooms | float |
| bedroomcnt | Number of bedrooms in home | float |
| square_feet | Calculated total finished living area of the home | float |
| latitude | Latitude of the middle of the parcel multiplied by 10<sup>6</sup> | float |
| longitude | Longitude of the middle of the parcel multiplied by 10<sup>6</sup> | float |
| year_built | The Year the principal residence was built | int |
| tax_value* | The total tax assessed value of the parcel | float |
| age_of_home | year_built minus 2021 | int |
| beds_and_baths | The sum of all bedrooms and bathrooms | float |
| beds_per_sqft | The number of bedrooms divided by the square_feet | float |
| baths_per_sqft | The number of bathrooms divided by the square_feet | float |
