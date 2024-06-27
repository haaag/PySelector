# pyselector
# See LICENSE file for copyright and license details.

PYTEST = pytest -v -ra -q

.PHONY: all lint test test-gui test-fzf test-dmenu test-rofi

all: test

test: lint
	@echo '>> Testing'
	$(PYTEST) --ignore=tests/test_fzf.py --ignore=tests/test_dmenu.py --ignore=tests/test_rofi.py
	@echo

test-fzf: lint
	@echo '>> Testing fzf'
	$(PYTEST) tests/test_fzf.py
	@echo

test-dmenu: lint
	@echo '>> Testing dmenu'
	$(PYTEST) tests/test_dmenu.py
	@echo

test-rofi: lint
	@echo '>> Testing rofi'
	$(PYTEST) tests/test_rofi.py
	@echo

test-gui: test-rofi test-dmenu test-fzf
	@echo

lint:
	@echo '>> Linting code'
	@ruff check .
	@codespell .
