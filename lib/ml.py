import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import datetime
from sklearn import metrics, preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split, ShuffleSplit, learning_curve, validation_curve, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from process_query import convert_causes

# BASE MACHINE LEARNING MODEL
class MLBase:
    def __init__(self):
        self.estimator = None
        self.file_name = None
        self.feature_cols = ['LATITUDE', 'LONGITUDE', 'FIRE_YEAR', 'MONTH', 'DAY_OF_WEEK']
        self.data = None
        
    def get_data(self):
        
        # load dataset
        try:
            conn = sqlite3.connect(r'../FPA_FOD_20170508.sqlite')
            sql_query = \
            """
            SELECT FOD_ID, FIRE_NAME, FIRE_SIZE, FIRE_SIZE_CLASS, LATITUDE, LONGITUDE, STATE, STAT_CAUSE_DESCR, date(DISCOVERY_DATE) AS DATE, FIRE_YEAR FROM Fires;
            """
            data = pd.read_sql(sql_query, conn)

            # convert causes
            data = convert_causes(data)

        finally:
            conn.close()

        # add columns
        data['DATE'] = pd.to_datetime(data['DATE'])
        data['MONTH'] = data['DATE'].dt.month
        data['DAY_OF_WEEK'] = data['DATE'].dt.dayofweek # Monday=0, Sunday=6

        # drop missing rows
        self.data = data.dropna()
    
    def fit_model(self, X, y):
        # split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

        # fit random forest classifier
        self.estimator.fit(X_train, y_train)
        
        # predict response for test dataset
        y_pred = self.estimator.predict(X_test)
        
        # store accuracy
        self.estimator.accuracy_ = metrics.accuracy_score(y_test, y_pred)
      
    def fit_save(self, X, y, accuracy):
        self.estimator.fit(X, y)
        self.estimator.accuracy_ = accuracy
        self.save()
        
    def save(self):
        # save model to lib folder; to be run within lib directory
        print('Compressing and saving model...\n')
        
        if self.estimator is not None:
            dump(self.estimator, './' + self.file_name, compress = 9)
            print('{} has been saved.\n'.format(self.file_name))
        else: 
            print('Error: No estimator created yet.')
    
    def load(self):
        # load model from lib folder; to be run within app.py
        print('Loading {}...\n'.format(self.file_name))
        self.estimator = load('./lib/' + self.file_name)    # access from app.py
        print('{} has been loaded.\n'.format(self.file_name))
    
    def predict(self, lat, long, year, month, day_of_week):
        # predict given LATITUDE, LONGITUDE, FIRE_YEAR, MONTH, DAY_OF_WEEK
        if self.estimator is not None:
            prediction = self.estimator.predict([[lat, long, year, month, day_of_week]])
            return prediction[0]
        else: 
            print('Error: No estimator created yet.')


# RANDOM FOREST TO PREDICT WILDFIRE CAUSE
class MLRandomForestCause(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = RandomForestClassifier(n_estimators=125, max_depth=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train random forest with 25 trees; to be run within lib directory
        print('Training random forest...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['STAT_CAUSE_DESCR']

        # fit model
        if save:
          self.fit_save(X, y, 0.588)
        else:
          self.fit_model(X, y)

          print('Random forest trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# RANDOM FOREST TO PREDICT WILDFIRE SIZE CLASS
class MLRandomForestSizeClass(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = RandomForestClassifier(n_estimators=125, max_depth=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train random forest with 25 trees; to be run within lib directory
        print('Training random forest...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['FIRE_SIZE_CLASS']

        # fit model
        if save:
          self.fit_save(X, y, 0.556)
        else:
          self.fit_model(X, y)

          print('Random forest trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# KNN TO PREDICT WILDFIRE CAUSE
class MLKnnCause(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = KNeighborsClassifier(n_neighbors=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train knn with 100 neighbors; to be run within lib directory
        print('Training KNN...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['STAT_CAUSE_DESCR']

        # fit model
        if save:
          self.fit_save(X, y, 0.625)
        else:
          self.fit_model(X, y)

          print('KNN trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# KNN TO PREDICT WILDFIRE SIZE CLASS
class MLKnnSizeClass(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = KNeighborsClassifier(n_neighbors=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train knn with 100 neighbors; to be run within lib directory
        print('Training KNN...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['FIRE_SIZE_CLASS']

        # fit model
        if save:
          self.fit_save(X, y, 0.559)
        else:
          self.fit_model(X, y)

          print('KNN trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# AdaBoost TO PREDICT WILDFIRE CAUSE
class MLAdaBoostCause(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=7), n_estimators=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train adaboost; to be run within lib directory
        print('Training AdaBoost...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['STAT_CAUSE_DESCR']

        # fit model
        if save:
          self.fit_save(X, y, 0.588)
        else:
          self.fit_model(X, y)

          print('AdaBoost trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# AdaBoost TO PREDICT WILDFIRE SIZE CLASS
class MLAdaBoostSizeClass(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=7), n_estimators=10)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train adaboost; to be run within lib directory
        print('Training AdaBoost...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['FIRE_SIZE_CLASS']

        # fit model
        if save:
          self.fit_save(X, y, 0.549)
        else:
          self.fit_model(X, y)

          print('AdaBoost trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# Gradient Boosting TO PREDICT WILDFIRE CAUSE
class MLHistGradientBoostingCause(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = HistGradientBoostingClassifier(max_depth=8)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train adaboost; to be run within lib directory
        print('Training Gradient Boosting...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['STAT_CAUSE_DESCR']

        # fit model
        if save:
          self.fit_save(X, y, 0.628)
        else:
          self.fit_model(X, y)

          print('Histogram Gradient Boosting trained with accuracy of {}.\n'.format(self.estimator.accuracy_))


# Gradient Boosting TO PREDICT WILDFIRE SIZE CLASS
class MLHistGradientBoostingSizeClass(MLBase):
    def __init__(self):
        super().__init__()
        self.estimator = HistGradientBoostingClassifier(max_depth=8)
        self.file_name = __class__.__name__ + '.joblib.z'  # name of stored class

    def train(self, save=False):
        # train adaboost; to be run within lib directory
        print('Training Gradient Boosting...\n')

        # load and clean data
        self.get_data()

        # identify features and label
        X = self.data[self.feature_cols]
        y = self.data['FIRE_SIZE_CLASS']

        # fit model
        if save:
          self.fit_save(X, y, 0.570)
        else:
          self.fit_model(X, y)

          print('Histogram Gradient Boosting trained with accuracy of {}.\n'.format(self.estimator.accuracy_))
          
if __name__ == '__main__':
    # train and save model for predicting wildfire cause
    cause = MLRandomForestCause()
    cause.train(True)
    cause = MLKnnCause()
    cause.train(True)
    cause = MLAdaBoostCause()
    cause.train(True)
    cause = MLHistGradientBoostingCause()
    cause.train(True)
    
    # train and save model for predicting wildfire size class
    size_class = MLRandomForestSizeClass()
    size_class.train(True)
    size_class = MLKnnSizeClass()
    size_class.train(True)
    size_class = MLAdaBoostSizeClass()
    size_class.train(True)
    size_class = MLHistGradientBoostingSizeClass()
    size_class.train(True)
    
    pass
