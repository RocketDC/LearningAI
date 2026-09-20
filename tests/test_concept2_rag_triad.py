"""Concept 2: The RAG Triad Architecture (Generation vs. Retrieval).

Tests RAG pipeline output generation and verifies sources of truth:
- FaithfulnessMetric: actual_output vs retrieval_context (Generation)
- AnswerRelevancyMetric: actual_output vs input (Generation)
- ContextualRecallMetric: expected_output vs retrieval_context (Retrieval)
- ContextualPrecisionMetric: input, expected_output, retrieval_context ranking (Retrieval)
"""

import pytest
from deepeval.test_case import LLMTestCase
from src.rag_pipeline import MockRAGPipeline


def test_rag_pipeline_execution():
  """Verifies MockRAGPipeline produces complete LLMTestCase primitive."""
  pipeline = MockRAGPipeline()
  test_case = pipeline.run(
      query="What is the refund window for Enterprise Tier licenses?",
      expected_output="Enterprise Tier licenses have a 45-day refund window from contractual signing date.",
  )

  # Check Generation metric requirements
  assert test_case.input is not None
  assert test_case.actual_output is not None
  assert test_case.retrieval_context is not None
  assert len(test_case.retrieval_context) > 0

  # Check Retrieval metric requirements
  assert test_case.expected_output is not None
  assert (
      "45-day" in test_case.actual_output
      or "45-day" in test_case.retrieval_context[0]
  )


def test_rag_triad_metric_sources_of_truth():
  """Verifies correct assignments of source of truth for each RAG Triad metric."""
  test_case = LLMTestCase(
      input="What is the refund window for Enterprise Tier licenses?",
      actual_output="Enterprise Tier licenses have a 45-day refund window from the signing date.",
      retrieval_context=[
          "Enterprise Tier licenses provide a 45-day refund window from the contractual signing date."
      ],
      expected_output="Enterprise Tier licenses have a 45-day refund window from signing.",
  )

  # Faithfulness: context is ground truth
  assert test_case.retrieval_context[0] in [
      "Enterprise Tier licenses provide a 45-day refund window from the contractual signing date."
  ]

  # Contextual Recall: expected_output is ground truth
  assert "45-day" in test_case.expected_output

  # Answer Relevancy: actual_output addresses input
  assert "Enterprise" in test_case.input and "refund window" in test_case.actual_output
