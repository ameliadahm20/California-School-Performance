## Predicting California School Performance on ELA Testing


#### ***Amelia Dahm and Lauren Phipps***

![bookimage](images/bookpic.jpg)


## Repository Structure

```
├── data                         <- Sourced externally and generated from code
├── EDA                          <- Notebooks pertaining to EDA and Visualization
├── ModelingProcess              <- Notebooks showing interative modeling process
├── images                       <- Images and graphs used in this project
├── Final_Notebook.ipynb         <- Final notebook of project
├── README.md                    <- The high-level overview of this project
├── Presentation.pdf             <- PDF version of project presentation
└── datacleaning.py              <- Code file for data cleaning and preparation
```

## Overview
\[WRITE THIS]


## Business Problem
Students' success during and after their K-12 education is closely tied to their literacy skills. Students who are proficient in English/Language Arts (ELA) are more likely to be successful in graduating and attending a post-secondary institution. As part of an initiative that started in 2015, California's goal is to have 100% of students reaching proficiency in ELA by 2023. As we are reaching the final years of this initiative, it is important to be able to predict which schools are on track to meet this target and determine the factors that have the highest impact on the students' proficiency. This project aims to determine these factors in order to address the needs that are not being met with additional funding, intervention programs, or community engagement and support. Through actionable recommendations, we can address the needs of districts that will aid in students reaching proficiency and, hopefully, being more successful throughout their life.


## Data Understanding
The data comes from California Department of Education and contains school district information from 2018-2019. It contains 940 rows, each representing a school district in California. The columns represent different characteristics about that district, from student demographic and enrollment information to geographic information. This data will be used to determine which features of a school have an impact on the percentage of students who meet testing standards in ELA.


## Data Preparation

We began our preparation by dropping columns that were not relevant to the analysis (`OBJECTID`, `CDCode`, etc), as well as columns that had a significant number of null values and were characteristics that only pertained to high schools (`GradPct`, `DropOutPct`, etc). We then created dummy variables out of several of the categorical columns: `SchoolType`, `AssistStatus`, `LocaleDistrict`, and `EnrollTotal`. We created a new feature that expressed `EnrollCharter` as a percent of `EnrollTotal`. Additionally, we scaled down any outliers. 

During this process, we also created the target variable. This was engineered from the `ELAStdPctMet` feature. In order to determine if a school was on target to reach 100% proficiency in ELA, we set the threshold at 61%, which was the value for 75% quantile. If a school is on target, target contains a 1, if not, a 0.

## Results

Based on prior knowledge and experience, we started our analysis by looking at the impact of socioeconomic status, English language learners, and absenteeism on a district being on target. Absenteeism refers to the percentage of students who missed 10 or more school days. 

![barcharts](images/barchart.jpg)

This chart shows that, as expected, the average percentage of students who are socioeconomically disadvantaged, English language learners, or chronically absent, is higher in districts that are not meeting their testing target. 

Furthermore, the map below shows the relationship between the percentage of students who are socioeconomically disadvantaged and the percentage of students meeting the ELA standards by district.

![CAmaps](images/CAmaps.jpg)

Again, it is clear to see the impact that socioeconomic status has on ELA testing proficiency.

In creating a model from this data, this project focused on models that are highly interpretable in order to be able to understand the importance of specific characteristics in hopes of obtaining actionable next steps to address the needs of districts. We used precision as the evaluation metric in order to select the best model. This is because this scenario requires minimizing false positives. In this case, we do not want districts to be labeled as on track for success and not receive additional support when they may need it. Using this metric, the best model was \[**insert model here!]. 

From this model, we determined the following features were the more impactful:

\[insert feature importance]




## Evaluation

\[talk about metric scores and pros/cons about the model]

## Conclusion and Next Steps

\[more research, community funding, smaller schools, additional ELL support]