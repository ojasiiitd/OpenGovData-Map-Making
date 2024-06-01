import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Paths to shapefiles
india_shp = "./India Shapefile With Kashmir/India Shape/india_st.shp"
rivers_shp = "./NRLP/datasets/rivers.shp"

'''
CROP LAT/LONG
# Define the latitude and longitude range
min_lat, max_lat = 26.7, 27
min_lon, max_lon = 80.8, 81

# Crop the shapefile based on the latitude and longitude range
cropped_shapefile = rivers_gdf.cx[min_lon:max_lon, min_lat:max_lat]

# # Save the cropped shapefile
# cropped_shapefile.to_file('cropped_shapefile.shp')
'''


# Read shapefiles into GeoDataFrames
india_gdf = gpd.read_file(india_shp)
rivers_gdf = gpd.read_file(rivers_shp)

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(12, 8))

# Plot India map
sns.set(style="whitegrid")  # Set seaborn style
# sns.despine()  # Remove spines

# Plot India
india_gdf.plot(ax=ax, color='lightyellow', edgecolor='gray', linewidth=0.5)

# Plot rivers
rivers_gdf.plot(ax=ax, color='blue', linewidth=1)

# Set plot title and labels
ax.set_title("Map of India with Rivers", fontsize=16)
ax.set_xlabel("Longitude", fontsize=12)
ax.set_ylabel("Latitude", fontsize=12)

# Show plot
plt.show()
