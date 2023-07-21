APPLICATION_NAME = clinguin

compile:
	python3 -m pip uninstall $(APPLICATION_NAME) -y
	python3 -m pip install ./

all:
	python3 -m pip uninstall $(APPLICATION_NAME) -y
	python3 -m pip install ./[doc]

clean:
	python3 -m pip uninstall $(APPLICATION_NAME) -y

