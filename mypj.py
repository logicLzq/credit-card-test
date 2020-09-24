import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier




def predict(test):
    #数据处理，处理的思路见
    cc_apps = pd.read_csv("data.csv", header=None)
    cc_apps = cc_apps.replace("?", np.NaN)
    cc_apps = cc_apps.fillna(cc_apps.mean())
    for col in cc_apps.columns:
        if cc_apps[col].dtypes == 'object':
            cc_apps[col] = cc_apps[col].fillna(cc_apps[col].value_counts().index[0])
    le = LabelEncoder()
    for col in cc_apps.columns:
        if cc_apps[col].dtype == 'object':
            cc_apps[col] = le.fit_transform(cc_apps[col])
    new = pd.DataFrame(test).T
    cc_apps.append(new)
    cc_apps = cc_apps.append(new, ignore_index=True)
    cc_apps_droped = cc_apps.drop([cc_apps.columns[10], cc_apps.columns[13]], axis=1)
    cc_apps_val = cc_apps_droped.values
    X, y = cc_apps_val[:, 0:13], cc_apps_val[:, 13]

    scaler = MinMaxScaler(feature_range=(0, 1))
    rescaledX = scaler.fit_transform(X)
    mytest = rescaledX[-1]
    rescaledX = np.delete(rescaledX, -1, axis=0)
    y = np.delete(y, -1, axis=0)
    knn = KNeighborsClassifier(n_neighbors=9)
    knn.fit(rescaledX, y)
    mytest = mytest.reshape(1, -1)
    y_pred = knn.predict(mytest)
    print(y_pred)
    result = int(y_pred)
    return result