[![DOI](https://zenodo.org/badge/226836523.svg)](https://zenodo.org/badge/latestdoi/226836523)

# Repository for Study Material

<h3> General Information </h3>
This repository contains all materials, data and data analysis files used in a labratory study documented in the research paper: Freihaut, P., & Göritz, A. S. (2021). Using the computer mouse for stress measurement - An empirical investigation and critical review. International Journal of Human - Computer Studies, 145, 102520. https://doi.org/10.1016/j.ijhcs.2020.102520 </br></br>

We wholeheartedly thank our colleagues Johannes Blum and Christoph Rockstroh for their ideas, comments and expertise in programming. Without you, the project would have been doomed to fail. We recommend everyone to check out their research on the interplay between virtual reality and biofeedback in the context of mental health (Resono VR Project: https://resono-vr.de/ ; Flowborne VR Project: https://flowborne.com/ )

<h3>Repository Structure</h3>
The repository contains four main elements

1. The folder <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Experimental_Apps">Experimental_Apps</a> contains the <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Experimental_Apps/labstudy-19">original experimental app</a> (in German) with which the experiment was conducted (A React Web Application). It additionally contains a <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Experimental_Apps/task_overview">demo app</a> (in English) which contains the mouse and keyboard tasks presented in the study. The demo app can also be tested live <a target="_blank" rel="noopener noreferrer" href="https://task-demo-app.web.app/">here</a>.
2. The folder <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Datasets">Datasets</a> contains all data used in the experiment. This includes the raw data file from the experimental app, the raw heart data collected durin the experiment as well as the raw eda data collected during the experiment. The data folder also contains aggregated datasets which were used for data analysis (mouse data, manipulation check data, images used for image classification and data files used for time-series classification)
3. The <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Data_Aggregation_Code">aggregation code folder</a> contains the code which was used to create the aggregated datafiles from the raw data. This folder includes seperate files for (1) processing (1.1) the mouse data, (1.2) the heart data, (1.3) the eda data, (1.4) questionnaire data, (2) creating an aggregated dataset
4. The <a href="https://github.com/Freihaut/Study_files_LabExperiment_19_Freihaut_-_Goeritz/tree/master/Data_Analysis_Code">data analysis code</a>. The folder contains a file for image classification analysis, a file for time-series classification analysis and a file that contains all other analysis (manipulation-check, paired-sample t-test on mouse features and classification using mouse features).

The data analysis files should be ready to run in order to reproduce all data analysis reported in the paper. The data analysis files use the datasets in the datasets folder. Each file contains comments and explanations on how to use it.

For questions regarding the study material contact: paul.freihaut@psychologie.uni.freiburg.de

To cite the material (according to Zenodo):</br>
Freihaut. (2020, July 13). Study Material for the research paper "Using the computer mouse for stress measurement" (Version v1.0.1). Zenodo. http://doi.org/10.5281/zenodo.3941808
