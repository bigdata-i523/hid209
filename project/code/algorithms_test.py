from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from numpy import *
from sklearn import svm
from sklearn import tree
from sklearn.cross_validation import cross_val_score
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB


# 1. read data from csv
def read_data():
    data_set = pd.read_csv("train.csv")
    data = data_set.values[0:, 1:]
    label = data_set.values[0:, 0]
    print("Data load completed.")
    return data, label


# plot 70 samples
def show_pic(data):
    print(shape(data))
    plt.figure(figsize=(7, 7))
    for digit_num in range(0, 70):
        plt.subplot(7, 10, digit_num + 1)
        grid_data = data[digit_num].reshape(28, 28)
        plt.imshow(grid_data, interpolation="none", cmap="afmhot")
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.savefig("data_samples.png")


# 2. Data Cleaning
# The data is from 0-255 for each cell.
# Normalize data by set all value > 0 to 1
def data_clean(data):
    m, n = shape(data)
    new_data = zeros((m, n))
    for i in range(m):
        for j in range(n):
            if data[i, j] > 0:
                new_data[i, j] = 1
            else:
                new_data[i, j] = 0
    print("Data clean completed.")
    return new_data


# 3. Feature Selection by PCA
def feature_selection(data):
    # First, use explained_variance to get recommended number of component
    pca = PCA()
    # pca_parameter = pca.fit(data)
    pca.fit(data)
    ev = pca.explained_variance_
    ev_ratio = []
    for i in range(len(ev)):
        ev_ratio.append(ev[i] / ev[0])

    # select number of component which have a higher ratio
    # than 0.05 with the first components
    n = 0
    for i in range(len(ev_ratio)):
        if ev_ratio[i] < 0.05:
            n = i
            # print(n)
            break

    # Then, PCA the model by the number of components
    # pca = PCA(n_components=n, whiten=True)
    pca = PCA(n_components=n, whiten=True)
    print("Feature selection completed.")
    return pca.fit_transform(data)


# 4. Model Selection
def model_acc(data, label, model):
    start = datetime.now()
    acc = cross_val_score(model, data, label, cv=5, scoring="accuracy").mean()
    end = datetime.now()
    time_use = (end - start).seconds
    print("Time use: ", time_use)
    print("Accuracy by cross validation: ", acc)


def dt_classifier(data, label, data_type):
    dt_model = tree.DecisionTreeRegressor()
    dt_model.fit(data, label)
    print("Test " + data_type + " using DT: ")
    model_acc(data, label, dt_model)


def nb_classifier(data, label, data_type):
    nb_model = GaussianNB()
    nb_model.fit(data, label)
    print("Test " + data_type + " using NB: ")
    model_acc(data, label, nb_model)


def lr_classifier(data, label, data_type):
    lr_model = LogisticRegression()
    lr_model.fit(data, label)
    print("Test " + data_type + " using LR: ")
    model_acc(data, label, lr_model)


def rf_classifier(data, label, flag):
    rf_model = RandomForestClassifier(n_estimators=100)
    rf_model.fit(data, label)
    print("Test " + flag + " using RF: ")
    model_acc(data, label, rf_model)


def svm_classifier(data, label, flag):
    svm_model = svm.SVC(kernel="rbf", C=10)
    svm_model.fit(data, label)
    # svc_clf = NuSVC(nu=0.1, kernel='rbf', verbose=True)
    print("Test " + flag + " using SVM: ")
    model_acc(data, label, svm_model)


def main():
    data, label = read_data()
    # show_pic(data)
    clean_data = data_clean(data)

    test_type = 3
    for i in range(1, 3):
        print("In %d test" % i)

        if test_type == 0:
            input_data = data
            str = "raw data"
        elif test_type == 1:
            input_data = clean_data
            str = "clean data"
        elif test_type == 2:
            input_data = feature_selection(data)
            str = "pca data"
        elif test_type == 3:
            input_data = feature_selection(clean_data)
            str = "pca clean data"

        dt_classifier(input_data, label, str)
        nb_classifier(input_data, label, str)
        lr_classifier(input_data, label, str)
        rf_classifier(input_data, label, str)
        svm_classifier(input_data, label, str)


main()
