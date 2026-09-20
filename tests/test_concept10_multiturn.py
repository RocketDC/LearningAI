"""Concept 10: Multi-Turn Conversational Evaluation & Memory Drift.

Audits multi-turn dialogue sessions using ConversationalTestCase to prevent
string concatenation masking intermediate turn failures or memory drift.
"""

import pytest
from deepeval.test_case import ConversationalTestCase, Turn


def test_conversational_test_case_multi_turn():
  turn_1 = Turn(
      role="user",
      content="What is the refund window for Enterprise Tier licenses?",
      retrieval_context=[
          "Enterprise Tier licenses have a 45-day refund window from signing."
      ],
  )

  turn_2 = Turn(
      role="assistant",
      content=(
          "Enterprise Tier licenses have a 45-day refund window from signing."
      ),
  )

  turn_3 = Turn(
      role="user",
      content="Does it apply to renewal contracts?",
      retrieval_context=[
          "Enterprise Tier 45-day refund policy applies to both initial and"
          " renewal contracts."
      ],
  )

  turn_4 = Turn(
      role="assistant",
      content=(
          "Yes, the 45-day refund window applies to renewal contracts as well."
      ),
  )

  convo_test = ConversationalTestCase(
      turns=[turn_1, turn_2, turn_3, turn_4]
  )

  assert len(convo_test.turns) == 4
  assert (
      convo_test.turns[0].content
      == "What is the refund window for Enterprise Tier licenses?"
  )
  assert (
      convo_test.turns[3].content
      == "Yes, the 45-day refund window applies to renewal contracts as well."
  )
