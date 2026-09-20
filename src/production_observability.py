"""Concept 8: Production Observability, Live Tracing & Continuous Eval Flywheel.

Implements Tiered Telemetry and automatic conversion of production anomalies
(downvotes or low quality metric scores) into deterministic LLMTestCase regression fixtures.
"""

import json
import re
from typing import Any, Dict, List, Optional
from deepeval.test_case import LLMTestCase
from .custom_metrics import BlacklistPIIMetric, ValidJSONMetric


class ProductionTrace:
  """Telemetry trace recording live user interaction."""

  def __init__(
      self,
      trace_id: str,
      input_prompt: str,
      actual_output: str,
      retrieval_context: List[str],
      user_feedback: Optional[str] = None,  # "thumbs_down", "thumbs_up"
      latency_ms: float = 120.0,
  ):
    self.trace_id = trace_id
    self.input_prompt = input_prompt
    self.actual_output = actual_output
    self.retrieval_context = retrieval_context
    self.user_feedback = user_feedback
    self.latency_ms = latency_ms


class ProductionTelemetryFlywheel:
  """Continuous Eval Flywheel manager processing 3-Tier production telemetry."""

  def __init__(self):
    self.pii_filter = BlacklistPIIMetric()
    self.anomalous_fixtures: List[LLMTestCase] = []

  def redact_pii(self, text: str) -> str:
    """Sanitizes PII from production trace text before converting to test fixture."""
    # Redact email addresses
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "[REDACTED_EMAIL]",
        text,
    )
    # Redact SSNs
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
    return text

  def process_tier1_heuristics(self, trace: ProductionTrace) -> bool:
    """Tier 1: 100% real-time deterministic checks."""
    test_case = LLMTestCase(
        input=trace.input_prompt, actual_output=trace.actual_output
    )
    score = self.pii_filter.measure(test_case)
    return score == 1.0

  def evaluate_and_ingest_trace(self, trace: ProductionTrace) -> Optional[LLMTestCase]:
    """Tier 3: Audits 100% of user-downvoted traces & converts to regression fixture."""
    is_anomaly = False

    # Check for negative user feedback
    if trace.user_feedback == "thumbs_down":
      is_anomaly = True

    # Check Tier 1 heuristic failure
    if not self.process_tier1_heuristics(trace):
      is_anomaly = True

    if is_anomaly:
      # PII Redaction & Sanitization
      sanitized_input = self.redact_pii(trace.input_prompt)
      sanitized_output = self.redact_pii(trace.actual_output)
      sanitized_context = [
          self.redact_pii(c) for c in trace.retrieval_context
      ]

      fixture = LLMTestCase(
          input=sanitized_input,
          actual_output=sanitized_output,
          retrieval_context=sanitized_context,
          expected_output="[GOLDEN_REFERENCE_REQUIRED]",
      )
      self.anomalous_fixtures.append(fixture)
      return fixture

    return None

  def export_regression_suite(self) -> List[LLMTestCase]:
    """Returns all ingested regression fixtures for CI pipeline execution."""
    return self.anomalous_fixtures
