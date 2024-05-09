"""Author: Anthony Epshtein"""

import data_preprocessing
from AI_models import LogisticRegression_Model, DecisionTrees_Model, KNeighborsClassifier_Model, ANN_Model

""" 
----- GLOBAL VARIABLES -----
use them to change preferences

This is list of months that ready at directory '..\\assets\\flight_reports' .
You can add different monthly flight reports if they are at exactly the same format, download them from source[1].
Change list bellow accordingly to content of folder. 
"""
MONTHS = ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06']

""" 
Determines whether datasets from source[1] will be re-processed, or the program will be using already processed data 
from 'out' directory.
Toogle on if there is need to process new flight reports that added to folder '..\\assets\\flight_reports' .
"""
REPROCESS_FLIGHT_DATA = False

""" 
Determines whether the weather data will be requested again fom server, 
or the program will be using already processed data from 'out\\weather' directory.

(WARNING: it will require time to complete all multiple requests to server).
(Note: if content of '..\\assets\\flight_reports' folder is changed it is necessary to request relevant weather data,
    but as long as same files used there is no need to request weather again.)
"""
REREQUEST_WEATHER_DATA = False



df = data_preprocessing.data_preprocessing(MONTHS, REPROCESS_FLIGHT_DATA, REREQUEST_WEATHER_DATA)
# Convert all columns to float, every column already in type int or float but sklearn won't work with int values.
df = df.astype(float)


# -------LogisticRegression----------
# LogisticRegression_Model(df)

# ---------DecisionTrees------------
# DecisionTrees_Model(df)

# --------------KNN-----------------
# KNeighborsClassifier_Model(df, k=10)
# KNeighborsClassifier_Model(df, k=4)

# --------------ANN-----------------
# ANN_Model(df, neurons=[5, 5, 5])
# ANN_Model(df, neurons=[5, 5])
# ANN_Model(df, neurons=[20, 20])
# ANN_Model(df, neurons=[2, 2])