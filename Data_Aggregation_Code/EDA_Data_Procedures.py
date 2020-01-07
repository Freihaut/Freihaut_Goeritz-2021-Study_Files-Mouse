'''
Code to calculate EDA parameters from the EDA raw data files per participant (and visualize the data).

THIS IS A PROCEDURE THAT IS USED TOGETHER WITH THE aggregated_dataset_creation.py file

The timestamps of the EDA data are matched with the timestamps of the data during the experiment to calculate
the EDA paramters during the desired experimental phase

The code most certainly is far from perfect and was written to fit the data analysis purpose of the study rather
than to establish a multi-purpose solution. This version of the code represents a stripped version that includes
(almost exclusively) only include the procedures that were used in the final data analysis as reported in the
manuscript.


For questions or error reporting contact: paul.freihaut@psychologie.uni-freiburg.de
'''



# Import Core Libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import operator


# the input dataset is the experiment raw dataset (Raw_Data_Experiment.json)
def get_eda_data(dataset):

    import os

    # get the relative path to the dataset
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    targetDir = os.path.join(parentDir, "Datasets")

    # Path to folder with raw eda data files
    data_path = targetDir + "/Raw_Data_EDA/"

    results = {}

    participant_index = 1

    # loop over each participant (as stored in the raw dataset)
    for participant in dataset:

        # if the participant completed the entire experiment
        if "phaseFinishedTimestamps" in dataset[participant] and "BfiNeuroticism" in dataset[participant]["phaseFinishedTimestamps"]:

            # save the data of each participant seperately for the low-stress and high-stress condition
            results[participant + "_HS"] = {}
            results[participant + "_LS"] = {}

            # get the participants physioID
            physio_id = dataset[participant]["MetaData"]["physioDataId"]

            # Use the physioID to grab the eda data file of the participant
            eda_data = pd.read_csv(data_path + physio_id + ".csv", sep=";")

            # the timestamps of the experiment and eda data are in different formats and need to be converted
            # Convert the UniversalTimestamps into an Epoch Timestamps (timestamp had a 2-hour offset with conversion
            # formular
            eda_data["convertedTimestamp"] = [int(((i - 621355968000000000) / 10000)) for i in
                                                eda_data["UniversalTimestamp"]]

            # Convert the EDA datapoint string values into floats
            eda_data["EDA"] = [float(i) for i in eda_data["EDA"]]

            # split the heart dataset into phases

            # get the participants timestamp information and sort it in ascending order
            sorted_timestamp_data = sorted(dataset[participant]["phaseFinishedTimestamps"].items(),
                                           key=operator.itemgetter(1))

            # create a list that has the start and end timestamp of the first and last task in each condition
            conditions_task = [{sorted_timestamp_data[11][0][:2] + "_tasks": [sorted_timestamp_data[11][1], sorted_timestamp_data[27][1]]},
                               {sorted_timestamp_data[30][0][:2] + "_tasks": [sorted_timestamp_data[30][1], sorted_timestamp_data[46][1]]}]

            # create a list that has the start and end timestamp of the starting and end page of each condition
            conditions_all = [{"LS_all": [dataset[participant]["phaseFinishedTimestamps"]["LS_Instr"],
                                       dataset[participant]["phaseFinishedTimestamps"]["LS_End"]]},
                              {"HS_all": [dataset[participant]["phaseFinishedTimestamps"]["HS_Instr"],
                                       dataset[participant]["phaseFinishedTimestamps"]["HS_End"]]}]

            # Make a list that contains the starting and end point of each experimental phase
            phases = [{sorted_timestamp_data[i+1][0]: [sorted_timestamp_data[i][1], sorted_timestamp_data[i+1][1]]}
                      for i in range(len(sorted_timestamp_data) - 1)]

            # add the condition time stamps to the phase list
            phases.extend(conditions_task)
            phases.extend(conditions_all)

            # a list with all phases during which the eda parameters are supposed to be calculated

            # complete list of all phases during the condition
            relevant_phases = ["HS_LoadingTask", "HS_Mental_Arithmetic_DragDrop", "HS_DragDrop",
                               "HS_Mental_Arithmetic_PatternTyping", "HS_PatternTyping",
                               "HS_Mental_Arithmetic_FollowBox", "HS_FollowBox", "HS_Mental_Arithmetic_PointClick",
                               "HS_PointClick", "HS_Mental_Arithmetic_Drawing", "HS_Drawing", "LS_LoadingTask",
                               "LS_Mental_Arithmetic_DragDrop", "LS_DragDrop", "LS_Mental_Arithmetic_PatternTyping",
                               "LS_PatternTyping", "LS_Mental_Arithmetic_FollowBox", "LS_FollowBox",
                               "LS_Mental_Arithmetic_PointClick", "LS_PointClick", "LS_Mental_Arithmetic_Drawing",
                               "LS_Drawing", "HS_all", "LS_all", "HS_tasks", "LS_tasks"]

            # alternatively a list of the eda data during the tasks in each condition only
            relevant_phases = ["HS_LoadingTask", "HS_DragDrop", "HS_PatternTyping", "HS_FollowBox", "HS_PointClick",
                               "HS_Drawing",
                               "LS_LoadingTask", "LS_DragDrop", "LS_PatternTyping", "LS_FollowBox", "LS_PointClick",
                               "LS_Drawing"]

            index = 0
            # loop over all phases
            for dic in phases:
                for phase in dic:
                    # only calc params from the phases in the experimental conditions
                    if phase in relevant_phases:

                        # get eda data during the phase (time interval)
                        phase_data = eda_data.loc[(dic[phase][0] < eda_data["convertedTimestamp"]) &
                                                    (eda_data["convertedTimestamp"] < dic[phase][1])]


                        # Apply a moving median filter to the data using a window size as big as the sampling rate(20Hz)
                        # and drop the NaN values
                        median_data = phase_data["EDA"].rolling(20).median().dropna()


                        ####
                        # Plot the phase data per participant
                        ####
                        # index += 1
                        # plot_data = median_data
                        # timestamps = np.array(phase_data["convertedTimestamp"])
                        # timestamps = timestamps - timestamps[0]

                        # # plt.subplot(2, 1, index)
                        # # plt.title(phase + "_" + participant)
                        # plt.plot(plot_data)
                        # plt.plot(phase_data["EDA"])
                        #
                        # plt.show()

                        # Calculate the eda parameters
                        eda_params = calc_eda_params(median_data, phase)

                        # store the calculated eda parameters in the corresponding dictionary
                        if "HS" in phase:
                            results[participant + "_HS"].update(eda_params)
                            results[participant + "_HS"]["par_index"] = participant_index
                            results[participant + "_HS"]["condition"] = 0
                        else:
                            results[participant + "_LS"].update(eda_params)
                            results[participant + "_LS"]["par_index"] = participant_index
                            results[participant + "_LS"]["condition"] = 1

        participant_index += 1

    # save the final results data as a pandas dataframe and return the dataframe, it contains a row per condition
    # per participant containing all calculated eda parameters
    final_data = pd.DataFrame(results).T
    print("EDA Data Successfully Processed!")
    return final_data


# function to calculate the eda parameters
def calc_eda_params(data, phase):

    params = {}

    # calculate different eda parameters using the rolling median eda datapoint list
    params.update({
        # phase[2:] + "_Datapoints": len(data),
        phase[2:] + "_Mean_Resistance": np.mean(data),
        # phase[2:] + "_Median_Resistance": np.median(data),
        # phase[2:] + "_Std_Resistance": np.std(data),
        # phase[2:] + "_Max_Resistance": max(data),
        # phase[2:] + "_Min_Resistance": min(data),
        # phase[2:] + "_RootMeanSquare_Resistance": np.sqrt(np.mean(np.square(data))),
    })

    return params