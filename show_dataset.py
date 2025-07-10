import pandas as pd

data = 'dataset/bike_fitting_dataset.csv'

#load data into a DataFrame object:
df = pd.read_csv(data)

print(df) 