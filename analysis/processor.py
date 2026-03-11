import pandas as pd
from data import storage
from core import engine
database=storage.get_connection()
engine=engine.Catalog(database)


class DataProcessor:
    def __init__(self):
        self.df = None
        self.data = engine
        self.models = {}

    def load_data(self):
        self.df=pd.DataFrame(self.data.get_analytics())
        print(self.df.shape)

    def prepare_features(self):
        self.df.fillna(0,inplace=True)
        self.df["total_demand"]=self.df["units_sold"]+self.df["units_missed"]
        print(self.df["total_demand"])
        self.df["sale_hour"]=pd.to_datetime(self.df["sale_hour"])
        start_time=(min(self.df["sale_hour"]))
        time_difference=self.df["sale_hour"]-start_time
        self.df['time_stamp']=time_difference.dt.total_seconds()/3600




    def train_linear_models(self):
        pass

    def predict_stockout(self, product_id, future_hours=1):
        pass

if __name__ == "__main__":
    processor = DataProcessor()
    print("DataProcessor Scaffold Initialized.")