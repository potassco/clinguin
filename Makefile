SHELL:=/bin/bash
APPLICATION_NAME = clinguin

compile:
	python3 -m pip uninstall $(APPLICATION_NAME) -y
	python3 -m pip install ./

all:
	rm -r clinguin/client/presentation/frontends/angular_frontend/clinguin_angular_frontend
	pushd angular_frontend/; ng build; popd
	mv angular_frontend/dist/clinguin_angular_frontend clinguin/client/presentation/frontends/angular_frontend
	python3 -m pip uninstall $(APPLICATION_NAME) -y
	python3 -m pip install ./[doc]

clean:
	python3 -m pip uninstall $(APPLICATION_NAME) -y

