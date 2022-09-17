import pandas as pd
from numpy import *
import numpy as np
import warnings
# from sklearn import preprocessing
from sklearn import datasets, linear_model
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn import metrics
# from sklearn.model_selection import train_test_split
# from sklearn import neighbors
from sklearn.metrics import confusion_matrix
from sklearn import svm
# from sklearn.pipeline import Pipeline
import pickle
from sklearn import tree
from sklearn.metrics import classification_report
warnings.filterwarnings("ignore")

data = pd.read_csv('train dataset.csv')
array = data.values
for i in range(len(array)):
    if array[i][0] == "Male":
        array[i][0] = 1
    else:
        array[i][0] = 0
df = pd.DataFrame(array)
maindf = df[[0, 1, 2, 3, 4, 5, 6]]
mainarray = maindf.values
temp = df[7]
train_y = temp.values
train_y = temp.values
for i in range(len(train_y)):
    train_y[i] = str(train_y[i])
lables = [
"Logistic Regression",
"SVM",
"Decision Tree"
]
models = [
linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter=1000),
svm.SVC(kernel="poly"),
tree.DecisionTreeClassifier()
]
# print("models")
for mno in range(len(models)):
    mul_lr = models[mno]
    mul_lr.fit(mainarray, train_y)
    print("")
    print("")
    if(mno == 0):print("Logistic Regression")
    if(mno == 1):print("Support Vector Machine")
    if(mno == 2):print("Decision Tree")
    print("")
    pickle.dump(mul_lr, open("./model.pkl", 'wb'))
    testdata = pd.read_csv('test dataset.csv')
    test = testdata.values
    for i in range(len(test)):
        if test[i][0] == "Male":
            test[i][0] = 1
        else:
            test[i][0] = 0
    df1=pd.DataFrame(test)
    testdf =df1[[0,1,2,3,4,5,6]]
    maintestarray=testdf.values
    y_pred = mul_lr.predict(maintestarray)
    real = df1[[7]].values
    predicted = list(y_pred)
    confusion = confusion_matrix(real, predicted)
    accuracy = np.diag(confusion).sum()/confusion.sum().sum()
    at = pd.DataFrame(classification_report(real, predicted,output_dict=True)).T
    print(at)
    print("")
    print("")
    for i in range(len(y_pred)):
        y_pred[i]=str((y_pred[i]))
    DF = pd.DataFrame(y_pred, columns=['Predicted Personality.'])
    DF.index=DF.index+1
    DF.index.names = ['Person No']
    DF.to_csv("output.csv")