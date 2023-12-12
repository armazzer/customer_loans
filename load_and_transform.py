import dataframetransform as cleandata

# Load data and assign to variable.
loans = cleandata.loans
columns_box = cleandata.cols_to_transform_box
columns_log = cleandata.cols_to_transform_log

if __name__ == "__main__":
    print(loans.info())
    # List all columns to be transformed.
    modified_cols = columns_box + columns_log
    length = len(modified_cols)
    print(f"List of columns to transform:{modified_cols} \n Number of columns to transform:{length}")
    # Check columns before transformation.
    print(loans[modified_cols].head(4))

# Transform data (remove skew).
cleandata.transform_original(loans, columns_box, columns_log)

if __name__ == "__main__":
    # Check columns after transformation.
    print(loans[modified_cols].head(4))


# Remove outliers.
loans = cleandata.remove_outliers_original(loans)

if __name__ == "__main__":
    print(loans.info())


# Drop collinear columns. 
loans = cleandata.drop_collinear(loans)

if __name__ == "__main__":
    print(loans.info())

