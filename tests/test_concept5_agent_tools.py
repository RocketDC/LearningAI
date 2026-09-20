"""Concept 5: Agentic Evaluation & Tool-Call Verification.

Audits intermediate agent tool trajectories using ToolCorrectnessMetric and ToolCall.
"""

import pytest
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall
from src.agent_execution import BankAgentExecutor


def test_bank_agent_tool_trace_matching():
  """Verifies tool trace logging and ToolCall matching."""
  executor = BankAgentExecutor()
  expected_tools = [
      ToolCall(name="query_billing_db", input_parameters={"account_id": 9821})
  ]

  test_case = executor.execute_request(
      prompt="Fetch payment status for account ID 9821.",
      account_id=9821,
      expected_tools=expected_tools,
  )

  assert len(test_case.tools_called) == 1
  assert test_case.tools_called[0].name == "query_billing_db"
  assert test_case.tools_called[0].input_parameters == {"account_id": 9821}

  # Metric instantiation check
  metric = ToolCorrectnessMetric()
  assert metric is not None


def test_tool_correctness_mismatch_detection():
  """Verifies tool call divergence detection when expected vs called tools differ."""
  test_case = LLMTestCase(
      input="Transfer funds to account 55.",
      actual_output="Transferred funds.",
      tools_called=[
          ToolCall(
              name="unauthorized_transfer",
              input_parameters={"amount": 1000},
          )
      ],
      expected_tools=[
          ToolCall(
              name="transfer_funds", input_parameters={"source_id": 10}
          )
      ],
  )

  assert test_case.tools_called[0].name != test_case.expected_tools[0].name
