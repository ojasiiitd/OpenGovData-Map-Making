import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import random
from matplotlib.patches import Polygon
from matplotlib.markers import MarkerStyle

def get_largest_n_wards(n , shapefile):
	# Load the shapefile
	lucknow_ward_boundary = shapefile

	# Calculate the area for each polygon and sort by area
	lucknow_ward_boundary['area'] = lucknow_ward_boundary.geometry.area
	lucknow_ward_boundary_sorted = lucknow_ward_boundary.sort_values(by='area', ascending=False)

	largest_polygons = lucknow_ward_boundary_sorted.head(n)

	return largest_polygons['Ward Name'].tolist()


# Paths to shapefiles
lucknow_shp_file = "./ward_boundary/Lucknow Ward Boundary.shp"

# Read shapefiles into GeoDataFrames
lucknow_gdf = gpd.read_file(lucknow_shp_file)

print(lucknow_gdf)
big_wards = get_largest_n_wards(20 , lucknow_gdf)
print(big_wards)

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(12, 8))

# Plot India map
sns.set(style="whitegrid")  # Set seaborn style
sns.despine()  # Remove spines

# # Plot India
lucknow_gdf.plot(ax=ax, cmap = "winter" , edgecolor='white', linewidth=0.6)

# Set plot title and labels
# ax.set_title("Map of Lucknow With Rivers", fontsize=16)
# ax.set_xlabel("Longitude", fontsize=12)
# ax.set_ylabel("Latitude", fontsize=12)

# Annotate all names
for idx, row in lucknow_gdf.iterrows():
	name = row['Ward Name']
	centroid = row.geometry.centroid
	if name in big_wards:
		ax.annotate(name, xy=(centroid.x, centroid.y),
					xytext=(2,-1), textcoords="offset points", fontsize=7, color='black')

	# Place map pin (marker) on centroid
	# ax.plot(centroid.x, centroid.y, marker='v', color='red', markersize=5, markeredgewidth=0, zorder=3)

ax.axis('off')
# Show plot
plt.savefig('figure.png', transparent=True)

plt.show()
