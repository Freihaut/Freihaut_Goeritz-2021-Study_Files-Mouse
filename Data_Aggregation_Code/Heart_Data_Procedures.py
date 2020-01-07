'''
Code to calculate heart data parameters from the heart raw data files per participant (and visualize the data).

THIS IS A PROCEDURE THAT IS USED TOGETHER WITH THE aggregated_dataset_creation.py file

The timestamps of the heart data are matched with the timestamps of the data during the experiment to calculate
the heart paramters during the desired experimental phase

The code most certainly is far from perfect and was written to fit the data analysis purpose of the study rather
than to establish a multi-purpose solution. This version of the code represents a stripped version that includes
(almost exclusively) only include the procedures that were used in the final data analysis as reported in the
manuscript.

For questions or error reporting contact: paul.freihaut@psychologie.uni-freiburg.de
'''

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import operator
# HRV Analysis package used https://github.com/Aura-healthcare/hrvanalysis
import hrvanalysis


# the input dataset is the experiment raw dataset (Raw_Data_Experiment.json)
def get_heart_data(dataset):

    import os

    # get the relative path to the dataset
    fileDir = os.path.dirname(os.path.abspath(__file__))
    parentDir = os.path.dirname(fileDir)
    targetDir = os.path.join(parentDir, "Datasets")

    # Path to folder with raw eda data files
    data_path = targetDir + "/Raw_Data_Heart/"

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

            # Use the physioID to grab the the heart data file of the participant
            heart_data = pd.read_csv(data_path + physio_id + ".csv", sep=";")

            # the timestamps of the experiment and eda data are in different formats and need to be converted
            # Convert the UniversalTimestamps into an Epoch Timestamps (timestamp had a 2-hour offset with conversion
            # formular
            heart_data["convertedTimestamp"] = [int(((i - 621355968000000000) / 10000)) for i in
                                                heart_data["UniversalTimestamp"]]

            # Convert the RR-Interval String values into floats
            heart_data["IBI"] = [float(i.replace(",", ".")) for i in heart_data["IBI"]]

            # split the heart dataset into phases

            # get the participants timestamp information and sort it in ascending order
            sorted_timestamp_data = sorted(dataset[participant]["phaseFinishedTimestamps"].items(),
                                           key=operator.itemgetter(1))

            # create a list that has the start and end timestamp of the first and last task in each condition
            conditions_task = [{sorted_timestamp_data[11][0][:2] + "_tasks": [sorted_timestamp_data[11][1], sorted_timestamp_data[27][1]]},
                               {sorted_timestamp_data[30][0][:2] + "_tasks": [sorted_timestamp_data[30][1], sorted_timestamp_data[46][1]]}]

            # create a list that has the start and end timestamp of the starting and end page of each condition
            conditions_all = [{"LS_all_": [dataset[participant]["phaseFinishedTimestamps"]["LS_Instr"],
                                       dataset[participant]["phaseFinishedTimestamps"]["LS_End"]]},
                              {"HS_all_": [dataset[participant]["phaseFinishedTimestamps"]["HS_Instr"],
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

                        # get heart data during the phase
                        phase_data = heart_data.loc[(dic[phase][0] < heart_data["convertedTimestamp"]) &
                                                    (heart_data["convertedTimestamp"] < dic[phase][1])]

                        ####
                        # Plot the phase data per participant
                        ####
                        # index += 1
                        # plot_data = phase_data["IBI"]
                        # timestamps = np.array(phase_data["convertedTimestamp"])
                        # timestamps = timestamps - timestamps[0]
                        #
                        # plt.subplot(2, 1, index)
                        # plt.title(phase + "_" + participant)
                        # plt.plot(timestamps, plot_data)
                        # plt.show()

                        # get number of valid datapoints, 350 and 1800 are chosen as cutoff-values as data points
                        # below or above the threshold likely represent artifacts instead of real values
                        valid_datapoints = sum([1 for i in phase_data["IBI"] if 350 < i < 1800])

                        # calculations for the high-stress condition
                        if "HS" in phase:
                            # get some descriptive statistics about the data
                            # results[participant + "_HS"].update({
                            #     phase[2:] + "_Datapoints": len(phase_data["IBI"]),
                            #     phase[2:] + "_Datapoints_With_0": len(phase_data[phase_data["IBI"] == 0]),
                            #     phase[2:] + "_Datapoints_Below_350": len(phase_data[phase_data["IBI"] < 350]),
                            #     phase[2:] + "_Datapoints_Above_1800": len(phase_data[phase_data["IBI"] > 1800]),
                            #     phase[2:] + "_Valid_Datapoints": valid_datapoints
                            # })

                            # calculate hrv parameters if there is a sufficient ammout of heart data in the phase
                            if valid_datapoints > 5:
                                # calculate the number of bad datapoints compared to the total number of datapoints in
                                # the phase (0 value data points are a special kind of artifacts that are removed
                                # seperately --> the heart rate sensor procudes a 0 value datapoint if no rr-interval
                                # is recorded during a certain timeframe)
                                bad_datapoints = (len(phase_data[phase_data["IBI"] < 350]) +
                                                  len(phase_data[phase_data["IBI"] > 1800]) -
                                                  len(phase_data[phase_data["IBI"] == 0])) / len(phase_data["IBI"])
                                # save the number of bad datapoints
                                # results[participant + "_HS"].update({
                                #     phase[2:] + "_artifacts_without_0": bad_datapoints
                                # })

                                # if the ammount of bad datapoints is too high, dont calculate heart parameters
                                if bad_datapoints > 0.05:
                                    print("Too many bad datapoints in phase " + phase + " for participant " + participant,
                                          "\n", bad_datapoints)

                                else:
                                    hrv_params = calc_hrv_params(phase_data, phase)
                                    results[participant + "_HS"].update(hrv_params)

                            else:
                                print("Not enough valid datapoints in phase " + phase + " for participant " + participant)

                        # calculations for the low-stress condition
                        else:
                            # get some descriptive statistics about the data
                            # results[participant + "_LS"].update({
                            #     phase[2:] + "_Datapoints": len(phase_data["IBI"]),
                            #     phase[2:] + "_Datapoints_With_0": len(phase_data[phase_data["IBI"] == 0]),
                            #     phase[2:] + "_Datapoints_Below_350": len(phase_data[phase_data["IBI"] < 350]),
                            #     phase[2:] + "_Datapoints_Above_1800": len(phase_data[phase_data["IBI"] > 1800]),
                            #     phase[2:] + "_Valid_Datapoints": valid_datapoints
                            # })

                            # calculate hrv parameters if there is a sufficient ammout of heart data in the phase
                            if valid_datapoints > 5:
                                bad_datapoints = (len(phase_data[phase_data["IBI"] < 350]) + len(
                                    phase_data[phase_data["IBI"] > 1800]) - len(
                                    phase_data[phase_data["IBI"] == 0])) / len(phase_data["IBI"])
                                # save the number of bad datapoints
                                # results[participant + "_LS"].update({
                                #     phase[2:] + "_artifacts_without_0": bad_datapoints
                                # })

                                # if the ammount of bad datapoints is too high, dont calculate heart parameters
                                if bad_datapoints > 0.05:
                                    print(
                                        "Too many bad datapoints in phase " + phase + " for participant " + participant,
                                        "\n", bad_datapoints)

                                else:
                                    hrv_params = calc_hrv_params(phase_data, phase)
                                    results[participant + "_LS"].update(hrv_params)

                            else:
                                print(
                                    "Not enough valid datapoints in phase " + phase + " for participant " + participant)

        participant_index += 1

    # save the final results data as a pandas dataframe and return the dataframe, it contains a row per condition
    # per participant containing all calculated heart parameters
    final_data = pd.DataFrame(results).T
    print("Heart Data Successfully Processed!")
    return final_data


# function to calculate the heart parameters
def calc_hrv_params(data, phase):

    params = {}

    # Delete 0-Values from Dataset (prevent interpolation of 0-values)
    data = [i for i in data["IBI"] if i != 0]

    # remove outlier data points using the hrv analysis package https://github.com/Aura-healthcare/hrvanalysis
    rr_intervals_without_outliers = hrvanalysis.remove_outliers(rr_intervals=data, low_rri=350, high_rri=1800)
    # interpolate outliers using the hrv analysis package https://github.com/Aura-healthcare/hrvanalysis
    preprocessed_data = hrvanalysis.interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                           interpolation_method='linear')

    # If the first or last datapoint is a NaN, it can`t be interpolated and must be kicked
    cleaned_data = [i for i in preprocessed_data if not np.isnan(i)]

    # The HRV package calculates different heart rate related parameters (of which only the mean heart rate is used
    # as a stressmarker in the present study, the full code to calculate all HRV parameters is listed below)
    # see https://github.com/Aura-healthcare/hrvanalysis

    # Time Domain Analysis
    hrv_time_domain = hrvanalysis.get_time_domain_features(cleaned_data)

    # Only get the mean heart rate parameter
    params.update({phase[3:] + "_mean_HR": hrv_time_domain["mean_hr"]})

    # get all HRV time domain parameters:
    # Mean_NNI, SDNN, SDSD, NN50, pNN50, NN20, pNN20, RMSSD, Median_NN,
    # Range_NN, CVSD, CV_NNI, Mean_HR, Max_HR, Min_HR, STD_HR
    # for key in hrv_time_domain.keys():
    #     params.update({phase[3:] + "_" + key: hrv_time_domain[key]})

    # Frequency Domain Anaylsis
    # hrv_frequency_domain = hrvanalysis.get_frequency_domain_features(cleaned_data, method='welch',
    #                                                                   sampling_frequency=4,
    #                                                                  interpolation_method='cubic',
    #                                                                  vlf_band=(0.003, 0.04), lf_band=(0.04, 0.15),
    #                                                                  hf_band=(0.15, 0.4))
    # get all HRV time domain parameters:
    # LF, HF, VLF, LH/HF ratio, LFnu, HFnu, Total_Power
    # for key in hrv_frequency_domain.keys():
    #     params.update({phase[2:] + "_" + key: hrv_frequency_domain[key]})

    # Geometrical Analysis
    # hrv_geometrical_features = hrvanalysis.extract_features.get_geometrical_features(cleaned_data)
    # get all geometrical analysis parameters:
    # Triangular_index, TINN
    # for key in hrv_geometrical_features.keys():
    #     params.update({phase[2:] + "_" + key: hrv_geometrical_features[key]})

    # CSI/CVI analysis
    # hrv_csi_cvi_features = hrvanalysis.extract_features.get_csi_cvi_features(cleaned_data)
    # get all CSI/CVI analysis parameters:
    # CSI, CVI, Modified_CSI, SD1, SD2, SD1/SD2 ratio, SampEn
    # for key in hrv_csi_cvi_features.keys():
    #     params.update({phase[2:] + "_" + key: hrv_csi_cvi_features[key]})

    return params
