import pandas as pd
import helpers as hlp

def get_clean_data():
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
    cleaned['Annuli'] = cleaned['Annuli'].apply(hlp.recode_decimal)
    cleaned['Annuli'] = pd.to_numeric(cleaned['Annuli'],downcast='integer')
    cleaned['Age_per_Weight'] = cleaned['Annuli'] / cleaned['Weight']

    # other
    print ("Cleaning other values ...")
    cleaned['Gender'] = cleaned['Gender'].apply(hlp.recode_sex)
    cleaned['Species'] = cleaned['Species'].apply(hlp.recode_species)

    
    return cleaned