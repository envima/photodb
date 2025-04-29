from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = 'Module to integrate custom YOLO model training. Requires Python>=3.2' 

setup(
	name ='photodb_yolo_object_detection', 
	version ='1.0.0', 
	author ='Noah Just', 
	author_email ='noah.just@geo.uni-marburg.de', 
	url ='https://gitlab.uni-marburg.de/justs/detection-and-segmentation', 
	description ='PhotoDB Object Detection', 
	long_description = long_description, 
	long_description_content_type ="text/markdown", 
	license ='MIT', 
	packages = find_packages(), 
	entry_points ={ 
		'console_scripts': [ 
			'photodb_yolo_reformat = photodb_yolo_object_detection.photodb_yolo_reformat:main',
			'photodb_yolo_train = photodb_yolo_object_detection.photodb_yolo_train:main',
			'photodb_yolo_detect = photodb_yolo_object_detection.photodb_yolo_detect:main'
		] 
	}, 
	classifiers = [ 
		"Programming Language :: Python :: 3", 
		"License :: OSI Approved :: MIT License", 
		"Operating System :: OS Independent", 
	], 
	keywords ='PhotoDB YOLO detection automatic', 
	install_requires = requirements, 
	zip_safe = False
) 
