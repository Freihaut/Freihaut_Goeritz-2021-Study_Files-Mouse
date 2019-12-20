# Import the core libraries
import pandas as pd
from itertools import groupby
import operator
from scipy import interpolate
import numpy as np
import math
import matplotlib.pyplot as plt

# Helper Functions for Mouse Data Calculations


# Interpolate the Mouse Data into equal time intervals (other researchers interpolate into an equal ammount of
# datapoints per trial (see Yamauchi & Xiao, 2017; Freeman et al. 2009)
# Input is the array with the original mousedatapoint objects
def interpolate_mouse_data(mouse_data):

    key, value1, value2 = "eventType", "MousePositionChanged", "MouseClick"

    # Seperately save the x- & y-coordinate aswell as the timestamp of each datapoint
    x_pos = []
    y_pos = []
    time = []
    # Alle Mauscklick Events werden auch gespeichert
    # mouseClicks = []

    # go trough all mousePositionChanged datapoints
    for datapoint in mouse_data:
        if datapoint[key] == value1:
            # save the x- & y-coordinate and the timestamp of the datapoint
            x_pos.append(datapoint["x"])
            y_pos.append(datapoint["y"])
            time.append(datapoint["time"])

    # if there is not enough data to interpolate, return -99
    if len(x_pos) < 2:
        return -99

    # Old Calculation if mouseclicks are relevant!
    # for datapoint in mouseData:
    #     if datapoint[key] == value2:
    #         mouseClicks.append(datapoint)
    #     elif datapoint[key] == value1:
    #         xPos.append(datapoint["x"])
    #         yPos.append(datapoint["y"])
    #         time.append(datapoint["time"])

    # creates an interpolation function using the x- & y-coordinate and the timeline
    inter_x = interpolate.interp1d(time, x_pos)
    inter_y = interpolate.interp1d(time, y_pos)

    # set start and end point of new timeline
    start = time[0]
    end = time[-1]

    # create a new timeline array with equal timesteps using the start and endpoints
    equal_time_intervals = np.arange(start, end, 15)

    # use the interpolation function to calculate the interpolated x- and y-coordinates on the equally spaced time
    # interval
    new_x = np.round(inter_x(equal_time_intervals), decimals=3)
    new_y = np.round(inter_y(equal_time_intervals), decimals=3)


    # bring the seperated dapoints together to a list containing datapoints with the corresponding coordinates and
    # timestamp
    joined_list = []

    filler = {}

    for i, j, k in zip(new_x, new_y, equal_time_intervals):
        filler["x"] = i
        filler["y"] = j
        filler["time"] = k
        joined_list.append(filler)
        filler = {}

    # chronologically sort datapoints by time -> necessary if mouseclick data needs to be integrated
    # interpolMouseData = sorted(joinedList, key=itemgetter("time"))

    # visualize the original vs the interpolated mouse data (x- & y-coordinates)
    # plt.plot(xPos, yPos, linestyle="--")
    # plt.plot(new_x, new_y, linestyle=":")
    #
    # fig, ax = plt.subplots()
    # ax.plot(xPos, yPos, 'o', new_x, new_y, '.')
    #
    # plt.show()

    return joined_list


# Removes mouse movement artifacts -> Artifact if x- & y- coordinate of consecutive movement datapoints are equal
# and if the timestamp of two consecutive movement datapoints are equal
def clean_mouse_data(mouse_data):

    # Sort the page data by timestamp (might not be needed because the mouse data are saved in an array like structure
    # in firebase --> when in doubt, leave it in
    sorted_page_data = sorted(mouse_data, key=operator.itemgetter("time"))

    key, value1, value2 = "eventType", "MousePositionChanged", "MouseClick"

    # Save the last datapoint
    last_coordinates = [0, 0]
    last_timestamp = 0

    # save the cleaned datapoints
    clean_list = []

    # count the number of removed datapoints and total datapoints
    artifacts = 0
    total_datapoints = 0

    # Loop over all datapoints
    for datapoint in sorted_page_data:
        # if its a mousePositionChanged Datapoint
        if datapoint[key] == value1:
            # and if the x- & y- coordinates are not equal to the previous datapoint or the timestamps are not equal
            if ([datapoint["x"], datapoint["y"]] != last_coordinates) and (datapoint["time"] > last_timestamp):
                # save the datapoint in the clean list
                clean_list.append(datapoint)
                # save the coordinates and the timestamp of the datapoint
                last_coordinates = [datapoint["x"], datapoint["y"]]
                last_timestamp = datapoint["time"]
            else:
                # increase the artifact counter
                artifacts += 1
            # increase the datapoint counter
            total_datapoints += 1
        elif datapoint[key] == value2:
            # if its another datapoint
            clean_list.append(datapoint)

    # print("Percentage of Artifacts in Movement Data: " + str((artifacts / total_datapoints) * 100))

    return clean_list


# Functions to calculate Mouse Movement Parameters ############################


# Gets task time which is equal to the time difference between the last and first datapoint in the task
def get_mouse_task_time(mouse_data):

    # Get the highest and lowest timepoint in the mousedata array
    last_timestamp = max(i["time"] for i in mouse_data)
    first_timestamp = min(i["time"] for i in mouse_data)

    # calculate the the task time
    task_time = last_timestamp - first_timestamp

    return {"task_time_": task_time}


# Get speed, acceleration and higher derivate mouse movement parameters
# This function uses the interpolated mouse data where a datapoint`s structure is
# {x: x-coord., y: y-coord, time: timestamp}
def get_mouse_movement_parameters(mouse_data):

    # time constanct between two datapoints
    interpol = 15

    # Save the last x- & y-coordinates
    last_x = False
    last_y = False

    # save the distance values
    distance = []

    # Loop over all datapoints
    for datapoint in mouse_data:
        if last_x and last_y:
            # calculate the difference between the datapoint and the previous datapoints x- & y-positions
            dx = float(datapoint["x"]) - float(last_x)
            dy = float(datapoint["y"]) - float(last_y)
            # calculate the euclidean distance between the two datapoints and save it
            distance.append(math.sqrt(pow(dx, 2) + pow(dy, 2)))
        # save the last x and y values
        last_x = datapoint["x"]
        last_y = datapoint["y"]

    # Calc the speed (dist / time) by dividing through the time difference between the timepoints = 10
    speed = [(i/0.015) for i in distance]
    # calc the velcocity as the change in speed over the change in time = (speed2 - speed1) / 10
    accel = np.diff(speed) / interpol
    # Seperate the acceleration data into positive and negative acceleration
    accel_pos, accel_neg = [i for i in accel if i >= 0], [i for i in accel if i <= 0]
    # calc jerk (derivative of accel) as the change in accel over the change in time = (accel2 - accel1) / 10
    jerk = np.diff(accel) / interpol
    # seperate the jerk data into negative and positive jerk
    jerk_pos, jerk_neg = [i for i in jerk if i >= 0], [i for i in jerk if i <= 0]
    # calc snap (derivative of jerk) as the change in jerk over the change in time = (jerk2 - jerk1) / 10
    snap = np.diff(jerk) / interpol
    # seperate the snap data into positive and negative snap data
    snap_pos, snap_neg = [i for i in snap if i >= 0], [i for i in snap if i <= 0]

    # calculate and save results --> get the total distance (using interpolated data) aswell as the mean and standard
    # deviations of speed, acceleration, jerk and snap
    results = {"mouse_dist_": np.sum(distance), "speed_mean_": np.mean(speed), "speed_sd_": np.std(speed),
               "pos_accel_mean": np.mean(accel_pos), "pos_accel_sd": np.std(accel_pos),
               "neg_accel_mean": np.mean(accel_neg), "neg_accel_sd": np.std(accel_neg),
               "pos_jerk_mean": np.mean(snap_pos), "pos_jerk_sd": np.std(snap_pos),
               "neg_jerk_mean": np.mean(snap_neg), "neg_jerk_sd": np.std(snap_neg),
               "pos_snap_mean": np.mean(jerk_pos), "pos_snap_sd": np.std(jerk_pos),
               "neg_snap_mean": np.mean(jerk_neg), "neg_snap_sd": np.std(jerk_neg)}

    return results


# Gets the distance to an ideal (straight) line between the start and end of a mouse action
def get_dist_from_ideal_line(mouse_data):

    # Formula derived from https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

    # store the deviations from the ideal line
    deviation = []

    # loop over all trials
    for trial in mouse_data:

        interpol_trial = interpolate_mouse_data(trial)
        if interpol_trial != -99:
            # get the start and end positions of the trial as the start and end markers of the ideal line
            start_point = max(trial, key=lambda x: x["time"])
            end_point = min(trial, key=lambda x: x["time"])
            # loop over all datapoints from a trial
            for datapoint in interpol_trial:
                # calculate the distance of the given datapoint from the ideal line
                num = (end_point["y"] - start_point["y"]) * datapoint["x"] - \
                      (end_point["x"] - start_point["x"]) * datapoint["y"] + \
                      end_point["x"] * start_point["y"] - end_point["y"] * start_point["x"]
                den = math.sqrt(pow((end_point["y"] - start_point["y"]), 2)
                                + pow((end_point["x"] - start_point["x"]), 2))
                dist = abs(num) / den
                # append the distance to the deviation array
                deviation.append(dist)

    results = {"total_dev_ideal_line_": np.sum(deviation),
               "mean_dev_ideal_line_": np.mean(deviation),
               "sd_dev_ideal_line_": np.std(deviation)}

    return results


# calculates the angle between two consecutive mouse movement vectors
def get_mouse_angles(mouse_data):

    # store the x- & y-coordinates of the two previous datapoints to calculate the previous two mouse movement vectors
    coordinates_0 = False
    coordinates_1 = False

    # stores the angle between two vectors (made up of three consecutive datapoints)
    # 0 degrees = straight forward
    # 180 degrees = straight backwars
    # 0 to 90 degrees: forward direction
    # 90 bis 180 degrees: backward direction
    angle3points = []

    # loop over all movement datapoints
    for datapoint in mouse_data:
        # if there are values for the previous two datapoints
        if coordinates_0 and coordinates_1:
            # calculate the vector between the recent datapoint and the previous datapoint
            vector1 = np.array([datapoint["x"], datapoint["y"]]) - np.array(coordinates_1)
            # calculate the vector between the previous datapoint and the previous previous datapoint
            vector2 = np.array(coordinates_1) - np.array(coordinates_0)
            # calculate the angle between two consecutive vectors (range -180 to 180)
            # from https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
            angle = np.arctan2(np.linalg.det([vector1, vector2]), np.dot(vector1, vector2))

            # second possible way to calc the angle (range 0 - 180) (both results are identical, throws an error
            # for one participant, origin unknown)
            # unit_vec1 = vector1 / np.linalg.norm(vector1)
            # unit_vec2 = vector2 / np.linalg.norm(vector2)
            # angle_test = np.arccos(np.clip(np.dot(unit_vec1, unit_vec2), -1.0, 1.0))

            # save the angle in the array
            angle3points.append(np.degrees(abs(angle)))
        # if a previous datapoint exists
        if coordinates_1:
            # set the previous datapoint to be the previous previous datapoint
            coordinates_0 = coordinates_1
        # set this datapoint to be the previous datapoint
        coordinates_1 = [datapoint["x"], datapoint["y"]]

    results = {"angle_mean_": np.mean(angle3points), "angle_sd_": np.std(angle3points)}

    return results


# Helper Function to calculate the Sample Entropy from Wikipedia (https://en.wikipedia.org/wiki/Sample_entropy)
def sample_entropy(array, m, r):

    def _maxdist(x_i, x_j):
        result = max([abs(ua - va) for ua, va in zip(x_i, x_j)])

        return result

    def _phi(m):
        x = [[array[j] for j in range(i, i + m - 1 + 1)] for i in range(N - m + 1)]

        C = 1. * np.array(
            [len([1 for j in range(len(x)) if i != j and _maxdist(x[i], x[j]) <= r]) for i in range(len(x))])

        return sum(C)

    N = len(array)

    return -np.log(_phi(m + 1) / _phi(m))


# calculate the number of directional changes on the x-axis and the sample entropy of the x- & y-coordinate vector
def get_x_y_flips_and_sample_entropy(mouse_data):

    # get all x- & y-coordinates seperately
    x_coordinates = [datapoint["x"] for datapoint in mouse_data]
    y_coordinates = [datapoint["y"] for datapoint in mouse_data]

    # calculate the shifts in x- & y-coordinates (difference between the coordinates)
    x_shifts = np.diff(x_coordinates)
    y_shifts = np.diff(y_coordinates)

    # function to calculate the number of flips (changing of direction on the axis)
    # alternative oneliner: flips = sum(array[i+1] * array[i] < 0 for i in range(len(array)-1)) cant be used because
    # this would ignore cases where there is movement in one direction, then no movement and then movement in the
    # opposite direction!
    def _calc_flips(array):

        # store the number of flips
        flips = 0
        # store the coordinates before and after a 0 movement on the axis
        coord_before_0 = 0
        coord_after_0 = 0

        # loop through all datapoints in the array
        for i in range(len(array)-1):
            # calculate the product of consecutive datapoints
            comp = array[i + 1] * array[i]
            # if the product is smaller than 0, a shift happened
            if comp < 0:
                flips += 1
            # if the product is excatly 0
            if comp == 0:
                # if the first datapoint is not 0
                if array[i] != 0:
                    # save it
                    coord_before_0 = array[i]
                # if the second datapoint is not 0
                elif array[i + 1] != 0:
                    # save it
                    coord_after_0 = array[i + 1]
                    # if the product of the datapoint before and after the 0 event is less than 0, a shift happened
                    if coord_before_0 * coord_after_0 < 0:
                        flips += 1

        return flips

    # Get the number of x- & y-flips
    x_flips = _calc_flips(x_shifts)
    y_flips = _calc_flips(y_shifts)

    # calculate the sample entropy using the recommendation from Hehman, Stolier and Freeman (2015):
    # window size m = 3 and tolerance r = 0.2 * std(shifted_array)
    # x_entropy = sample_entropy(x_shifts, 3, 0.2 * np.std(x_shifts))
    # y_entropy = sample_entropy(y_shifts, 3, 0.2 * np.std(y_shifts))
    # add if entropy is calculated: "x_entropy": x_entropy, "y_entropy": y_entropy

    results = {"x_flips_": x_flips, "y_flips_": y_flips}

    return results


# Mouse Movement Visualization Procedures ##########################################

def visualize_mouse_movement(data, participant, task, taskindex):

    key, value, value2 = "eventType", "MousePositionChanged", "MouseClick"

    # saves the movement data seperately to plot x against y (as positions on the screen)
    mouse_move_x_values = []
    mouse_move_y_values = []

    # saves the coordinates of the mouseclicks to plot them as x and y positions on the screen
    mouse_click_x_values = []
    mouse_click_y_values = []

    # loop over all datapoints
    for datapoint in data:
        # if its a movement point save the coordinates to the movement arrays
        if key in datapoint and datapoint[key] == value:
            mouse_move_x_values.append(datapoint["x"])
            mouse_move_y_values.append(datapoint["y"])
        # if its a click save the coordinates to the click array
        elif key in datapoint and datapoint[key] == value2:
            mouse_click_x_values.append(datapoint["x"])
            mouse_click_y_values.append(datapoint["y"])


    # create a scatterplot using the movement and click data

    # figsize=((1920/mydpi)/2, (1080/mydpi)/2)
    # get the dpi of the screen
    mydpi = 96
    # set the fig size to the size and dpi of the screen
    fig = plt.figure(figsize=((1920/mydpi)/2.5, (1080/mydpi)/2.5), dpi=mydpi)

    # create a list with numbers in ascending order corresponding to the lenth of the movement data, this list is
    # used to give each movement datapoint a unique color on the color map of the plot
    colors = np.arange(len(mouse_move_x_values))

    # get the axis of the plot and set its size to the screen size
    axes = plt.gca()
    axes.set_ylim([1080, 0])
    axes.set_xlim([0, 1920])

    # output a scatterplot of the movement data, each datapoint gets a color corresponing to its number in the color
    # list according to a color map (default color map is used)
    # s=(72. / fig.dpi) ** 2 --> size of a dot is equal to one pixel (used a higher number, because dots are really
    # small in the small pictures
    plt.scatter(mouse_move_x_values, mouse_move_y_values, c=colors, marker="o", s=((72. / fig.dpi) ** 2)*5)

    # plot the click datapoints aswell
    plt.scatter(mouse_click_x_values, mouse_click_y_values, color="black", marker="o", s=((72. / fig.dpi) ** 2)*5)

    # give the plot a title
    # plt.title(task + "_" + participant)

    # hide the axis
    plt.axis("off")

    # show the plot
    # plt.show()

    # save the figure in the corresponding folder (bbox_inches: tight removes some unnecessary whitespace)
    # plt.savefig('Task_vs_Task/' + task[3:] + "_" + str(participant) + "_" + str(taskindex) + '.png')

    plt.savefig('Loading_Bilder/' + task + "_" + str(participant) + '.png', bbox_inches="tight")
    plt.close()


# Plan - Calculate Mouse Data Seperately for Each Task using the same helper functions but slightly different logic
# depending on the task --> e.g. if the task allows for the calculation of ideal line difference measurements


# Mouse Tasks --> Es muss immer darauf geachtet werden, dass die Aufgabe komplett ausgeführt wurde, bzw. es muss
# geprüft werden, ob die Aufgabe komplett ausgefüllt wurde!

# Point & Click Task: Ab dem ersten (erfolgreichen) Klick auf den Mittelkreis bis zum Ende = letzter Klick
def get_point_click_data(dataset):

    pc_task = ["HS_PointClick", "LS_PointClick"]

    results = {}

    participant_index = 1

    bad_cases_point_click = ["INFvFzlNN7UeZRqvtoe8hejtnvX2",
                             "PRPyIVrPUVgCFtZ60nqvXc4wUov2",
                             "Vhi1KMa2MecuTnTzWb8QBp9rNDw1",
                             "X5mfB1vgISTp6cagPLnp0zyh4EI2",
                             "ZnI96HDrRZV9xNlfQxgTU0CeoDX2",
                             "zf3H80XYGSf9U3pZM5xxOm69qTT2"]

    for participant in dataset:

        # Dictionary for row data per participant
        results[participant] = {}

        # Dictionary for calculating the difference scores between the conditions
        diff_creation = {}

        task_index = 0

        for task in pc_task:

            # create a row for each task
            results[participant + "_" + task[:2]] = {}

            if task in dataset[participant]:

                all_data = dataset[participant][task]
                cleaned_data = clean_mouse_data(all_data)
                # print(task, participant_index, len(cleaned_data))

                # create a list with all data excluding the mousemovement to the first circle
                task_data = [datapoint for datapoint in cleaned_data if 0 < datapoint["circlesClicked"] < 26]

                # Below code is used to create a dictionary with the raw eda data per participant per phase
                # from collections import defaultdict

                # results[participant][task] = defaultdict(list)
                #
                # for datapoint in task_data:
                #     results[participant][task]["circlesClicked"].append(datapoint["circlesClicked"])
                #     results[participant][task]["eventType"].append(datapoint["eventType"])
                #     results[participant][task]["time"].append(datapoint["time"])
                #     results[participant][task]["x"].append(datapoint["x"])
                #     results[participant][task]["y"].append(datapoint["y"])
                #
                # results[participant][task]["DiffTime"] = [i - min(results[participant][task]["time"]) for i in results[participant][task]["time"]]
                # end of code for raw data dictionary creation

                # visualize_mouse_movement(task_data, participant_index, task, task_index)

                task_index += 1

                interpol_task_data = interpolate_mouse_data(task_data)

                # Split the list into lists with the trial data (data between clicking on two targets)
                trial_data = [list(g) for k, g in groupby(task_data, operator.itemgetter("circlesClicked"))]
                # if len(trial_data) < 25:
                #     print(participant + " has completed " + str(len(trial_data)) + " trials in " + task)


                # calculate relevant parameters
                parameters = {}

                # Calc Task Time
                task_time = get_mouse_task_time(interpol_task_data)
                parameters.update(task_time)
                # Movement related parameters
                movement_params = get_mouse_movement_parameters(interpol_task_data)
                parameters.update(movement_params)
                # Angle Parameters
                angles = get_mouse_angles(interpol_task_data)
                parameters.update(angles)
                # Entropy and x-y-flips
                flips_entropy = get_x_y_flips_and_sample_entropy(interpol_task_data)
                parameters.update(flips_entropy)
                # Distance from Ideal Line Parameters
                dist_line = get_dist_from_ideal_line(trial_data)
                parameters.update(dist_line)
                # Number of trials
                parameters.update({"num_trials": len(trial_data)})

                # save task parameters
                diff_creation[task] = parameters

                # save and output parameters
                for param in parameters:
                    # results[participant][task + "_" + param] = np.round(parameters[param], 3)
                    results[participant + "_" + task[:2]][task[3:] + "_" + param] = np.round(parameters[param], 3)


                # Add information about participant and trial
                # results[participant + "_" + task[:2]][task[3:] + "_par_index"] = participant_index
                # if task[:2] == "HS":
                #     results[participant + "_" + task[:2]]["condition"] = 0
                # elif task[:2] == "LS":
                #     results[participant + "_" + task[:2]]["condition"] = 1

        # save difference value parameters in output dictionary
        # if "HS_PointClick" in diff_creation:
        #     for item in diff_creation["HS_PointClick"]:
        #         if item in diff_creation["LS_PointClick"]:
        #             results[participant]["Diff_PointClick_" + item] = diff_creation["HS_PointClick"][item] - \
        #                                                            diff_creation["LS_PointClick"][item]

        participant_index += 1

    # save the dictionary with the raw data per participant per phase as a file using the pickle module
    # import pickle
    # with open("PointClick_dict.pkl", "wb") as f:
    #     pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    final_data = pd.DataFrame(results).T
    print("Point & Click Data Successfully Processed!")
    return final_data


# Alle Daten ab Start des ersten Drags
def get_drag_drop_data(dataset):

    dd_task = ["HS_DragDrop", "LS_DragDrop"]

    bad_cases_drag_drop = [
        "Vhi1KMa2MecuTnTzWb8QBp9rNDw1",
        "ZnI96HDrRZV9xNlfQxgTU0CeoDX2",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32"
    ]

    results = {}

    participant_index = 1

    for participant in dataset:

        # Dictionary for row data per participant
        results[participant] = {}

        # Dictionary for calculating the difference scores between the conditions
        diff_creation = {}
        task_index = 0

        for task in dd_task:

            # create a row for each task
            results[participant + "_" + task[:2]] = {}

            if task in dataset[participant]:

                all_data = dataset[participant][task]
                cleaned_data = clean_mouse_data(all_data)

                # visualize_mouse_movement(cleaned_data, participant_index, task)

                # create a list with all data from the start of the first dragging
                task_data = [datapoint for datapoint in cleaned_data if datapoint["dragging"] or
                             0 < datapoint["circleNumber"]]

                # Below code is used to create a dictionary with the raw eda data per participant per phase
                # from collections import defaultdict
                #
                # results[participant][task] = defaultdict(list)
                #
                # for datapoint in task_data:
                #     results[participant][task]["circleNumber"].append(datapoint["circleNumber"])
                #     results[participant][task]["circlesDragged"].append(datapoint["circlesDragged"])
                #     results[participant][task]["dragging"].append(datapoint["dragging"])
                #     results[participant][task]["eventType"].append(datapoint["eventType"])
                #     results[participant][task]["time"].append(datapoint["time"])
                #     results[participant][task]["x"].append(datapoint["x"])
                #     results[participant][task]["y"].append(datapoint["y"])
                #
                # results[participant][task]["DiffTime"] = [i - min(results[participant][task]["time"]) for i in
                #                                           results[participant][task]["time"]]
                # end of code for raw data dictionary creation

                # visualize_mouse_movement(task_data, participant_index, task, task_index)

                task_index += 1

                # Goal: Create a list that contains trial data for successfull drag & drop operations split into
                # the part where the user drags the circle and the part where the user navigates to the dragging circle

                # Step 1: Split the Data into lists for each dragging trial (including unsuccessfull dragging attempts)
                all_trial_data = [list(g) for k, g in groupby(task_data, operator.itemgetter("circlesDragged"))]

                # print(len(all_trial_data))
                #
                # for trial in all_trial_data:
                #     visualize_mouse_movement(trial, participant, task)

                # Initiate a list holding the final successful trial data
                successful_trials = []

                # loop over all dragging trials starting with the second trial
                for trial in all_trial_data[1:]:
                    # create a list for each circle dragged in the dragging trial
                    trial_trials = [list(g) for k, g in groupby(trial, operator.itemgetter("circleNumber"))]
                    # the successfull drag trial is the last trial in the list
                    relevant_trial = trial_trials[-1]
                    # create a list with datapoints when the circle is being dragged
                    relevant_dragging = [i for i in relevant_trial if i["dragging"]]
                    # create a list with datapoints when the circle is not dragged (being navigated to)
                    relevant_searching = [i for i in relevant_trial if not i["dragging"]]
                    # Add both lists to the successful_trial list

                    # visualize_mouse_movement(relevant_dragging, participant, task)

                    successful_trials.extend([relevant_searching, relevant_dragging])

                # if len(successful_trials) < 29:
                #     print(participant + " has completed " + str(len(successful_trials)) + " trials in " + task)
                #
                #
                interpol_task_data = interpolate_mouse_data(task_data)

                # calculate relevant parameters
                parameters = {}

                # Calc Task Time
                task_time = get_mouse_task_time(interpol_task_data)
                parameters.update(task_time)
                # Movement related parameters
                movement_params = get_mouse_movement_parameters(interpol_task_data)
                parameters.update(movement_params)
                # Angle Parameters
                angles = get_mouse_angles(interpol_task_data)
                parameters.update(angles)
                # Entropy and x-y-flips
                flips_entropy = get_x_y_flips_and_sample_entropy(interpol_task_data)
                parameters.update(flips_entropy)
                # Distance from Ideal Line Parameters
                dist_line = get_dist_from_ideal_line(successful_trials)
                parameters.update(dist_line)
                # Number of trials
                num_trials = max(i["circlesDragged"] for i in task_data)
                parameters.update({"num_trials": num_trials})
                # Number of Dragged Circles
                num_drags = max(i["circleNumber"] for i in task_data)
                parameters.update({"num_drags": num_drags})

                # save task parameters
                # diff_creation[task] = parameters

                # save and output parameters
                for param in parameters:
                    # results[participant][task + "_" + param] = np.round(parameters[param], 3)
                    results[participant + "_" + task[:2]][task[3:] + "_" + param] = np.round(parameters[param], 3)

                # Add information about participant and trial
                # results[participant + "_" + task[:2]][task[3:] + "_par_index"] = participant_index
                # if task[:2] == "HS":
                #     results[participant + "_" + task[:2]]["condition"] = 0
                # elif task[:2] == "LS":
                #     results[participant + "_" + task[:2]]["condition"] = 1

        # save difference value parameters in output dictionary
        # if "HS_DragDrop" in diff_creation:
        #     for item in diff_creation["HS_DragDrop"]:
        #         if item in diff_creation["LS_DragDrop"]:
        #             results[participant]["Diff_DragDrop_" + item] = diff_creation["HS_DragDrop"][item] - \
        #                                                            diff_creation["LS_DragDrop"][item]

        participant_index += 1

    # save the dictionary with the raw data per participant per phase as a file using the pickle module
    # import pickle
    # with open("DragDrop_dict.pkl", "wb") as f:
    #     pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    final_data = pd.DataFrame(results).T
    print("Drag & Drop Data Successfully Processed!")
    return final_data


# Alle Daten während der Aufgabenbearbeitung
def get_loading_task_data(dataset):

    # Question: How to handle no movement data?! --> The current datasample does not include such a case (yet!)

    loading_task = ["HS_LoadingTask", "LS_LoadingTask"]

    results = {}

    participant_index = 1

    for participant in dataset:

        results[participant] = {}

        task_index = 0

        for task in loading_task:

            # create a row for each task
            # results[participant + "_" + task[:2]] = {}

            if task in dataset[participant]:

                print("proessing participant " + str(participant_index), participant)

                task_data = dataset[participant][task]

                cleaned_data = clean_mouse_data(task_data)

                # print(participant, task, len(cleaned_data))
                # visualize_mouse_movement(cleaned_data, participant_index, task, task_index)

                # Below code is used to create a dictionary with the raw eda data per participant per phase
                from collections import defaultdict

                results[participant][task] = defaultdict(list)

                for datapoint in cleaned_data:
                    results[participant][task]["eventType"].append(datapoint["eventType"])
                    results[participant][task]["time"].append(datapoint["time"])
                    results[participant][task]["x"].append(datapoint["x"])
                    results[participant][task]["y"].append(datapoint["y"])

                results[participant][task]["DiffTime"] = [i - min(results[participant][task]["time"]) for i in
                                                          results[participant][task]["time"]]
                # end of code for raw data dictionary creation

                task_index += 1

                # calculate relevant parameters
                # parameters = {}
                #
                # # if there is movement data in the loading task
                # if len(cleaned_data) > 2:
                #
                #     interpol_task_data = interpolate_mouse_data(cleaned_data)
                #
                #     # Movement related parameters
                #     movement_params = get_mouse_movement_parameters(interpol_task_data)
                #     parameters.update(movement_params)
                #     # Angle Parameters
                #     angles = get_mouse_angles(interpol_task_data)
                #     parameters.update(angles)
                #     # Entropy and x-y-flips
                #     flips_entropy = get_x_y_flips_and_sample_entropy(interpol_task_data)
                #     parameters.update(flips_entropy)
                #     parameters.update({"movement": 1})
                # # if there is no movement data in the loading task
                # else:
                #     parameters.update({"movement": 0})
                #
                # # save and output parameters
                # for param in parameters:
                #     # results[participant][task + "_" + param] = np.round(parameters[param], 3)
                #     results[participant + "_" + task[:2]][task[3:] + "_" + param] = np.round(parameters[param], 3)




                # # Add information about participant and trial
                # results[participant + "_" + task[:2]][task[3:] + "_par_index"] = participant_index
                # if task[:2] == "HS":
                #     results[participant + "_" + task[:2]]["condition"] = 0
                # elif task[:2] == "LS":
                #     results[participant + "_" + task[:2]]["condition"] = 1

        participant_index += 1

    # save the dictionary with the raw data per participant per phase as a file using the pickle module
    import pickle
    with open("LoadingTask_dict.pkl", "wb") as f:
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    final_data = pd.DataFrame(results).T
    print("Loading Task Data Successfully Processed!")
    return final_data


# Ab dem Start der Aufgabe = sobald die Maus in die Box bewegt wurde
def get_follow_box_task_data(dataset):

    follow_box_task = ["HS_FollowBox", "LS_FollowBox"]

    results = {}

    participant_index = 1

    for participant in dataset:

        # Dictionary for row data per participant
        results[participant] = {}

        # Dictionary for calculating the difference scores between the conditions
        diff_creation = {}

        for task in follow_box_task:

            # create a row for each task
            results[participant + "_" + task[:2]] = {}

            if task in dataset[participant]:

                all_data = dataset[participant][task]
                cleaned_data = clean_mouse_data(all_data)

                # create a list with all data excluding the mousemovement to the first circle
                task_data = [datapoint for datapoint in cleaned_data if datapoint["taskStarted"]]

                # Below code is used to create a dictionary with the raw eda data per participant per phase
                # from collections import defaultdict
                #
                # results[(participant, task)] = defaultdict(list)
                #
                # for datapoint in task_data:
                #     results[(participant, task)]["inBox"].append(datapoint["inBox"])
                #     results[(participant, task)]["eventType"].append(datapoint["eventType"])
                #     results[(participant, task)]["time"].append(datapoint["time"])
                #     results[(participant, task)]["x"].append(datapoint["x"])
                #     results[(participant, task)]["y"].append(datapoint["y"])
                #
                # results[(participant, task)]["DiffTime"] = [i - min(results[(participant, task)]["time"]) for i in
                #                                           results[(participant, task)]["time"]]
                # end of code for raw data dictionary creation

                # test = None
                # visualize_mouse_movement(task_data, participant_index, task, test)

                interpol_task_data = interpolate_mouse_data(task_data)

                # calculate relevant parameters
                parameters = {}

                # Movement related parameters
                movement_params = get_mouse_movement_parameters(interpol_task_data)
                parameters.update(movement_params)
                # Angle Parameters
                angles = get_mouse_angles(interpol_task_data)
                parameters.update(angles)
                # Entropy and x-y-flips
                flips_entropy = get_x_y_flips_and_sample_entropy(interpol_task_data)
                parameters.update(flips_entropy)
                # datapoints inside the box versus outside the box
                datapoints_inside = sum(1 for i in task_data if i["inBox"])
                total_datapoints = len(task_data)
                parameters.update({"in_box_ratio": datapoints_inside/total_datapoints})

                # save task parameters
                # diff_creation[task] = parameters

                # save and output parameters
                for param in parameters:
                    # results[participant][task + "_" + param] = np.round(parameters[param], 3)
                    results[participant + "_" + task[:2]][task[3:] + "_" + param] = np.round(parameters[param], 3)

                # # Add information about participant and trial
                # results[participant + "_" + task[:2]][task[3:] + "_par_index"] = participant_index
                # if task[:2] == "HS":
                #     results[participant + "_" + task[:2]]["condition"] = 0
                # elif task[:2] == "LS":
                #     results[participant + "_" + task[:2]]["condition"] = 1

        # # save difference value parameters in output dictionary
        # if "HS_FollowBox" in diff_creation:
        #     for item in diff_creation["HS_FollowBox"]:
        #         if item in diff_creation["LS_FollowBox"]:
        #             results[participant]["Diff_FollowBox_" + item] = diff_creation["HS_FollowBox"][item] - diff_creation["LS_FollowBox"][item]

        participant_index += 1

    # save the dictionary with the raw data per participant per phase as a file using the pickle module
    # import pickle
    # with open("FollowBox_dict.pkl", "wb") as f:
    #     pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    final_data = pd.DataFrame(results).T
    print("Follow Box Data Successfully Processed!")
    return final_data


# Ab dem Start der Aufgabe = sobald der erste Zeichenpunkt berührt wurde und man zeichnen kann
def get_steering_task_data(dataset):
    steering_task = ["HS_Drawing", "LS_Drawing"]

    bad_cases_drawing = [
        "4ibZh6HiVrPknUuvasf6CIVD1L42",
        "9DdqeM3mkRWvD4MCMcWvFH4wIhA2",
        "GzlieWRWOJgquA0nDZtBFExSW0E2",
        "PRPyIVrPUVgCFtZ60nqvXc4wUov2",
        "V6TlsMC21YbLX2MyjUiEiVrhgMk2",
        "Vhi1KMa2MecuTnTzWb8QBp9rNDw1",
        "WpwRDjuqqdRavEdFOgqbpRA19Q32",
        "b8KoZn71FhOsv46MKFAlqdhTBXM2",
        "bD83eNrrWTgjMkVAdibgZNiebTe2",
        "cgS7wdlEL3XTYUiBbXGDGCoyJWe2",
        "dOXefJ4hHEfRsYTTFfn6NfATnh32",
        "gJnYNGrs0lhMSKDh9i466E2MiJn2",
        "nDsahKaZCEUMI732rmmyANfauCj1",
        "nQl80EJnrxYnsuoVqEFhTMzZVgl2",
        "pPx9EQjAJuN5wxinUZjO6DUsZDo1",
        "uQ5ly8q3nPQZHi56WJFlw0Y3A4E2",
        "zoCupEvJwahE0hRlqKWLyP8TRrJ2"
    ]

    results = {}

    participant_index = 1

    for participant in dataset:

        # Dictionary for row data per participant
        results[participant] = {}

        # Dictionary for calculating the difference scores between the conditions
        diff_creation = {}

        for task in steering_task:

            # dictionary for row data per task (condition)
            results[participant + "_" + task[:2]] = {}

            if task in dataset[participant]:

                all_data = dataset[participant][task]
                cleaned_data = clean_mouse_data(all_data)

                # create a list with all data from the start of the first drawing to the end of the 10th trial
                task_data = [datapoint for datapoint in cleaned_data if (datapoint["canDraw"] and
                             datapoint["touchedMilestones"] < 11) or
                             0 < datapoint["touchedMilestones"] < 11]


                # Below code is used to create a dictionary with the raw eda data per participant per phase
                # from collections import defaultdict
                #
                # results[participant][task] = defaultdict(list)
                #
                # for datapoint in task_data:
                #     results[participant][task]["canDraw"].append(datapoint["canDraw"])
                #     results[participant][task]["isDrawing"].append(datapoint["isDrawing"])
                #     results[participant][task]["touchedMilestones"].append(datapoint["touchedMilestones"])
                #     results[participant][task]["eventType"].append(datapoint["eventType"])
                #     results[participant][task]["time"].append(datapoint["time"])
                #     results[participant][task]["x"].append(datapoint["x"])
                #     results[participant][task]["y"].append(datapoint["y"])
                #
                # results[participant][task]["DiffTime"] = [i - min(results[participant][task]["time"]) for i in
                #                                           results[participant][task]["time"]]
                # end of code for raw data dictionary creation

                # test = None
                # visualize_mouse_movement(task_data, participant_index, task, test)

                interpol_task_data = interpolate_mouse_data(task_data)

                # Split the list into lists with the trial data (data between clicking on two targets)
                all_trial_data = [list(g) for k, g in groupby(task_data, operator.itemgetter("touchedMilestones"))]
                # if len(all_trial_data) < 13:
                #     print(participant + " has completed " + str(len(all_trial_data)) + " trials in " + task)

                # Because trial data includes mouse movement to to startpoint, only data is included when participants
                # started to draw (clicked on the start point)
                draw_trial_data = []

                for trial in all_trial_data:
                    draw_trial = [datapoint for datapoint in trial if datapoint["canDraw"]]
                    draw_trial_data.append(draw_trial)


                # calculate relevant parameters
                parameters = {}

                # Calc Task Time
                task_time = get_mouse_task_time(interpol_task_data)
                parameters.update(task_time)
                # Movement related parameters
                movement_params = get_mouse_movement_parameters(interpol_task_data)
                parameters.update(movement_params)
                # Angle Parameters
                angles = get_mouse_angles(interpol_task_data)
                parameters.update(angles)
                # Entropy and x-y-flips
                flips_entropy = get_x_y_flips_and_sample_entropy(interpol_task_data)
                parameters.update(flips_entropy)
                # Distance from Ideal Line Parameters
                dist_line = get_dist_from_ideal_line(draw_trial_data)
                parameters.update(dist_line)
                # Number of trials
                parameters.update({"num_drawings": len(draw_trial_data)})

                # save task parameters
                # diff_creation[task] = parameters

                # # save and output parameters
                for param in parameters:
                    # save parameter with task info in participant row
                    # results[participant][task + "_" + param] = np.round(parameters[param], 3)
                    # save task parameter in condition row
                    results[participant + "_" + task[:2]][task[3:] + "_" + param] = np.round(parameters[param], 3)

                # Add information about participant and trial to each condition row
                results[participant + "_" + task[:2]][task[3:] + "_par_index"] = participant_index
                if task[:2] == "HS":
                    results[participant + "_" + task[:2]]["condition"] = 0
                elif task[:2] == "LS":
                    results[participant + "_" + task[:2]]["condition"] = 1

        # save difference value parameters in output dictionary
        # if "HS_Drawing" in diff_creation:
        #     for item in diff_creation["HS_Drawing"]:
        #         if item in diff_creation["LS_Drawing"]:
        #             results[participant]["Diff_Drawing_" + item] = diff_creation["HS_Drawing"][item] - diff_creation["LS_Drawing"][item]

        # incremeant the participant index
        participant_index += 1

    # save the dictionary with the raw data per participant per phase as a file using the pickle module
    # import pickle
    # with open("Drawing_dict.pkl", "wb") as f:
    #     pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    final_data = pd.DataFrame(results).T
    print("Steering Task Data Successfully Processed!")
    return final_data
