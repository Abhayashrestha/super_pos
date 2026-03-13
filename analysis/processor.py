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
        for p_id in self.df["product_id"].unique():
            prod= self.df[self.df["product_id"] == p_id]
            mean_x=prod["time_stamp"].mean()
            mean_y=prod["total_demand"].mean()
            numerator=((prod["time_stamp"]-mean_x)*(prod["total_demand"]-mean_y)).sum()
            denominator=((prod["time_stamp"]-mean_x)**2).sum()
            m=numerator/denominator
            b=mean_y-(m*mean_x)
            self.models={"m":m,"b":b}




    def predict_stockout(self, product_id, future_hours=1):
        pass

if __name__ == "__main__":
    processor = DataProcessor()
    print("DataProcessor Scaffold Initialized.")