WORKDIR := $(shell pwd)

COMMAND_FOR_RUN=
FILE_NAME=
TEST_PATH=

help: ## Display help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


run_decision_tree: FILE_NAME=src/katas/decission_tree/main.py
run_decision_tree: run_script ## Run decission tree kata

run_notebook: run_container ## Run notebook on port

run_test: COMMAND_FOR_RUN=pytest ./tests/$(TEST_PATH)
run_test: run_container ## Run tests.  Use TEST_PATH for set file name (root of the test placed in the tests dir)

run_script: COMMAND_FOR_RUN=python $(FILE_NAME)
run_script: run_container

run_container: .build/image
	echo  $(COMMAND_FOR_RUN)
	docker run -it -p 80:8888  \
	-v $(WORKDIR):/home/jovyan/work/ \
	ds_kata:latest $(COMMAND_FOR_RUN)


.build/image: .build Dockerfile requirements.txt
	docker build -t ds_kata:latest -f Dockerfile .
	touch $@

.build:
	mkdir .build
