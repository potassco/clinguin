
SETUP_FILE = setup.py
APPLICATION_NAME = clinguin


compile:
	pip uninstall $(APPLICATION_NAME) -y
	python $(SETUP_FILE) install

clean:
	pip uninstall $(APPLICATION_NAME) -y

format:
	autopep8 start.py
	autopep8 clinguin
	pylint start.py
	pylint clinguin


