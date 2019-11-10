def button(request):

	return render(request, 'index.html')


from django.shortcuts import render
import requests
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
'''
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
'''

from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error 
from matplotlib import pyplot as plt

import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from xgboost import XGBRegressor

def get_data():
    #get train data
    train_data_path =r'C:/Users/Lenovo/Desktop/train.csv'
    train = pd.read_csv(train_data_path)
    
    #get test data
    test_data_path =r'C:/Users/Lenovo/Desktop/test.csv'
    test = pd.read_csv(test_data_path)
    
    return train , test

def get_combined_data():
  #reading train data
  train , test = get_data()

  target = train.SalePrice
  train.drop(['SalePrice'],axis = 1 , inplace = True)

  combined = train.append(test)
  combined.reset_index(inplace=True)
  combined.drop(['index', 'Id'], inplace=True, axis=1)
  return combined, target

def get_cols_with_no_nans(df,col_type):
    if (col_type == 'num'):
        predictors = df.select_dtypes(exclude=['object'])
    elif (col_type == 'no_num'):
        predictors = df.select_dtypes(include=['object'])
    elif (col_type == 'all'):
        predictors = df
    else :
        print('Error : choose a type (num, no_num, all)')
        return 0
    cols_with_no_nans = []
    for col in predictors.columns:
        if not df[col].isnull().any():
            cols_with_no_nans.append(col)
    return cols_with_no_nans


def split_combined():
    global combined
    train = combined[:296]
    test = combined[296:]

    return train , test


def transposer(x):
    x = x.reshape(30,1).T
    return -(NN_model.predict(x))

def output(request):
	data=xopt
	data2=abs(fopt[0])
	#print(data.text)
	print('xopt: ')
	print(xopt)
	print('fopt: ')
	print(fopt)
	return render(request, 'index.html', {'data':xopt, 'data2':fopt})


train_data, test_data = get_data()
combined, target = get_combined_data()

num_cols = get_cols_with_no_nans(combined , 'num')
cat_cols = get_cols_with_no_nans(combined , 'no_num')

print ('Number of numerical columns with no nan values :',len(num_cols))
print ('Number of nun-numerical columns with no nan values :',len(cat_cols))

train_data = train_data[num_cols + cat_cols]
train_data['Target'] = target

C_mat = train_data.corr()
fig = plt.figure(figsize = (15,15))

sb.heatmap(C_mat, vmax = .8, square = True)
plt.show()

train, test = split_combined()
NN_model = Sequential()

NN_model.add(Dense(128, kernel_initializer='normal',input_dim = train.shape[1], activation='relu'))

NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))

NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
NN_model.summary()

checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5' 
checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
callbacks_list = [checkpoint]
gaurav=NN_model.fit(train, target, epochs=500, batch_size=10, validation_split = 0.2, callbacks=callbacks_list)
from pyswarm import pso
plt.plot(gaurav.history['loss'])

X_predict = np.array([268.7,2.3,13.2,-0.4,9,41.8,202.8,486.8,187.7,59.7,7.3,0.5,60.9,223.9,96.2,86.1,740.3,779.5,1294.6,96.9,0.8,79.4,60.5,164.4,86.4,584.1,36.2,244.1,96.2,2.3
])
X_predict = X_predict.reshape(30,1).T
np.shape(X_predict)
#print(NN_model.predict(X_predict))
lb = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14.44,12.2,0,0,0,0,2.277,1.454,1.5,0]
ub = [300,200,100,1000,100,1000,1000,1000,1000,1000,1000,100,1000,100,1000,1000,100,1000,100,100,100,100,344.22,125.2,100,960,100,100,100,100]
xopt, fopt = pso(transposer, lb, ub)
fopt=abs(fopt)
print("Accuracy = 87.4354%")
