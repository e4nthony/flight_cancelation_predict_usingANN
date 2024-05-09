import time


def LogisticRegression_Model(df):
    start_time = time.time()
    print("Started LogisticRegression_Model...")
    # Importing necessary libraries
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score

    # Splitting the dataset into features and target variable
    features = df.drop(columns=['WEATHER_CANCEL'])
    target_variable = df['WEATHER_CANCEL']

    # Splitting the dataset into training sets and testing sets
    features_train_set, features_test_set, target_train_set, target_test_set = \
        train_test_split(features, target_variable, test_size=0.5, random_state=50)

    # Create Logistic Regression classifier
    logistic_regression = LogisticRegression(max_iter=1000000)

    # Train the classifier on the training data
    logistic_regression.fit(features_train_set, target_train_set)

    # Make predictions on the test data
    predictions = logistic_regression.predict(features_test_set)

    # Calculate accuracy
    accuracy = accuracy_score(target_test_set, predictions)
    print("Accuracy score:", accuracy)

    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(target_test_set, predictions)
    print("Mean Squared Error:", mse)
    print("Time [sec]:", time.time() - start_time)


def DecisionTrees_Model(df):
    print("Started DecisionTrees_Model...")
    start_time = time.time()
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score

    # Select features and target_variable from dataset
    features = df.drop(columns=['WEATHER_CANCEL'])
    target_variable = df['WEATHER_CANCEL']

    # Split the data into training and testing sets
    features_train_set, features_test_set, target_train_set, target_test_set = \
        train_test_split(features, target_variable, test_size=0.5, random_state=50)

    decision_tree = DecisionTreeClassifier(random_state=50)

    # Train
    decision_tree.fit(features_train_set, target_train_set)

    predictions = decision_tree.predict(features_test_set)

    accuracy = accuracy_score(target_test_set, predictions)
    print("Accuracy:", accuracy)

    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(target_test_set, predictions)
    print("Mean Squared Error:", mse)
    print("Time [sec]:", time.time() - start_time)


def KNeighborsClassifier_Model(df, k):
    """
    :param df: dataset
    :param k: you need to provide the function the number of neighbors to vote.
    """
    M_DEBUG_MODE = True
    start_time = time.time()

    print("Started KNeighborsClassifier_Model... With k=", k)
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    # Select features and target_variable from dataset
    features = df.drop(columns=['WEATHER_CANCEL'])
    target_variable = df['WEATHER_CANCEL']

    # Split the data into training and testing sets
    features_train_set, features_test_set, target_train_set, target_test_set = \
        train_test_split(features, target_variable, test_size=0.5, random_state=50)

    # Creates KNN classifier, n_neighbors is number of the nearest samples (k) to account in computation
    knn_classifier = KNeighborsClassifier(n_neighbors=k)

    if M_DEBUG_MODE: print("Training process started...")
    # Training process is just fitting sets
    knn_classifier.fit(features_train_set, target_train_set)

    if M_DEBUG_MODE: print("predict()")
    # Make actual predictions
    predictions = knn_classifier.predict(features_test_set)

    accuracy = accuracy_score(target_test_set, predictions)
    print("Accuracy score:", accuracy)

    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(target_test_set, predictions)
    print("Mean Squared Error:", mse)
    print("Time [sec]:", time.time() - start_time)


def ANN_Model(df, neurons):
    """
    :param df: dataset
    :param neurons: you need to provide the function the list of 'neurons',
                    the number of hidden layers neurons is count of items in list 'neurons',
                    and the count of neurons at each layer is value of each of items in list 'neurons'.
    """
    start_time = time.time()
    print(f"ANN_Model... With hiddden_layer_neurons:{neurons} (sizes in each hidden layer)")
    from sklearn.model_selection import train_test_split
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score

    # Select features and target_variable from dataset
    features = df.drop(columns=['WEATHER_CANCEL'])
    target_variable = df['WEATHER_CANCEL']

    # Split the data into training and testing sets
    features_train_set, features_test_set, target_train_set, target_test_set = \
        train_test_split(features, target_variable, test_size=0.3, random_state=30)

    # Create ANN using multi-layer perceptron (MLP)
    ann_classifier = MLPClassifier(hidden_layer_sizes=neurons, max_iter=5000, random_state=50)

    # Train
    ann_classifier.fit(features_train_set, target_train_set)

    predictions = ann_classifier.predict(features_test_set)

    accuracy = accuracy_score(target_test_set, predictions)
    print("Accuracy score:", accuracy)

    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(target_test_set, predictions)
    print("Mean Squared Error:", mse)

    print("Time [sec]:", time.time() - start_time)
