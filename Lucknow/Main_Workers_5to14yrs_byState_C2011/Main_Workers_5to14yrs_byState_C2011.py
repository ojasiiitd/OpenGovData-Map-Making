# %%
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datagovindia import DataGovIndia
from fuzzywuzzy import fuzz , process

# %%
# To Sync The Data From Source
MY_API_KEY = "579b464db66ec23bdd000001973d3e2bd75e45f07473b608e00799e8"

datagovin = DataGovIndia(MY_API_KEY) # Specify API key if not set as an environment variable
datagovin.sync_metadata(7000 , 20)

# %%
# searching available dataframes by name

def search_datagov(search_term , columns = ['title', 'description']):
    search_data = datagovin.search(search_term)
    # search_data = datagovin.search(search_term , search_fields=columns)

    if len(search_data) > 0:

        search_titles = search_data['title']
        search_id = search_data['resource_id']

        # for res in zip(search_id , search_titles):
        #     print(res)

        return zip(search_id , search_titles)
    
    return "Not Found"

# %%
# getting a resource by ID

def datagov_data(r_id , save=False , filename = ''):
    data = datagovin.get_data(r_id)
    if save:
        data.to_csv(filename, index=False)

    print(data.columns)
    print(data.sample(5))
    return data

# %%
def show_unmerged(df1 , df2 , col):
    # Perform an outer merge
    merged_outer = pd.merge(df1, df2, how='outer', on=col, indicator=True)

    # Filter out rows that were included in the inner merge
    deleted_rows = merged_outer[merged_outer['_merge'] == 'left_only']

    # Print the deleted rows
    print(deleted_rows)


# %%
def get_state_pop(state):
    india_df = pd.read_excel("C:\\Users\\Ojasva Saxena\\Desktop\\Personal\\Maps\\Lucknow\\2011-IndiaState.xlsx")
    
    # print(india_df.columns)

    states_total = india_df[['Name','TRU','TOT_P']][india_df['TRU'] == 'Total']
    states_total = states_total[['Name' , 'TOT_P']]
    
    best_match = process.extract(state, states_total['Name'], limit=1)[0][0]
    print("Matched Value:" , best_match)
    
    return states_total[states_total['Name'] == best_match]['TOT_P'].astype('int32').tolist()[0]

# %%
result = search_datagov("Census 2011")

for x in result:
    print(x)

# %%
# 
data = datagov_data("0130c981-8fd0-4b00-bf95-36e3c2c8708d" , True , "Main_Workers_5to14yrs_byState_C2011.csv") # State-wise Details of main Workers in the Age Group of 5-14 years as per Census 2011 (Ministry of Labour and Employment)

# %%
data.columns = ['sr.no' , 'state' , 'main_workers_5_14']

data = data.drop(data.index[-1])
data['state'] = data['state'].replace('Andhra Pradesh **', 'ANDHRA PRADESH')

data['state'] = data['state'].str.upper()
data['main_workers_5_14'] = data['main_workers_5_14'].astype('int32')

# for i in range(len(data['main_workers_5_14'])):
#     data['main_workers_5_14'][i] = data['main_workers_5_14'][i] / get_state_pop(data['state'][i])

# Calculate the proportion of main workers aged 5-14 relative to state population
data['main_workers_5_14'] = data['main_workers_5_14'] / data['state'].apply(get_state_pop)

data['main_workers_5_14'] = data['main_workers_5_14'] * 100

data

# %%
shp_path =  "C:\\Users\\Ojasva Saxena\\Desktop\\Personal\\Maps\\maps-master\\maps-master\\Survey-of-India-Index-Maps\\stateBoundary\\stateBoundary.shp"
map_gdf = gpd.read_file(shp_path)
map_gdf.sample(5)

# %%
map_gdf['state'] = map_gdf['state'].replace({
'ANDAMAN & NICOBAR':'Andaman & Nicobar Island'.upper(),
'CHANDIGARH':'Andaman & Nicobar Island'.upper(),
'ANDAMAN & NICOBAR':'Andaman & Nicobar Island'.upper(),
'CHANDIGARH':'Chandigarh U.T.'.upper(),
'DADAR & NAGAR HAVELI':'Dadra & Nagar Haveli'.upper(),
'DAMAN & DIU':'Daman & Diu U.T.'.upper(),
'DELHI':'Delhi U.T.'.upper(),
'LAKSHADWEEP':'Lakshadweep UT'.upper(),
'PUDUCHERRY':'Puducherry U.T.'.upper(),
'TELANGANA':'Andhra Pradesh'.upper(),
})

# show_unmerged(map_gdf , data , 'state')

map_data = pd.merge(map_gdf , data , on='state' , how='left')

# %%
sns.set(style="whitegrid")  # Set seaborn style
sns.despine()  # Remove spines

# Create a figure and axis object
ax = map_data.boundary.plot(edgecolor="black" , linewidth=0.6 , figsize=(12,8))
map_data.plot(ax=ax, column='main_workers_5_14' , legend="True" , cmap='PuOr')

# Set plot title and labels
ax.set_title("Percentage of Main Workers - Children (5-14 years) by State \n (Source: Census, 2011) \n (Ministry of Labour and Employment)")
plt.axis("off")

# Save the plot
plt.savefig('Main_Workers_5to14yrs_byState_C2011.png')
plt.show()


# %%
def get_state_pop(state):
    india_df = pd.read_excel("C:\\Users\\Ojasva Saxena\\Desktop\\Personal\\Maps\\Lucknow\\2011-IndiaState.xlsx")
    
    # print(india_df.columns)

    states_total = india_df[['Name','TRU','TOT_P']][india_df['TRU'] == 'Total']
    states_total = states_total[['Name' , 'TOT_P']]
    
    best_match = process.extract(state, states_total['Name'], limit=1)[0][0]
    print("Matched Value:" , best_match)
    
    return states_total[states_total['Name'] == best_match]['TOT_P'].astype('int32').tolist()[0]

# %%



