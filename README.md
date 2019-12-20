# Repository for Study Material

<h3> General Information </h3>
This repository contains all materials, data and data analysis files used in a labratory study documented in the research paper "Using the computer mouse for stress measurement – an empirical investigation and critical review" by Freihaut & Göritz, which will hopefully by published in the near future.</br></br>

We also wholeheartedly thank our colleagues Johannes Blum and Christoph Rockstroh for their ideas, comments and expertise in programming. Without you, the project would have been doomed to fail. We recommend everyone to check out their research on the interplay between virtual reality and biofeedback in the context of mental health (Resono VR Project: https://resono-vr.de/ ; Flowborne VR Project: https://flowborne.com/ )

<h3>Repository Structure</h3>
The repository contains four main elements

1. The folder experiment_material contains the original experimental app (in German) with which the experiment was conducted (A React Web Application). It additionally contains a demo app (in English) which contains the mouse and keyboard tasks presented in the study. The demo app can also be tested live <a target="_blank" rel="noopener noreferrer" href="https://task-demo-app.web.app/">here</a>.
2. The data folder contains all data used in the experiment. This includes the raw data file from the experimental app, the raw heart data collected durin the experiment as well as the raw eda data collected during the experiment. The data folder also contains aggregated datasets which were used for data analysis (mouse data, manipulation check data, images used for image classification and data files used for time-series classification)
3. The aggregation code folder contains the code which was used to create the aggregated datafiles from the raw data. This folder includes seperate files for (1) processing (1.1) the mouse data, (1.2) the heart data, (1.3) the eda data, (1.4) questionnaire data, (2) creating an aggregated dataset
4. The data analysis code. The folder contains a file for image classification analysis, a file for time-series classification analysis and a file that contains all other analysis (manipulation-check, paired-sample t-test on mouse features and classification using mouse features).

The data analysis code should run using the correspondent dataset (they need to be correctly imported in the data analysis files).

For questions regarding the study material contact: paul.freihaut@psychologie.uni.freiburg.de
