import pandas as pd
import numpy as np
from scipy.stats import boxcox

import transformed_data as data
import dataframeinfo as info
import plotter as plots

# Assign data from transformed_data to variable "loans". 
loans = data.loans

if __name__ == "__main__":
    loans_info = info.DataFrameInfo(loans)
    # Show dataframe shape.
    print(loans_info.shape())
    # Show percentage missing values in columns with missing values only.
    print(loans_info.percent_na())
    # Show count of missing values in columns with missing values only.
    print(loans_info.count_na())

    # Create instance of the Plotter class. 
    loans_plots = plots.Plotter(loans)
    # Create heatmap of missing values.
    print(loans_plots.heatmap(18, 14))
    # Create correlation matirx.
    print(loans_plots.correlation(18, 14))


class DataFrameTransform:
    def __init__ (self, data):
        self.data = data

    def calc_corr(self, col_y, col_x):
        correlation = self.data[col_y].corr(self.data[col_x])
        return correlation

    def corr_impute(self, col_y, col_x):
        corr = self.calc_corr(col_y, col_x)    
        def impute(row):
            if pd.isnull(row[col_y]):
                return row[col_x] * corr
            else:
                return row[col_y]
        self.data[col_y] = self.data.apply(impute, axis=1)

    def impute_median(self, column):
        self.data[column] = self.data[column].fillna(self.data[column].median())

    def impute_mode(self, column):       
        def mode():
            mode = self.data[column].mode()
            mode_value = mode.iloc[0]
            return mode_value
        self.data[column] = self.data[column].fillna(mode())

    def drop_rows(self, column):
        self.data.dropna(subset=[column], inplace=True)

    def drop_columns(self, columns):
        self.data = self.data.drop(columns, axis=1, inplace=True)

    def add_constant(self, columns, constant):
        self.data.loc[:, columns] += constant

    def box_cox_transform(self, column):
        transformed_values, lambda_value = boxcox(self.data[column])
        self.data[column] = transformed_values
        if __name__ == "__main__":
            print(lambda_value)

    def log_transform(self, columns):
        self.data[columns] = self.data[columns].map(lambda x: np.log(x) if x > 0 else 0)


class DataFrameSliceTransform:
    def __init__(self, data):
        self.data = data.copy()

    def conditional_impute(self, column, condition, value):
        
        conditional_slice = self.data.loc[condition, column]
        self.data.loc[condition, column] = conditional_slice.fillna(value)
        return self
    
    def return_series(self, column):
        return self.data[column]  


# Create instance of the DataFrameTransform class. 
loans_cleaning = DataFrameTransform(loans)

# Create instance of the DataFrameSliceTransform class.
loans_slice_cleaning = DataFrameSliceTransform(loans)

# Impute missing values in funded_amount, based on correlation with loan_amount. 
loans_cleaning.corr_impute("funded_amount", "loan_amount")

# Create condition for slicing term_months.
condition = loans["total_rec_int"] < 13619.26
# Run impute on term_months slice based on condition of total_rec_int and required value for that coddition/slice. Return result as a new series. 
filled_slice = loans_slice_cleaning.conditional_impute("term_months", condition, 36.0).return_series("term_months")
# Fill all remaining nulls of the new series (filled_slice) with the other value, 60.0.
filled_slice = filled_slice.fillna(60.0)
# Replace original term_months column with new column.
loans["term_months"] = filled_slice

# Impute nulls of int_rate with median. 
loans_cleaning.impute_median("int_rate")

# Impute nulls of employment_min_years with mode.
loans_cleaning.impute_mode("employment_min_years")

# Impute nulls of last_payment_date with mode. 
loans_cleaning.impute_mode("last_payment_date")

# Impute nulls of next_payment_date with mode. 
loans_cleaning.impute_mode("next_payment_date")

# Drop rows where last_credit_pull_date = NaN.
loans_cleaning.drop_rows("last_credit_pull_date")

# Drop rows where collections_12_mths_ex_med = NaN.
loans_cleaning.drop_rows("collections_12_mths_ex_med")

# Drop columns mths_since_last_delinq, mths_since_last_record, mths_since_last_major_derog
loans_cleaning.drop_columns(["mths_since_last_delinq", "mths_since_last_record", "mths_since_last_major_derog"])


if __name__ == "__main__":
    # Create new instance of the DataFrameInfo class.
    loans_cleaned = info.DataFrameInfo(loans)
    # Show dataframe shape.
    print(loans_cleaned.shape())
    # Show percentage missing values in columns with missing values only.
    print(loans_cleaned.percent_na())

    # Create new instance of the Plotter class.
    loans_plots_cleaned = plots.Plotter(loans)
    # Show heatmap of all all data/missing values. 
    print(loans_plots_cleaned.heatmap(14, 10))


# TRANSFORM SKEWED COLUMNS

# Box-Cox transform
# Create a copy of the dataframe.
loans_box_cox = loans.copy()
# Create new instance of the DataFrameTransform class
loans_transform = DataFrameTransform(loans_box_cox)
# List coluns to apply the Box-Cox transformation to.
cols_to_transform = ['loan_amount', 'funded_amount', 'funded_amount_inv', 'instalment', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']
# Identify subgroup of columns that contain zeroes.
zero_cols = loans.columns[(loans == 0).any()]
zero_cols = list(zero_cols) # All zero-containing columns in the dataframe.
cols_add_constant = [col for col in cols_to_transform if col in zero_cols] # Columns for transformation that contain zeroes. 
# Add constant to zero-containing columns.
loans_transform.add_constant(cols_add_constant, 1)
# Run transformation
for col in cols_to_transform:
    loans_transform.box_cox_transform(col)

# Log transformation
loans_transform.log_transform('annual_inc')
loans_transform.log_transform('inq_last_6mths')
