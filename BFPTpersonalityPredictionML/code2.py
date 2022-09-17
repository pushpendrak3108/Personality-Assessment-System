import pandas as pd
from numpy import *
import numpy as np
import warnings

warnings.filterwarnings("ignore")
# from sklearn import preprocessing
from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn import metrics
# from sklearn.model_selection import train_test_split
# from sklearn import neighbors
from sklearn import svm
# from sklearn.pipeline import Pipeline
import pickle
from sklearn import tree

data = pd.read_csv('train dataset.csv')
array = data.values
# print(array)
# processing data
for i in range(len(array)):
    if array[i][0] == "Male":
        array[i][0] = 1
    else:
        array[i][0] = 0
print('array')
print(array)
df = pd.DataFrame(array)
# print(df.head())
maindf = df[[0, 1, 2, 3, 4, 5, 6]]
mainarray = maindf.values
print('mainarray')
print(mainarray)
temp = df[7]
print('temp df7')
print(temp)
train_y = temp.values
print('train y')
print(train_y)
#print(mainarray)
train_y = temp.values
for i in range(len(train_y)):
    train_y[i] = str(train_y[i])
labels = [
    "Logistic Regression",
    "SVM",
    "Decision Tree"
]
models = [
    linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter=1000),
    svm.SVC(kernel="poly"),
    tree.DecisionTreeClassifier()
]
# mul_lr = svm.SVC(kernel="poly")
# mul_lr = Pipeline([
#("LR", linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter = 1000))
# ("SVM", svm.SVC(kernel="linear"))
# ])
print("Accuracy:")
for mno in range(len(models)):
    mul_lr = models[mno]
    mul_lr.fit(mainarray, train_y)
    # save the model to disk
    modelname = labels[mno]+".pkl"
    pickle.dump(mul_lr, open(modelname, 'wb'))
    testdata = pd.read_csv('test dataset.csv')
    test = testdata.values
    for i in range(len(test)):
        if test[i][0] == "Male":
            test[i][0] = 1
        else:
            test[i][0] = 0
    df1 = pd.DataFrame(test)
    testdf = df1[[0, 1, 2, 3, 4, 5, 6]]
    maintestarray = testdf.values
    print('main test array')
    print(maintestarray)
    y_pred = mul_lr.predict(maintestarray)
    # print(maintestarray[0])
    # print(list(y_pred), df1[[7]].values)
    real = df1[[7]].values
    predicted = list(y_pred)
    error = 0
    for i in range(len(predicted)):
        if real[i][0] != predicted[i]:
            error += 1
    print(labels[mno]+ ":", ((len(predicted) - error) / len(predicted)) * 100)
    for i in range(len(y_pred)):
        y_pred[i] = str((y_pred[i]))
    DF = pd.DataFrame(y_pred, columns=['Predicted Personality.'])
    DF.index = DF.index + 1
    DF.index.names = ['Person No']
    DF.to_csv(labels[mno]+"output.csv")
