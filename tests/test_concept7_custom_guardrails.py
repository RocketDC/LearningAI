"""Concept 7: Deterministic Unit Guardrails & Custom BaseMetric.

Executes low-latency (<5ms), zero-token custom BaseMetric guardrails:
ValidJSONMetric, RegexGuardrailMetric, LatencyCapMetric, BlacklistPIIMetric.
"""

import pytest
from deepeval.test_case import LLMTestCase
from src.custom_metrics import (
    BlacklistPIIMetric,
    LatencyCapMetric,
    RegexGuardrailMetric,
    ValidJSONMetric,
)


def test_valid_json_guardrail():
  metric = ValidJSONMetric(threshold=1.0)

  valid_case = LLMTestCase(
      input="Get JSON", actual_output='{"status": "SUCCESS", "code": 200}'
  )
  assert metric.measure(valid_case) == 1.0
  assert metric.is_successful() is True

  invalid_case = LLMTestCase(input="Get JSON", actual_output="Invalid { JSON")
  assert metric.measure(invalid_case) == 0.0
  assert metric.is_successful() is False


def test_regex_guardrail():
  metric = RegexGuardrailMetric(
      pattern=r"Enterprise Tier.*45-day", threshold=1.0
  )

  valid_case = LLMTestCase(
      input="Policy?",
      actual_output="Enterprise Tier licenses have a 45-day refund window.",
  )
  assert metric.measure(valid_case) == 1.0

  invalid_case = LLMTestCase(
      input="Policy?", actual_output="Standard licenses have a 14-day window."
  )
  assert metric.measure(invalid_case) == 0.0


def test_latency_cap_guardrail():
  metric = LatencyCapMetric(max_latency_ms=200.0)

  fast_case = LLMTestCase(
      input="Prompt", actual_output="Output", completion_time=120.0
  )
  assert metric.measure(fast_case) == 1.0

  slow_case = LLMTestCase(
      input="Prompt", actual_output="Output", completion_time=450.0
  )
  assert metric.measure(slow_case) == 0.0


def test_blacklist_pii_guardrail():
  metric = BlacklistPIIMetric(forbidden_keywords=["api_secret_key"])

  clean_case = LLMTestCase(
      input="Data", actual_output="General public information string."
  )
  assert metric.measure(clean_case) == 1.0

  ssn_leak_case = LLMTestCase(
      input="User info", actual_output="User SSN is 123-45-6789."
  )
  assert metric.measure(ssn_leak_case) == 0.0
  assert "PII pattern match" in metric.reason

  keyword_leak_case = LLMTestCase(
      input="Config", actual_output="Here is api_secret_key=xyz."
  )
  assert metric.measure(keyword_leak_case) == 0.0
  assert "Forbidden keyword found" in metric.reason
