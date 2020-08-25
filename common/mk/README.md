# Common Make
Commonly used and repeated Makefile functionality is added here to facilitate easier Makefile
creation for different parts of the project.

## Usage
The make file uses a git alias created by `git config --global --add alias.root '!pwd'`. This can be changed to use `git rev-parse --show-toplevel` instead of `git root` if desired.

Include at the top of a new Makefile:
```
ROOT_DIR:=$(shell git root)
include $(ROOT_DIR)/common/mk/common.mk
```
If the Makefile is being used to control docker-compose services, also add.
```
include $(ROOT_DIR)/common/mk/docker-compose.mk
```

New targets can be added and will automatically be included in the help printout. Any message describing the target can be added immediately after the target with `## DESCRIPTION GOES HERE`. To add it to a group of the help section (or create a new grouping), add @GROUP_NAME immediately after ##, with no spaces. `##@groupName DESCRIPTION_GOES_HERE`

## Reference
Based off of https://github.com/krom/docker-compose-makefile
