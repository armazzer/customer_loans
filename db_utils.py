import yaml
import pandas as pd
from sqlalchemy import create_engine

def load_credentials():
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
        return credentials

credentials = load_credentials()

class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials
        self.df = pd.DataFrame()

    def read_data(self, conn):
        loan_payments = pd.read_sql_table('loan_payments', conn)
        self.df = loan_payments

    def get_data(self): 
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
        self.df.to_csv("loan_payments.csv")


connector = RDSDatabaseConnector(credentials)
connector.get_data()
connector.make_csv()