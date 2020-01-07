'''
This code can be used to reproduce the data analysis done in the manuscript. In the course of the experimental analysis
of the data, many more approaches were performed which are not part of this file but can be requested from the author. This
includes different tests (e.g. test for equal variance, regression approaches instead of classification,
classification and regression using the questionnaire data and physiological data ...) or different data preprocessing
strategies such as principal component analysis etc. The results of all other approaches did not reveal any significant
relationship between mouse usage and stress or stress markers.

You can use this file to execute the analysis in order to reproduce the results presented in the paper and inspect the
data analysis code.

The code most certainly is far from perfect and was written to fit the data analysis purpose of the study rather
than to establish a multi-purpose solution.

For questions, improvmenents or error reporting contact: paul.freihaut@psychologie.uni-freiburg.de
'''


# import core libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

###################################
# Setup to run the desired analysis
###################################

# In the following lines you can choose the analysis you want to run

# This file contains the following data analysis procedures
# 1. Paired sample t-test with manipulation check data
# 2. Paired sample t-test with mouse usage data
# 3. Condition classification based on the mouse usage features with a permutation test
# 4. Condition classification based on the mouse usage features with bootstrapping

# In order to run the analysis, chose one of the data analysis procedure and set them as the analysis variable value.
# You can modify the "targets" list to your own choice, e.g. if you want to do the manipulation check using the EDA data
# only, modify the "targets" list of the t_test_manipulation_check variable to only include "eda_data"
# As a default, all possibilities are chosen

# 1. analysis: Paired sample t-test with manipulation check data
t_test_manipulation_check = {
    "name": "t_test_manipulation_check",
    "targets": ["heart_data", "eda_data", "questionnaire"]
}

# 2. analysis: Paired sample t-test with mouse usage data
t_test_mouse_usage = {
    "name": "t_test_mouse_usage",
    "targets": ["PointClick", "DragDrop", "Drawing", "FollowBox"]
}

# 3. analysis: Condition classification based on the mouse usage features with a permutation test
classification_permutation = {
    "name": "classification_permutation",
    "targets": ["PointClick", "DragDrop", "Drawing", "FollowBox"]
}

# 4. analysis: Condition classification based on the mouse usage features with bootstrapping
classification_bootstrap = {
    "name": "classification_bootstrap",
    "targets": ["PointClick", "DragDrop", "Drawing", "FollowBox"]
}


# Set the value of the analysis variable to the desired analysis
# Default: t_test manipulation check with the eda, heart and questionnaire data)
analysis = t_test_manipulation_check

# RUN THE SCRIPT TO GET THE RESULTS. THEY ARE SAVED IN A TEXT FILE THAT IS CREATED AND NAMED ACCORDING TO THE ANALYSIS
# Do not modify the code below if you just want to run the analysis

################
# Analysis Code
################

# The following code is the data analysis code. It is written to work with the prodecure of this specific data analysis
# file. If you modify the code, it might not be possible to execute the data analysis any more.

##################################
# Paired-Sample-T-Test Analysis
##################################

# Steps:
# 1. get the dataset with the data to analyse and prepare the data for the analysis
# 2. run the analysis and save the results


# prepare the manipulation check data for the t_test_analysis
def manipulation_check_data_t_test(data_source):

    import os

    # get the relative path to the dataset
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    targetDir = os.path.join(parentDir, "Datasets")

    # Get and use data
    dataset = pd.read_csv(targetDir + "/Manipulation_Check_Data.csv", sep='\t', encoding='utf-8')

    # set the index to be the participantID in order to be able to filter bad cases by their names
    dataset = dataset.set_index("ParticipantId")

    # drop the Unnamed column
    dataset = dataset.drop('Unnamed: 0', axis=1)

    # remove participants from the dataset that have no data except for a condition
    dataset = dataset.dropna(how="all")

    # store information about cases that need to be exclused from statistical analysis (based on prior sanity checks)

    bad_cases_heart_data = [
        "V6TlsMC21YbLX2MyjUiEiVrhgMk2_HS", "V6TlsMC21YbLX2MyjUiEiVrhgMk2_LS",
        "QJ1jbbS5crQeT8NtefEk8cqck6a2_HS", "QJ1jbbS5crQeT8NtefEk8cqck6a2_LS",
        "bD83eNrrWTgjMkVAdibgZNiebTe2_HS", "bD83eNrrWTgjMkVAdibgZNiebTe2_LS",
        "nQl80EJnrxYnsuoVqEFhTMzZVgl2_HS", "nQl80EJnrxYnsuoVqEFhTMzZVgl2_LS",
        "zH98oKnznGRDas55OgA25hFvTnO2_HS", "zH98oKnznGRDas55OgA25hFvTnO2_LS"
    ]

    bad_cases_eda = [
        "DEhCMZqN9jOlZWFNQQk4YHoix5u2_HS", "DEhCMZqN9jOlZWFNQQk4YHoix5u2_LS"
    ]

    # create the datasets per manipulation check indicator

    # heart data

    if data_source == "heart_data":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_heart_data)

        # get heart rate feature columns
        heart_data_cols = [i for i in dataset_del.head(0) if "mean_HR" in i]

        # append the condition column
        heart_data_cols.append("condition")

        # create data set for analysis
        dv = dataset_del.loc[:, heart_data_cols]

        return dv

    # eda data
    if data_source == "eda_data":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_eda)

        # get eda feature columns
        eda_data_cols = [i for i in dataset_del.head(0) if "Mean_Resistance" in i]

        # append the condition column
        eda_data_cols.append("condition")

        # create data set for analysis
        dv = dataset_del.loc[:, eda_data_cols]

        return dv

    # questionnaire data

    if data_source == "questionnaire":

        # create the MDBF scales

        # step 1: recode some items
        dataset["MDBF_angespannt"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)
        dataset["MDBF_nervÃ¶s"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)
        dataset["MDBF_schlÃ¤frig"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)
        dataset["MDBF_unglÃ¼cklich"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)
        dataset["MDBF_unzufrieden"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)
        dataset["MDBF_ermattet"].replace([0, 1, 2, 3, 4], [4, 3, 2, 1, 0], inplace=True)

        # step 2: compute scale

        # good mood versus bad mood
        dataset["MDBF_GS"] = (dataset["MDBF_wohl"] + dataset["MDBF_gut"] +
                              dataset["MDBF_unglÃ¼cklich"] + dataset["MDBF_unzufrieden"]) / 4

        # alertness versus tiredness
        dataset["MDBF_WM"] = (dataset["MDBF_frisch"] + dataset["MDBF_wach"] +
                              dataset["MDBF_schlÃ¤frig"] + dataset["MDBF_ermattet"]) / 4

        # rest versus unrest
        dataset["MDBF_RU"] = (dataset["MDBF_ausgeglichen"] + dataset["MDBF_ruhig"] +
                              dataset["MDBF_angespannt"] + dataset["MDBF_nervÃ¶s"]) / 4

        #########
        # calculate and print Cronbach`s Alpha
        #########

        # get information about the condition
        hs_frame = dataset[dataset["condition"] == 0]
        ls_frame = dataset[dataset["condition"] == 1]

        # get the relevant columns for each scale
        hs_mdbf_gs = hs_frame.loc[:, ["MDBF_wohl", "MDBF_gut", "MDBF_unglÃ¼cklich", "MDBF_unzufrieden"]]
        hs_mdbf_wm = hs_frame.loc[:, ["MDBF_frisch", "MDBF_wach", "MDBF_schlÃ¤frig", "MDBF_ermattet"]]
        hs_mdbf_ru = hs_frame.loc[:, ["MDBF_ausgeglichen", "MDBF_ruhig", "MDBF_angespannt", "MDBF_nervÃ¶s"]]

        ls_mdbf_gs = ls_frame.loc[:, ["MDBF_wohl", "MDBF_gut", "MDBF_unglÃ¼cklich", "MDBF_unzufrieden"]]
        ls_mdbf_wm = ls_frame.loc[:, ["MDBF_frisch", "MDBF_wach", "MDBF_schlÃ¤frig", "MDBF_ermattet"]]
        ls_mdbf_ru = ls_frame.loc[:, ["MDBF_ausgeglichen", "MDBF_ruhig", "MDBF_angespannt", "MDBF_nervÃ¶s"]]

        # calculate and print out Cronbach's Alphas
        import pingouin as pg

        print("Cronbach's Alphas with 95 CI:")
        print("High Stress condition:")
        print("MBF_GS:", pg.cronbach_alpha(data=hs_mdbf_gs), "MBF_WM:", pg.cronbach_alpha(data=hs_mdbf_wm),
              "MBF_RU:", pg.cronbach_alpha(data=hs_mdbf_ru))
        print("Low Stress Condition")
        print("MBF_GS:", pg.cronbach_alpha(data=ls_mdbf_gs), "MBF_WM:", pg.cronbach_alpha(data=ls_mdbf_wm),
              "MBF_RU:", pg.cronbach_alpha(data=ls_mdbf_ru))

        #########
        # End of Cronbach`s Alpha Calculation
        #########

        # get questionnaire feature columns
        questionnaire_cols = [i for i in dataset.head(0) if "Arousal" in i or "Valence" in i]

        questionnaire_cols.extend(["nostalgia", "stress", "MDBF_GS", "MDBF_WM", "MDBF_GS", "condition"])

        # create data set for analysis
        dv = dataset.loc[:, questionnaire_cols]

        return dv


# prepare the mouse data for t_test analysis
def mouse_data_t_test(task):

    import os

    # get the relative path to the dataset
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    targetDir = os.path.join(parentDir, "Datasets")

    # Get and use data
    dataset = pd.read_csv(targetDir + "/Aggregated_Mouse_Data.csv", sep='\t', encoding='utf-8')

    # set the index to be the participantID in order to be able to filter bad cases by their names
    dataset = dataset.set_index("ParticipantId")

    # store the cases for each tasks that need to be excluded from statistical analysis

    bad_cases_point_click = ["INFvFzlNN7UeZRqvtoe8hejtnvX2_HS", "INFvFzlNN7UeZRqvtoe8hejtnvX2_LS",
                             "PRPyIVrPUVgCFtZ60nqvXc4wUov2_HS", "PRPyIVrPUVgCFtZ60nqvXc4wUov2_LS",
                             "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_HS", "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_LS",
                             "X5mfB1vgISTp6cagPLnp0zyh4EI2_HS", "X5mfB1vgISTp6cagPLnp0zyh4EI2_LS",
                             "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_HS", "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_LS",
                             "zf3H80XYGSf9U3pZM5xxOm69qTT2_HS", "zf3H80XYGSf9U3pZM5xxOm69qTT2_LS"]

    bad_cases_drag_drop = [
        "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_HS", "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_LS",
        "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_HS", "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_LS",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32_HS", "dOXefJ4hHEfRsYTTFfn6NfATnh32_LS"
    ]

    bad_cases_drawing = [
        "4ibZh6HiVrPknUuvasf6CIVD1L42_HS", "4ibZh6HiVrPknUuvasf6CIVD1L42_LS",
        "9DdqeM3mkRWvD4MCMcWvFH4wIhA2_HS", "9DdqeM3mkRWvD4MCMcWvFH4wIhA2_LS",
        "GzlieWRWOJgquA0nDZtBFExSW0E2_HS", "GzlieWRWOJgquA0nDZtBFExSW0E2_LS",
        "PRPyIVrPUVgCFtZ60nqvXc4wUov2_HS", "PRPyIVrPUVgCFtZ60nqvXc4wUov2_LS",
        "WpwRDjuqqdRavEdFOgqbpRA19Q32_HS", "WpwRDjuqqdRavEdFOgqbpRA19Q32_LS",
        "b8KoZn71FhOsv46MKFAlqdhTBXM2_HS", "b8KoZn71FhOsv46MKFAlqdhTBXM2_LS",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32_HS", "dOXefJ4hHEfRsYTTFfn6NfATnh32_LS",
        "gJnYNGrs0lhMSKDh9i466E2MiJn2_HS", "gJnYNGrs0lhMSKDh9i466E2MiJn2_LS",
        "nDsahKaZCEUMI732rmmyANfauCj1_HS", "nDsahKaZCEUMI732rmmyANfauCj1_LS",
        "pPx9EQjAJuN5wxinUZjO6DUsZDo1_HS", "pPx9EQjAJuN5wxinUZjO6DUsZDo1_LS",
    ]

    # create the datasets per task

    # point and click task
    if task == "PointClick":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_point_click)

        # get mouse usage feature columns
        point_click_cols = [i for i in dataset_del.head(0) if "PointClick" in i]
        # append the condition column
        point_click_cols.append("condition")

        # create the dataset
        point_click_data = dataset_del.loc[:, point_click_cols].dropna(how="all")

        dv = point_click_data.loc[:, point_click_cols]

    # drag drop task
    if task == "DragDrop":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_drag_drop)

        # get mouse usage feature columns
        drag_drop_cols = [i for i in dataset_del.head(0) if "DragDrop" in i]
        # append the condition column
        drag_drop_cols.append("condition")

        # create the dataset
        drag_drop_data = dataset_del.loc[:, drag_drop_cols].dropna(how="all")

        drag_drop_cols.remove('DragDrop_num_drags')
        drag_drop_cols.remove('DragDrop_num_trials')

        dv = drag_drop_data.loc[:, drag_drop_cols]

    # drawing task
    if task == "Drawing":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_drawing)

        # get mouse usage feature columns
        drawing_cols = [i for i in dataset_del.head(0) if "Drawing" in i]
        # append the condition column
        drawing_cols.append("condition")

        # create the dataset
        drawing_data = dataset_del.loc[:, drawing_cols].dropna(how="all")

        drawing_cols.remove('Drawing_num_drawings')
        drawing_cols.remove('Drawing_par_index')

        dv = drawing_data.loc[:, drawing_cols]

    # follow-box task
    if task == "FollowBox":

        # get mouse usage feature columns
        box_columns = [i for i in dataset.head(0) if "FollowBox" in i]
        # append the condition column
        box_columns.append("condition")

        # create the dataset
        box_data = dataset.loc[:, box_columns].dropna(how="all")

        dv = box_data.loc[:, box_columns]

    return dv


# use the mouse data feature datasets to do the paired_sample_t_tests
def paired_sample_t_test(dataframe):

    # get specfic data frames per condition (to compare them in the t-test)
    hs_frame = dataframe[dataframe["condition"] == 0]
    ls_frame = dataframe[dataframe["condition"] == 1]

    # print(hs_frame.shape, ls_frame.shape)

    # create a text file and save the results in it
    with open("Results_Paired_sample_tTest.txt","a") as f:
        # loop over each variable in the column
        for i in range(len(dataframe.columns)):
            # write down the variable name and the task
            f.write(list(dataframe.columns)[i] + "\n")
            # write down the number of participants
            f.write("N = " + str(hs_frame.shape[0]) + "\n")
            # write down the mean and standard deviations of the variable
            f.write("HS Mean: " + str(np.mean(hs_frame.iloc[:, i])) + ", HS Sd: " + str(np.std(hs_frame.iloc[:, i])) + "\n")
            f.write(
                "LS Mean: " + str(np.mean(ls_frame.iloc[:, i])) + ", LS Sd: " + str(np.std(ls_frame.iloc[:, i])) + "\n")
            # write down the results of the t-test
            f.write(str(stats.ttest_rel(hs_frame.iloc[:, i], ls_frame.iloc[:, i])))
            f.write("\n" + "\n" + "\n")

    # close the text file
    f.close()


#######################################################
# Condition Classification Machine Learning Analysis
########################################################

# Steps:
# 1. get the dataset with the data to analyse and prepare the data for the analysis
# 2. run the analysis and save the results

# create the dataset for the task condition classification
def ml_mouse_data(task):

    import os

    # get the relative path to the dataset
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    targetDir = os.path.join(parentDir, "Datasets")

    # Get and use data
    dataset = pd.read_csv(targetDir + "/Aggregated_Mouse_Data.csv", sep='\t', encoding='utf-8')

    # set the index to be the participantID in order to be able to filter bad cases by their names
    dataset = dataset.set_index("ParticipantId")

    # store the cases for each tasks that need to be excluded from statistical analysis

    bad_cases_point_click = ["INFvFzlNN7UeZRqvtoe8hejtnvX2_HS", "INFvFzlNN7UeZRqvtoe8hejtnvX2_LS",
                             "PRPyIVrPUVgCFtZ60nqvXc4wUov2_HS", "PRPyIVrPUVgCFtZ60nqvXc4wUov2_LS",
                             "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_HS", "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_LS",
                             "X5mfB1vgISTp6cagPLnp0zyh4EI2_HS", "X5mfB1vgISTp6cagPLnp0zyh4EI2_LS",
                             "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_HS", "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_LS",
                             "zf3H80XYGSf9U3pZM5xxOm69qTT2_HS", "zf3H80XYGSf9U3pZM5xxOm69qTT2_LS"]

    bad_cases_drag_drop = [
        "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_HS", "Vhi1KMa2MecuTnTzWb8QBp9rNDw1_LS",
        "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_HS", "ZnI96HDrRZV9xNlfQxgTU0CeoDX2_LS",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32_HS", "dOXefJ4hHEfRsYTTFfn6NfATnh32_LS"
    ]

    bad_cases_drawing = [
        "4ibZh6HiVrPknUuvasf6CIVD1L42_HS", "4ibZh6HiVrPknUuvasf6CIVD1L42_LS",
        "9DdqeM3mkRWvD4MCMcWvFH4wIhA2_HS", "9DdqeM3mkRWvD4MCMcWvFH4wIhA2_LS",
        "GzlieWRWOJgquA0nDZtBFExSW0E2_HS", "GzlieWRWOJgquA0nDZtBFExSW0E2_LS",
        "PRPyIVrPUVgCFtZ60nqvXc4wUov2_HS", "PRPyIVrPUVgCFtZ60nqvXc4wUov2_LS",
        "WpwRDjuqqdRavEdFOgqbpRA19Q32_HS", "WpwRDjuqqdRavEdFOgqbpRA19Q32_LS",
        "b8KoZn71FhOsv46MKFAlqdhTBXM2_HS", "b8KoZn71FhOsv46MKFAlqdhTBXM2_LS",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32_HS", "dOXefJ4hHEfRsYTTFfn6NfATnh32_LS",
        "gJnYNGrs0lhMSKDh9i466E2MiJn2_HS", "gJnYNGrs0lhMSKDh9i466E2MiJn2_LS",
        "nDsahKaZCEUMI732rmmyANfauCj1_HS", "nDsahKaZCEUMI732rmmyANfauCj1_LS",
        "pPx9EQjAJuN5wxinUZjO6DUsZDo1_HS", "pPx9EQjAJuN5wxinUZjO6DUsZDo1_LS",
    ]

    # point and click task
    if task == "PointClick":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_point_click)

        # get point click data columns
        point_click_cols = [i for i in dataset_del.head(0) if "PointClick" in i]

        point_click_cols.append("condition")
        point_click_cols.append("Drawing_par_index")

        point_click_data = dataset_del.loc[:, point_click_cols].dropna(how="all")

        # get the independent variable data column
        iv = point_click_data.condition

        # get the the group variable data column
        groups = point_click_data.Drawing_par_index

        point_click_cols.remove('PointClick_num_trials')
        point_click_cols.remove('Drawing_par_index')
        point_click_cols.remove("condition")

        # get the dependent variable data column
        dv = point_click_data.loc[:, point_click_cols]

    # drag and drop data
    if task == "DragDrop":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_drag_drop)

        # get drag and drop data columns
        drag_drop_cols = [i for i in dataset_del.head(0) if "DragDrop" in i]

        drag_drop_cols.append("condition")
        drag_drop_cols.append("Drawing_par_index")

        drag_drop_data = dataset_del.loc[:, drag_drop_cols].dropna(how="all")

        # get the independent variable data column
        iv = drag_drop_data.condition

        # get the the group variable data column
        groups = drag_drop_data.Drawing_par_index

        drag_drop_cols.remove('DragDrop_num_drags')
        drag_drop_cols.remove('DragDrop_num_trials')
        drag_drop_cols.remove('Drawing_par_index')
        drag_drop_cols.remove("condition")

        # get the dependent variable data column
        dv = drag_drop_data.loc[:, drag_drop_cols]

    # drawing task
    if task == "Drawing":

        # drop bad cases
        dataset_del = dataset.drop(bad_cases_drawing)

        # get drawing data columns
        drawing_cols = [i for i in dataset_del.head(0) if "Drawing" in i]

        drawing_cols.append("condition")

        drawing_data = dataset_del.loc[:, drawing_cols].dropna(how="all")

        # get the independent variable data column
        iv = drawing_data.condition

        # get the the group variable data column
        groups = drawing_data.Drawing_par_index

        drawing_cols.remove('Drawing_num_drawings')
        drawing_cols.remove('Drawing_par_index')
        drawing_cols.remove("condition")

        # get the dependent variable data column
        dv = drawing_data.loc[:, drawing_cols]

    # follow box task
    if task == "FollowBox":

        # get follow_box task data columns
        box_columns = [i for i in dataset.head(0) if "FollowBox" in i]

        box_columns.append("condition")
        box_columns.append("Drawing_par_index")

        box_data = dataset.loc[:, box_columns].dropna(how="all")

        # get the independent variable data column
        iv = box_data.condition

        # get the the group variable data column
        groups = box_data.Drawing_par_index

        box_columns.remove("Drawing_par_index")
        box_columns.remove("condition")

        # get the dependent variable data column
        dv = box_data.loc[:, box_columns]

    return dv, iv, groups


# Permutation test classification function
def ml_permutation_test(task, dv, iv, groups):

    # import sk learn modules to perform the permutation test
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import permutation_test_score
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler

    # import classifier algorithms
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier

    # Create custom classes for data transformation in the sklearn pipeline
    from sklearn.base import TransformerMixin, BaseEstimator

    # Feature Selection Class
    class FeatureSelection(BaseEstimator, TransformerMixin):

        """
        Select a subset of features depending on the chosen selection criteria
        1: all = Use all features
        2: filter =  Use features whose dependent t-test values are below a certain threshold (use k-best features
        3: wrapper =  choose the best subset of n features during cross validation
        4: embedded = use feature importance of an algorithm to select important features
        """

        def __init__(self, method="ignore", threshold=.10):
            self.method = method
            self.threshold = threshold
            self.sel_columns = []

        def fit(self, X, y):

            # Filter Methods using a paired-sample t-test
            if self.method == "filter":

                # to use a sampled pair t-test the data must first be split into its within-design
                split_data = {}

                # change dataformat from DataFrame to np.ndarray (dirty fix)
                x_data = X.to_numpy()

                # Only works because order of the data is as following:
                # person 1 HS, person 1 LS, person 2 HS, person 2 LS... !
                for i in range(len(x_data[0])):
                    split_data[i] = [[], []]
                    split_data[i][0] = [el[i] for num, el in enumerate(x_data) if num % 2 == 0]
                    split_data[i][1] = [el[i] for num, el in enumerate(x_data) if num % 2 != 0]

                # to select the k best features (doesnt matter if they are better or worse than a p-value threshold
                t_test_results = {}

                for feature_num in split_data:
                    t_test_results[feature_num] = abs(stats.ttest_rel(split_data[feature_num][0], split_data[feature_num][1])[0])

                # get the smallest k t-values
                import heapq
                k_smallest = heapq.nsmallest(max(t_test_results) - 4, t_test_results, key=t_test_results.get)

                # get a list of the names of the selected features
                self.sel_columns = list(X.iloc[:, k_smallest].columns)

                return self

            # Wrapper Methods: Search for "optimal ammount of features" using a selection process (adding the feature
            # that most improves accuracy until no feature addition improves accuracy == Foward Selection)
            # Using the mlxtend library ("stepwise selection procedure using k-fold-cv")
            # was not used in the manuscript
            elif self.method == "wrapper":

                from mlxtend.feature_selection import SequentialFeatureSelector as SFS
                from sklearn.model_selection import GroupKFold
                from sklearn.ensemble import RandomForestClassifier

                # get grouping information of data
                groups = np.arange(len(X)) // 2
                # Initialize a Group-k-fold-cross validator
                cv_gen = GroupKFold(5).split(X, y, groups)

                # Initialize a classifier (could be any other classifier aswell!)
                clf = RandomForestClassifier(n_estimators=100, random_state=25)
                # initialize the feature selector
                sfs = SFS(clf, k_features=(1, 10), forward=True, scoring="accuracy", cv=list(cv_gen))

                feature_names = list(X.columns)
                sfs = sfs.fit(X, y, custom_feature_names=feature_names)
                selected_features = sfs.k_feature_names_

                self.sel_columns = [feat for feat in feature_names if feat not in selected_features]

                return self

            # Embedded Methods
            # Use a Classifier and its importance to select a subset of features
            elif "embedded" in self.method:

                from sklearn.feature_selection import SelectFromModel

                if self.method == "embedded_lsvc":
                    from sklearn.svm import LinearSVC
                    lsvc = LinearSVC(penalty="l1", C=0.1, dual=False, max_iter=5000).fit(X, y)
                    model = SelectFromModel(lsvc, prefit=True)

                if self.method == "embedded_logReg":
                    from sklearn.linear_model import LogisticRegression
                    logreg = LogisticRegression(penalty="l1", solver="liblinear").fit(X, y)
                    model = SelectFromModel(logreg, prefit=True)

                if self.method == "embedded_trees":
                    from sklearn.ensemble import RandomForestClassifier
                    forest = RandomForestClassifier(n_estimators=100).fit(X, y)
                    model = SelectFromModel(forest, prefit=True)

                selected_features = list(X.iloc[:, model.get_support(indices=True)].columns)
                # print(len(selected_features))

                self.sel_columns = [feat for feat in list(X.columns) if feat not in selected_features]

                return self

            # if not method is specified or method name is written wrongly use all features and no feature selection
            else:
                print("Either no feature selection algorithm was used or it was misspelled. "
                      "Defaulted to use all features")
                return self

        def transform(self, X, y=None):

            # drop all non-chosen features from the dataset
            return X.drop(self.sel_columns, axis=1)

    # class to handle multicollinearity between mouse usage features
    # was not used in the manuscript
    class HandleMulticollinearity(BaseEstimator, TransformerMixin):

        """
        handle multicollinearity among independent variables based on three methods:
        1: Ignore = Use all independent variables
        2: Variance Inflation Factor: Use the VIF to stepwise remove independent variables until a threshold is met
        3: Correlation: Remove all independent variables with a correlation higher than a threshold
        """

        def __init__(self, method="ignore", threshold=.80):
            self.method = method
            self.threshold = threshold
            self.sel_columns = []

        def fit(self, X, y=None):

            if self.method == "ignore":
                # dont drop any columns
                return self

            # stepwise remove variables based on their variance inflation factor
            elif self.method == "vlf":

                # calculate the vlf for a model with all dvs and remove a dv as long as a threshold is not met
                from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
                from statsmodels.tools.tools import add_constant

                cols_to_delete = []

                X = add_constant(X)

                while True:
                    vlfs = pd.Series([vif(X.values, i) for i in range(X.shape[1])], index=X.columns)
                    max_vlf = vlfs[1:].max()
                    idx = vlfs[1:].idxmax()
                    # print(max_vlf, idx)
                    if max_vlf >= 10:
                        cols_to_delete.append(idx)
                        X.drop(idx, axis=1, inplace=True)
                    else:
                        break

                # drop the constant column
                self.sel_columns = cols_to_delete

                return self

            # remove all variables with a correlation higher than a selected threshold
            elif self.method == "corr":

                # create a correlation matrix
                corr_matrix = X.corr().abs()

                # select the upper triangle of a correlation matrix
                upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

                # find index of features with correlations greater than a threshold and drop them from dataframe
                self.sel_columns = [column for column in upper.columns if any(upper[column] > self.threshold)]

                return self

            else:

                print("Chosen method " + self.method + " does not exist. Defaulted to ignore multicollinearity")
                return self

        def transform(self, X, y=None):

            # return the dataframe without the columns that were deleted
            return X.drop(self.sel_columns, axis=1)

    # Debugger class to get information about the data inside the pipeline
    class Debug(BaseEstimator, TransformerMixin):

        def transform(self, X):

            # return the data
            print(X.shape)
            return X

        def fit(self, X, y=None, **fit_params):

            return self

    # initiate machine learning algorithms
    log_reg = LogisticRegression(solver="liblinear")
    gnb = GaussianNB()
    svm = SVC()
    forest = RandomForestClassifier(n_estimators=100, random_state=25)

    # chose which algorithms are used for the analysis
    algorithms = [log_reg, gnb, svm, forest]

    # Save the Results into a Textfile (the text file is created once and results are appended to the end of the file
    with open(
            "Permutation_Test_Results.txt",
            "a") as f:

        # general task information
        f.write("\n" + "\n" + "Accuracy Prediction and Evaluation Using the Permutation Test and No Feature Selection" + "\n")
        f.write("Task: " + str(task) + "\n")

        for algorithm in algorithms:

            # initiate the pipeline and select the desired configurations for handling multicollinearity and
            # the feature selection procedure (here all features are used

            pipe = Pipeline([
                ("multicollinearity", HandleMulticollinearity(method="ignore")),
                ("feat_selection", FeatureSelection(method="ignore", threshold=.25)),
                ("scaler", StandardScaler()),
                ("clf", algorithm)
            ])

            cv = GroupKFold(n_splits=5)

            n_classes = np.unique(iv).size

            # ATTENTION: Changed the behavior of permutation_scores in the sklearn library to return the mean and standard
            # deviation of the cross validation without permutation

            # get the mean cross validation score, the standard deviation of the cv scores, the permuation scores and the
            # p-value of the permutation test
            score, std, permutation_scores, pvalue = permutation_test_score(
                pipe, dv, iv, scoring="accuracy", cv=cv, groups=groups, n_permutations=1000, n_jobs=1)

            # write down the results in the textfile
            f.write("Using the " + str(algorithm)[:10] + " algorithm" + "\n")
            f.write(str("Mean classification Accuracy: %.2f%%" % (100 * score)) + "\n")
            f.write(str("Classification Stand. Deviation: %.2f%%" % (100 * std)) + "\n")
            f.write(str( "Difference from Random pValue: " + str(pvalue)) + "\n")

            print("Mean classification Accuracy: %.2f%%" % (100 * score), "\n",
                  "Classification Stand. Deviation: %.2f%%" % (100 * std), "\n",
                   "Difference from Random pValue: " + str(pvalue))

            acc = np.mean(permutation_scores[:, 0])
            f.write(str('Permutation Accuracy: %.2f%%' % (100 * acc))  + "\n")
            print('Permutation Accuracy: %.2f%%' % (100 * acc))

            # Confidence interval
            lower = np.percentile(permutation_scores[:, 0], 2.5)
            upper = np.percentile(permutation_scores[:, 0], 97.5)
            f.write(str('Permutation 95%% Confidence interval: [%.2f, %.2f]' % (100 * lower, 100 * upper))  + "\n"  + "\n"  + "\n")
            print('Permutation 95%% Confidence interval: [%.2f, %.2f]' % (100 * lower, 100 * upper))

            # Create and save a plot of the procedure
            plt.hist(permutation_scores, bins=np.arange(np.min(permutation_scores), np.max(permutation_scores), 2.5),
                     alpha=0.6, rwidth=1.0, edgecolor="black")
            ylim = plt.ylim()
            plt.plot(2 * [score], ylim, "--r", linewidth=3,
                     label="Mean Accuracy: %s, p = %s" % (np.round(np.mean(score), 2), pvalue))
            plt.plot(2 * [lower], ylim, "--b", linewidth=2, label="Permutation CI95: " "[%s, %s]" % (lower, upper))
            plt.plot(2 * [upper], ylim, "--b", linewidth=2)
            plt.plot(2 * [np.mean(permutation_scores)], ylim, "--g", linewidth=3,
                     label="Mean Permutation Score: " "%s" % (np.round(np.mean(permutation_scores), 2)))
            plt.ylim(ylim)
            plt.xlabel("Accuracy Score")
            plt.ylabel("Frequency")
            plt.title("Permutation Test" + task + str(algorithm)[:5] + "")
            plt.legend(loc="upper left")
            # plt.savefig("Permuation_Test_" + task + str(algorithm)[:5] + ".png")
            plt.show()

    f.close()


# bootstrap classification function
def ml_bootstrap(task, dv, iv, groups):

    # import classifier algorithms
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier

    # helper function that creates a new, resampled dataframe
    def resample_df(df, l):

        new_df = pd.DataFrame()

        for i in l:
            el1 = df.iloc[int(i * 2 - 1)]
            new_df = pd.concat([new_df, el1.to_frame().T])
            el2 = df.iloc[int(i * 2 - 2)]
            new_df = pd.concat([new_df, el2.to_frame().T])

        return new_df

    # helper function for feature selection
    def classifier_feature_selection(dv, x_train, y_train, x_test, method="all", threshold=0.05):

        # Filter Methods: Paired-sample t-test
        if method == "filter":

            # to use a sampled pair t-test the data must first be split into its within-design
            split_data = {}

            # Only works because order of the data is as following: person 1 HS, person 1 LS, person 2 HS, person 2 LS.
            for i in range(len(x_train[0])):
                split_data[i] = [[], []]
                split_data[i][0] = [el[i] for num, el in enumerate(x_train) if num % 2 == 0]
                split_data[i][1] = [el[i] for num, el in enumerate(x_train) if num % 2 != 0]

            # to select the k best features (doesnt matter if they are better or worse than a p-value threshold
            t_test_results = {}

            for feature_num in split_data:
                t_test_results[feature_num] = abs(
                    stats.ttest_rel(split_data[feature_num][0], split_data[feature_num][1])[0])

            # get the smallest k t-values
            import heapq
            k_smallest = heapq.nsmallest(max(t_test_results) - 4, t_test_results, key=t_test_results.get)
            k_largest = heapq.nlargest(5, t_test_results, key=t_test_results.get)

            feature_names = list(dv.iloc[:, k_largest].columns)

            # transform the old feature matrix into a new feature matrix keepin only the features that pass the test
            x_train_transformed = []
            x_test_transformed = []

            for person in x_train:
                x_train_transformed.append([i for j, i in enumerate(person) if j not in k_smallest])

            for person in x_test:
                x_test_transformed.append([i for j, i in enumerate(person) if j not in k_smallest])

            x_train_transformed = np.array(x_train_transformed)
            x_test_transformed = np.array(x_test_transformed)

            return feature_names, x_train_transformed, x_test_transformed

        # Wrapper Methods: Search for an "optimal amount of features" using a selection process (adding the feature
        # that most improves accuracy until no feature addition improves accuracy == Forward Selection)
        # Using the mlxtend library ("stepwise selection procedure using k-fold-cv)
        if method == "wrapper":
            # other available tuning options:
            # -choose a different classifier
            # -choose a different numer of features
            # -choose a different stepwise algorithm
            from sklearn.svm import SVC
            from mlxtend.feature_selection import SequentialFeatureSelector as SFS
            from sklearn.model_selection import GroupKFold

            # get grouping information of data
            groups = np.arange(len(x_train)) // 2
            # Initialize a Group-k-fold-cross validator
            cv_gen = GroupKFold(5).split(x_train, y_train, groups)

            # Initialize a classifier (could be any other classifier aswell!)
            svc = SVC(gamma="auto")
            # initialize the feature selector
            sfs = SFS(svc, k_features=(1, 10), forward=True, scoring="accuracy", cv=list(cv_gen))

            feature_names = list(dv.columns)
            sfs = sfs.fit(x_train, y_train, custom_feature_names=feature_names)
            selected_features = sfs.k_feature_names_

            # print(selected_features, sfs.k_score_)

            x_train_transformed = sfs.transform(x_train)
            x_test_transformed = sfs.transform(x_test)

            return selected_features, x_train_transformed, x_test_transformed

        # Embedded Methods
        # Use a Classifier and its importance to select a subset of features (for example using the SelectFromModel class
        # in sk learn and then transform the train and test set to only include the subset!
        if "embedded" in method:

            from sklearn.feature_selection import SelectFromModel

            if method == "embedded_lsvc":
                from sklearn.svm import LinearSVC
                lsvc = LinearSVC(penalty="l1", C=0.1, dual=False, max_iter=5000).fit(x_train, y_train)
                model = SelectFromModel(lsvc, prefit=True)

            if method == "embedded_logReg":
                from sklearn.linear_model import LogisticRegression
                logreg = LogisticRegression(penalty="l1", solver="liblinear").fit(x_train, y_train)
                model = SelectFromModel(logreg, prefit=True)

            if method == "embedded_trees":
                from sklearn.ensemble import RandomForestClassifier
                forest = RandomForestClassifier(n_estimators=100).fit(x_train, y_train)
                model = SelectFromModel(forest, prefit=True)

            feature_names = list(dv.iloc[:, model.get_support(indices=True)].columns)

            x_train_transformed = model.transform(x_train)
            x_test_transformed = model.transform(x_test)

            return feature_names, x_train_transformed, x_test_transformed

        # use all features
        if method == "all":
            feature_names = list(dv.columns)

            return feature_names, x_train, x_test
        # Feature Transformation (not a feature selection procedure in a narrow sense) -> not sure if useful for
        # within-participant data structure: ON-HOLD

    # initiate machine learning algorithms
    log_reg = LogisticRegression(solver="liblinear")
    gnb = GaussianNB()
    svm = SVC()
    forest = RandomForestClassifier(n_estimators=100, random_state=25)

    algorithms = [log_reg, gnb, svm, forest]

    # Save the Results into a Textfile (the text file is created once and results are appended to the end of the file
    with open(
            "Bootstrap_Results.txt",
            "a") as f:

        # store some general information
        f.write(
            "\n" + "\n" + "Accuracy Prediction and Evaluation Using Bootstrapping with all features" + "\n" + "\n")
        f.write("Task: " + str(task) + "\n" + "\n")
        print("Processing Task: " + task)

        for algorithm in algorithms:

            # Vanilla bootstrap Implementation
            from sklearn.utils import resample

            # store bootstrap results
            acc_scores = []

            # create a groups list and rename the groups in ascending order
            new_groups = np.arange(len(np.unique(groups)))

            # choose number of bootstrap samples
            num_bootstraps = 1000

            # start bootstrapping
            for i in range(num_bootstraps):

                # hacky way to use the resample_df function for the iv series
                new_iv = iv.to_frame()

                # resample the groups
                train_groups = resample(new_groups)
                # get the test groups (groups not used in train groups)
                test_groups = [i for i in new_groups if i not in train_groups]

                # get the train and test datasets
                X_train = resample_df(dv, train_groups)
                y_frame_train = resample_df(new_iv, train_groups)
                y_train = pd.Series(y_frame_train.iloc[:, 0])

                X_test = resample_df(dv, test_groups)
                y_frame_test = resample_df(new_iv, test_groups)
                y_test = pd.Series(y_frame_test.iloc[:, 0])

                # Standardize the Features
                from sklearn import preprocessing
                scaler = preprocessing.StandardScaler().fit(X_train)
                X_train = scaler.transform(X_train)
                X_test = scaler.transform(X_test)

                # feature selection
                # Choose a feature selection procedure
                sel_features, x_train_trans, x_test_trans = classifier_feature_selection(dv, X_train, y_train, X_test,
                                                                                         method="all", threshold=0.15)

                # choose an algorithm
                clf = algorithm

                # Fit the training data to the model
                clf.fit(x_train_trans, y_train)

                # predict the test data labels
                y_pred = clf.predict(x_test_trans)

                # get evaluation metrics
                from sklearn.metrics import accuracy_score
                from sklearn.metrics import cohen_kappa_score
                from sklearn.metrics import brier_score_loss
                from sklearn.metrics import f1_score
                from sklearn.metrics import roc_auc_score
                test_acc = accuracy_score(y_test, y_pred)
                # test_acc = cohen_kappa_score(y_test, y_pred)
                # test_acc = brier_score_loss(y_test, y_pred)
                # test_acc = f1_score(y_test, y_pred)
                # test_acc = roc_auc_score(y_test, y_pred)

                # save the accuracy score of the bootstrapped sample
                acc_scores.append(test_acc)


            # write the results down in the text file
            f.write("Algorithm: " + str(algorithm)[:5] + "\n")
            print("\n", str(algorithm)[:5])
            f.write("Bootstrap Mean: " + str(np.mean(acc_scores)) + "\n")
            f.write("Bootstrap Std: " + str(np.std(acc_scores)) + "\n")
            print("Bootstrap mean: ", np.mean(acc_scores))
            print("Bootstrap std: ", np.std(acc_scores))
            lower = np.round(np.percentile(acc_scores, 2.5), 3)
            upper = np.round(np.percentile(acc_scores, 97.5), 3)
            f.write('Bootstrap 95%% Confidence interval: [%.2f, %.2f]' % (100 * lower, 100 * upper) + "\n" + "\n")
            print('Bootstrap 95%% Confidence interval: [%.2f, %.2f]' % (100 * lower, 100 * upper), "\n", "\n")

            # Create and save a plot of the procedure
            plt.hist(acc_scores, bins=np.arange(np.min(acc_scores), np.max(acc_scores), 2.5),
                     alpha=0.6, rwidth=1.0, edgecolor="black", color="orange")
            ylim = plt.ylim()
            plt.plot(2 * [np.mean(acc_scores)], ylim, "--r", linewidth=3,
                     label="Mean Accuracy: " "%s" % (np.round(np.mean(acc_scores), 2)))
            plt.plot(2 * [lower], ylim, "--b", linewidth=2, label="CI95: " "[%s, %s]" % (lower, upper))
            plt.plot(2 * [upper], ylim, "--b", linewidth=2)
            plt.plot(2 * [50], ylim, "--g", linewidth=3, label="Chance: 50.00")
            plt.ylim(ylim)
            plt.xlabel("Accuracy Score")
            plt.ylabel("Frequency")
            plt.title("Bootstrap " + task + str(algorithm)[:5] + "")
            plt.legend(loc="upper left")
            # plt.savefig("Bootstrap_" + task + str(algorithm)[:5] + ".png")
            plt.show()

        f.close()


#############################
# Code that runs the analysis
#############################

# the below code takes the dictionary with the chosen analysis as the input parameter and runs the chosen analysis
# it will not work if the analysis variable is set to a value other than the 4 options in the analysis setup

def run_analysis(chosen_analysis):

    print("Running " + chosen_analysis["name"])

    for target in chosen_analysis["targets"]:

        print("Running the analysis for task " + target)

        if chosen_analysis["name"] == "t_test_manipulation_check":

            dv = manipulation_check_data_t_test(target)
            paired_sample_t_test(dv)

        elif chosen_analysis["name"] == "t_test_mouse_usage":

            dv = mouse_data_t_test(target)
            paired_sample_t_test(dv)

        elif chosen_analysis["name"] == "classification_permutation":

            dv, iv, groups = ml_mouse_data(target)
            ml_permutation_test(target, dv, iv, groups)

        elif chosen_analysis["name"] == "classification_bootstrap":

            dv, iv, groups = ml_mouse_data(target)
            ml_bootstrap(target, dv, iv, groups)

    print("Analysis finished!")


# run the analysis
run_analysis()


