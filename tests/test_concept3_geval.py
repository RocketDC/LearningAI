"""Concept 3: The G-Eval Framework (Custom LLM-as-a-Judge).

Demonstrates configuring GEval with natural language criteria, evaluation_params,
Auto-CoT evaluation_steps, and score thresholds.
"""

import pytest
from deepeval.metrics import GEval
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
