import pandas as pd

def load_data():
    loans = pd.read_csv("loan_payments.csv", index_col=0)
    return loans

loans = load_data()