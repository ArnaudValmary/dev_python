
pip_version := $(shell pip --version 2>/dev/null | cut -d ' ' -f 2)

deps_file_pipenv = Pipfile
deps_file_poetry = pyproject.toml

is_pipenv := $(shell if [[ -f "$(deps_file_pipenv)" ]]; then echo yes; else echo no; fi)
is_poetry := $(shell if [[ -f "$(deps_file_poetry)" ]]; then if grep '^\[tool\.poetry\]$$' "$(deps_file_poetry)" >/dev/null 2>&1; then echo yes; else echo no; fi; else echo no; fi)

requirements_file := requirements.txt

ifeq ($(is_poetry),yes)
	cmd_deps_tool             := poetry
	deps_tool_name            := $(ansi_fg_green)$(ansi_bold)Poetry$(ansi_norm)
	deps_tool_version         := $(shell poetry --version 2>/dev/null | cut -d ' ' -f 3)
	path_deps_env             := $(shell $(cmd_deps_tool) env info -p)
	dir_deps_env              := $(lastword $(subst /, ,$(path_deps_env)))
	opt_deps_groups           := $(shell echo '$(deps_groups)' | sed -e 's/ /,/g')
	file_env                  := pyproject.toml
	file_env_lock             := poetry.lock
	cmd_deps_env_remove       := $(cmd_deps_tool) env remove '$(dir_deps_env)'; true
	cmd_deps_lock_remove      := rm --force '$(file_env_lock)'
	cmd_deps_install          := $(cmd_deps_tool) install
	cmd_deps_install_all      := $(cmd_deps_install) --with $(opt_deps_groups)
	cmd_deps_graph            := $(cmd_deps_tool) show --tree
	cmd_deps_graph_all        := $(cmd_deps_graph) --with $(opt_deps_groups)
	cmd_deps_requirements     := $(cmd_deps_tool) export --format=requirements.txt --output=$(requirements_file)
	cmd_deps_requirements_all := $(cmd_deps_requirements) --with $(opt_deps_groups)
else ifeq ($(is_pipenv),yes)
	cmd_deps_tool             := pipenv
	deps_tool_name            := $(ansi_fg_green)$(ansi_bold)Pipenv$(ansi_norm)
	deps_tool_version         := $(shell pipenv --version 2>/dev/null | cut -d ' ' -f 3)
	path_deps_env             := $(shell $(cmd_deps_tool) env info -p)
	dir_deps_env              := $(lastword $(subst /, ,$(path_deps_env)))
	opt_deps_groups           := $(shell echo '$(deps_groups)' | sed -e 's/ /,/g')
	file_env                  := Pipfile
	file_env_lock             := Pipfile.lock
	cmd_deps_install          := $(cmd_deps_tool) install
	cmd_deps_install_all      := $(cmd_deps_tool) install --dev
	cmd_deps_graph            := $(cmd_deps_tool) graph
	cmd_deps_graph_all        := $(cmd_deps_graph)
	cmd_deps_requirements     := $(cmd_deps_tool) requirements
	cmd_deps_requirements_all := $(cmd_deps_requirements)
endif

cmd_deps_run := $(cmd_deps_tool) run
ifeq ($(dir_deps_env),)
	dir_deps_env_print := not defined
else
	dir_deps_env_print := '$(dir_deps_env)'
endif

help_deps:
	@echo "• Dependencies (with $(deps_tool_name) version $(deps_tool_version))"
	@echo "  ⤷ deps_clean       : Clean dependencies environment & files"
	@echo "  ⤷ deps_install     : Install minimal dependencies"
	@echo "  ⤷ deps_install_all : Install all dependencies"
	@echo "  ⤷ graph            : Print graph with minimal dependencies"
	@echo "  ⤷ graph_all        : Print graph with all dependencies"
	@echo "  ⤷ requirements     : Build & print 'requirements.txt' file with minimal dependencies"
	@echo "  ⤷ requirements_all : Build & print 'requirements.txt' file with all dependencies"
	@echo

deps_clean:
	$(cmd_deps_env_remove)
	$(cmd_deps_lock_remove)

deps_install: deps_clean
	$(cmd_deps_install)

deps_install_all: deps_clean
	$(cmd_deps_install_all)

graph:
	$(cmd_deps_graph)

graph_all:
	$(cmd_deps_graph_all)

poetry_install_plugins:
	poetry self add poetry-plugin-export

requirements_clean:
	rm --force "$(requirements_file)"

requirements: requirements_clean
	$(cmd_deps_requirements)

requirements_all: requirements_clean
	$(cmd_deps_requirements_all)

help_targets  := $(help_targets) help_deps
clean_targets := $(clean_targets) clea
targets       := $(targets) deps_clean deps_install deps_install_all graph graph_all poetry_install_plugins requirements_clean requirements requirements_all
