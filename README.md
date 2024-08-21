# Flight cancellation prediction using Machine Learning Algorithms

## 📋 Table of content

- [Description](#-description)
- [Installation](#-installation)
- [Usage](#-usage)

<br/>

## 📖 Description
This is my Final project at "Artificial Intellgence" course.

This project implements Artificial Intellgence approaches and algorithms, aiming to compare their efficency on particular dataset for research purposes.<br/>
As an example, the project focuses on the problem of predicting whether a flight will be canceled on the following day due to current weather conditions."

The list of Algorithms that were compared:
- 'Logistic Regression Algorithm'
- 'K-Nearest Neighbors Algorithm (KNN)'
- 'Decision Trees Algorithm'
- 'Artificial Neural Network (ANN)'

For details please refer to [Project Report pdf](Project%20Report%20-%20Flight%20cancellation%20prediction%20depending%20on%20weather%20conditions%20day%20before%20flight%20using%20Machine%20Learning%20Algorithms..pdf "Project Report") document.

> note: Project built on Windows OS, using Python 3.10

<br/>

## ⚒ Installation 
Program uses Python 3.10 and above.

### Check Python Installation (using Git Bash terminal):
Using shell navigate to project directory and then run:
```bash
py --version
py -m pip --version
```
### Install Project Dependencies:
Project uses `numpy` and `pandas` pakages for dataset manipulations.<br/>
Also `scikit-learn` pakage as AI toolset.

For using Weather API we need additional pakages: <br/>
`openmeteo-requests`, `requests-cache` and `retry-requests`. 

All of them specified in [requirements.txt](requirements.txt "Project Dependencies File") file.<br/>
Run following command to install all of the project dependencies:

```bash
py -m pip install -r requirements.txt
```

<br/>

## 🚀 Usage
Launch program by running the main.py file:
```bash
py src/main.py
```
There are Global Variables located in driver file ([main.py](src/main.py "main.py")) that affects program behaviour.<br/>
For detailed instructions navigate to [main.py](src/main.py "main.py") and read docstrings.

<!-- readme version 2024-08-21 -->
