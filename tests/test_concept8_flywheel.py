"""Concept 8: Production Observability, Live Tracing & Continuous Eval Flywheel.

Tests converting user-downvoted production traces into PII-redacted,
deterministic LLMTestCase regression fixtures for CI/CD pipeline integration.
"""

import pytest
from src.production_observability import (
    ProductionTelemetryFlywheel,
    ProductionTrace,
)


def test_flywheel_pii_redaction():
  flywheel = ProductionTelemetryFlywheel()

  raw_prompt = "Customer user@corp.com with SSN 123-45-6789 requested refund."
  redacted = flywheel.redact_pii(raw_prompt)

  assert "[REDACTED_EMAIL]" in redacted
  assert "user@corp.com" not in redacted
  assert "[REDACTED_SSN]" in redacted
  assert "123-45-6789" not in redacted


def test_downvoted_trace_conversion_to_ci_fixture():
  flywheel = ProductionTelemetryFlywheel()

  trace = ProductionTrace(
      trace_id="tr-88912",
      input_prompt="Contact John john.doe@acme.com for enterprise contract.",
      actual_output="Contact info sent to john.doe@acme.com.",
      retrieval_context=["Enterprise contract contact: john.doe@acme.com"],
      user_feedback="thumbs_down",
  )

  fixture = flywheel.evaluate_and_ingest_trace(trace)

  assert fixture is not None
  assert "[REDACTED_EMAIL]" in fixture.input
  assert "john.doe@acme.com" not in fixture.input
  assert len(flywheel.export_regression_suite()) == 1
