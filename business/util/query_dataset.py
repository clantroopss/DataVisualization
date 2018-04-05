import time
from util import get_business_index_for_longitude
from business.models import master_category_keywords, category_cluster_group

def does_categories_fall_in_filtered_categories(categories, filtered_categories):

	if len(filtered_categories) == len(master_category_keywords)-1:
		return True
	else:
		for category in categories:
			if category_cluster_group[category] in filtered_categories:
				return True;
	return False
	

def get_clustered_businesses_within_location(businesses, location_dictionary, number_of_cluster_rows, number_of_cluster_columns, businesses_in_category, rating_range_string, price_range_string, should_include_non_priced_businesses):

	
	start_time = time.time()
	
	rating_low = float(rating_range_string.split("-")[0])
	rating_high = float(rating_range_string.split("-")[1])
	
	price_low = int(price_range_string.split("-")[0])
	price_high = int(price_range_string.split("-")[1])
	
	clustered_businesses = [ [ [] for i in range(number_of_cluster_columns) ] for j in range(number_of_cluster_rows) ]	
	latitude_step_size = (location_dictionary['north'] - location_dictionary['south']) / number_of_cluster_rows
	longitude_step_size = (location_dictionary['east'] - location_dictionary['west']) / number_of_cluster_columns
	
	current_index = get_business_index_for_longitude (businesses, location_dictionary['west'])

	while current_index < len(businesses):
		business = businesses[current_index]
		cluster_row_for_business, cluster_column_for_business = int((business['latitude']-location_dictionary['south'])/latitude_step_size), int((business['longitude']-location_dictionary['west'])/longitude_step_size)
		
		if 0 <= cluster_column_for_business < number_of_cluster_columns:
			if 0 <= cluster_row_for_business < number_of_cluster_rows:
			
			
				if rating_low <= business['stars'] <= rating_high:
				
					if does_categories_fall_in_filtered_categories(business['categories'], businesses_in_category):
					
						if should_include_non_priced_businesses:
							if 'Price Range' not in business['attributes']:
								clustered_businesses[cluster_row_for_business][cluster_column_for_business].append(business)
								is_added = True
							
						if 'Price Range' in business['attributes'] and price_low <= business['attributes']['Price Range'] <= price_high:
							clustered_businesses[cluster_row_for_business][cluster_column_for_business].append(business)
							is_added = True
		else:
			break
		current_index += 1

	result_size = 0
	
	for lat_index in range(number_of_cluster_rows):
		for long_index in range(number_of_cluster_columns):
			result_size += len(clustered_businesses[lat_index][long_index])
	
	return clustered_businesses