"""Concept 2: RAG Triad Architecture (Retrieval vs. Generation).

Decouples the Retriever (Shopper) and Generator (Chef) components
and constructs LLMTestCase instances for independent evaluation.
"""

from typing import Dict, List, Optional
from deepeval.test_case import LLMTestCase


class MockKnowledgeBase:
  """Simulated knowledge base for RAG retrieval context."""

  DOCUMENTS = {
      "enterprise_refund": (
          "Enterprise Tier licenses provide a 45-day refund window from the"
          " contractual signing date. Policy applies to both initial and"
          " renewal contracts."
      ),
      "standard_refund": (
          "Standard Tier licenses provide a 14-day refund window from the date"
          " of purchase."
      ),
      "sso_integration": (
          "Enterprise Tier includes SAML 2.0 and OIDC single sign-on (SSO)"
          " integrations with Okta, Azure AD, and PingIdentity."
      ),
      "rate_limits": (
          "Enterprise Tier API rate limit is set at 10,000 requests per minute."
      ),
  }


class MockRetriever:
  """Shopper: Fetches relevant text chunks based on query."""

  def __init__(self, kb: MockKnowledgeBase):
    self.kb = kb

  def retrieve(self, query: str) -> List[str]:
    query_lower = query.lower()
    results = []
    if "enterprise" in query_lower or "refund" in query_lower:
      results.append(self.kb.DOCUMENTS["enterprise_refund"])
    if "standard" in query_lower:
      results.append(self.kb.DOCUMENTS["standard_refund"])
    if "sso" in query_lower or "saml" in query_lower or "okta" in query_lower:
      results.append(self.kb.DOCUMENTS["sso_integration"])
    if not results:
      results.append(self.kb.DOCUMENTS["enterprise_refund"])
    return results


class MockGenerator:
  """Chef: Generates response using query and retrieved context."""

  def generate(self, query: str, context: List[str]) -> str:
    combined_context = "\n".join(context)
    if "refund window" in query.lower() and "enterprise" in query.lower():
      return (
          "Enterprise Tier licenses have a 45-day refund window from the"
          " signing date."
      )
    elif "sso" in query.lower():
      return (
          "Enterprise Tier supports Okta, Azure AD, and PingIdentity for SSO."
      )
    else:
      return f"Based on the provided information: {combined_context[:100]}..."


class MockRAGPipeline:
  """Full RAG Pipeline assembling Retriever and Generator into LLMTestCase traces."""

  def __init__(self):
    self.kb = MockKnowledgeBase()
    self.retriever = MockRetriever(self.kb)
    self.generator = MockGenerator()

  def run(
      self, query: str, expected_output: Optional[str] = None
  ) -> LLMTestCase:
    # Step 1: Retrieval
    retrieved_context = self.retriever.retrieve(query)

    # Step 2: Generation
    actual_output = self.generator.generate(query, retrieved_context)

    # Step 3: Package into standardized LLMTestCase
    return LLMTestCase(
        input=query,
        actual_output=actual_output,
        retrieval_context=retrieved_context,
        expected_output=expected_output,
    )
