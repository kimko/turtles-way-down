import pandas as pd
import numpy as np

import helpers as hlp

FILE_NAME = "All Site Data oct 2021.xlsx"
SITES = [
    "RamseyLB2021",
    "SB 2021",
    "Gresham",
    "MasonFLO",
    "Whitaker",
    "ElaineSB1999-2001",
]


def get_clean_data():
    df = load_data("source/" + FILE_NAME)
    df = clean_data(df)
    df = new_features(df)
    return df


def load_data(fileName):
    print("Loading data " + fileName)
    df = pd.DataFrame()
    for site in SITES:
        print(site)
        new = pd.read_excel(fileName, sheet_name=site)
        new["Source"] = "{}|{}".format(FILE_NAME, site)
        df = df.append(new, sort=False)
    return df


def clean_data(df):
    """clean data (convert string to decimals, recode categorical data etc etc)
    Original attribute values are maintained in a copy. Eg:
        Weight: cleaned data
        Weight_orig: original data
    """
    # decimals
    print("Cleaning decimals ...")
    df["Weight_orig"] = df.Weight
    df["Weight"] = df["Weight"].apply(hlp.recode_decimal)
    df["Weight"] = pd.to_numeric(df["Weight"], downcast="float")
    df["Carapace_orig"] = df.Carapace
    df["Carapace"] = df["Carapace"].apply(hlp.recode_decimal)
    df["Carapace"] = pd.to_numeric(df["Carapace"], downcast="float")
    df["Plastron_orig"] = df.Plastron
    df["Plastron"] = df["Plastron"].apply(hlp.recode_decimal)
    df["Plastron"] = pd.to_numeric(df["Plastron"], downcast="float")
    df["Annuli_orig"] = df.Annuli
    df["Annuli"] = df["Annuli"].apply(hlp.recode_decimal)
    df["Annuli"] = pd.to_numeric(df["Annuli"], downcast="integer")

    # other
    print("Cleaning other values ...")
    df["Gender_orig"] = df.Gender
    df["Gender"] = df["Gender"].apply(hlp.recode_sex)
    df["Species_orig"] = df.Species
    df["Species"] = df["Species"].apply(hlp.recode_species)
    df["Gravid_orig"] = df.Gravid
    df["Gravid"] = df["Gravid"].apply(hlp.recode_gravid)
    df["Date_orig"] = df.Date
    df["Date"] = pd.to_datetime(df.Date_orig)
    return df


def new_features(df):
    """Add new features to data"""
    print("Add new features ...")
    # distinguish Spring, Fall and pregnant females (don't care about juvenilles/unknown)
    df["gender_plus"] = df["Gender"]
    df.loc[df.Gravid, "gender_plus"] = "f_gra"

    df["gender_seasons"] = df["Gender"]
    df.loc[df.Gravid, "gender_seasons"] = "f_gra"

    # add features
    df["Age_To_Weight"] = df["Annuli"] / df["Weight"]

    # Calcuate Number of recaptures
    df_captures = df[["ID", "Date"]].groupby("ID").count()
    df_captures.columns = ["recapture_count"]
    df_captures.reset_index(inplace=True)
    df = pd.merge(df, df_captures, how="outer", on="ID")

    # recalculate annuli
    df_min = pd.pivot_table(
        df[df.Annuli > 0],
        values=["Date", "Annuli"],
        index=["ID"],
        aggfunc={"Date": min, "Annuli": min},
    )
    df_min.columns = ["annuli_min", "date_min"]
    df_min.reset_index(inplace=True)

    df = pd.merge(df, df_min, how="outer", on="ID")
    df["year"] = df.Date.map(lambda x: x.year)
    df["year_min"] = df.date_min.map(lambda x: x.year)
    df["Annuli_orig"] = df.Annuli
    df.Annuli = df.year - df.year_min + df.annuli_min
    df.Annuli = np.nan_to_num(df.Annuli)
    df["Annuli"] = pd.to_numeric(df["Annuli"], downcast="integer")

    # Annuli Buckets
    buckets = 5
    interval = int(df["Annuli"].max() / buckets)
    buckets = [i for i in range(0, df["Annuli"].max() + interval, interval)]
    labels = ["'{0} - {1}'".format(i, i + interval) for i in buckets]
    df["Annuli_Group"] = pd.cut(
        df.Annuli, buckets, labels=labels[:-1], include_lowest=True
    )

    return df


if __name__ == "__main__":
    print("Loading, cleaning and transforming data...")
    df = get_clean_data()
    df.to_csv("turtles.csv")
    print("Exported to turtles.csv")
