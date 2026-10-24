# Shorter names for the builder's steps. verify/run.sh is the front door, and runs each of these as a stage.
PY ?= python3
SOURCES ?= $(abspath ..)

.PHONY: build check dist verify verify-quick clean

build:
	$(PY) -I build/build_kit.py --sources "$(SOURCES)"

check:
	$(PY) -I build/build_kit.py --check --sources "$(SOURCES)"

dist:
	$(PY) -I build/build_kit.py --zip --sources "$(SOURCES)"

verify:
	SOURCES="$(SOURCES)" bash verify/run.sh

verify-quick:
	SOURCES="$(SOURCES)" bash verify/run.sh --budget quick

clean:
	rm -rf dist .gate-state
