import sys, os, json
from collections import Counter
import constants

def update_modified_time_for_file (file_path):
    
	file_details_dictionary = {}
	file_name = file_path.split('/')[-1]
	
	if os.stat(constants.file_details_file_path).st_size > 0:
		with open(constants.file_details_file_path, 'r') as file_obj:
			file_details_dictionary = json.load(file_obj)
		file_obj.close()

	file_details_dictionary[file_name] = os.stat(file_path).st_mtime

	with open(constants.file_details_file_path, 'w') as file_obj:
		json.dump(file_details_dictionary, file_obj)
	file_obj.close()
	
	return True
	

def is_file_not_modified_since_last_usage (file_path):

	file_name = file_path.split('/')[-1]
	
	file_details_dictionary = {}
	
	if os.stat(constants.file_details_file_path).st_size > 0:
		with open(constants.file_details_file_path, 'r') as file_obj:
			file_details_dictionary = json.load(file_obj)
		file_obj.close()
	
	return file_name in file_details_dictionary and os.stat(file_path).st_mtime == file_details_dictionary[file_name] and os.stat(file_path).st_size > 0
	
def get_cluster_categories_dictionary_from_cached_data():

	cluster_details_dictionary = {}
	
	with open(constants.cached_categories_cluster_file_path, 'r') as file_obj:
			cluster_details_dictionary = json.load(file_obj)
	file_obj.close()
	
	return cluster_details_dictionary
	

def get_all_clustered_categories_for_master_categories(businesses, master_category_keywords):

	if is_file_not_modified_since_last_usage (constants.cached_categories_cluster_file_path) and is_file_not_modified_since_last_usage (constants.business_dataset_path):
		print "Using cached data for getting categories"
		return get_cluster_categories_dictionary_from_cached_data()
		
	else:
		if not is_file_not_modified_since_last_usage (constants.cached_categories_cluster_file_path):
			print "%s is modified since last use" %(constants.cached_categories_cluster_file_path)
		if not is_file_not_modified_since_last_usage (constants.business_dataset_path):
			print "%s is modified since last use" %(constants.business_dataset_path)			
			
		update_modified_time_for_file (constants.business_dataset_path)
		cluster_details_dictionary = cluster_categories_into_master_categories(businesses, master_category_keywords)
		
		with open(constants.cached_categories_cluster_file_path, 'w') as file_obj:
			json.dump(cluster_details_dictionary, file_obj)
		file_obj.close()
		print "Categories cluster cached in %s" %(constants.cached_categories_cluster_file_path)			
		update_modified_time_for_file (constants.cached_categories_cluster_file_path)
		return cluster_details_dictionary
	
	

def get_all_categories_in_sorted_order (businesses):

	tags = []
	for business in businesses:
		for category in business['categories']:
			tags.append(category)
	
	tags_occurances = Counter(tags)	
	tags_occurances_list = sorted(tags_occurances.iteritems(), key = lambda (k, v): (v, k), reverse = True)
	tags = []	
	for row in tags_occurances_list:
		tags.append(row[0])
	
	return tags


def cluster_categories_into_master_categories (businesses, master_category_keywords):

	categories = get_all_categories_in_sorted_order(businesses)
	master_category, main_categories = {}, []
	number_of_categories_processed = 0
	
	for current_category in categories:

		if current_category in master_category_keywords:
			master_category[current_category] = current_category
		else:
			cluster_value_for_current_category = {}		

			for business in businesses:
				if current_category in business['categories']:
					for each_category in business['categories']:
						if each_category in cluster_value_for_current_category and each_category != current_category:
							cluster_value_for_current_category[each_category] = cluster_value_for_current_category[each_category] + 1
						elif each_category != current_category:
							cluster_value_for_current_category[each_category] = 1		

			master_category[current_category] = max(cluster_value_for_current_category.iteritems(), key = lambda (k, v): (v))[0]
			main_categories.append(master_category[current_category])
		
		number_of_categories_processed += 1
		sys.stdout.write("Processed: %d categories\r" % (number_of_categories_processed) )
		sys.stdout.flush()
	
	main_categories = set(main_categories)

	replacement_done = True
	
	print "\nRefining category clusters\n"
	
	while replacement_done:
		replacement_done = False
		for current_category in main_categories:
			my_master_category = master_category[current_category]
			if current_category not in master_category_keywords and my_master_category in master_category_keywords:
				for each_category in master_category:
					if master_category[each_category] == current_category:
						master_category[each_category] = my_master_category
						replacement_done = True		
	for category in master_category:
		if master_category[category] not in master_category_keywords:
			master_category[category] = 'Unknown'
			
	return master_category