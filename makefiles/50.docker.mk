docker_version := $(shell docker --version 2>/dev/null | cut -d ' ' -f 3 | tr -d ,)
