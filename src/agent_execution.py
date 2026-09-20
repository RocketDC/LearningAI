"""Concept 5: Agentic Evaluation & Tool-Call Verification.

Captures tool execution traces with ToolCall and verifies tool selection,
schema parameters, and intermediate steps using ToolCorrectnessMetric.
"""

from typing import Any, Dict, List, Optional
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams


class BankAgentExecutor:
  """Simulated Autonomous Banking Agent that records tool invocation traces."""

  def __init__(self):
    self.tool_catalog = {
        "query_billing_db": self._query_billing_db,
        "transfer_funds": self._transfer_funds,
        "fetch_user_profile": self._fetch_user_profile,
    }

  def _query_billing_db(self, account_id: int) -> Dict[str, Any]:
    return {"account_id": account_id, "status": "PAID", "balance": 1500.00}

  def _transfer_funds(self, source_id: int, dest_id: int, amount: float) -> str:
    return f"Transferred ${amount} from {source_id} to {dest_id}"

  def _fetch_user_profile(self, user_id: int) -> Dict[str, Any]:
    return {"user_id": user_id, "tier": "Enterprise", "email": "user@corp.com"}

  def execute_request(
      self, prompt: str, account_id: int, expected_tools: List[ToolCall]
  ) -> LLMTestCase:
    """Executes prompt, logs tool call parameters, and returns LLMTestCase."""
    tools_called = []

    if "payment status" in prompt.lower() or "billing" in prompt.lower():
      res = self._query_billing_db(account_id)
      tools_called.append(
          ToolCall(
              name="query_billing_db", input_parameters={"account_id": account_id}
          )
      )
      actual_output = (
          f"Account {account_id} payment status is marked as {res['status']}."
      )
    elif "profile" in prompt.lower():
      res = self._fetch_user_profile(account_id)
      tools_called.append(
          ToolCall(
              name="fetch_user_profile", input_parameters={"user_id": account_id}
          )
      )
      actual_output = (
          f"User profile for {account_id} retrieved. Tier: {res['tier']}."
      )
    else:
      actual_output = "No action taken."

    return LLMTestCase(
        input=prompt,
        actual_output=actual_output,
        tools_called=tools_called,
        expected_tools=expected_tools,
    )
