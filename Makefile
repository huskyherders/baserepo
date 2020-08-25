# REQUIRED SECTION
ROOT_DIR:=$(shell git root)
include $(ROOT_DIR)/common/mk/common.mk
# END OF REQUIRED SECTION

.PHONY: lint

export USER_ID = $(shell id -u)
export GROUP_ID = $(shell id -g)

lint: ##@commands-repo Run lint on all code that has changed in the repo.
	@cd lint && make lint

build: ##@commands-build Build target
	@echo "Test"
