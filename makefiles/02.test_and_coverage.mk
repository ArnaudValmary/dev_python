
cmd_pytest         := pytest --verbose --full-trace -r A
cmd_pytest_xunit   := $(cmd_pytest) --junitxml="$(test_junit_filename)" -o junit_family=xunit1

cmd_test                  := $(cmd_deps_tool) run $(cmd_pytest)
cmd_test_xunit            := $(cmd_deps_tool) run $(cmd_pytest_xunit)

cmd_coverage       := coverage run -m pytest
cmd_coverage_html  := coverage html
cmd_coverage_xunit := pytest \
	--junitxml "$(coverage_junit_filename)" \
	--cov-config="$(coverage_config_filename)" \
	--cov-report "xml:$(coverage_xml_report_filename)"

cmd_coverage_all          := $(cmd_deps_tool) run $(cmd_coverage); $(cmd_deps_tool) run $(cmd_coverage_html)
cmd_coverage_xunit        := $(cmd_deps_tool) run $(cmd_coverage_xunit)

test_junit_filename = ./junit.result.xml

coverage_junit_filename      = ./junit.coverage.xml
coverage_config_filename     = ./.coveragerc
coverage_xml_report_filename = ./coverage.xml
coverage_html_report_dirname = ./htmlcov
coverage_report_filename     = ./.coverage

test_and_coverage_help:
	@echo "• Test & coverage"
	@echo "  ⤷ test_clean       : Clean all test result files"
	@echo "  ⤷ test             : Run test"
	@echo "  ⤷ test_html        : Run test with HTML output"
	@echo "  ⤷ test_xunit       : Run test with Xunit output"
	@echo "  ⤷ coverage         : Run coverage"
	@echo "  ⤷ coverage_html    : Run coverage with HTML output"
	@echo "  ⤷ coverage_open    : Open coverage HTML report"
	@echo "  ⤷ coverage_xunit   : Run coverage with Xunit output"
	@echo

test_clean:
	find . -name "__pycache__" -exec rm --recursive --force '{}' \; 2>/dev/null; true
	rm --recursive --force ./tmp/*

test: test_clean test_xunit_clean coverage_clean coverage_xunit_clean
	$(cmd_test)

test_xunit_clean: test_clean
	rm --force "$(test_junit_filename)"

test_xunit: test_xunit_clean
	$(cmd_test_xunit)

coverage_html_clean: test_clean
	rm --recursive --force "$(coverage_html_report_dirname)"

coverage_html: coverage_html_clean
	$(cmd_coverage_all)

coverage_open: coverage_html
	firefox "$(coverage_html_report_dirname)/index.html"

coverage_xunit_clean: test_clean
	rm --force "$(coverage_report_filename)" "$(coverage_xml_report_filename)" "$(coverage_junit_filename)"

coverage_xunit: coverage_xunit_clean
	$(cmd_coverage_xunit)

help_targets  := $(help_targets) test_and_coverage_help
clean_targets := $(clean_targets) test_clean
targets       := $(targets) test_clean test test_xunit test_xunit_clean coverage_html_clean coverage coverage_open coverage_xunit_clean coverage_xunit
