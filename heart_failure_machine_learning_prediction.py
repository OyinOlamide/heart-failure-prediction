# -*- coding: utf-8 -*-
"""Heart Failure Machine Learning Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LSrilnlxoviYjeMuzK0qHkiMcd-yRoj3

# Data Description

Age: Age in years.

Anaemia: 0 = False, 1 = True

Creatinine_phosphokinase: Level of CPK enzyme in the blood.

Diabetes: 0 = False, 1 = True

Ejection fraction: Percentage of how much blood the left ventricle pumps out with each contraction.

High blood pressure: 0 = False, 1 = True

Platelets: Platelet count in the blood.

Serum creatinine: Measure of creatinine in the blood.

Serum sodium: The measure of sodium in the blood.

Sex: 0 = Woman, 1 = Man

Smoking: 0 = False, 1 = True

Time: Number of days

Death event: 0 = False, 1 = True
"""

from google.colab import files

# Commented out IPython magic to ensure Python compatibility.
#necessary imports

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %matplotlib inline

import warnings
warnings.filterwarnings("ignore")

import plotly as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import download_plotlyjs, plot, init_notebook_mode, iplot

HF=files.upload()

import io
HF = pd.read_csv(io.BytesIO(HF["heart_failure_clinical_records_dataset.csv"]))

pip install plotly

pip install -U seaborn

pip install xgboost

HF.head()

HF.dtypes

HF.columns

HF.shape

HF.info

HF.describe()

plt.figure(figsize=(15,10))
sns.heatmap(HF.corr(method='pearson'), annot=True)

"""## Renaming Columns"""

HF.rename(columns={'creatinine_phosphokinase':'CPK','high_blood_pressure':'HBP', 'ejection_fraction':'EF', 'DEATH_EVENT':'death_event'},inplace=True);
HF.rename(columns=lambda x:x.strip().replace(' ','_'),inplace=True)

HF.columns

#check for null values

HF.isnull()

HF.isnull().sum()

#Check for duplicated values

HF.duplicated()

HF.duplicated().sum()

HF.drop_duplicates(subset=None, keep='first', inplace=False)

HF.nunique()

"""## Exploratory Data Analysis

**The Target Column Is The** **Death** **Event** **Column**


Death Event Column
"""

plt.figure(figsize = (12, 7))
 
sns.countplot(y = 'death_event', data = HF)
plt.show()
 
values = HF['death_event'].value_counts()
labels = ['Survived', 'Dead']
 
fig, ax = plt.subplots(figsize = (5, 5), dpi = 100)
explode = (0, 0.06)
 
patches, texts, autotexts = ax.pie(values, labels = labels, autopct = '%1.2f%%', shadow = True,
                                   startangle = 90, explode = explode)
 
plt.setp(texts, color = 'grey')
plt.setp(autotexts, size = 12, color = 'white')
autotexts[1].set_color('black')
plt.show()

"""**ALL CONTINOUS VALUE**S

Age Column
"""

plt.figure(figsize = (15, 6))
plt.style.use('ggplot')

sns.distplot(HF['age'])
plt.show()

#Check for outliers
sns.boxplot(HF['age'])

"""CPK"""

sns.kdeplot(
   data=HF, x="CPK", hue="death_event",
   fill=True, common_norm=False, palette="rocket",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['CPK'])

"""Ejection Fraction (EF)"""

sns.kdeplot(
   data=HF, x="EF", hue="death_event",
   fill=True, common_norm=False, palette="viridis",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['EF'])

"""Platelets"""

sns.kdeplot(
   data=HF, x="platelets", hue="death_event",
   fill=True, common_norm=False, palette="tab10",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['platelets'])

"""Serum Sodium"""

sns.kdeplot(
   data=HF, x="serum_sodium", hue="death_event",
   fill=True, common_norm=False, palette="husl",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['serum_sodium'])

"""Serum Creatinine"""

sns.kdeplot(
   data=HF, x="serum_creatinine", hue="death_event",
   fill=True, common_norm=False, palette="cubehelix",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['serum_creatinine'])

"""Time"""

sns.kdeplot(
   data=HF, x="time", hue="death_event",
   fill=True, common_norm=False, palette="flare",
   alpha=.5, linewidth=0,
)

#Check for outliers

sns.boxplot(HF['time'])

"""**ALL BOOLEAN VALUES**

Anaemia
"""

(HF['anaemia'].value_counts()/sum(HF['anaemia'].value_counts()))*100

HF.anaemia.value_counts()

HF.groupby(['anaemia', 'death_event'])['death_event'].count()

plt.figure(figsize = (16, 8))

sns.countplot('anaemia', hue = 'death_event', data = HF)
plt.show()

"""Diabetes"""

(HF['diabetes'].value_counts()/sum(HF['diabetes'].value_counts()))*100

HF.diabetes.value_counts()

HF.groupby(['diabetes', 'death_event'])['death_event'].count()

plt.figure(figsize = (16, 8))

sns.countplot('diabetes', hue = 'death_event', data = HF)
plt.show()

"""Hgh Blood Pressure (HBP)"""

(HF['HBP'].value_counts()/sum(HF['HBP'].value_counts()))*100

HF.HBP.value_counts()

HF.groupby(['HBP', 'death_event'])['death_event'].count()

plt.figure(figsize = (16, 8))

sns.countplot('HBP', hue = 'death_event', data = HF)
plt.show()

"""Sex"""

(HF['sex'].value_counts()/sum(HF['sex'].value_counts()))*100

HF.sex.value_counts()

HF.groupby(['sex', 'death_event'])['death_event'].count()

plt.figure(figsize = (16, 8))

sns.countplot('sex', hue = 'death_event', data = HF)
plt.show()

"""Smoking"""

(HF['smoking'].value_counts()/sum(HF['smoking'].value_counts()))*100

HF.smoking.value_counts()

HF.groupby(['smoking', 'death_event'])['death_event'].count()

plt.figure(figsize = (16, 8))

sns.countplot('smoking', hue = 'death_event', data = HF)
plt.show()

"""# **Model Building**"""

outliers = ['CPK','Platelets','serum_sodium','serum_creatinine']
def outlier_removal(HF,column):
    q1 = HF[column].quantile(0.25)
    q3 = HF[column].quantile(0.75)
    iqr = q3 - q1
    point_low = q1 - 1.5 * iqr
    point_high = q3 + 1.5 * iqr
    clean_HF = HF.loc[(HF[column] >  point_low) & (HF[column] <  point_high)]
    return clean_HF

# clean the dataset by removing outliers
HF_cleaned = outlier_removal(outlier_removal(outlier_removal(HF,'CPK'),'serum_creatinine'),'serum_sodium')
print(HF.shape)
print(HF_cleaned.shape)

X = HF.drop('death_event',axis=1)
y = HF['death_event']

from imblearn.over_sampling import RandomOverSampler
rs = RandomOverSampler(random_state=42)
X, y = rs.fit_resample(X,y)
X.shape,y.shape

features = ['age', 'anaemia', 'CPK', 'diabetes',
       'EF', 'HBP', 'platelets',
       'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time']
label = ['death_event']
X=HF[features]
y=HF[label]

from sklearn.model_selection import train_test_split
X_train,X_test, y_train,y_test=train_test_split(X,y,test_size=0.33, shuffle =True,random_state=42)

F1 = ['time','EF','serum_creatinine','age','serum_sodium','HBP']
predictors = HF[F1]
target = HF["death_event"]

X_train, X_test, y_train, y_test = train_test_split(predictors, target, test_size = 0.22, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()

X_train = sc.fit_transform(X_train[F1])
X_test = sc.transform(X_test[F1])

"""Logistic Regression"""

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X_train,y_train)

y_pred_log_reg = log_reg.predict(X_test)
y_pred_log_reg

from sklearn.metrics import f1_score, roc_auc_score,accuracy_score,confusion_matrix, precision_recall_curve, auc, roc_curve, recall_score, classification_report 
classification_report = classification_report(y_test, y_pred_log_reg)
print(classification_report)

print(accuracy_score(y_test,y_pred_log_reg))

auc = roc_auc_score(y_test, y_pred_log_reg)
auc

"""Random Forest"""

from sklearn.ensemble import RandomForestClassifier
RFC = RandomForestClassifier()

#random forest
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

acc_randomforest = round(accuracy_score(y_pred, y_test) * 100, 2)
print("Random Forest Model Accuracy : ",acc_randomforest)
print(classification_report)

auc = roc_auc_score(y_pred, y_test)
auc

"""MLPC"""

from sklearn.neural_network import MLPClassifier
M = MLPClassifier(hidden_layer_sizes=(128,128))

M.fit(X_train,y_train)
y_predM = M.predict(X_test)
print(f1_score(y_test,y_predM))
print(confusion_matrix(y_test,y_predM))
print(classification_report)

auc = roc_auc_score(y_test, y_predM)
auc

"""XGB"""

import xgboost as xgb
model = xgb.XGBClassifier()
model.fit(X_train,y_train)
y_pred1 = model.predict(X_test)
roc_auc_score(y_test, y_pred1)

print(classification_report)

accuracy = accuracy_score(y_test, y_pred1)
print(accuracy)

"""Gaussian Naive Bayes"""

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

#gaussian naive bayes
gnb = GaussianNB()
gnb.fit(X_train, y_train)
  
# making predictions on the testing set
y_pred = gnb.predict(X_test)
  
# comparing actual response values (y_test) with predicted response values (y_pred)
acc_naivebayes = round(accuracy_score(y_test, y_pred)*100,2)
print("Gaussian Naive Bayes model accuracy(in %):",acc_naivebayes )
print(classification_report)

auc = roc_auc_score(y_test, y_pred)
auc

"""SVM"""

#SVM Classifier

from sklearn.svm import SVC  
clf = SVC(kernel='linear') 
  
# fitting x samples and y classes 
clf.fit(X_train, y_train) 
y_pred = clf.predict(X_test)

acc_SVM = round(accuracy_score(y_pred, y_test) * 100, 2)
print("SVM Model Accuracy : ",acc_SVM)
print(classification_report)

auc = roc_auc_score(y_pred, y_test)
auc

"""DTC"""

from sklearn.tree import DecisionTreeClassifier

modeldt = DecisionTreeClassifier()

# fit the model with the training data
modeldt.fit(X_train,y_train)

# depth of the decision tree
print('Depth of the Decision Tree :', modeldt.get_depth())

# predict the target on the train dataset
predict_train = modeldt.predict(X_train)

# Accuray Score on train dataset
accuracy_train = accuracy_score(y_train,predict_train)
print('accuracy_score on train dataset : ', accuracy_train)

# predict the target on the test dataset
predict_test = model.predict(X_test)

# Accuracy Score on test dataset
accuracy_test = accuracy_score(y_test,predict_test)
print('accuracy_score on test dataset : ', accuracy_test*100)
print(classification_report)

auc = roc_auc_score(y_test, predict_test)
auc

"""Gradient Boostingg Classifier"""

from sklearn.ensemble import GradientBoostingClassifier
import lightgbm

gradientboost_clf = GradientBoostingClassifier(max_depth=2, random_state=1)
gradientboost_clf.fit(X_train,y_train)
gradientboost_pred = gradientboost_clf.predict(X_test)
gradientboost_f1 = f1_score(y_test, gradientboost_pred)
gradientboost_f1
 
acc_GBC= round(accuracy_score(y_pred, y_test) * 100, 2)
print(acc_GBC)
print(classification_report)

auc = roc_auc_score(y_pred, y_test)
auc

"""LGBMC"""

from sklearn.metrics import precision_score
lgb_clf = lightgbm.LGBMClassifier(max_depth=2, random_state=4)
lgb_clf.fit(X_train,y_train)
lgb_pred = lgb_clf.predict(X_test)
lgb_f1 = f1_score(y_test, lgb_pred)
lgb_precision = precision_score(y_test, lgb_pred)
lgb_f1

acc_lgb = round(accuracy_score(y_test, lgb_pred) * 100, 2)
acc_lgb

auc = roc_auc_score(y_test, lgb_pred)
auc

# saving the model 
import pickle 
pickle_out = open("classifier.pkl", mode = "wb") 
pickle.dump(RFC, pickle_out) 
pickle_out.close()

#!pip install -q pyngrok

#!pip install -q streamlit

#!pip install -q streamlit_ace

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
#  
# import pickle
# import streamlit as st
#  
# # loading the trained model
# pickle_in = open('classifier.pkl', 'rb') 
# classifier = pickle.load(pickle_in)
#  
# @st.cache()
#   
# # defining the function which will make the prediction using the data which the user inputs 
# def prediction(time,EF,serum_creatinine,age,serum_sodium,HBP):   
#  
#     # Pre-processing user input    
#     if HBP == "Yes":
#         HBP = 1
#     else:
#         HBP = 0
#  
#   
#     # Making predictions 
#     prediction = classifier.predict( 
#         [[time,EF,serum_creatinine,age,serum_sodium,HBP]])
#      
#     if prediction == 0:
#         pred = 'Will Survive'
#     else:
#         pred = 'Will Die'
#     return pred
#       
#   
# # this is the main function in which we define our webpage  
# def main():       
#     # front end elements of the web page 
#     html_temp = """ 
#     <div style ="background-color:yellow;padding:13px"> 
#     <h1 style ="color:black;text-align:center;">Streamlit Heart Failure Survival Prediction App</h1> 
#     </div> 
#     """
#       
#     # display the front end aspect
#     st.markdown(html_temp, unsafe_allow_html = True) 
#       
#     # following lines create boxes in which user can enter data required to make prediction 
#     age = st.number_input("What Is Patient's Age?") 
#     HBP = st.selectbox('Does Patient Have High Blood Pressure?',("Yes","No"))
#     time = st.number_input("How Long Has Patient Had It?") 
#     EF = st.number_input("Ejection Fraction In Percentage")
#     serum_creatinine = st.number_input("How much creatinine is in the patient's blood?")
#     serum_sodium = st.number_input("How much sodium is in the patient's blood?")
#     result =""
#       
#     # when 'Predict' is clicked, make the prediction and store it 
#     if st.button("Predict"): 
#         result = prediction(time,EF,serum_creatinine,age,serum_sodium,HBP) 
#         st.success('Patient {}'.format(result))
#         
#      
# if __name__=='__main__': 
#     main()

!streamlit run app.py &>/dev/null&

!git init

!mkdir -p ~/.streamlit/

!echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

# Commented out IPython magic to ensure Python compatibility.
# %%writefile requirements.txt
#  
# streamlit

# Commented out IPython magic to ensure Python compatibility.
# %%writefile Procfile
#  
# web: sh setup.sh && streamlit run app.py

"""This  to install Heroku"""

!curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

"""Or the 2 cells of code below;"""

!sudo /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

!brew install heroku/brew/heroku

!heroku login -i

!heroku create #input_your_app_name (it'd look like this: app_name.)

from pyngrok import ngrok
 
public_url = ngrok.connect('8501')
public_url