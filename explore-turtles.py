
import numpy as np
import os.path
import matplotlib.pyplot as plt
import seaborn as sns
# my custom helper functions
import helpers as hlp
import turtles

####
#### Hyposis Male grow faster than female
####

#filter data: Naitive turle and relevant
print ("Filtering Natives ...")
natives = turtles.get_clean_data()
natives = natives[natives['Weight']!=0]
natives = natives[natives['Carapace']!=0]
natives = natives[natives['Plastron']!=0]
natives = natives[natives['Species']=='Cpb']

### Beeswarm
print ("Plotting swarm plot ...")
sns.set()
_ = plt.figure(1)
_ = plt.suptitle('Native Tutles Swarmplots ' + str(natives.Weight.count()))
_ = plt.subplot(2,2,1)
_ = sns.swarmplot(x='Gender', y='Weight', data=natives,size=3,color='red')
_ = plt.xlabel('Gender')
_ = plt.ylabel('Weight')

_ =plt.subplot(2,2,2)
_ = sns.swarmplot(x='Gender', y='Carapace', data=natives,size=3)
_ = plt.ylabel('Carapace')

_ =plt.subplot(2,2,3)
_ = sns.swarmplot(x='Gender', y='Plastron', data=natives,size=3)
_ = plt.ylabel('Plastron')

### ECDFs
print ("Plotting Cumulative Distribution Function...")
# Compute ECDFs
x_WeightF, y_WeightF = hlp.ecdf(natives[natives['Gender']=='f']['Weight'])
x_WeightM, y_WeightM = hlp.ecdf(natives[natives['Gender']=='m']['Weight'])

_ = plt.figure(2)
_ = plt.suptitle('Cumulative Distribution ' + str(natives.Weight.count()))
_ = plt.subplot(2,2,1)
_ = plt.plot(x_WeightF, y_WeightF, marker='.',linestyle = 'none')
_ = plt.plot(x_WeightM, y_WeightM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Weight (g)')
_ = plt.ylabel('ECDF')

x_CarapaceF, y_CarapaceF = hlp.ecdf(natives[natives['Gender']=='f']['Carapace'])
x_CarapaceM, y_CarapaceM = hlp.ecdf(natives[natives['Gender']=='m']['Carapace'])

_ = plt.subplot(2,2,2)
_ = plt.plot(x_CarapaceF, y_CarapaceF, marker='.',linestyle = 'none')
_ = plt.plot(x_CarapaceM, y_CarapaceM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Carpace (mm)')
_ = plt.ylabel('ECDF')

x_PlastronF, y_PlastronF = hlp.ecdf(natives[natives['Gender']=='f']['Plastron'])
x_PlastronM, y_PlastronM = hlp.ecdf(natives[natives['Gender']=='m']['Plastron'])

_ = plt.subplot(2,2,3)
_ = plt.plot(x_PlastronF, y_PlastronF, marker='.',linestyle = 'none')
_ = plt.plot(x_PlastronM, y_PlastronM, marker='.',linestyle = 'none')
_ = plt.margins(0.02)
_ = plt.legend(('Female', 'Male'), loc='lower right')
_ = plt.xlabel('Plastron (mm)')
_ = plt.ylabel('ECDF')

## Lineplot Age + Weight, Carapace, Plastron
natives = natives[natives['Annuli']!=0]

### FEMALE
females = natives[natives['Gender']=='f']
print ("Plotting Lineplots for Age + Weight, Carapace and Plastron ...")
sns.reset_orig()
_ = plt.figure(3)
_ = plt.suptitle('Native Females Histogram '  + str(females.Weight.count()))
_ = plt.subplot(2,2,1)
#_ = plt.scatter(females['Annuli'], females['Weight'],s=10)
_ = plt.hist2d(females['Annuli'], females['Weight'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Weight')

_ =plt.subplot(2,2,2)
#_ = plt.scatter(females['Annuli'], females['Carapace'])
_ = plt.hist2d(females['Annuli'], females['Carapace'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Carapace')

_ =plt.subplot(2,2,3)
#_ = plt.scatter(females['Annuli'],females['Plastron'])
_ = plt.hist2d(females['Annuli'], females['Plastron'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Plastron')

### MALES
males = natives[natives['Gender']=='m']
print ("Plotting Lineplots for Age + Weight, Carapace and Plastron ...")
sns.reset_orig()
_ = plt.figure(4)
_ = plt.suptitle('Native Males Histogram '  + str(males.Weight.count()))
_ = plt.subplot(2,2,1)
#_ = plt.scatter(natives['Annuli'], natives['Weight'],s=10)
_ = plt.hist2d(males['Annuli'], males['Weight'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Weight')

_ =plt.subplot(2,2,2)
#_ = plt.scatter(males['Annuli'], males['Carapace'])
_ = plt.hist2d(males['Annuli'], males['Carapace'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Carapace')

_ =plt.subplot(2,2,3)
#_ = plt.scatter(males['Annuli'],males['Plastron'])
_ = plt.hist2d(males['Annuli'], males['Plastron'],cmap='Greens',bins=(10,10))
_ = plt.colorbar()
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Plastron')


### Swarmplot with Hue
print ("Plotting swarm plot with hue ...")
sns.set()
_ = plt.figure(5)
_ = plt.suptitle('Native Tutles Swarmplots with hue by Gender' + str(natives.Weight.count()))
_ = plt.subplot(2,2,1)
_ = sns.swarmplot(x='Annuli', y='Weight', hue='Gender',data=natives,dodge=True,size=4)
_ = plt.xlabel('Annuli')
_ = plt.ylabel('Weight')

_ =plt.subplot(2,2,2)
_ = sns.swarmplot(x='Annuli', y='Carapace', hue='Gender',data=natives,dodge=True,size=4)
_ = plt.ylabel('Carapace')

_ =plt.subplot(2,2,3)
_ = sns.swarmplot(x='Annuli', y='Plastron', hue='Gender',data=natives,dodge=True,size=4)
_ = plt.ylabel('Plastron')

corr = natives[['Gender','Annuli','Weight','Carapace','Plastron']]
corr = corr.corr()
# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

_ = plt.show()
#_ = plt.savefig('./analysis/native_ECDF_Plastron_Plastron.png')