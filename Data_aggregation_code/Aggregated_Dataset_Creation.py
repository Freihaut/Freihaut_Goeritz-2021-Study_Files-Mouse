'''
This file imports the different data set creation files(questionnaire data, heart data, eda data and mouse data)
and merges them into a single file that can be used for further analysis.

This can be flexibly used to create datasets depending on the variables of interest (e.g. only heart data, only
physiological data (heart and eda)...

The code most certainly is far from perfect and was written to fit the data analysis purpose of the study rather
than to establish a multi-purpose solution. This version of the code represents a stripped version that includes
(almost exclusively) only include the procedures that were used in the final data analysis as reported in the
manuscript.

For questions or error reporting contact: paul.freihaut@psychologie.uni-freiburg.de
'''

# import core modules
import json
import pandas as pd
import datetime

# import Data Creation Files
import Questionnaire_Data_Creation as quest
import Mouse_Data_Creation as mouse
import Heart_Data_Creation as heart
import EDA_Data_Creation as eda

# get the raw dataset
with open("../Datasets/Raw_Data_Experiment.json") as jsonData:
    dataset = json.load(jsonData)

# Get the relevant datasets with the calculated parameters (here, all are chosen to create a dataset containing all
# relevant variables
questionnaire_data = quest.get_selfreport_data(dataset)
heart_data = heart.get_heart_data(dataset)
eda_data = eda.get_eda_data(dataset)
# point_click_data = mouse.get_point_click_data(dataset)
# drag_drop_data = mouse.get_drag_drop_data(dataset)
# steering_data = mouse.get_steering_task_data(dataset)
# follow_box_data = mouse.get_follow_box_task_data(dataset)

# Concat all datasets to create a single dataset (the list in the concat function must be replaced with the chosen
# subdatasets (here all are chosen)
final_df = pd.concat([questionnaire_data, heart_data, eda_data, point_click_data,
                     drag_drop_data, steering_data, follow_box_data], axis=1, sort=False)

# Name the index to be the ParticipantId and reset the index to create a new column with the Participant Id
final_df.index.name = "ParticipantId"
final_df = final_df.reset_index()

# print information about the data frame
# print(list(final_df.head(0))
# print(final_df.shape)

# Create a CSV file and save it on the desktop
final_df.to_csv(r"path\name_of_dataset" + datetime.date.today().isoformat() + ".csv", sep='\t', encoding='utf-8')