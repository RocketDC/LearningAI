"""Pytest configuration and environment fixtures for DeepEval unit tests."""

import os
import pytest

# Ensure dummy API key is set for offline metric initialization tests
os.environ["OPENAI_API_KEY"] = "mock-api-key-for-testing-12345"
os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"


@pytest.fixture(autouse=True)
def setup_test_env():
  """Automatically sets up mock API key environment for all test runs."""
  os.environ["OPENAI_API_KEY"] = "mock-api-key-for-testing-12345"
  os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"
  yield
