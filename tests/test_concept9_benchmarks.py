"""Concept 9: Model Benchmarking, Evaluation Datasets & Trade-Offs.

Demonstrates versioned EvaluationDataset instantiation and Pareto frontier benchmarking.
"""

import pytest
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase


def test_evaluation_dataset_instantiation():
  test_case_1 = LLMTestCase(
      input="Refund policy for Enterprise?",
      actual_output="45-day window.",
      expected_output="45-day window from signing.",
  )
  test_case_2 = LLMTestCase(
      input="SSO support for Enterprise?",
      actual_output="Supports SAML 2.0 and OIDC.",
      expected_output="Supports SAML 2.0 and OIDC.",
  )

  dataset = EvaluationDataset()
  dataset.add_test_case(test_case_1)
  dataset.add_test_case(test_case_2)

  assert len(dataset.test_cases) == 2
  assert dataset.test_cases[0].input == "Refund policy for Enterprise?"
  assert dataset.test_cases[1].expected_output == "Supports SAML 2.0 and OIDC."
