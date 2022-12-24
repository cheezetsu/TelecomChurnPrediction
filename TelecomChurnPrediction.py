# -*- coding: utf-8 -*-
"""Telecom Churn Prediction Colab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ovewHAby4qPeRpX1PFg_JnbP8ldeDWe6

คณะผู้จัดทำ

นาย เกริกพล รัตนภูมิ 6209680195

นางสาว นงนภัส วงศ์ปิยะชัย 6309650734

นางสาว ธวัลรัตน์ เรืองรัตนเมธี 6309650890

นาย ภูกิจณัฏฐ์ เมฆาสวัสดิ์วงค์ 6309650908
"""

# Import all necessary libraries
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from mpl_toolkits.mplot3d import Axes3D

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

"""# **Data Source:**

Each row represents a customer, each column contains customer’s attributes described on the column Metadata. The raw data contains 7043 rows (customers) and 21 columns (features).

We will use the dataset ``Telecom_Churn_Prediction.csv`` downloaded from Kaggle throughout this project.
"""

from google.colab import drive
drive.mount('/content/drive')

# Read the data
telecom_cust = pd.read_csv('/content/drive/MyDrive/CS345/dataset/Telecom_Churn_Prediction.csv')

"""## Looking at the data"""

# First five rows of data
telecom_cust.head()

# The dimensionality of data
print("Shape of data: {}".format(telecom_cust.shape))

# All the columns
print("Feature names: \n{}".format(telecom_cust.columns.values))

"""## Visualizing the distribution of individual variables
 
 นำตัวอย่างบางส่วนมาจาก https://www.kaggle.com/code/bandiatindra/telecom-churn-prediction/notebook

### Demographics

#### Gender
"""

colors = ['#3AB0FF', '#F87474']
gender_percent = telecom_cust['gender'].value_counts()*100.0/len(telecom_cust)

ax = (telecom_cust['gender'].value_counts()*100.0/len(telecom_cust)).plot(kind = 'bar', color = colors)
ax.set_title('Gender Distribution')
ax.set_xlabel('Gender')
ax.set_ylabel('Customers (%)')

# set bar labels
patches = ax.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()/2
   ax.annotate('{:.2f}%'.format(gender_percent[i]), (x, y), ha = 'center', fontsize = 12, color = 'black')

plt.show()

"""About half of the customers are male and the other half are female.

#### Senior Citizen
"""

colors = ['#FF6464', '#BCE29E']
SeniorCitizen_percent = telecom_cust['SeniorCitizen'].value_counts()*100.0/len(telecom_cust)

ax = (telecom_cust['SeniorCitizen'].value_counts()*100.0/len(telecom_cust)).plot(kind = 'bar', color = colors)
ax.set_title('Senior Citizen Distribution')
ax.set_xlabel('Senior Citizen')
ax.set_ylabel('Customers (%)')

# set bar labels
patches = ax.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()/2
   ax.annotate('{:.2f}%'.format(SeniorCitizen_percent[i]), (x, y), ha = 'center', fontsize = 12, color = 'black')

plt.show()

"""Only about 16% of the customers are senior citizens. Thus most of the customers are young people.

#### Partner and Dependent
"""

df1 = pd.melt(telecom_cust, id_vars = ['customerID'], value_vars = ['Partner', 'Dependents'])
df2 = df1.groupby(['variable', 'value']).count().unstack()
df3 = df2*100/len(telecom_cust)
colors = ['#FF6464', '#BCE29E']

ax = df3.loc[:, 'customerID'].plot.bar(stacked = True, color = colors)
ax.set_title('Customers with Partner and Dependent')
ax.set_ylabel('Customers (%)')
ax.legend(loc = 'center')

# set bar labels
for p in ax.patches: 
  width, height = p.get_width(), p.get_height()
  x, y = p.get_xy()
  ax.annotate('{:.2f}%'.format(height), (p.get_x() + .25 * width, p.get_y() + .4 * height), color = 'black')

"""Only about half of customers have a dependent, while the other half do not. """

partner_dependent = telecom_cust.groupby(['Partner', 'Dependents']).size().unstack()
colors = ['#FF6464', '#BCE29E']

ax = (partner_dependent.T*100.0/partner_dependent.T.sum()).T.plot(kind = 'bar', stacked = True, color = colors)
ax.set_title('Customers with/without Dependent based on whether they have a partner')
ax.set_ylabel('Customers (%)')
ax.legend(loc = 'center')

# set bar labels
for p in ax.patches: 
  width, height = p.get_width(), p.get_height()
  x, y = p.get_xy()
  ax.annotate('{:.2f}%'.format(height), (p.get_x() + .25 * width, p.get_y() + .4 * height), color = 'black')

"""Among the customers who do not have any partners, most of them also do not have any dependents.

### Customers Account Information

#### Tenure
"""

# ax = sns.distplot
plt.hist(telecom_cust['tenure'], bins = 35, edgecolor='black')
plt.title('Customers Distribution by their Tenure')
plt.xlabel('Tenure (months)')
plt.ylabel('Amount of Customers')

plt.show()

"""Most of the customers have been with the company for just a month, while quite many for about 72 months.

#### Contract
"""

colors = ['#BA94D1', '#EF9A53', '#47B5FF']
contract_num = telecom_cust['Contract'].value_counts()

ax = (telecom_cust['Contract'].value_counts()).plot(kind = 'bar', color = colors)
ax.set_title('Customers Distribution by their Contract')
ax.set_xlabel('Contract')
ax.set_ylabel('Amount of Customers')

# set bar labels
patches = ax.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()/2
   ax.annotate(str("{:,}".format(list(contract_num)[i])), (x, y), ha = 'center', fontsize = 12, color = 'black')

plt.show()

"""Most of the customers are in the month-to-month contract, while 1 year and 2 year contracts have almost the same number of customers.

#### Tenure and Contract
"""

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (20, 5), sharey = True)

ax = sns.distplot(telecom_cust[telecom_cust['Contract'] == 'Month-to-month']['tenure'],
                  hist = True, kde = False, bins = 35, color = '#BA94D1',
                  hist_kws = {'edgecolor': 'black'}, ax = ax1)
ax.set_title('Month to Month Contract')
ax.set_xlabel('Tenure (months)')
ax.set_ylabel('Amount of Customers')

ax = sns.distplot(telecom_cust[telecom_cust['Contract'] == 'One year']['tenure'],
                  hist = True, kde = False, bins = 35, color = '#EF9A53',
                  hist_kws = {'edgecolor': 'black'}, ax = ax2)
ax.set_title('One Year Contract')
ax.set_xlabel('Tenure (months)')

ax = sns.distplot(telecom_cust[telecom_cust['Contract'] == 'Two year']['tenure'],
                  hist = True, kde = False, bins = 35, color = '#47B5FF',
                  hist_kws = {'edgecolor': 'black'}, ax = ax3)

ax.set_title('Two year Contract')
ax.set_xlabel('Tenure (months)')

"""Most of the monthly contracts last for 1-2 months, while the 2-year contracts tend to last for 70 months. This shows that the customers who take a long contract are more loyal to the company and tend to stay with it for a longer period of time.

### Services
"""

services = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
            'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
colors = ['#BA94D1', '#EF9A53', '#47B5FF']

fig, axes = plt.subplots(3, 3, figsize = (15, 12))

for i, service in enumerate(services):
  if i < 3:
    ax = telecom_cust[service].value_counts().plot(kind = 'bar', ax = axes[i, 0], color = colors)

  elif i >= 3 and i < 6:
    ax = telecom_cust[service].value_counts().plot(kind = 'bar', ax = axes[i - 3, 1], color = colors)

  elif i < 9:
    ax = telecom_cust[service].value_counts().plot(kind = 'bar', ax = axes[i - 6, 2], color = colors) 

  ax.set_title(service)

"""### Monthly Charges and Total Charges"""

x = telecom_cust['MonthlyCharges']
y = pd.to_numeric(telecom_cust.TotalCharges, errors='coerce')

plt.scatter(x, y)
plt.xlabel('Monthly Charges')
plt.ylabel('Total Charges')

plt.show()

"""The total charges increase as the monthly charge for the customer increase.

### Payment Method
"""

colors = ['#BA94D1', '#EF9A53', '#47B5FF', '#FFABE1']
payment_percent = telecom_cust['PaymentMethod'].value_counts()*100.0/len(telecom_cust)

ax = (telecom_cust['PaymentMethod'].value_counts()*100.0/len(telecom_cust)).plot(kind = 'bar', color = colors)
ax.set_title('Payment Method Distribution')
ax.set_xlabel('Payment Method')
ax.set_ylabel('Customers (%)')

# set bar labels
patches = ax.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()/2
   ax.annotate('{:.2f}%'.format(payment_percent[i]), (x, y), ha = 'center', fontsize = 12, color = 'black')

plt.show()

"""Most customers use electronic checks for payment.

### Churn
"""

colors = ['#BCE29E', '#FF6464']
churn_percent = telecom_cust['Churn'].value_counts()*100.0/len(telecom_cust)

ax = (telecom_cust['Churn'].value_counts()*100.0/len(telecom_cust)).plot(kind = 'bar', color = colors)
ax.set_title('Churn Rate')
ax.set_xlabel('Churn')
ax.set_ylabel('Customers (%)')

# set bar labels
patches = ax.patches
for i in range(len(patches)):
   x = patches[i].get_x() + patches[i].get_width()/2
   y = patches[i].get_height()/2
   ax.annotate('{:.2f}%'.format(churn_percent[i]), (x, y), ha = 'center', fontsize = 12, color = 'black')

plt.show()

"""About 73% of the customers do not churn.

#### Churn by Seniority
"""

colors = ['#BCE29E', '#FF6464']
senior_churn = telecom_cust.groupby(['SeniorCitizen', 'Churn']).size().unstack()

ax = (senior_churn.T*100.0/senior_churn.T.sum()).T.plot(kind = 'bar', stacked = True, color = colors)
ax.set_title('Churn by Seniority')
ax.set_ylabel('Customers (%)')
ax.legend(loc = 'best')

# set bar labels
for p in ax.patches: 
  width, height = p.get_width(), p.get_height()
  x, y = p.get_xy()
  ax.annotate('{:.2f}%'.format(height), (p.get_x() + .25 * width, p.get_y() + .4 * height), color = 'black')

"""Senior citizen have almost double churn rate than young people.

#### Churn by Tenure
"""

sns.boxplot(telecom_cust['Churn'], telecom_cust['tenure'])

"""The customers who do not churn tend to stay for a longer tenure with the company

#### Churn by Contract
"""

colors = ['#BCE29E', '#FF6464']
contract_churn = telecom_cust.groupby(['Contract', 'Churn']).size().unstack()

ax = (contract_churn.T*100.0/contract_churn.T.sum()).T.plot(kind = 'bar', stacked = True, color = colors)
ax.set_title('Churn by Contract')
ax.set_ylabel('Customers (%)')
ax.legend(loc = 'best')

# set bar labels
for p in ax.patches: 
  width, height = p.get_width(), p.get_height()
  x, y = p.get_xy()
  ax.annotate('{:.2f}%'.format(height), (p.get_x() + .25 * width, p.get_y() + .4 * height), color = 'black')

"""The customers who have a month-to-month contract have a very high churn rate.

#### Churn by Monthly Charges and Total Charges
"""

ax = sns.kdeplot(telecom_cust['MonthlyCharges'][(telecom_cust['Churn'] == 'No') ], color = "#BCE29E", shade = True)
ax = sns.kdeplot(telecom_cust['MonthlyCharges'][(telecom_cust['Churn'] == 'Yes') ], ax = ax, color = "#FF6464", shade= True)
ax.set_title('Distribution of Monthly Charges by churn')
ax.set_xlabel('Monthly Charges')
ax.set_ylabel('Density')
ax.legend(['Not Churn', 'Churn'], loc = 'upper right')

x = pd.to_numeric(telecom_cust.TotalCharges, errors='coerce')

ax = sns.kdeplot(x[(telecom_cust['Churn'] == 'No') ], color = "#BCE29E", shade = True)
ax = sns.kdeplot(x[(telecom_cust['Churn'] == 'Yes') ], ax = ax, color= "#FF6464", shade = True)
ax.set_title('Distribution of Total Charges by Churn')
ax.set_xlabel('Total Charges')
ax.set_ylabel('Density')
ax.legend(['Not Churn', 'Churn'], loc='upper right')

"""Higher customers churn when monthly charges are high, But in total charges, higher churn when the total charges are lower.

# **Data Preparation:**

## Explore the data
"""

# Checking the data types of all the columns
telecom_cust.dtypes

# Converting Total Charges to a numerical data type
telecom_cust.TotalCharges = pd.to_numeric(telecom_cust.TotalCharges, errors='coerce')
telecom_cust.dtypes

# Check whether any null value exists
telecom_cust.isnull().sum()

"""From the above output, there are 11 missing values for Total Charges

## Data Cleansing
"""

# Removing missing values 
telecom_cust.dropna(inplace = True)

# Removing unnecessary columns
telecom_cust.drop(['customerID'], axis = 1, inplace = True)

print("Shape after dropping: {}".format(telecom_cust.shape))

"""## Data Transformation"""

# Converting the predictor label into binary numeric variables (0 and 1)
telecom_cust['Churn'].replace(to_replace = 'No', value = 0, inplace = True)
telecom_cust['Churn'].replace(to_replace = 'Yes', value = 1, inplace = True)
telecom_cust['Churn']

# Converting the categorical features into dummy variables
telecom_cust_dummies = pd.get_dummies(telecom_cust)
telecom_cust_dummies.head()

"""## Feature Selection - ปัจจัยที่ส่งผลต่อการเลิกใช้บริการของลูกค้า"""

# Plotting the correlation of Churn with other features
plt.figure(figsize = (20, 10))
telecom_cust_dummies.corr()['Churn'].sort_values(ascending = False).plot(kind = 'bar')

"""Month-to-month contracts, a lack of online security, and technical support appear to be positively related to churn. While tenure and two-year contracts appear to be negatively correlated.

It's interesting to note that churn appears to be adversely correlated with services like online backup, tech support, streaming TV, etc. that don't require an internet connection.

# **Data Representation:**
"""

X_telecom_cust, y_telecom_cust = telecom_cust_dummies.drop('Churn', axis = 1), telecom_cust_dummies['Churn']

# Create training and testing set
X_train, X_test, y_train, y_test = train_test_split(X_telecom_cust, y_telecom_cust, random_state = 0)

print("X_train shape: {}".format(X_train.shape)) 
print("y_train shape: {}".format(y_train.shape))

print("X_test shape: {}".format(X_test.shape)) 
print("y_test shape: {}".format(y_test.shape))

"""# **Modeling:**

## Baseline Models

We will apply LazyClassifier and compare every model based on the Accuracy of each model.
"""

!pip3 install -U lazypredict

from lazypredict.Supervised import LazyClassifier

clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric = None,classifiers = 'all')
models,predictions = clf.fit(X_train, X_test, y_train, y_test)

print(models)

models.sort_values(by = 'Accuracy',inplace = True,ascending = False)
line = px.line(data_frame= models ,y =["Accuracy"] , markers = True)
line.update_xaxes(title="Model",
              rangeslider_visible = False)
line.update_yaxes(title = "Accuracy")
line.update_traces(line_color="red")
line.update_layout(showlegend = True,
    title = {
        'text': 'Accuracy vs Model'})

line.show()

"""## Logistic Regression"""

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression().fit(X_train, y_train)

print("Accuracy of Logistic Regression classifier on training set: {:.3f}".format(lr.score(X_train, y_train)))
print("Accuracy of Logistic Regression classifier on test set: {:.3f}".format(lr.score(X_test, y_test)))

"""### LR with scaling"""

from sklearn.preprocessing import MinMaxScaler

# Scaling the data using MinMaxScaler
scaler = MinMaxScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LogisticRegression()
lr.fit(X_train_scaled, y_train)

print("Accuracy of Logistic Regression classifier on training set (with scaling): {:.3f}".format(lr.score(X_train_scaled, y_train)))
print("Accuracy of Logistic Regression classifier on test set (with scaling): {:.3f}".format(lr.score(X_test_scaled, y_test)))

"""### LR with GridSearchCV"""

# Check the list of available parameters
lr.get_params().keys()

lr_param_grid = {"C": [0.001, 0.01, 0.1, 1, 10, 100, 1000], 
                 "penalty": ['l1','l2'], 
                 "solver": ['newton-cg', 'lbfgs', 'liblinear']}  
lr_cv = GridSearchCV(LogisticRegression(), lr_param_grid, cv=5)
lr_cv.fit(X_train_scaled, y_train)

print("Best parameters: {}".format(lr_cv.best_params_))
print("Best cross-validation score: {:.3f}".format(lr_cv.best_score_))

print("Accuracy of Logistic Regression on test set (with tuning): {:.3f}".format(lr_cv.score(X_test_scaled, y_test)))

# To get the weight of all variables
weights = pd.Series(lr.coef_[0],
                 index=X_telecom_cust.columns.values)
print (weights.sort_values(ascending = False)[:10].plot(kind='bar'))

print(weights.sort_values(ascending = False)[-10:].plot(kind='bar'))

"""**Observations:**

We can see that some variables have a positive relation to Churn, while some have negative relation. Negative relation means that Churn tends to decrease with that variable.

*   We can see that in plotting distribution of tenure and contract, two year contract along with tenure have the most negative relation with Churn as predicted by logistic regressions
*   Having DSL internet service also reduces the pobability of Churn
*   Total charges, month-to-month contract and fibre optic internet services can lead to higher churn rates. This's interesting because even if fiber optic service is faster, customers are likely to churn.

## Linear Support Vector Machines
"""

from sklearn.svm import LinearSVC

svc = LinearSVC().fit(X_train, y_train)

print("Accuracy of Linear Support Vector Machines on training set: {:.3f}".format(svc.score(X_train, y_train)))
print("Accuracy of Linear Support Vector Machines on test set: {:.3f}".format(svc.score(X_test, y_test)))

"""### SVC with scaling"""

svc = LinearSVC()
svc.fit(X_train_scaled, y_train)

print("Accuracy of Linear Support Vector Machines on training set (with scaling): {:.3f}".format(svc.score(X_train_scaled, y_train)))
print("Accuracy of Linear Support Vector Machines on test set (with scaling): {:.3f}".format(svc.score(X_test_scaled, y_test)))

"""### SVC with GridSearchCV"""

# Check the list of available parameters
svc.get_params().keys()

svc_param_grid = {"C": [0.001, 0.01, 0.1, 1, 10, 100, 1000], 
                  "penalty": ['l1','l2']}  
svc_cv = GridSearchCV(LinearSVC(), svc_param_grid, cv=5)
svc_cv.fit(X_train_scaled, y_train)

print("Best parameters: {}".format(svc_cv.best_params_))
print("Best cross-validation score: {:.3f}".format(svc_cv.best_score_))

print("Accuracy of Linear Support Vector Machines on test set (with tuning): {:.3f}".format(svc_cv.score(X_test_scaled, y_test)))

"""## Random Forest"""

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_train, y_train)

print("Accuracy of Random Forest Classifier on training set: {:.3f}".format(forest.score(X_train, y_train)))
print("Accuracy of Random Forest Classifier on test set: {:.3f}".format(forest.score(X_test, y_test)))

importances = forest.feature_importances_
weights = pd.Series(importances,
                 index=X_telecom_cust.columns.values)
weights.sort_values()[-10:].plot(kind = 'barh')

"""**Observations:**


*   From the random forest algorithm, total charges, tenure, and monthly charges are the most important features to predict churn, the results are very similar to logistic regression and from we visualization.

## PCA
"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_telecom_cust)
X_telecom_cust_scaled = scaler.transform(X_telecom_cust)

# Keep the first three principal components of the data
pca = PCA(n_components = 3, random_state = 0)
pca.fit(X_telecom_cust_scaled)
X_telecom_cust_pca = pca.transform(X_telecom_cust_scaled)

print("Original shape: {}".format(str(X_telecom_cust_scaled.shape)))
print("Reduced shape: {}".format(str(X_telecom_cust_pca.shape)))

print("Principal components: \n", pca.components_.T)

exp_var = pca.explained_variance_ratio_

print("Total variation explained: {0} = {1:.2f}%".format(exp_var, sum(pca.explained_variance_ratio_*100)))

print("Variance of 1st principal component: {:.3f}%".format(pca.explained_variance_ratio_[0]*100))

plt.matshow(pca.components_, cmap='viridis')
plt.yticks([0, 1], ["First component", "Second component"])
plt.colorbar()
plt.xticks(range(len(telecom_cust_dummies.columns.values)),
           telecom_cust_dummies.columns.values, rotation=60, ha='left')
plt.xlabel("Feature")
plt.ylabel("Principal components")

"""## Clustering - การจัดกลุ่มลูกค้าที่ใช้บริการ

### Clustering KMean Without PCA for detect Customer Churn Segment
"""

from sklearn.cluster import KMeans 

monthlyp_and_tenure = telecom_cust[['MonthlyCharges', 'tenure']][telecom_cust.Churn == 1]

scaler = MinMaxScaler()
monthly_and_tenure_standardized = pd.DataFrame(scaler.fit_transform(monthlyp_and_tenure) )
monthly_and_tenure_standardized.columns = ['MonthlyCharges', 'tenure']

kmeans = KMeans(n_clusters = 5, random_state = 0).fit(monthly_and_tenure_standardized)

monthly_and_tenure_standardized['cluster'] = kmeans.labels_

fig, ax = plt.subplots(figsize=(13, 8))
plt.scatter(monthly_and_tenure_standardized['MonthlyCharges'], monthly_and_tenure_standardized['tenure'],
           c = monthly_and_tenure_standardized['cluster'], cmap = 'brg', s=100)

plt.title('Clustering churned users by monthly Charges and tenure')
plt.xlabel('Monthly Charges')
plt.ylabel('Tenure')


plt.show()

"""### KMeans"""

km = KMeans(n_clusters=2)
clusters = km.fit_predict(X_telecom_cust_pca)
X_telecom_cust_pca = pd.DataFrame(X_telecom_cust_pca)
                                  
X_telecom_cust_pca["label"] = clusters

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label == 0], X_telecom_cust_pca[1][X_telecom_cust_pca.label == 0], X_telecom_cust_pca[2][X_telecom_cust_pca.label == 0], c='blue', s=60)
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label == 1], X_telecom_cust_pca[1][X_telecom_cust_pca.label == 1], X_telecom_cust_pca[2][X_telecom_cust_pca.label == 1], c='red', s=60)
#ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label == 2], X_telecom_cust_pca[1][X_telecom_cust_pca.label == 2], X_telecom_cust_pca[2][X_telecom_cust_pca.label == 2], c='green', s=60)

ax.view_init(30, 130)
plt.xlabel("First principal component")
plt.ylabel("Second principal component")
ax.set_zlabel('Third principal component')
plt.show()

"""### DBScan"""

from sklearn.cluster import DBSCAN

for eps in[1,3,5,7,9,11,13]:
  print("\neps={}".format(eps))
  dbscan = DBSCAN(eps=eps, min_samples=40)
  labels = dbscan.fit_predict(X_telecom_cust_pca)
  print("Clusters present: {}".format(np.unique(labels)))
  print("Clusters sizes : {}".format(np.bincount(labels+1)))

dbscan = DBSCAN(eps=1, min_samples=40)
labels = dbscan.fit_predict(X_telecom_cust_pca)
                                  
X_telecom_cust_pca["label_db"] = labels
 
fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label_db == 0], X_telecom_cust_pca[1][X_telecom_cust_pca.label_db == 0], X_telecom_cust_pca[2][X_telecom_cust_pca.label_db == 0], c='blue', s=60)
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label_db == 1], X_telecom_cust_pca[1][X_telecom_cust_pca.label_db == 1], X_telecom_cust_pca[2][X_telecom_cust_pca.label_db == 1], c='red', s=60)
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label_db == 2], X_telecom_cust_pca[1][X_telecom_cust_pca.label_db == 2], X_telecom_cust_pca[2][X_telecom_cust_pca.label_db == 2], c='green', s=60)

ax.view_init(30, 130)
plt.xlabel("First principal component")
plt.ylabel("Second principal component")
ax.set_zlabel('Third principal component')
plt.show()

"""### PCA with Actual"""

X_telecom_cust_pca["label_Real"] = y_telecom_cust

fig = plt.figure(figsize=(30,20))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label_Real == 0], X_telecom_cust_pca[1][X_telecom_cust_pca.label_Real == 0], X_telecom_cust_pca[2][X_telecom_cust_pca.label_Real == 0], c='blue', s=60)
ax.scatter(X_telecom_cust_pca[0][X_telecom_cust_pca.label_Real == 1], X_telecom_cust_pca[1][X_telecom_cust_pca.label_Real == 1], X_telecom_cust_pca[2][X_telecom_cust_pca.label_Real == 1], c='red', s=60)


ax.view_init(30, 130)
plt.xlabel("First principal component")
plt.ylabel("Second principal component")
ax.set_zlabel('Third principal component')
plt.show()

"""# **Evaluation:**"""

# Make predictions on test dataset
lr_predictions = lr.predict(X_test_scaled)
svc_predictions = svc.predict(X_test_scaled)
forest_predictions = forest.predict(X_test_scaled)

# Evaluate predictions
print("Logistic Regression accuracy score: {:.3f}".format(accuracy_score(y_test, lr_predictions)))
print("Linear Support Vector Machines accuracy score: {:.3f}".format(accuracy_score(y_test, svc_predictions)))
print("Random Forest accuracy score: {:.3f}".format(accuracy_score(y_test, forest_predictions)))

import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
      plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

plt.figure(figsize = (5, 5))
plot_confusion_matrix(confusion_matrix(y_test, lr_predictions), classes=['churn=0', 'churn=1'], normalize= False,  title='Logistic Regression Confusion matrix')
print(classification_report(y_test, lr_predictions))

plt.figure(figsize = (5, 5))
plot_confusion_matrix(confusion_matrix(y_test, svc_predictions), classes=['churn=0', 'churn=1'], normalize= False,  title='Linear Support Vector  Confusion matrix')
print(classification_report(y_test, svc_predictions))

plt.figure(figsize = (5, 5))
plot_confusion_matrix(confusion_matrix(y_test, forest_predictions), classes=['churn=0', 'churn=1'], normalize= False,  title='Random Forest Confusion matrix')
print(classification_report(y_test, forest_predictions))