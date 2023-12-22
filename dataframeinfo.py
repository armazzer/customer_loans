import pandas as pd
# import transformed_data as data

# loans = data.loans

class DataFrameInfo():
    def __init__(self, data):
        self.data = data

    def percent_na(self):
        pd.set_option("display.precision", 2)
        missing_values = ((self.data.isnull().mean()).round(4)) * 100
        missing_values_only = missing_values[missing_values > 0]
        print("Column               Missing values (%) \n", missing_values_only)

    def count_na(self):
         pd.set_option("display.precision", 2)
         missing_count = self.data.isnull().sum()
         missing_count_only = missing_count[missing_count > 0]
         print("Column                Missing values \n", missing_count_only)

    def value_counts_pct(self, column):
        pd.set_option("display.precision", 3)
        pct_value_counts = self.data[column].value_counts()/len(self.data[column].dropna()) * 100
        print("Value              Count(%) \n", pct_value_counts)

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
        num_types = ["int64", "float64"]
        pd.set_option("display.precision", 4)
        mean = round(self.data[column].mean(), 3) if self.data[column].dtypes in num_types else self.data[column].mean()
        median = round(self.data[column].median(), 3) if self.data[column].dtypes in num_types else self.data[column].median()
        mode = round(self.data[column].mode(), 3) if self.data[column].dtypes in num_types else self.data[column].mode()
        stdev = round(self.data[column].std(), 3) if self.data[column].dtypes in num_types else self.data[column].std()
        print(f"{column}: \n mean: {mean} \n median: {median} \n mode: {mode.iloc[0] if len(list(mode)) == 1 else list(mode)} \n standard deviation: {stdev}")
        