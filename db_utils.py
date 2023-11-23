import yaml
import pandas as pd
from sqlalchemy import create_engine

def load_credentials():
'''This function reads the credentials file, returning a dictionary'''
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
        return credentials

credentials = load_credentials()

class RDSDatabaseConnector:
    '''This class is used to connect to the RDS database, extract the required data, and save the data in a csv file
        Attributes:
            credentials (dict): a dictionary of credentials required to connect to the RDS database.
            df (dataframe): a dataframe that is initially empty, and will be updated with data extracted from the RDS database.'''
    def __init__(self, credentials):
        self.credentials = credentials
        self.df = pd.DataFrame()

    def read_data(self, conn):
        '''This method reads data from a selected table, given as argument to the read_sql_table function, via the connection established in the get_data method.
        The class attribute df is then updated with the resulting dataframe'''
        loan_payments = pd.read_sql_table('loan_payments', conn)
        self.df = loan_payments

    def get_data(self):
        '''This method creates an engine to establish a connection to the RDS database. 
        The read_data method then runs as a sub-method.''' 
        DATABASE_TYPE = "postgresql"
        DBAPI = "psycopg2"
        HOST = self.credentials["RDS_HOST"]
        USER = self.credentials["RDS_USER"]
        PASSWORD = self.credentials["RDS_PASSWORD"]
        DATABASE = self.credentials["RDS_DATABASE"]
        PORT = self.credentials["RDS_PORT"]
        
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
            self.read_data(conn)

    def make_csv(self):
        '''This method saves the extracted data to a csv file'''
        self.df.to_csv("loan_payments.csv")


connector = RDSDatabaseConnector(credentials)
connector.get_data()
connector.make_csv()