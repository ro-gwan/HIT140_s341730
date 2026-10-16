'''
#########prepwork######


import pandas as pd

df = pd.read_csv("Fifa2/prep/squad_48_teams_2.csv")
print('\n\n\nFinalised Fifa squad: raw player data')
print(df.info())

df_f = df[['Country_ANA','POS','CAPS','GOALS','DOB']]
df_f['DOB'] = pd.to_datetime(df_f['DOB'],unit='D', origin='1899-12-30')

#get age at start of FIFA2026

reference_date = pd.Timestamp('2026-06-11')
def calculateAge(dob):
    age = reference_date.year - dob.year
    # take 1 off if the birthday hasn't happened yet by the reference date
    if (reference_date.month, reference_date.day) < (dob.month, dob.day):
        age -= 1
    return age
df_f['Age'] = df_f['DOB'].apply(calculateAge)
print(df_f.info())
print(df_f.head())


# team goal,caps, age by country

df_ff = df_f.groupby('Country_ANA' )
goca = df_ff[['CAPS','GOALS']].sum().add_suffix('_total')
avg = df_ff[['CAPS','GOALS']].mean().add_suffix('_average')
ageMedian= df_ff['Age'].median().rename('Age_median')
dft = goca.join(avg).join(ageMedian).reset_index()
print(dft.info())
print(dft.head())


# team goals and caps by country and play position

df_ff = df_f.groupby(['Country_ANA', 'POS'])
posAvg = df_ff[['CAPS', 'GOALS']].mean().unstack('POS')
# flatten column names 
posAvg.columns = [f'{stat}_{pos}_mean' for stat, pos in posAvg.columns]
posAvg = posAvg.reset_index()
dft = dft.merge(posAvg, on='Country_ANA', how='left')

print("\n\nFinal squad player data grouped into countries, \n caps and goals calculated by playing positions, \n median team age at 11/06/2026 calculated from DOB")
print(dft.info())
print(dft.info())
print(dft.head())
dft.to_csv('Final_48_team_stats.csv)

###### used excel to wrangle into model datasheets  ####
'''


import pandas as pd
import math
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn import metrics
from sklearn import linear_model
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import QuantileTransformer
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('Fifa2/model1/Model_1_test18.csv')


print('\n\n\nModel_1_test18 initial dataset')
print(df.info())
print(df.head())

# LINEAR REGRESSION USING STATSMODELS



# Separate explanatory variables (x) starting from column 2 from the response variable (y= goal difference)
'''# dont specify only values 
x = df.iloc[:,3:-1]
y = df.iloc[:,-1]
x = sm.add_constant(x)   # to calculate intercept b0
model = sm.OLS(y,x).fit()
pred = model.predict(x)
model_report = model.summary()
print(model_report)

#Rescale to better compare units

#standard scaler =no significant change r^2 .165
#power transform = small improve- r^2 .175
#try quantile transformer to normalise distrobutionr^2 .169
#try robust scaler= no significant change r^2 .165
#keep PowerTransform

scaler= PowerTransformer()
std_x = scaler.fit_transform(x)
# Restore column names to x
std_x_df = pd.DataFrame(std_x, index=x.index, columns=x.columns)
#restore x to fit it  back in to into the model
x= std_x_df


# Build and evaluate the linear regression model
x = sm.add_constant(x)   # to calculate intercept b0
model = sm.OLS(y,x).fit()
pred = model.predict(x)
model_report = model.summary()
print(model_report)

#heatmap to see which variables to drop
# Plot correlation matrix
corr = df.iloc[:,3:].corr()

# Plot the correlation as heatmap
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=False,
    annot=True
)

# customise the labels
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
)

plt.show()
'''
# variables with least sifnificant corrolation with Y (Goal Difference)
# DF_Avg_cap_diff(.0085) , Squad Goal Rate Difference (.019), MF_Avg_cap_diff (.02)
#remove these and restart model

df = df.drop('DF_Avg_cap_diff', axis=1)
df = df.drop('MF_Avg_cap_diff', axis=1)
df = df.drop('Squad Goal Rate Difference', axis=1)

print("\n\n\nModel 1 dataset FINAL-8 explanatory variables")
print(df.info())
# dont specify only values 
x = df.iloc[:,3:-1]
y = df.iloc[:,-1]
'''
x = sm.add_constant(x)   # to calculate intercept b0
model = sm.OLS(y,x).fit()
pred = model.predict(x)
model_report = model.summary()
print(model_report)'''
# better adjusted results- R^2 = .161/ adj r^2 = .09

#Rescale to better compare units
scaler= PowerTransformer()
std_x = scaler.fit_transform(x)
# Restore column names to x
std_x_df = pd.DataFrame(std_x, index=x.index, columns=x.columns)
#restore x to fit it  back in to into the model
x= std_x_df


# Build and evaluate the linear regression model
x = sm.add_constant(x)   # to calculate intercept b0
model = sm.OLS(y,x).fit()
pred = model.predict(x)
model_report = model.summary()
print(model_report)


#standard scaler =no significant change r^2 .161
#power transform = small improve- r^2 .170
#try quantile transformer to normalise distrobutionr^2 .165
#try robust scaler= no significant change r^2 .161
#keep PowerTransform


#Visualise  final dataset

corr = df.iloc[:,3:].corr()

# Plot the correlation as heatmap
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=False,
    annot=True
)
font_style = {'fontsize' : 10}
# customise the labels
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right',
    fontdict=font_style
)


sns.set_theme(font_scale=.5)
f = sns.pairplot(df)
f.figure.suptitle('Goal Difference pairplot', y=1)

plt.show()

#strong right skew in whole dataset

# no obvious linear relationship with Y (goal difference)
#try different linear regression model

x = df.iloc[:,3:-1].values
y = df.iloc[:,-1].values

#Rescale to better compare units
scaler= PowerTransformer()
x = scaler.fit_transform(x)



model= LinearRegression()
test_split = .2
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_split, random_state=0)
model.fit(X_train, y_train)
# Print the intercept and coefficient learned by the linear regression model
print("Intercept: ",model.intercept_)
print("Coefficient: ",model.coef_)

y_pred = model.predict(X_test)
df_pred = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
print(df_pred.head(10))

# Compute standard performance metrics of the linear regression:
mae = metrics.mean_absolute_error(y_test, y_pred) # Mean Absolute Error
mse = metrics.mean_squared_error(y_test, y_pred) # Mean Squared Error
rmse =  math.sqrt(metrics.mean_squared_error(y_test, y_pred)) # Root Mean Square Error
y_max = y.max()
y_min = y.min()
rmse_norm = rmse / (y_max - y_min) # Normalised Root Mean Square Error
r_2 = metrics.r2_score(y_test, y_pred) # R-Squared

print('\n\n\n Multiple Linear Regression performance metrics:\n\t(data scaled using PowerTransformer)\n\t(train/test split at %.2f test)'%test_split)
print("MAE:  %.3f"%mae)
print("MSE: %.3f"%mse)
print("RMSE: %.3f"%rmse)
print("RMSE (Normalised): %.3f"%rmse_norm)
print("R^2: %.3f"%r_2)

#KFOLD
#use k-fold cross validation to evaluate the model
k = 10
kf= KFold(n_splits=k, random_state=None)
#odel = LogisticRegression()

model = LinearRegression()
Nrmse = []
rSqr = []

for train_index, test_index in kf.split(x):
    X_train, X_test =x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    model.fit(X_train,y_train)
    y_pred =model.predict(X_test)
    
    mae = metrics.mean_absolute_error(y_test, y_pred) # Mean Absolute Error
    mse = metrics.mean_squared_error(y_test, y_pred) # Mean Squared Error
    rmse =  math.sqrt(metrics.mean_squared_error(y_test, y_pred)) # Root Mean Square Error
    y_max = y.max()
    y_min = y.min()
    rmse_norm = rmse / (y_max - y_min) # Normalised Root Mean Square Error  
    Nrmse.append(rmse_norm)
    r_2 = metrics.r2_score(y_test, y_pred)
    rSqr.append(r_2)
    
    
    
avg_r2_score = sum(rSqr)/k
avg_nrmse = sum(Nrmse)/k

print("\n Model perferformance at %.2f test split, \n  using (%d)  Kfold validation  "%(test_split,k))
# print('R^2 of each fold   : {}'.format(rSqr),'\n   NRMSE of each fold : {}'.format(Nrmse))
print('Average   R^2   : %.3f\n  Average NRMSE : %.3f'%(avg_r2_score,avg_nrmse))






"""
COMPARE THE PERFORMANCE OF THE LINEAR REGRESSION MODEL
VS.  DUMMY MODEL (BASELINE) THAT USES MEAN AS THE BASIS OF ITS PREDICTION
"""
print("\n\n##### BASELINE MODEL #####\n(based on mean data values)")

# Compute mean of values in (y) training set and replicate the mean values as many times as there are values in the test set
y_base = np.mean(y_train)
y_pred_base = [y_base] * len(y_test)

#Show the predicted values of (y) next to the actual values of (y)
df_base_pred = pd.DataFrame({"Actual": y_test, "Predicted": y_pred_base})
print(df_base_pred.head())

# Compute standard performance metrics of the baseline model:
mae = metrics.mean_absolute_error(y_test, y_pred_base)
mse = metrics.mean_squared_error(y_test, y_pred_base)
rmse =  math.sqrt(metrics.mean_squared_error(y_test, y_pred_base))
rmse_norm = rmse / (y_max - y_min)
r_2 = metrics.r2_score(y_test, y_pred_base)

print("MAE: %.3f"%mae)
print("MSE: %.3f"%mse)
print("RMSE: %.3f"%rmse)
print("RMSE (Normalised): %.3f"%rmse_norm)
print("R^2:  %.3f"%r_2)