''''
Code to grab the questionnaire data

THIS IS A PROCEDURE THAT IS USED TOGETHER WITH THE aggregated_dataset_creation.py file

The code most certainly is far from perfect and was written to fit the data analysis purpose of the study rather
than to establish a multi-purpose solution. This version of the code represents a stripped version that includes
(almost exclusively) only include the procedures that were used in the final data analysis as reported in the
manuscript.

For questions or error reporting contact: paul.freihaut@psychologie.uni-freiburg.de
'''

# import core modules
import pandas as pd


def get_selfreport_data(dataset):

    # Create a dictionary with all results (creating a pandas dataframe and filling it with data is less efficient)
    results = {}

    # Fill the dictionary with the relevant data
    for participant in dataset:

        # Create a new dictionary for the results of each participant
        results[participant + "_HS"] = {}
        results[participant + "_LS"] = {}

        # Add the neuroticism items (not used in the manuscript)
        # if "BfiNeuroticism" in dataset[participant]:
        #     for item in dataset[participant]["BfiNeuroticism"]:
        #         results[participant + "_HS"][item] = dataset[participant]["BfiNeuroticism"][item]
        #         results[participant + "_LS"][item] = dataset[participant]["BfiNeuroticism"][item]

        # Add the sociodemographic items
        if "Soziodem" in dataset[participant]:
            for item in dataset[participant]["Soziodem"]:
                results[participant + "_HS"][item] = dataset[participant]["Soziodem"][item]
                results[participant + "_LS"][item] = dataset[participant]["Soziodem"][item]

        # Add the Questions After the Tasks (not used in the manuscript)
        # if "QuestionsAfterTasks" in dataset[participant]:
        #     for item in dataset[participant]["QuestionsAfterTasks"]:
        #         results[participant + "_HS"][item] = dataset[participant]["QuestionsAfterTasks"][item]
        #         results[participant + "_LS"][item] = dataset[participant]["QuestionsAfterTasks"][item]

        # Add the HS_MDBF items
        if "HS_Mdbf" in dataset[participant]:
            for item in dataset[participant]["HS_Mdbf"]:
                results[participant + "_HS"][item] = dataset[participant]["HS_Mdbf"][item]

        # Add the HS_MDBF items
        if "LS_Mdbf" in dataset[participant]:
            for item in dataset[participant]["LS_Mdbf"]:
                results[participant + "_LS"][item] = dataset[participant]["LS_Mdbf"][item]

        # Add the SAM items for each condition for each task
        for page in dataset[participant]:
            if "SAM" in page:
                if "HS" in page:
                    for item in dataset[participant][page]:
                        results[participant + "_HS"][page[2:] + "_" + item] = dataset[participant][page][item]
                else:
                    for item in dataset[participant][page]:
                        results[participant + "_LS"][page[2:] + "_" + item] = dataset[participant][page][item]

        # Add the Mental Arithmetic Task Score for each condition for each task (not used in the manuscript)
        # for page in dataset[participant]:
        #     if "Mental_Arithmetic" in page:
        #         score = 0
        #         for task in dataset[participant][page]:
        #             if task["answer"] == task["solution"]:
        #                 score += 1
        #             else:
        #                 score -= 1
        #         if "HS" in page:
        #             results[participant + "_HS"][page[2:] + "_score"] = score
        #         else:
        #             results[participant + "_LS"][page[2:] + "_score"] = score

        # Add whether the experiment started with the high or low stress condition the Condition
        # results[participant + "_HS"]["start_with_hs"] = dataset[participant]["MetaData"]["condition"]
        # results[participant + "_LS"]["start_with_hs"] = dataset[participant]["MetaData"]["condition"]

        # Add the Task Order (not used in the manuscript)
        # taskOrder = []
        # for phase in dataset[participant]["MetaData"]["taskOrder"]:
        #     taskOrder.append(phase["phase"])
        # results[participant + "_HS"]["task_order"] = taskOrder
        # results[participant + "_LS"]["task_order"] = taskOrder

    # save the final results data as a pandas dataframe and return the dataframe, it contains a row per condition
    # per participant containing all questionnaire data
    df = pd.DataFrame(results).T
    print("Self Report and Performance Data Successfully Processed")
    return df