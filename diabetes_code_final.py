# -*- coding: utf-8 -*-
"""Diabetes_FDS_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QZaAq6xxPpOEAPDEzwXGtXECHgkI_6og
"""

# Importing essential libraries
import numpy as np
import pandas as pd

from google.colab import files
uploaded = files.upload()

import io

# Loading the dataset
df = pd.read_csv(io.BytesIO(uploaded['diabetes.csv']))

# Returns number of rows and columns of the dataset
df.shape

# Returns an object with all of the column headers 
df.columns

# Returns different datatypes for each columns (float, int, string, bool, etc.)
df.dtypes

# Returns the first x number of rows when head(num). Without a number it returns 5
df.head()

# Returns basic information on all columns
df.info()

# Returns basic statistics on numeric columns
df.describe().T

# Returns true for a column having null values, else false
df.isnull().any()

df = df.rename(columns={'DiabetesPedigreeFunction':'DPF'})
df.head()

# Commented out IPython magic to ensure Python compatibility.
# Importing essential libraries for visualization
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

# Plotting the Outcomes based on the number of dataset entries
plt.figure(figsize=(10,7))
sns.countplot(x='Outcome', data=df)

# Removing the unwanted spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Headings
plt.xlabel('Has Diabetes')
plt.ylabel('Count')

plt.show()

# Replacing the 0 values from ['Glucose','BloodPressure','SkinThickness','Insulin','BMI'] by NaN
df_copy = df.copy(deep=True)
df_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = df_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)
df_copy.isnull().sum()

# To fill these Nan values the data distribution needs to be understood
# Plotting histogram of dataset before replacing NaN values
columns = list(df)[0:-1] # Excluding Outcome column which has only 
df[columns].hist(stacked=False, bins=100, figsize=(15,30), layout=(10,2)); 
# Histogram of first 8 columns

# Replacing NaN value by mean, median depending upon distribution
df_copy['Glucose'].fillna(df_copy['Glucose'].mean(), inplace=True)
df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].mean(), inplace=True)
df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].median(), inplace=True)
df_copy['Insulin'].fillna(df_copy['Insulin'].median(), inplace=True)
df_copy['BMI'].fillna(df_copy['BMI'].median(), inplace=True)

df_copy.isnull().sum()

# Plotting histogram of dataset after replacing NaN values
columns = list(df_copy)[0:-1] # Excluding Outcome column which has only 
df_copy[columns].hist(stacked=False, bins=100, figsize=(15,30), layout=(10,2)); 
# Histogram of first 8 columns

# patients with diabetes may ingest more glucose
sns.distplot(df[df["Outcome"] == 1].Glucose, label="Diabetes")
sns.distplot(df[df["Outcome"] == 0].Glucose, label="Not Diabetes")
plt.legend()

# patients with diabetes may ingest more glucose
sns.distplot(df[df["Outcome"] == 1].BMI, label="Diabetes")
sns.distplot(df[df["Outcome"] == 0].BMI, label="Not Diabetes")
plt.legend()

# Check if there are any correlations between the features. 
sns.heatmap(df.corr())





from sklearn.model_selection import train_test_split

X = df.drop(columns='Outcome')
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
print('X_train size: {}, X_test size: {}'.format(X_train.shape, X_test.shape))

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Creating ANN Model
from sklearn.neural_network import MLPClassifier
model_ANN = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=1000, random_state=42)
model_ANN.fit(X_train, y_train)

# Creating a confusion matrix ANN 
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
y_pred = model_ANN.predict(X_test)
cm_ANN = confusion_matrix(y_test, y_pred)
cm_ANN

# Plotting the confusion matrix ANN
plt.figure(figsize=(10,7))
p = sns.heatmap(cm_ANN, annot=True, cmap="Blues", fmt='g')
plt.title('Confusion matrix for ANN Model - Test Set')
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.show()

# Accuracy Score for ANN
score = round(accuracy_score(y_test, y_pred),4)*100
print("Accuracy on test set ANN: {}%".format(score))

# Classification Report ANN
print(classification_report(y_test, y_pred))

from sklearn.metrics import roc_curve, auc
y_pred_quant = model_ANN.predict_proba(X_test)[:, 1] #Only keep the first column, which is the 'pos' values
fpr, tpr, thresholds = roc_curve(y_test, y_pred_quant)

plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.rcParams['font.size'] = 12
fig_title = ("ROC curve for ANN model, AUC = %0.3f" %(auc(fpr,tpr)))
plt.title(fig_title)
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.grid(True)





# Creating Random Forest Model
from sklearn.ensemble import RandomForestClassifier
model_RF = RandomForestClassifier(n_estimators=20, random_state=0)
model_RF.fit(X_train, y_train)

# Creating a confusion matrix RF
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
y_pred = model_RF.predict(X_test)
cm_RF = confusion_matrix(y_test, y_pred)
cm_RF

# Plotting the confusion matrix RF
plt.figure(figsize=(10,7))
p = sns.heatmap(cm_RF, annot=True, cmap="Blues", fmt='g')
plt.title('Confusion matrix for Random Forest Model - Test Set')
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.show()

# Accuracy Score for RF
score = round(accuracy_score(y_test, y_pred),4)*100
print("Accuracy on test set: {}%".format(score))

# Classification Report RF
print(classification_report(y_test, y_pred))

from sklearn.metrics import roc_curve, auc
y_pred_quant = model_RF.predict_proba(X_test)[:, 1] #Only keep the first column, which is the 'pos' values
fpr, tpr, thresholds = roc_curve(y_test, y_pred_quant)

plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.rcParams['font.size'] = 12
fig_title = ("ROC curve for RF model, AUC = %0.3f" %(auc(fpr,tpr)))
plt.title(fig_title)
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.grid(True)

## Feature importance in Random Forest
diabetes_features = [x for i,x in enumerate(df.columns) if i!=8]
def plot_feature_importances_diabetes(model):
    plt.figure(figsize=(8,6))
    n_features = 8
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), diabetes_features)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")
    plt.ylim(-1, n_features)
plot_feature_importances_diabetes(model_RF)

# Using GridSearchCV to explore other possible algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit

# Creating a function to calculate best model for this problem
def find_best_model(X, y):
    models = {
        'logistic_regression': {
            'model': LogisticRegression(solver='lbfgs', multi_class='auto'),
            'parameters': {
                'C': [1,5,10]
               }
        },
        
        'decision_tree': {
            'model': DecisionTreeClassifier(splitter='best'),
            'parameters': {
                'criterion': ['gini', 'entropy'],
                'max_depth': [5,10]
            }
        },
        

        'svm': {
            'model': SVC(gamma='auto'),
            'parameters': {
                'C': [1,10,20],
                'kernel': ['rbf','linear']
            }
        }

    }
    
    scores = [] 
    cv_shuffle = ShuffleSplit(n_splits=5, test_size=0.20, random_state=0)
        
    for model_name, model_params in models.items():
        gs = GridSearchCV(model_params['model'], model_params['parameters'], cv = cv_shuffle, return_train_score=False)
        gs.fit(X, y)
        scores.append({
            'model': model_name,
            'best_parameters': gs.best_params_,
            'score': gs.best_score_
        })
        
    return pd.DataFrame(scores, columns=['model','best_parameters','score'])

find_best_model(X_train, y_train)

# Creating SVM Model
model_SVM = SVC(kernel='linear', C=1, random_state=42)

model_SVM.fit(X_train, y_train)

# Creating a confusion matrix SVM
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
y_pred = model_SVM.predict(X_test)
cm_SVM = confusion_matrix(y_test, y_pred)
cm_SVM

# Plotting the confusion matrix SVM
plt.figure(figsize=(10,7))
p = sns.heatmap(cm_SVM, annot=True, cmap="Blues", fmt='g')
plt.title('Confusion matrix for SVM Model - Test Set')
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.show()

# Accuracy Score for SVM
score = round(accuracy_score(y_test, y_pred),4)*100
print("Accuracy on test set: {}%".format(score))

# Classification Report SVM
print(classification_report(y_test, y_pred))



# Creating a function for prediction
def predict_diabetes(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age):
    preg = int(Pregnancies)
    glucose = float(Glucose)
    bp = float(BloodPressure)
    st = float(SkinThickness)
    insulin = float(Insulin)
    bmi = float(BMI)
    dpf = float(DPF)
    age = int(Age)

    x = [[preg, glucose, bp, st, insulin, bmi, dpf, age]]
    x = sc.transform(x)

    return model_ANN.predict(x)

# Prediction 1
# Input sequence: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age
prediction = predict_diabetes(5, 120, 92, 10, 81, 26.1, 0.551, 67)[0]
if prediction:
  print('Oops! You have diabetes.')
else:
  print("Great! You don't have diabetes.")

# Prediction 2
# Input sequence: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age
prediction = predict_diabetes(1, 117, 88, 24, 145, 34.5, 0.403, 40)[0]
if prediction:
  print('Oops! You have diabetes.')
else:
  print("Great! You don't have diabetes.")

# Prediction 3
# Input sequence: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age
prediction = predict_diabetes(2, 81, 72, 15, 76, 30.1, 0.547, 25)[0]
if prediction:
  print('Oops! You have diabetes.')
else:
  print("Great! You don't have diabetes.")

