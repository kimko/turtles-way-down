import pandas as pd
import helpers as hlp
import numpy as np

def get_clean_data():
    fileName1 = '/Users/kim/Projects/turtles-way-down/source/Turtle Data.xls'
    fileName2 = '/Users/kim/Projects/turtles-way-down/source/MF Trapping Data.xlsx'
    df = clean_data(fileName1,True)
    df['Capture Location']   = 'Gresham'
    

    df2 = clean_data(fileName2)
    df2['Capture Location']   = 'Mason Flats'
    df2['Source'] = 'MF Trapping Data.xlsx|All Capture Data'
    df = df.append(df2,sort=False)
    
    return df

def clean_data(fileName,big_file=False):
    #columnNames = ['Name','Address']

    print ("Loading data " + fileName)
    df = pd.DataFrame()
    if (big_file):
        for year in range(2008,2014+1):
            print(year)
            new = pd.read_excel(fileName,sheet_name=str(year))
            new['Source'] = '{}|{}'.format('Turtle Data.xls',str(year))
            df = df.append(new,sort=False)
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
    cleaned['Gravid'] = cleaned['Gravid'].apply(hlp.recode_gravid)
    # add features
    cleaned['Age_To_Weight'] = cleaned['Annuli'] / cleaned['Weight']
    buckets = 5
    buckets = int(cleaned['Annuli'].max() / buckets)
    labels = ["{0} - {1}".format(i, i + buckets) for i in range(0, cleaned['Annuli'].max(), buckets)]
    cleaned['Annuli_Group'] = pd.cut(cleaned.Annuli, range(0, cleaned.Annuli.max()+buckets, buckets), right=False, labels=labels)
    # Calcuate Number of recaptures
    df = cleaned[['ID','Date']].groupby('ID').count()
    df.columns = ['recapture_count']
    df.reset_index(inplace=True)
    cleaned = pd.merge(cleaned,df,how='outer',on='ID')

    # recalculate annuli
    df = pd.pivot_table(cleaned[cleaned.Annuli > 0],values=['Date','Annuli'],index=['ID'],aggfunc={'Date': min,'Annuli': min})
    df.columns = ['lowest_annuli','first_date']
    df.reset_index(inplace=True)
    
    cleaned = pd.merge(cleaned,df,how='outer',on='ID')
    cleaned['date_year'] = cleaned.Date.map(lambda x: x.year)
    cleaned['first_date_year'] = cleaned.first_date.map(lambda x: x.year)
    cleaned['new_annuli'] = cleaned.date_year - cleaned.first_date_year + cleaned.lowest_annuli
    cleaned.new_annuli = np.nan_to_num(cleaned.new_annuli)

    # distinguish pregnant females
    cleaned['gender_plus'] = cleaned['Gender']
    cleaned.loc[cleaned.Gravid == True,'gender_plus'] = 'f_gra'
    return cleaned

#natives[['ID','Date','Recapture','recapture_count','Annuli','date_year','first_date_year','lowest_annuli','new_annuli','Gender','Weight','Carapace','Plastron','Source']].set_index('ID').to_clipboard()