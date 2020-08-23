# REQUIRED SECTION
ROOT_DIR:=$(shell git root)
include $(ROOT_DIR)/common/mk/common.mk
include $(ROOT_DIR)/common/mk/docker-compose.mk
# END OF REQUIRED SECTION

.PHONY: lint lint_all

export USER_ID = $(shell id -u)
export GROUP_ID = $(shell id -g)

lint: ## Run lint on all code that has changed in the repo.
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --exit-code-from lint_git lint_git

lintAll: ## Run lint on all code regardless of if it has changed or not.
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --exit-code-from lint_all lint_all
