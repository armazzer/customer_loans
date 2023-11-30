import pandas as pd
import transformed_data as data

loans = data.loans

class DataFrameInfo():
    def __init__(self, data):
        self.data = data

    def percent_na(self):
        pd.set_option("display.precision", 2)
        missing_values = ((self.data.isnull().mean()).round(4)) * 100
        missing_values_only = missing_values[missing_values > 0]
        print("Column               Missing values (%) \n", missing_values_only)

    def shape(self):
        shape = self.data.shape
        print(f"The shape of the dataframe or array is: {shape}")

    def distinct(self, column):
        distinct_cats = list(self.data[column].dropna().unique())
        print("Number of categories (excluding nulls):", len(list(distinct_cats)))
        print("Distinct categories:", *distinct_cats, sep='\n')

    def dtypes(self):
        dtypes = self.data.dtypes
        print("Column                        Data type \n", dtypes)

    def df_summary_stats(self):
        pd.set_option("display.precision", 2)
        df_stats = self.data.dropna().describe()
        print(df_stats)

    def column_summary_stats(self, column):
        pd.set_option("display.precision", 2)
        col_stats = self.data[column].dropna().describe()
        print(col_stats)

    def column_stats(self, column):
        pd.set_option("display.precision", 4)
        mean = round(self.data[column].mean(), 3)
        median = round(self.data[column].median(), 3)
        mode = round(self.data[column].mode(), 3)
        stdev = round(self.data[column].std(), 3)
        print(f"{column}: \n mean: {mean} \n median: {median} \n mode: {mode.iloc[0] if len(list(mode)) == 1 else list(mode)} \n standard deviation: {stdev}")
        