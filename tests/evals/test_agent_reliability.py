"""Operational Integration: CI/CD Pytest Automation.

Deterministic unit testing inside tests/evals/test_agent_reliability.py.
Integrates with `deepeval test run` and standard `pytest`.
Halts execution with exit code 1 if assertions fail.
"""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, ToolCall
from src.custom_metrics import BlacklistPIIMetric, ValidJSONMetric


@pytest.fixture
def agent_trace():
  return LLMTestCase(
      input="Query refund window for Enterprise Tier.",
      actual_output="Enterprise licenses have a 45-day refund window.",
      retrieval_context=["Enterprise licenses have a 45-day refund window."],
      tools_called=[
          ToolCall(
              name="fetch_policy", input_parameters={"tier": "enterprise"}
          )
      ],
      expected_tools=[
          ToolCall(
              name="fetch_policy", input_parameters={"tier": "enterprise"}
          )
      ],
  )


def test_agent_reliability_ci_gate(agent_trace):
  """CI/CD unit assertion gate validating deterministic metrics."""
  pii_guard = BlacklistPIIMetric(forbidden_keywords=["secret_token"])

  # assert_test halts immediately with non-zero exit code on failure
  assert_test(agent_trace, [pii_guard])
