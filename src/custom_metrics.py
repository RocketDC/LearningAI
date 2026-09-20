"""Concept 7: Deterministic Unit Guardrails & Custom BaseMetric.

Zero-cost, low-latency (<5ms) programmatic guardrails created by subclassing
DeepEval's BaseMetric.
"""

import json
import re
from typing import List, Optional
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class ValidJSONMetric(BaseMetric):
  """Guardrail ensuring actual_output is valid JSON."""

  def __init__(self, threshold: float = 1.0):
    self.threshold = threshold
    self.score = 0.0
    self.success = False
    self.reason = ""
    self.async_mode = False

  def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    try:
      json.loads(test_case.actual_output)
      self.score = 1.0
      self.success = True
      self.reason = "Output is valid JSON."
    except Exception as e:
      self.score = 0.0
      self.success = False
      self.reason = f"JSON validation failed: {str(e)}"
    return self.score

  async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    return self.measure(test_case, *args, **kwargs)

  def is_successful(self) -> bool:
    return self.score >= self.threshold

  @property
  def __name__(self):
    return "Valid JSON Guardrail"


class RegexGuardrailMetric(BaseMetric):
  """Guardrail ensuring actual_output matches a required regex pattern."""

  def __init__(self, pattern: str, threshold: float = 1.0):
    self.pattern = pattern
    self.threshold = threshold
    self.score = 0.0
    self.success = False
    self.reason = ""
    self.async_mode = False

  def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    if re.search(self.pattern, test_case.actual_output):
      self.score = 1.0
      self.success = True
      self.reason = f"Output matched regex pattern: '{self.pattern}'."
    else:
      self.score = 0.0
      self.success = False
      self.reason = f"Output failed to match regex pattern: '{self.pattern}'."
    return self.score

  async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    return self.measure(test_case, *args, **kwargs)

  def is_successful(self) -> bool:
    return self.score >= self.threshold

  @property
  def __name__(self):
    return "Regex Guardrail"


class LatencyCapMetric(BaseMetric):
  """Guardrail checking execution latency against a maximum threshold (ms)."""

  def __init__(self, max_latency_ms: float = 500.0, threshold: float = 1.0):
    self.max_latency_ms = max_latency_ms
    self.threshold = threshold
    self.score = 0.0
    self.success = False
    self.reason = ""
    self.async_mode = False

  def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    latency = getattr(test_case, "completion_time", None)
    if latency is None and getattr(test_case, "metadata", None):
      latency = test_case.metadata.get("latency_ms")

    if latency is None:
      self.score = 1.0
      self.success = True
      self.reason = "No latency recorded; passing by default."
      return self.score

    if latency <= self.max_latency_ms:
      self.score = 1.0
      self.success = True
      self.reason = (
          f"Latency {latency:.2f}ms is within cap of {self.max_latency_ms:.2f}ms."
      )
    else:
      self.score = 0.0
      self.success = False
      self.reason = (
          f"Latency {latency:.2f}ms exceeded cap of {self.max_latency_ms:.2f}ms."
      )
    return self.score

  async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    return self.measure(test_case, *args, **kwargs)

  def is_successful(self) -> bool:
    return self.score >= self.threshold

  @property
  def __name__(self):
    return "Latency Cap Guardrail"


class BlacklistPIIMetric(BaseMetric):
  """Guardrail detecting PII or restricted keywords in actual_output."""

  DEFAULT_PATTERNS = [
      r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
      r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
      r"\b(sk-[a-zA-Z0-9]{32,})\b",  # API Key pattern
  ]

  def __init__(
      self,
      forbidden_keywords: Optional[List[str]] = None,
      threshold: float = 1.0,
  ):
    self.forbidden_keywords = forbidden_keywords or []
    self.threshold = threshold
    self.score = 1.0
    self.success = True
    self.reason = "No PII or blacklisted terms detected."
    self.async_mode = False

  def measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    violations = []
    output = test_case.actual_output

    for pattern in self.DEFAULT_PATTERNS:
      if re.search(pattern, output):
        violations.append(f"PII pattern match: {pattern}")

    for kw in self.forbidden_keywords:
      if kw.lower() in output.lower():
        violations.append(f"Forbidden keyword found: '{kw}'")

    if violations:
      self.score = 0.0
      self.success = False
      self.reason = f"PII/Blacklist guardrail failed: {', '.join(violations)}"
    else:
      self.score = 1.0
      self.success = True
      self.reason = "No PII or blacklisted terms detected."

    return self.score

  async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
    return self.measure(test_case, *args, **kwargs)

  def is_successful(self) -> bool:
    return self.score >= self.threshold

  @property
  def __name__(self):
    return "Blacklist PII Guardrail"
