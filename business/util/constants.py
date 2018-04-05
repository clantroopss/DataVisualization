import os
from django.conf import settings

project_path			=	settings.BASE_DIR

app_path				=	os.path.join(project_path, "business")

resources_path			=	os.path.join(app_path, "resources")

dataset_path			=	os.path.join(project_path, "business\\data\\yelp")

business_dataset_path	=	os.path.join(dataset_path, "business.json")

checkin_dataset_path	=	os.path.join(dataset_path, "checkin.json")

review_dataset_path		=	os.path.join(dataset_path, "review.json")

tip_dataset_path		=	os.path.join(dataset_path, "tip.json")

user_dataset_path		=	os.path.join(dataset_path, "user.json")

# Cached data contents

cached_data_folder_path	=	os.path.join(resources_path, "cached_data")

file_details_file_path	=	os.path.join(cached_data_folder_path, "file_details.json")

cached_categories_cluster_file_path	=	os.path.join(cached_data_folder_path, "cached_categories_cluster.json")