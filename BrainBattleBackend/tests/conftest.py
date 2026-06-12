# conftest.py – shared pytest configuration for Brain Battle backend tests
# Place this file in:  BrainBattleBackend/tests/conftest.py

import sys, os

# Ensure BrainBattleBackend package folder is on sys.path for all test files
BACKEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'BrainBattleBackend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, os.path.abspath(BACKEND_DIR))
