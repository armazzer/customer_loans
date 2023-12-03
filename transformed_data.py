import pandas as pd
import numpy as np
from datetime import datetime
import load_data as data

loans = data.loans

class DataTransform:
    def __init__(self, series):
        self.series = series 

    def return_series(self):
        return self.series

    def display_series(self):
        print(self.series.head(3))
        print("Non-null count:", self.series.count())
        return self

    def to_date(self, date_format):
        self.date_format = date_format
        self.series = pd.to_datetime(self.series, format=date_format)
        # Format the result as ISO dates with seconds precision
        self.series = self.series.astype('datetime64[s]')
        return self
    
    def to_timedelta(self):
        int_series = self.series.apply(lambda x: int(x) if not pd.isna(x) else pd.NaT)
        days_in_month = 30
        timedelta_arr = np.where(int_series.notna(), pd.to_timedelta(int_series * days_in_month, unit='D'), pd.NaT)
        timedelta_ser = pd.Series(timedelta_arr)
        self.series = timedelta_ser.astype('timedelta64[s]')
        return self

    def to_category(self):
        self.series = self.series.astype('category')
        return self

    def to_num(self):
        self.series = pd.to_numeric(self.series, errors='coerce')
        return self
    
    def round(self, n):
        self.series = self.series.round(n)
        return self
    
    def to_int(self):
        self.series = self.series.astype('int64')
        return self
    # This will only work if there are no missing values, because the type of NaN is float.

    def split_value(self):
        self.series = self.series.apply(lambda x: x.split()[0] if isinstance(x, str) else x)
        return self
    
    def replace_values(self, replacement_dict):
        self.series = self.series.replace(replacement_dict)
        return self

# Convert series 'grade' to category datatype. 
transform_grade = DataTransform(loans["grade"])
loans["grade_cat"] = transform_grade.to_category().return_series()
loans["grade"] = loans["grade_cat"]
loans = loans.drop(columns=["grade_cat"])

# From series "term": remove 'months' part of string and convert to numeric datatype.
transform_term = DataTransform(loans["term"])
# Create as new column
loans["term_months"] = transform_term.split_value().to_num().round(0).return_series()
# Replace original column
loans["term"] = loans["term_months"]
# Remove redundant column
loans = loans.drop(columns=["term_months"])
# Rename original column
loans.rename(columns={"term": "term_months"}, inplace=True)

# Convert sub_grade from object to category datatype.
subgrade_transform = DataTransform(loans["sub_grade"])
subgrade_cat = subgrade_transform.to_category().return_series()
loans["sub_grade"] = subgrade_cat

# Convert 'employment_length' from object to float datatype. 
# Initially remove "years" from string object, then replace "10+" with "10" and "<"" with "0" ("<"" was originally "< 1 year").
# Finally, convert to numeric. 
# Replace original column and change column name to refect data. 
employment_length_transform = DataTransform(loans["employment_length"])
replacement_dict = {"10+": "10", "<": "0"}
employment_length_years = employment_length_transform.split_value().replace_values(replacement_dict).to_num().return_series()
loans["employment_length"] = employment_length_years
loans.rename(columns={"employment_length": "employment_min_years"}, inplace=True)

# Convert 'home_ownership' from object to category
home_ownership_transform = DataTransform(loans["home_ownership"])
home_ownership_cat = home_ownership_transform.to_category().return_series()
loans["home_ownership"] = home_ownership_cat

# Convert 'issue_date' from object to datetime64, format as date string YYYY-MM
issue_date_transform = DataTransform(loans["issue_date"])
issue_date_iso = issue_date_transform.to_date("%b-%Y").return_series()
loans["issue_date"] = issue_date_iso

# Convert 'payment_plan' from object to category datatype.
payment_plan_transform = DataTransform(loans["payment_plan"])
payment_plan_cat = payment_plan_transform.to_category().return_series()
loans["payment_plan"] = payment_plan_cat

# Convert 'earliest_credit_line' from object to datetime64, format as date string YYYY-MM
earliest_credit_line_transform = DataTransform(loans["earliest_credit_line"])
earliest_credit_line_iso = earliest_credit_line_transform.to_date("%b-%Y").return_series()
loans["earliest_credit_line"] = earliest_credit_line_iso

# Convert 'mths_since_last_delinq' from float to timedelta.
# msld_transform = DataTransform(loans["mths_since_last_delinq"])
# msld_timedelta = msld_transform.to_timedelta().return_series()
# loans["mths_since_last_delinq"] = msld_timedelta

# Convert 'mths_since_last_record' from float to timedelta.
mslr_transform = DataTransform(loans["mths_since_last_record"])
mslr_timedelta = mslr_transform.to_timedelta().return_series()
loans["mths_since_last_record"] = mslr_timedelta

# Convert 'last_payment_date' from object to datetime64[s].
last_payment_date_transform = DataTransform(loans["last_payment_date"])
last_payment_iso = last_payment_date_transform.to_date("%b-%Y").return_series()
loans["last_payment_date"] = last_payment_iso

# Convert 'next_payment_date' from object to datetime64[s].
next_payment_date_transform = DataTransform(loans["next_payment_date"])
next_payment_iso = next_payment_date_transform.to_date("%b-%Y").return_series()
loans["next_payment_date"] = next_payment_iso

# Convert 'last_credit_pull_date' from object to datetime64, format as date string YYYY-MM.
last_credit_pull_date_transform = DataTransform(loans["last_credit_pull_date"])
last_credit_pull_iso = last_credit_pull_date_transform.to_date("%b-%Y").return_series()
loans["last_credit_pull_date"] = last_credit_pull_iso

# Convert 'mths_since_last_major_derog' from float to timedelta.
mslmd_transform = DataTransform(loans["mths_since_last_major_derog"])
mslmd_timedelta = mslmd_transform.to_timedelta().return_series()
loans["mths_since_last_major_derog"] = mslmd_timedelta