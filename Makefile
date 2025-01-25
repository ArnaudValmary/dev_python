
deps_groups = dev

#
# Imports
#

help_targets  := help_base
clean_targets :=
targets       :=

all: help

include ./makefiles/*.mk

#
# Deps tools
#

.PHONY: $(targets) $(clean_targets) $(help_targets)

help_base:
	@echo "Makefile targets available..."
	@echo

help:  $(help_targets)
clean: $(clean_targets)
