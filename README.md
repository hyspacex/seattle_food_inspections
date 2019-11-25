# Seattle Food Inspection Project

## Project Goal

The broad goal of this project is to create a visual representation of the link between food inspection scores in Seattle, Washington and various demographic information of the surrounding area. At least in north west Ethiopia (see [this paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4057591/)), "[m]arital status [...] [and] monthly income [...] were found found to be significantly associated with good food handling [p]ractices." The cited study describes food handling inspection data on an individual-by-individual basis, where we use local business food inspection score as a proxy for food handling practices for the individuals in the surrounding community. 

The demographic information we consider come from the [American Community Surveys](https://www.census.gov/programs-surveys/acs) from the Census Bureau. The food inspection data comes from King County's [Open Data](https://data.kingcounty.gov/). 

The demographic information includes various relationship status information and median income, broken down by county. The food inspection information includes location information for businesses along with health inspection scores. 

## File Structure

```
.
|   .DS_Store
|   .gitignore
|   README.md
|
+---.ipynb_checkpoints
|       clean-checkpoint.ipynb
|       tech_review-checkpoint.ipynb
|
+---data
|   |   .DS_Store
|   |
|   +---clean_data
|   |   |   clean.ipynb
|   |   |   clean_census.csv
|   |   |   trial.csv
|   |   |
|   |   \---.ipynb_checkpoints
|   |           clean-checkpoint.ipynb
|   |
|   +---metadata
|   |       .DS_Store
|   |       ACS_17_5YR_S1201_metadata.csv
|   |       ACS_17_5YR_S1903_metadata.csv
|   |
|   \---raw_data
|           Food_Establishment_Inspection.csv
|           Income_ACS_17_5YR_S1903_with_ann.csv
|           Marital_ACS_17_5YR_S1201_with_ann.csv
|
\---docs
    |   comp_spec.md
    |   Food_Establishment_Inspection_Data.csv
    |   fun_spec.md
    |
    \---tech_review
        |   Technology review.pdf
        |   tech_review.ipynb
        |
        \---.ipynb_checkpoints
                tech_review-checkpoint.ipynb

```