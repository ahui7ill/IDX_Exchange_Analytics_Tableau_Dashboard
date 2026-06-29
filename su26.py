import pandas as pd
import glob
import matplotlib.pyplot as plt

#WK0-1

path = r"C:\Users\ahui4\Downloads\IDX_list_sold"

sold_files = glob.glob(f"{path}\\CRMLSSold*.csv")
list_files = glob.glob(f"{path}\\CRMLSListing*.csv")

def load_csv(file):
    df = pd.read_csv(file)

    # remove last two columns if this is a _filled file
    if file.endswith("_filled.csv"):
        df = df.iloc[:, :-2]

    return df
    
sold_dfs = []
for file in sold_files:
    df = load_csv(file)

    #print(file)
    #print(len(df))

    sold_dfs.append(df)

sold_df = pd.concat(sold_dfs, ignore_index=True)
print(sold_df.shape)

#SOLD ROW COUNT: 634847, SOLD COL COUNT: 82, 

list_dfs = []

for file in list_files:
    df = load_csv(file)

    #print(file)
    #print(len(df))

    list_dfs.append(df)

list_df = pd.concat(list_dfs, ignore_index=True)
print(list_df.shape)

#LIST ROW COUNT: 253318, LIST COL COUNT: 82, 

res_list = list_df[list_df['PropertyType'] == 'Residential']
res_sold = sold_df[sold_df['PropertyType'] == 'Residential']

print(res_list.shape)
print(res_sold.shape)

#AFTER FILTERING
#LIST ROW COUNT: 160384, LIST COL COUNT: 82, 
#SOLD ROW COUNT: 426361, SOLD COL COUNT: 82, 


#WK2

print(res_sold.shape) 
print(res_list.shape) 

print(res_sold.dtypes) 
print(res_list.dtypes) 

print(res_sold['PropertyType'].unique()) 
print(res_list['PropertyType'].unique()) 

missing = pd.DataFrame({"Sold Missing Count": res_sold.isnull().sum(), 
                        "Sold Missing Percent": res_sold.isnull().mean() * 100})

missing = missing.sort_values( "Sold Missing Percent", ascending=False ) 

missing["High Missing"] = (missing["Sold Missing Percent"] > 90)

print(missing)

cols = [ "ClosePrice",  "LivingArea", "DaysOnMarket"]

summary = res_sold[cols].describe(
    percentiles=[0.01,0.05,0.25,0.5,0.75,0.95,0.99]
)

print(summary)

cols_to_drop = missing[missing["High Missing"]].index
filtered_sold = res_sold.drop(columns=cols_to_drop)

print(filtered_sold.shape)



