
SETUP_FILE = setup.py
APPLICATION_NAME = clinguin


compile:
	pip uninstall $(APPLICATION_NAME) -y
	python $(SETUP_FILE) install

clean:
	pip uninstall $(APPLICATION_NAME) -y

