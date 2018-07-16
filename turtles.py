import pandas as pd
import helpers as hlp

def get_clean_data():
    fileName1 = '/Users/kim/Projects/turtles-way-down/source/Turtle Data.xls'
    fileName2 = '/Users/kim/Projects/turtles-way-down/source/MF Trapping Data.xlsx'
    df = clean_data(fileName1,True)
    df['Capture Location']   = 'Gresham'

    df2 = clean_data(fileName2)
    df2['Capture Location']   = 'Mason Flats'

    df = df.append(df2,sort=False)
    
    return df

def clean_data(fileName,big_file=False):
    #columnNames = ['Name','Address']

    print ("Loading data " + fileName)
    df = pd.DataFrame()
    if (big_file):
        for year in range(2008,2014+1):
            print(year)
            df = df.append(pd.read_excel(fileName,sheet_name=str(year)),sort=False)
    else:
        df = pd.read_excel(fileName)


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

    # other
    print ("Cleaning other values ...")
    cleaned['Gender'] = cleaned['Gender'].apply(hlp.recode_sex)
    cleaned['Species'] = cleaned['Species'].apply(hlp.recode_species)

    # add features
    cleaned['Age_To_Weight'] = cleaned['Annuli'] / cleaned['Weight']
    buckets = 5
    buckets = int(cleaned['Annuli'].max() / buckets)
    labels = ["{0} - {1}".format(i, i + buckets) for i in range(0, cleaned['Annuli'].max(), buckets)]
    cleaned['Annuli_Group'] = pd.cut(cleaned.Annuli, range(0, cleaned.Annuli.max()+buckets, buckets), right=False, labels=labels)
    
    return cleaned

