import geopandas as gpd

# Load the shapefile
lucknow_ward_boundary = gpd.read_file('./ward_boundary/Lucknow Ward Boundary.shp')

# Calculate the area for each polygon and sort by area
lucknow_ward_boundary['area'] = lucknow_ward_boundary.geometry.area
lucknow_ward_boundary_sorted = lucknow_ward_boundary.sort_values(by='area', ascending=False)

# Get the 25 largest polygons
largest_25_polygons = lucknow_ward_boundary_sorted.head(25)

# Optionally, you can save this subset to a new shapefile
largest_25_polygons.to_file('largest_25_polygons.shp')

# Display the information of the 25 largest polygons
print(largest_25_polygons['Ward Name'])
