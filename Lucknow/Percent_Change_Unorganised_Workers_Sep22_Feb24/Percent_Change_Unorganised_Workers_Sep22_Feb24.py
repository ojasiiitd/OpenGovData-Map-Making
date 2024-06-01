# %%
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datagovindia import DataGovIndia
from fuzzywuzzy import process

# %%
# To Sync The Data From Source
MY_API_KEY = "579b464db66ec23bdd000001973d3e2bd75e45f07473b608e00799e8"

datagovin = DataGovIndia(MY_API_KEY) # Specify API key if not set as an environment variable
# datagovin.sync_metadata(7000 , 20)

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
def standardize_states(state):
    india_df = pd.read_csv("C:\\Users\\Ojasva Saxena\\Desktop\\Personal\\Maps\\Lucknow\\Unorganised_Workers_e-Shram_byStateFeb24.csv")
    
    # print(india_df.columns)

    states_total = india_df[['state_ut']]

    states_total['state_ut'] = states_total['state_ut'].str.upper()
 
    best_match = process.extract(state.upper(), states_total['state_ut'], limit=1)[0][0]
    print("Matched Value:" , best_match)
    
    return best_match

# %%
result = search_datagov("unorganised")

for x in result:
    print(x)

# %%
# b3fe933d-908d-44e7-8d94-a4a37c7b2c3d - 'State/UT-wise Number of Unorganised Workers Registered on e-Shram Portal as on 31-01-2024
data1 = datagov_data("b3fe933d-908d-44e7-8d94-a4a37c7b2c3d" , True , "Unorganised_Workers_e-Shram_byStateFeb24.csv") # State/UT-wise Number of Unorganised Workers Registered on e-Shram Portal as on 31-01-2024

# 3b3af246-e617-4b33-82f8-2476be24023c - 'State/UT wise number of registrations of unorganised workers as on 25-09-2022
data2 = datagov_data("3b3af246-e617-4b33-82f8-2476be24023c" , True , "Unorganised_Workers_Registered_byStateSep22.csv") # State/UT wise number of registrations of unorganised workers as on 25-09-2022

# %%
data1.columns = ['state no.' , 'state' , 'resgistered_unorganised_feb24']

data2.drop('last_updated' , axis=1 , inplace=True)
data2.columns = ['state no.' , 'state' , 'resgistered_unorganised_sep22']

data1.drop('state no.' , axis=1 , inplace=True)
data2.drop('state no.' , axis=1 , inplace=True)

data1 = data1.drop(data1.index[-1])

data1['resgistered_unorganised_feb24'] = data1['resgistered_unorganised_feb24'].astype('int32')
data2['resgistered_unorganised_sep22'] = data2['resgistered_unorganised_sep22'].astype('int32')

standardized_states1 = []

# Iterate over each state name in the 'state' column
for state in data1['state']:
    # Apply the standardize_states function to the state name and append the result to the list
    standardized_state = standardize_states(state)
    standardized_states1.append(standardized_state)

# Replace the 'state' column with the standardized state names
data1['state'] = standardized_states1

standardized_states2 = []

# Iterate over each state name in the 'state' column
for state in data2['state']:
    # Apply the standardize_states function to the state name and append the result to the list
    standardized_state = standardize_states(state)
    standardized_states2.append(standardized_state)

# Replace the 'state' column with the standardized state names
data2['state'] = standardized_states2


# %%
data_diff = pd.merge(data1 , data2 , how="inner" , on="state")

data_diff["change"] = ( (data_diff['resgistered_unorganised_feb24'] - data_diff['resgistered_unorganised_sep22']) / (data_diff['resgistered_unorganised_sep22']) ) * 100

data_diff

# %%
shp_path =  "C:\\Users\\Ojasva Saxena\\Desktop\\Personal\\Maps\\maps-master\\maps-master\\Survey-of-India-Index-Maps\\stateBoundary\\stateBoundary.shp"
map_gdf = gpd.read_file(shp_path)

map_gdf.columns = ['state' , 'geometry']

standardized_states = []

# Iterate over each state name in the 'state' column
for state in map_gdf['state']:
    # Apply the standardize_states function to the state name and append the result to the list
    standardized_state = standardize_states(state)
    standardized_states.append(standardized_state)

# Replace the 'state' column with the standardized state names
map_gdf['state'] = standardized_states

map_gdf

# %%
map_data = pd.merge(map_gdf , data_diff , how='left' , on="state")

# %%
sns.set(style="whitegrid")  # Set seaborn style
sns.despine()  # Remove spines

# Create a figure and axis object
ax = map_data.boundary.plot(edgecolor="black" , linewidth=0.6 , figsize=(12,8))
map_data.plot(ax=ax, column='change' , legend="True" , cmap='YlGnBu')

for idx, row in map_data.iterrows():
	if row['change'] > 0:
	    change = "+" + str(round(row['change'] , 1))
	else:
	    change = "-" + str(round(row['change'] , 1))

	centroid = row.geometry.centroid
	ax.annotate(change, xy=(centroid.x, centroid.y), xytext=(0,0), textcoords="offset points", fontsize=9, color='darkred',fontfamily='serif')


# Set plot title and labels
# ax.set_title("Percentage Change in Number of Unorganised Workers Registered \n Sept '22 to Feb '24")
ax.set_title("पंजीकृत असंगठित श्रमिकों की संख्या में प्रतिशत परिवर्तन\n सितम्बर '22 - फ़रवरी '24")
plt.axis("off")

# Save the plot
# plt.savefig('Percent_Change_Unorganised_Workers_Sep22_Feb24.png')
plt.savefig('Percent_Change_Unorganised_Workers_Sep22_Feb24_Hindi.png')
plt.show()

# %%



