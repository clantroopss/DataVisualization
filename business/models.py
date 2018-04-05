from django.db import models
from util.renderJSON import *
from util.cluster_categories import get_all_clustered_categories_for_master_categories
import os

master_category_keywords = ['Restaurants', 'Food', 'Beauty & Spas', 'Bars', 'Nightlife', 'Arts & Entertainment', 'Event Planning & Services', 'Fitness & Instruction', 'Active Life', 'Local Services', 'Professional Services', 'Public Services & Government', 'Financial Services', 'Home Services', 'Auto Repair', 'Automotive', 'Pets', 'Health & Medical', 'Shopping', 'Specialty Schools', 'Hotels & Travel', 'Religious Organizations', 'Unknown']

number_of_cluster_rows = 10
number_of_cluster_columns = 15
businesses = []
category_cluster_group = {}
reviews = {}
users = []

def init_models():
	global businesses
	global category_cluster_group
	global reviews
	global users

	businesses = get_businesses()
	category_cluster_group = get_all_clustered_categories_for_master_categories(businesses, master_category_keywords)
	businesses = sorted(businesses, key=lambda businesses: (businesses['longitude'], businesses['latitude']))

	reviews = get_reviews_index_on_business_id()
    
	print "\n Application ready to go go at localhost:8080 \n"