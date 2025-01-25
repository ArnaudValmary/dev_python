
info_help:
	@echo "• Information"
	@echo "  ⤷ info             : Print informations"
	@echo "  ⤷ about            : About this Makefile"
	@echo

info:
	@echo "• OS: $(os_name)"
	@echo "• Deps tool: $(deps_tool_name), version $(deps_tool_version)"
	@echo "  ⤷ Virtualenv directory: $(dir_deps_env_print)"
	@echo "• Docker (version $(docker_version))"
	@echo "• Python (version $(python_version))"
	@echo "• Pip (version $(pip_version))"

help_targets := $(help_targets) info_help
targets      := $(targets) info
