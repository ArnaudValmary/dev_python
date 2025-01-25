os_name_n := $(shell uname -s)
os_name   := $(shell if [[ "$(os_name_n)" == "Darwin" ]]; then echo "macOS"; else echo "$(os_name_n)"; fi)
