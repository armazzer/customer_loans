import pandas as pd
import numpy as np
from scipy.stats import boxcox
from scipy.stats import normaltest

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
        self.quantiles_dict = {}
        self.k2_dict = {}

    def k2_calc(self, column):
        data = self.data[column]
        # D’Agostino’s K^2 Test
        stat, p = normaltest(data, nan_policy='omit')
        k2 = round(stat, 2)
        self.k2_dict[column] = k2

    def return_k2(self):
        return self.k2_dict
    
    def calc_corr_matrix(self):
        numeric_cols = self.data.select_dtypes(include=["int64", "float64"])
        correlation_matrix = numeric_cols.corr()
        return correlation_matrix
    
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

    def fill_vals(self, col_nulls, col_ref):
        self.data[col_nulls] = self.data[col_nulls].fillna(self.data[col_ref])

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

    def log_transform_ind_col(self, column):
        log_column = self.data[column].map(lambda x: np.log(x) if x > 0 else 0)
        return log_column

    def quantiles_calc(self, column):
         # Calculate IQR
        num_types = ["int64", "float64"]
        Q1 = round((np.percentile(self.data[column], 25)), 3) if self.data[column].dtypes in num_types else np.percentile(self.data[column], 25)
        Q3 = round((np.percentile(self.data[column], 75)), 3) if self.data[column].dtypes in num_types else np.percentile(self.data[column], 75)
        IQR = round((Q3 - Q1), 3) if self.data[column].dtypes in num_types else Q1 - Q3
        # Calculate Whiskers
        lower_whisker = round((Q1 - 1.5 * IQR), 3) if self.data[column].dtypes in num_types else Q1 - 1.5 * IQR
        upper_whisker = round((Q3 + 1.5 * IQR), 3) if self.data[column].dtypes in num_types else Q1 + 1.5 * IQR
        quantiles_dict_col = {"Q1": Q1, "Q3": Q3, "IQR": IQR, "lower_whisker": lower_whisker, "upper_whisker": upper_whisker}
        self.quantiles_dict[column] = quantiles_dict_col
        if __name__ == "__main__":
            print(f"{column}: {quantiles_dict_col}")

    def show_quantiles(self):
        #print(self.quantiles_dict)
        return(self.quantiles_dict)
    
    def drop_collinear_cols(self):
        collinear_cols = ["funded_amount", "funded_amount_inv", "instalment", "total_payment", "out_prncp_inv", "total_rec_prncp", "collection_recovery_fee"]
        self.data.drop(collinear_cols, axis=1, inplace=True)
    

class DataFrameSliceTransform:
    def __init__(self, data):
        self.data = data.copy()

    def conditional_impute(self, column, condition, value):
        
        conditional_slice = self.data.loc[condition, column]
        self.data.loc[condition, column] = conditional_slice.fillna(value)
        return self
    
    def return_series(self, column):
        return self.data[column]  

# HANDLE MISSING VALUES.
    
# CHANGE THIS SECTION ("LOANS_CLEANING") INTO A FUNCTION WHEN YOU HAVE TIME LATER. 
    
# Create instance of the DataFrameTransform class. 
loans_cleaning = DataFrameTransform(loans)

# Create instance of the DataFrameSliceTransform class.
loans_slice_cleaning = DataFrameSliceTransform(loans)

# Impute missing values in funded_amount, based on values in loan_amount. 
loans_cleaning.fill_vals("funded_amount", "loan_amount")

# WILL TRY DROPPING ALL NULLS IN FUNDED AMOUNT INSTEAD
# loans_cleaning.drop_rows("funded_amount")

# Create condition for slicing term_months.
# condition = loans["total_rec_int"] < 13619.26
# Run impute on term_months slice based on condition of total_rec_int and required value for that condition/slice. Return result as a new series. 
# filled_slice = loans_slice_cleaning.conditional_impute("term_months", condition, 36.0).return_series("term_months")
# Fill all remaining nulls of the new series (filled_slice) with the other value, 60.0.
# filled_slice = filled_slice.fillna(60.0)
# Replace original term_months column with new column.
# loans["term_months"] = filled_slice
loans_cleaning.impute_mode("term_months")

# WILL TRY DROPPING ALL NULLS IN TERM_MONTHS INSTEAD
#loans_cleaning.drop_rows("term_months")

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
    
cols_to_transform_box = ['loan_amount', 'funded_amount', 'funded_amount_inv', 'instalment', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']
cols_to_transform_log = ['annual_inc', 'inq_last_6mths']

def transform_copy(dataframe, columns_box=None, columns_log=None):
    # Create a copy of the dataframe.
    loans_transformed = dataframe.copy()
    # Create new instance of the DataFrameTransform class
    loans_transform = DataFrameTransform(loans_transformed)
    # Box-Cox transform
    # For columns to apply the Box-Cox transformation to:
    # Identify subgroup of columns that contain zeroes.
    zero_cols = dataframe.columns[(dataframe == 0).any()]
    zero_cols = list(zero_cols) # All zero-containing columns in the dataframe.
    cols_add_constant = [col for col in columns_box if col in zero_cols] # Columns for transformation that contain zeroes. 
    # Add constant to zero-containing columns.
    loans_transform.add_constant(cols_add_constant, 1)
    # Run transformation on all required columns.
    for col in columns_box:
        loans_transform.box_cox_transform(col)

    # Log transformation
    for col in columns_log:
        loans_transform.log_transform(col)

    return loans_transformed


def transform_original(dataframe, columns_box=None, columns_log=None):
    # Create a copy of the dataframe.
    loans_transformed = dataframe
    # Create new instance of the DataFrameTransform class
    loans_transform = DataFrameTransform(loans_transformed)
    # Box-Cox transform
    # For columns to apply the Box-Cox transformation to:
    # Identify subgroup of columns that contain zeroes.
    zero_cols = dataframe.columns[(dataframe == 0).any()]
    zero_cols = list(zero_cols) # All zero-containing columns in the dataframe.
    cols_add_constant = [col for col in columns_box if col in zero_cols] # Columns for transformation that contain zeroes. 
    # Add constant to zero-containing columns.
    loans_transform.add_constant(cols_add_constant, 1)
    # Run transformation on all required columns.
    for col in columns_box:
        loans_transform.box_cox_transform(col)

    # Log transformation
    for col in columns_log:
        loans_transform.log_transform(col)


if __name__ == "__main__":
    transform_original(loans, cols_to_transform_box, cols_to_transform_log)
    modified_cols = cols_to_transform_box + cols_to_transform_log
    print(loans[modified_cols].head(4))


# REMOVE OUTLIERS
    
# Below is a very coarse approach, removing all points outside the upper and lower whiskers of box plots, only in columns where the data distribution is relatively normal (K2 test). 
# I wasn't sure how to identify outliners in a more refined way, and pretty much did not have time. 

def true_num_cols(loans):
    all_cols = loans.columns
    non_cat_types = ["int64", "float64", "datetime64[s]"]
    non_cat_cols = [col for col in all_cols if loans[col].dtypes in non_cat_types]
    cols_to_exclude = ["id", "member_id", "policy_code", "application_type", "term_months"]
    true_num_cols = [item for item in non_cat_cols if item not in cols_to_exclude]
    return true_num_cols

def remove_outliers_copy(loans): # "loans" could be any dataframe, was going to take ages to change everything to "dataframe" below.
    # First create instance of the DataFrameTransform class and generate K2 dict.
    columns_to_test = true_num_cols(loans)
    loans_test = DataFrameTransform(loans)
    for col in columns_to_test:
        num_types = ["int64", "float64"]
        if loans[col].dtypes in num_types: 
            loans_test.k2_calc(col)
    loans_k2_dict = loans_test.return_k2()
 
    # Generate list of columns to remove outliers from.
    cols_drop_outliers = [col for col in columns_to_test if "date" not in col and "earliest" not in col and loans_k2_dict[col] < 2000]
    if __name__ == "__main__":
        print(cols_drop_outliers)
        print(len(cols_drop_outliers))
        # cols_drop_outliers = ['loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']

    # Generate quantiles_dict.
    loans_calcs = DataFrameTransform(loans)
    for col in columns_to_test:
        loans_calcs.quantiles_calc(col)
    quantiles_dict = loans_calcs.show_quantiles() # Not sure how/why quantiles_dict is not accessed.
    
    # Copy dataframe.
    loans_copy = loans.copy()
    
    # Remove outliers
    for col in cols_drop_outliers:
        loans_copy = loans_copy[loans_copy[col] >= quantiles_dict[col]["lower_whisker"]]
        loans_copy = loans_copy[loans_copy[col] <= quantiles_dict[col]["upper_whisker"]]

    return loans_copy


def remove_outliers_original(loans): # "loans" could be any dataframe, was going to take ages to change everything to "dataframe" below.
    # First create instance of the DataFrameTransform class and generate K2 dict.
    columns_to_test = true_num_cols(loans)
    loans_test = DataFrameTransform(loans)
    for col in columns_to_test:
        num_types = ["int64", "float64"]
        if loans[col].dtypes in num_types: 
            loans_test.k2_calc(col)
    loans_k2_dict = loans_test.return_k2()
 
    # Generate list of columns to remove outliers from.
    cols_drop_outliers = [col for col in columns_to_test if "date" not in col and "earliest" not in col and loans_k2_dict[col] < 2000]
    if __name__ == "__main__":
        print(cols_drop_outliers)
        print(len(cols_drop_outliers))
        # cols_drop_outliers = ['loan_amount', 'funded_amount', 'funded_amount_inv', 'int_rate', 'instalment', 'annual_inc', 'dti', 'open_accounts', 'total_accounts', 'total_payment', 'total_payment_inv', 'total_rec_prncp', 'total_rec_int', 'last_payment_amount']

    # Generate quantiles_dict.
    loans_calcs = DataFrameTransform(loans)
    for col in columns_to_test:
        loans_calcs.quantiles_calc(col)
    quantiles_dict = loans_calcs.show_quantiles() # DON'T KNNOW WHY/HOW THIS WAS NOT ACCESSED.

     # Assign dataframe.
    loans_no_out = loans        # NOT SURE THIS IS WORKING RIGHT. CONFUSION OVER RETURN STATEMENTS, ETC.  

    # Remove outliers
    for col in cols_drop_outliers:
        loans_no_out = loans_no_out[loans_no_out[col] >= quantiles_dict[col]["lower_whisker"]]
        loans_no_out = loans_no_out[loans_no_out[col] <= quantiles_dict[col]["upper_whisker"]]

    return loans_no_out


# REMOVE COLLINEAR COLUMNS

def drop_collinear(data):
    loans_drop_collinear = DataFrameTransform(data)
    loans_drop_collinear.drop_collinear_cols()
    return data

if __name__ == "__main__":
    loans = remove_outliers_original(loans) # NEED TO CHECK OUTPUT MORE THOROUGHLY, NOT SURE IT'S WORKING RIGHT. 
    loans = drop_collinear(loans)
    print(loans.head())
    loans_plots_updated = plots.Plotter(loans)
    matrix = loans_plots_updated.correlation(14, 8)
    print(type(loans))
    print(loans.shape)
    print(matrix)
    print(loans.info())

