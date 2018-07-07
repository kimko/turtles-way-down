import pandas as pd
import numpy as np
import os.path
import matplotlib.pyplot as plt
import seaborn as sns
# my custom helper functions
import helpers as hlp

fileName = '/Users/kim/Projects/turtles-way-down/source/Turtle Data.xls'
#columnNames = ['Name','Address']

print ("Loading data " + fileName)
df = pd.DataFrame()
for year in range(2008,2014):
    df = df.append(pd.read_excel(fileName,sheet_name=str(year)),sort=False)


#DATA CLEANING
cleaned = df.copy()
# decimals
print ("Cleaning decimals ...")
cleaned['Weight'] = cleaned['Weight'].apply(hlp.recode_decimal)
cleaned['Weight'] = pd.to_numeric(cleaned['Weight'],downcast='float')
cleaned['Carapace'] = cleaned['Carapace'].apply(hlp.recode_decimal)
cleaned['Carapace'] = pd.to_numeric(cleaned['Carapace'],downcast='float')
cleaned['Plastron'] = cleaned['Plastron'].apply(hlp.recode_decimal)
cleaned['Plastron'] = pd.to_numeric(cleaned['Plastron'],downcast='float')

# other
print ("Cleaning other values ...")
cleaned['Gender'] = cleaned['Gender'].apply(hlp.recode_sex)
cleaned['Species'] = cleaned['Species'].apply(hlp.recode_species)

#filter data: Naitive turle and relevant
print ("Filtering Natives ...")
natives = cleaned.copy()
natives = natives[natives['Weight']!=0]
natives = natives[natives['Carapace']!=0]
natives = natives[natives['Plastron']!=0]
natives = natives[natives['Species']=='Cpb']

### Beeswarm
print ("Plotting Beeswarms Graph ...")
sns.set()
_ = plt.figure(1)
_ = plt.title('Native Tutles Swarmplots')
_ = plt.subplot(2,2,1)
_ = sns.swarmplot(x='Gender', y='Weight', data=natives,size=3)
_ = plt.xlabel('Gender')
_ = plt.ylabel('Weight')

_ =plt.subplot(2,2,2)
_ = sns.swarmplot(x='Gender', y='Carapace', data=natives,size=3)
#_ = plt.xlabel('Gender')
_ = plt.ylabel('Carapace')

_ =plt.subplot(2,2,3)
_ = sns.swarmplot(x='Gender', y='Plastron', data=natives,size=3)
#_ = plt.xlabel('Gender')
_ = plt.ylabel('Plastron')

#_ = plt.show()
#_ = plt.savefig('./analysis/native_swarmPlots.png')

### ECDFs
print ("Plotting Cumulative Distribution Function...")
# Compute ECDFs
x_WeightF, y_WeightF = hlp.ecdf(natives[natives['Gender']=='f']['Weight'])
x_WeightM, y_WeightM = hlp.ecdf(natives[natives['Gender']=='m']['Weight'])

_ = plt.figure(2)
_ = plt.subplot(2,2,1)
_ = plt.title('Weight - Cumulative Distribution')
_ = plt.plot(x_WeightF, y_WeightF, marker='.',linestyle = 'none')
_ = plt.plot(x_WeightM, y_WeightM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Weight (g)')
_ = plt.ylabel('ECDF')

x_CarapaceF, y_CarapaceF = hlp.ecdf(natives[natives['Gender']=='f']['Carapace'])
x_CarapaceM, y_CarapaceM = hlp.ecdf(natives[natives['Gender']=='m']['Carapace'])

_ = plt.subplot(2,2,2)
_ = plt.title('Carapace - Cumulative Distribution')
_ = plt.plot(x_CarapaceF, y_CarapaceF, marker='.',linestyle = 'none')
_ = plt.plot(x_CarapaceM, y_CarapaceM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Carpace (mm)')
_ = plt.ylabel('ECDF')

x_PlastronF, y_PlastronF = hlp.ecdf(natives[natives['Gender']=='f']['Plastron'])
x_PlastronM, y_PlastronM = hlp.ecdf(natives[natives['Gender']=='m']['Plastron'])

_ = plt.subplot(2,2,3)
_ = plt.title('Plastron - Cumulative Distribution')
_ = plt.plot(x_PlastronF, y_PlastronF, marker='.',linestyle = 'none')
_ = plt.plot(x_PlastronM, y_PlastronM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Plastron (mm)')
_ = plt.ylabel('ECDF')

_ = plt.show()
#_ = plt.savefig('./analysis/native_ECDF_Plastron_Plastron.png')

