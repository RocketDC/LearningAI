"""Concept 1: The LLMTestCase Primitive & Assertion Mechanics.

Tests the core data structure (LLMTestCase) and execution paradigms:
- assert_test(): unit testing in Pytest with halting exceptions.
- evaluate(): dataset-level benchmarking without throwing exceptions.
"""

import pytest
from deepeval import assert_test, evaluate
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase, ToolCall
from src.custom_metrics import ValidJSONMetric


def test_llm_test_case_instantiation():
  """Verifies LLMTestCase primitive attributes."""
  test_case = LLMTestCase(
      input="What is the refund window for Enterprise Tier licenses?",
      actual_output="Enterprise Tier licenses have a 45-day refund window from the signing date.",
      retrieval_context=[
          "Standard Tier licenses provide a 14-day refund window.",
          "Enterprise Tier licenses provide a 45-day refund window from the contractual signing date.",
      ],
      expected_output="Enterprise Tier licenses have a 45-day refund window.",
      tools_called=[
          ToolCall(name="fetch_policy", input_parameters={"tier": "enterprise"})
      ],
      expected_tools=[
          ToolCall(name="fetch_policy", input_parameters={"tier": "enterprise"})
      ],
  )

  assert test_case.input is not None
  assert test_case.actual_output is not None
  assert len(test_case.retrieval_context) == 2
  assert len(test_case.tools_called) == 1
  assert test_case.tools_called[0].name == "fetch_policy"


def test_assert_test_pass():
  """Verifies assert_test() passes cleanly when score >= threshold."""
  test_case = LLMTestCase(
      input="Return user details in JSON format.",
      actual_output='{"user_id": 9821, "status": "active"}',
  )
  metric = ValidJSONMetric(threshold=1.0)
  assert_test(test_case, [metric])


def test_evaluate_dataset_paradigm():
  """Verifies evaluate() processes datasets without halting exceptions."""
  test_cases = [
      LLMTestCase(
          input="Query 1",
          actual_output='{"status": "ok"}',
      ),
      LLMTestCase(
          input="Query 2",
          actual_output='{"status": "pending"}',
      ),
  ]
  metric = ValidJSONMetric(threshold=1.0)

  res = evaluate(test_cases, [metric])
  assert res is not None
