import pandas as pd

import numpy as np

from sklearn import svm

from sklearn.metrics import fbeta_score
from sklearn.metrics import accuracy_score

from sklearn import preprocessing

from sklearn.model_selection import train_test_split

from sklearn.decomposition import PCA


data = pd.read_csv("model.csv")

data = data.dropna(subset=['x_001'])
data[data.iloc[:,2:]<0] = np.nan
X = data.iloc[:,2:]
training_mean = X.mean()
X =X.fillna(training_mean)
Y = data['y']
X = preprocessing.scale(X)


def get_score(y_pred,y_true):
    acc_ = accuracy_score(y_true=y_true,y_pred=y_pred)
    TP = np.sum((y_pred==1) & (y_true == 1))
    precision = TP / np.sum(y_pred)
    recall = TP / np.sum(y_true)
    print('TP: ',TP,'/', np.sum(y_true), 'all ',np.sum(y_pred), ' accuracy: ',acc_, ' precision: ',precision, ' recall: ',recall, ' F_score: ', 2 * precision * recall / (precision + recall),fbeta_score(y_true=y_true,y_pred=y_pred,beta=1) )



pca = PCA(50)
training_X, test_X, training_Y, test_Y = train_test_split(X, Y, test_size=0.3,shuffle = True)


training_X = pca.fit_transform(training_X)

clf = svm.SVC(gamma='auto', probability=True)
clf.fit(training_X, training_Y)


test_X = pca.transform(test_X)
preY = clf.predict(test_X)


get_score(preY, test_Y)


test_data = pd.read_csv("test.csv")



test_data = test_data.iloc[:, 1:]
test_data[test_data.iloc[:, 1: ] < 0] = np.nan
test_data = test_data.fillna(training_mean)
test_data = preprocessing.scale(test_data)

test_data = pca.transform(test_data)


res = clf.predict(test_data)


np.savetxt('result.csv', res,fmt='%d',delimiter=',')
