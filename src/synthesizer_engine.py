"""Concept 4: Synthetic Test Data Generation & Evolution (Synthesizer).

Ingests raw documents and mutates seed queries using Multi-Hop, Reasoning Evolution,
and Constraint Mutation algorithms to generate synthetic goldens.
"""

from typing import Dict, List, Optional
from deepeval.test_case import LLMTestCase


class QueryEvolutionType:
  MULTI_HOP = "multi_hop"
  REASONING = "reasoning_evolution"
  CONSTRAINT = "constraint_mutation"


class MockSynthesizerEngine:
  """Synthetic Data Generator evolving seed prompts into goldens."""

  def __init__(self, documents: Optional[List[str]] = None):
    self.documents = documents or [
        (
            "Enterprise Tier licenses provide a 45-day refund window from"
            " contractual signing date."
        ),
        (
            "Enterprise Tier includes SAML 2.0 and OIDC single sign-on (SSO)"
            " integrations."
        ),
        (
            "Standard Tier licenses provide a 14-day refund window from date of"
            " purchase."
        ),
    ]

  def evolve_query(self, seed_query: str, evolution_type: str) -> str:
    """Mutates a simple seed query using synthetic evolution algorithms."""
    if evolution_type == QueryEvolutionType.MULTI_HOP:
      return f"{seed_query} Also, does this tier include SSO SAML integration?"
    elif evolution_type == QueryEvolutionType.REASONING:
      return f"If a customer signs an Enterprise contract on Jan 1st and requests a refund on Feb 10th, is it eligible under the refund policy? Explain your reasoning."
    elif evolution_type == QueryEvolutionType.CONSTRAINT:
      return f"{seed_query} Provide answer in fewer than 15 words without using the term 'window'."
    return seed_query

  def generate_synthetic_goldens(
      self, seed_queries: List[str]
  ) -> List[LLMTestCase]:
    """Generates synthetic LLMTestCase instances with retrieval context and goldens."""
    goldens = []
    evolutions = [
        QueryEvolutionType.MULTI_HOP,
        QueryEvolutionType.REASONING,
        QueryEvolutionType.CONSTRAINT,
    ]

    for idx, seed in enumerate(seed_queries):
      evo_type = evolutions[idx % len(evolutions)]
      evolved_prompt = self.evolve_query(seed, evo_type)

      goldens.append(
          LLMTestCase(
              input=evolved_prompt,
              actual_output="",  # Populated during model benchmark evaluation
              retrieval_context=self.documents,
              expected_output=(
                  "Synthetic Golden Answer: Grounded response based on"
                  " source documents."
              ),
          )
      )

    return goldens
