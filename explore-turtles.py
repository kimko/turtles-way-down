import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt
import seaborn as sns
import re

def recode_sex(sex_value):
    if sex_value in ['Male','male?','m','M']:
        return 'm'
    elif sex_value in ['Female','F','f']:
        return 'f'
    else:
        return 'unknown'

def recode_decimal(dirty_decimal=''):
    _ = []
    if not dirty_decimal:
        return 0
    if str(dirty_decimal):
        _ = re.findall(r"[-+]?\d*\.\d+|\d+",str(dirty_decimal))
    if _:
        return _[0]

fileName = './source/Turtle Data.xls'
#columnNames = ['Name','Address']

df = pd.DataFrame()
for year in range(2008,2014):
    df = df.append(pd.read_excel(fileName,sheet_name=str(year)),sort=False)

cleaned = df
cleaned['Gender'] = cleaned['Gender'].apply(recode_sex)
cleaned['Weight'] = cleaned['Weight'].apply(recode_decimal)
cleaned['Weight'] = pd.to_numeric(cleaned['Weight'],downcast='float')
#cleaned = df[df['Gender'].isin(['m','f'])][['Gender','Weight','Weight','Plastron']]

### Beeswarm
_ = sns.swarmplot(x='Gender', y='Weight', data=df)
_ = plt.xlabel('Gender')
_ = plt.ylabel('Weight')
_ = plt.show()
