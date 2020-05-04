""" Utilities functions"""

import os
import csv
import environ

from cride.circles.models import Circle

""" 
	Aux function to load circles from
	a circles csv file located at /app/dummy_data folder
"""
def load_circles(circles_csv_name):
	path = (environ.Path(__file__) - 3).path('dummy_data')
	os.chdir(path)
	with open(circles_csv_name) as circles_file:
		reader = csv.DictReader(circles_file)
		for row in reader:
			circle = Circle(
				name=row['name'],
				slug_name=row['slug_name'],
				is_public=row['is_public'],
				verified=row['verified'],
				members_limit=row['members_limit']
			)
			circle.save()
	print('Circles were loaded succesfully')
