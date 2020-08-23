# REQUIRED SECTION
ROOT_DIR:=$(shell git root)
include $(ROOT_DIR)/common/mk/common.mk
# END OF REQUIRED SECTION

.PHONY: help up start stop restart logs status clean lint lint_all

export USER_ID = $(shell id -u)
export GROUP_ID = $(shell id -g)

lint: ## Run lint on all code that has changed in the repo.
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --exit-code-from lint_gi lint_git

lint_all: ## Run lint on all code regardless of if it has changed or not.
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up --exit-code-from lint_all lint_all

up: ## Start all or c=<name> containers in foreground
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c)

start: ## Start all or c=<name> containers in background
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d $(c)

stop: ## Stop all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)

restart: ## Restart all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) stop $(c)
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up $(c) -d

logs: ## Show logs for all or c=<name> containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs --tail=100 -f $(c)

status: ## Show status of containers
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

clean: confirm ## Clean all data
	@$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down
