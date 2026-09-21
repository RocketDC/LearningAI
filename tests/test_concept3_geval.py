"""Concept 3: The G-Eval Framework (Custom LLM-as-a-Judge).

Demonstrates configuring GEval with natural language criteria, evaluation_params,
Auto-CoT evaluation_steps, score thresholds, and custom DeepSeek judge models (DeepSeekModel).
"""

import os
import pytest
from deepeval.metrics import GEval
from deepeval.models import DeepSeekModel
from deepeval.test_case import SingleTurnParams


def test_geval_metric_configuration():
  """Verifies GEval metric structure and initialization."""
  geval_metric = GEval(
      name="Schema and Policy Adherence",
      criteria=(
          "Determine whether the agent output strictly adheres to the required"
          " policy and JSON schema without inventing ungrounded attributes."
      ),
      evaluation_params=[
          SingleTurnParams.INPUT,
          SingleTurnParams.ACTUAL_OUTPUT,
      ],
      evaluation_steps=[
          "Check if all mandatory JSON keys are present in actual_output.",
          "Verify that no extra ungrounded keys have been generated.",
          "Ensure numerical values stay within bounded operational ranges.",
      ],
      threshold=0.85,
  )

  assert geval_metric.name == "Schema and Policy Adherence"
  assert geval_metric.threshold == 0.85
  assert len(geval_metric.evaluation_steps) == 3
  assert SingleTurnParams.INPUT in geval_metric.evaluation_params
  assert SingleTurnParams.ACTUAL_OUTPUT in geval_metric.evaluation_params


def test_geval_with_deepseek_model():
  """Verifies binding DeepSeekModel via environment DEEPSEEK_API_KEY as judge for GEval framework."""
  api_key = os.getenv("DEEPSEEK_API_KEY")
  if not api_key:
    pytest.skip("DEEPSEEK_API_KEY environment variable not set")

  deepseek_judge = DeepSeekModel(model="deepseek-chat", api_key=api_key)

  geval_deepseek = GEval(
      name="DeepSeek Policy Judge",
      criteria=(
          "Verify that actual_output provides an accurate refund policy response"
          " without introducing ungrounded claims."
      ),
      evaluation_params=[
          SingleTurnParams.INPUT,
          SingleTurnParams.ACTUAL_OUTPUT,
      ],
      model=deepseek_judge,
      threshold=0.80,
  )

  assert geval_deepseek.name == "DeepSeek Policy Judge"
  assert geval_deepseek.model == deepseek_judge
