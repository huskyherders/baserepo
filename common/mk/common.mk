MK_DIR := $(ROOT_DIR)/common/mk
include $(MK_DIR)/variables.mk
-include .make.env

f ?= $(DOCKER_COMPOSE_FILE)
DOCKER_COMPOSE_FILE := $(f)

.DEFAULT_GOAL := help

help: ##@other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

confirm:
	@( read -p "$(RED)Are you sure? [y/N]$(RESET): " sure && case "$$sure" in [yY]) true;; *) false;; esac )

mk-version: ##@other Show current version of mk-lib
	@echo $(MK_VERSION)
