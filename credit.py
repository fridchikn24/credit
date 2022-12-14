# -*- coding: utf-8 -*-
"""Sameeullah_File1_hw5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BM9LvNLu3CrUfODdPB3cF24y8wWcwMwA

Imports
"""

import warnings
warnings.filterwarnings(action='once')

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install feature_engine

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install -U scikit-learn

import sklearn
import feature_engine

# Commented out IPython magic to ensure Python compatibility.
# For DataFrames and manipulations
import pandas as pd
import numpy as np
import scipy.stats as stats

# For data Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as po
import plotly.graph_objects as go

# %matplotlib inline
import plotly.io as pio
pio.renderers.default = 'colab'

# For splitting the dataset
from sklearn.model_selection import train_test_split

# drop arbitrary features
from sklearn.datasets import fetch_openml

# For categorical variables
from feature_engine.encoding import OneHotEncoder
from feature_engine.encoding import RareLabelEncoder
from feature_engine.encoding import DecisionTreeEncoder
from feature_engine.encoding import MeanEncoder

# For scaling the data
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from feature_engine.transformation import YeoJohnsonTransformer
from feature_engine.transformation import LogTransformer

# DIscretization
from sklearn.preprocessing import KBinsDiscretizer

# Handling Outliers
from feature_engine.outliers import Winsorizer

# feature engine wrapper 
from feature_engine.wrappers import SklearnTransformerWrapper

# Using KNN classification for our data
from sklearn.neighbors import KNeighborsClassifier

# creating pipelines 
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Hyper parameter tuning
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

# learning Curves
from sklearn.model_selection import learning_curve

# draws a confusion matrix
from sklearn.metrics import plot_confusion_matrix 

# save and load models
import joblib

# Pathlib to navigate file system
from pathlib import Path

from google.colab import drive
drive.mount('/content/drive')

#import os
#os.makedirs("/content/drive/MyDrive/teaching_fall_2021/ml_fall_2021/HW_Assignments/HW5/saved_models")
#!ls

save_model_folder  = Path('/content/drive/MyDrive/')

# Load data from  https://www.openml.org/d/31
X, y = fetch_openml("credit-g", version=1, as_frame=True, return_X_y=True)
X

def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.2, 1.0, 5)):
    """
    Generate 2 plots: the test and training learning curve, the training
    samples vs fit times curve.

    Parameters
    ----------
    estimator : estimator instance
        An estimator instance implementing `fit` and `predict` methods which
        will be cloned for each validation.

    title : str
        Title for the chart.

    X : array-like of shape (n_samples, n_features)
        Training vector, where ``n_samples`` is the number of samples and
        ``n_features`` is the number of features.

    y : array-like of shape (n_samples) or (n_samples, n_features)
        Target relative to ``X`` for classification or regression;
        None for unsupervised learning.

    axes : array-like of shape (3,), default=None
        Axes to use for plotting the curves.

    ylim : tuple of shape (2,), default=None
        Defines minimum and maximum y-values plotted, e.g. (ymin, ymax).

    cv : int, cross-validation generator or an iterable, default=None
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:

          - None, to use the default 5-fold cross-validation,
          - integer, to specify the number of folds.
          - :term:`CV splitter`,
          - An iterable yielding (train, test) splits as arrays of indices.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : int or None, default=None
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.

    train_sizes : array-like of shape (n_ticks,)
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the ``dtype`` is float, it is regarded
        as a fraction of the maximum size of the training set (that is
        determined by the selected validation method), i.e. it has to be within
        (0, 1]. Otherwise it is interpreted as absolute sizes of the training
        sets. Note that for classification the number of samples usually have
        to be big enough to contain at least one sample from each class.
        (default: np.linspace(0.1, 1.0, 5))
    """
    if axes is None:
        _, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].set_title(title)
    if ylim is not None:
        axes[0].set_ylim(*ylim)
    axes[0].set_xlabel("Training examples")
    axes[0].set_ylabel("Score")

    train_sizes, train_scores, test_scores, fit_times, _ = \
        learning_curve(estimator, X, y, cv=cv, n_jobs=n_jobs,
                       train_sizes=train_sizes,
                       return_times=True,
                       random_state=123)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)

    # Plot learning curve
    axes[0].grid()
    axes[0].fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    axes[0].fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    axes[0].plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    axes[0].plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    axes[0].legend(loc="best")

    # Plot n_samples vs fit_times
    axes[1].grid()
    axes[1].plot(train_sizes, fit_times_mean, 'o-')
    axes[1].fill_between(train_sizes, fit_times_mean - fit_times_std,
                         fit_times_mean + fit_times_std, alpha=0.1)
    axes[1].set_xlabel("Training examples")
    axes[1].set_ylabel("fit_times")
    axes[1].set_title("Scalability of the model")

    return plt

# Create a list of categorical variables
# Since the dtype of categorical variable is Object we can compare the values with 'O' 
categorical = [var for var in X.columns if X[var].dtype.name == 'category']

# Create a list of discrete variables
# we do not want to consider Exited as this is target variable
discrete = [
    var for var in X.columns if X[var].dtype.name != 'category'
    and len(X[var].unique()) < 20
]

# Create a list of continuous Variables
continuous = [
    var for var in X.columns if X[var].dtype.name != 'category'
    if var not in discrete
]

var_rare_labels= [
 'credit_history',
 'purpose',
 'savings_status',
 'personal_status',
 'other_parties',
 'other_payment_plans',
 'job',
]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=123, stratify =y)

credit_risk_pipeline_1 = Pipeline([                           

    ('rare_label_encoder',
      RareLabelEncoder(tol=.05,n_categories =2,variables = var_rare_labels)),

    ('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True)),

    ('log_transformer', 
     LogTransformer(variables = continuous)),

    ('scalar',
            SklearnTransformerWrapper(StandardScaler(), variables = continuous)),

    ('knn',
     KNeighborsClassifier())
  ])

param_grid_2 = {
   # 'discretizer_cs__transformer__n_bins': range(1,5,1),
    #'discretizer_bal__transformer__n_bins': range(1,5,1),
    'scalar__transformer': [StandardScaler()],
    'knn__n_neighbors': range(6,20,1),
    'knn__weights': ['uniform', 'distance'],
    'knn__p': [1, 2]
    
}

# now we set up the grid search with cross-validation
grid_knn_2 = GridSearchCV(credit_risk_pipeline_1, param_grid_2,cv=5,return_train_score= True)

grid_knn_2.fit(X_train, y_train)

print(grid_knn_2.best_params_)

file_best_estimator_round2 = save_model_folder / 'knn_round2_best_estimator.pkl'

# specify the file to save complete grid results
file_complete_grid_round2 = save_model_folder / 'knn_round2_complete_grid.pkl'

joblib.dump(grid_knn_2.best_estimator_, file_best_estimator_round2)

# save complete grid results
joblib.dump(grid_knn_2, file_complete_grid_round2)

loaded_best_estimator_round2 = joblib.load(file_best_estimator_round2)

# load complete grid results
loaded_complete_grid_round2 = joblib.load(file_complete_grid_round2)

plot_learning_curve(loaded_best_estimator_round2, 'Learning Curves KNN', X_train, y_train, n_jobs=-1)

print(loaded_best_estimator_round2.score(X_train,y_train))



print(loaded_complete_grid_round2.best_score_)

# check the test scores for final model
# Compare the cross validation score of round1, round2, and round3.
# Whichever round has best cross validation score, use the best estimator from that round to predict the test scores
print(f'Test data accauracy for round 2: {loaded_best_estimator_round2.score(X_test,y_test)}')

# use the best estimator selected in previous step to plot the confusion matrix
print(f'Test data accauracy for round 2: {loaded_best_estimator_round2.score(X_test,y_test)}')
plot_confusion_matrix(loaded_best_estimator_round2, X_test, y_test,
                                
                                 cmap=plt.cm.Blues,
                                 normalize = 'true')
plt.grid(False)
plt.show()

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from feature_engine.encoding import DecisionTreeEncoder
from sklearn.tree import DecisionTreeClassifier

churn_pipeline_dtree = Pipeline([
    ('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True)),

    ('dtree',
     DecisionTreeClassifier(random_state=0))
])

param_grid__tree_1 = {
    'dtree__max_depth': np.arange(4,20),
    'dtree__min_samples_leaf': np.arange(2,20,4)
    #'dtree__max_leaf_nodes': np.arange(4, 20)
     }

grid_dtree1 = GridSearchCV(churn_pipeline_dtree, param_grid__tree_1,
                           cv=5, return_train_score= True, n_jobs=-1)
grid_dtree1.fit(X_train,y_train)

print(grid_dtree1.best_params_)

file_params_tree1 = save_model_folder / 'dtree_round1_params.pkl'
file_model_tree1 = save_model_folder / 'dtree_round1_model.pkl'

joblib.dump(grid_dtree1.best_estimator_, file_params_tree1)
joblib.dump(grid_dtree1, file_model_tree1)

loaded_dtree_params_round1 = joblib.load(file_params_tree1)
loaded_dtree_model_round1 = joblib.load(file_model_tree1)

plot_learning_curve(loaded_dtree_params_round1, 'Learning Curves dtree', X_train, y_train, n_jobs=-1)

#let's check the train scores
print(loaded_dtree_model_round1.score(X_train,y_train))

#let's check the cross validation score
print(loaded_dtree_model_round1.best_score_)

param_grid__tree_2 = {
    'dtree__max_depth': np.arange(1,9),
    'dtree__min_samples_leaf': np.arange(10,18)
    #'dtree__max_leaf_nodes': np.arange(4, 20)
     }

grid_dtree2 = GridSearchCV(churn_pipeline_dtree,param_grid__tree_2,cv=5,return_train_score = True, n_jobs=-1)
grid_dtree2.fit(X_train,y_train)

print(grid_dtree2.best_params_)

file_params_tree2 = save_model_folder / 'dtree_round2_params.pkl'
file_model_tree2 = save_model_folder / 'dtree_round2_model.pkl'

joblib.dump(grid_dtree2.best_estimator_, file_params_tree2)
joblib.dump(grid_dtree2, file_model_tree2)

loaded_dtree_params_round2 = joblib.load(file_params_tree2)
loaded_dtree_model_round2 = joblib.load(file_model_tree2)

plot_learning_curve(loaded_dtree_params_round2, 'Learning Curves dtree', X_train, y_train, n_jobs=-1)

#let's check the train scores
print(loaded_dtree_model_round2.score(X_train,y_train))

#let's check the cross validation score
print(loaded_dtree_model_round2.best_score_)

#cd = categorical + continuous
#print(cd)
pipeline_log = Pipeline([
    
    ('one_hot_encoder',
      OneHotEncoder(variables=categorical,drop_last=True)),

    ('scalar',
      SklearnTransformerWrapper(StandardScaler(), variables = continuous)),

    ('logreg',
     LogisticRegression(random_state=123, max_iter =100000, n_jobs=-1
                       ,solver = 'saga'))
])

np.linspace(0,1, 5)
param_grid_log1 = {
    'scalar__transformer': [StandardScaler(), MinMaxScaler()],
    'logreg__C': [10000000000],
    'logreg__l1_ratio': np.linspace(0, 1, 5)
    }
grid_logreg_1 = GridSearchCV(pipeline_log, param_grid_log1,
                           cv=5, return_train_score= True, n_jobs=-1 )
grid_logreg_1.fit(X_train,y_train)

print(grid_logreg_1.best_params_)

file_params_log1 = save_model_folder / 'logreg_params.pkl'
file_model_log1 = save_model_folder / 'logreg_model.pkl'

joblib.dump(grid_logreg_1.best_estimator_, file_params_log1)
joblib.dump(grid_logreg_1, file_model_log1)

loaded_logreg_params_log1 = joblib.load(file_params_log1)
loaded_logreg_model_log1 = joblib.load(file_model_log1)

plot_learning_curve(loaded_logreg_params_log1 , 'Learning Curves logreg', X_train, y_train, n_jobs=-1)

#let's check the train scores
print(loaded_logreg_model_log1.score(X_train,y_train))

#let's check the cross validation score
print(loaded_logreg_model_log1.best_score_)

print(f'Test data accauracy for decision tree : {loaded_dtree_params_round1.score(X_test,y_test)}')
plot_confusion_matrix(loaded_dtree_params_round1, X_test, y_test,
                                
                                 cmap=plt.cm.Blues,
                                 normalize = 'true')
plt.grid(False)
plt.show()

print(f'Test data accauracy for log reg : {loaded_logreg_params_log1.score(X_test,y_test)}')
plot_confusion_matrix(loaded_logreg_params_log1, X_test, y_test,
                                
                                 cmap=plt.cm.Blues,
                                 normalize = 'true')
plt.grid(False)
plt.show()

"""Based on the Confusion matrices and test data accuracy, Decison Trees are the best model to run on this data. It scales better and has a similar Test data accuracy to the highest model."""

