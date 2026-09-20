"""Generates the DeepEval 10-Concept Enterprise Reference Guide PDF."""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class NumberedCanvas(canvas.Canvas):
  """Two-pass canvas to dynamically compute and draw 'Page X of Y' page numbers."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._saved_page_states = []

  def showPage(self):
    self._saved_page_states.append(dict(self.__dict__))
    self._startPage()

  def save(self):
    num_pages = len(self._saved_page_states)
    for state in self._saved_page_states:
      self.__dict__.update(state)
      self.draw_decorations(num_pages)
      super().showPage()
    super().save()

  def draw_decorations(self, page_count):
    self.saveState()
    self.setFont("Helvetica", 8)
    self.setFillColor(colors.HexColor("#64748b"))

    # Running header on pages > 1
    if self._pageNumber > 1:
      self.drawString(
          36,
          762,
          "DeepEval Enterprise Architecture Reference - 10 Foundational"
          " Concepts",
      )
      self.setStrokeColor(colors.HexColor("#cbd5e1"))
      self.setLineWidth(0.5)
      self.line(36, 756, 576, 756)

    # Running footer on all pages
    page_text = f"Page {self._pageNumber} of {page_count}"
    self.drawRightString(576, 25, page_text)
    self.drawString(
        36,
        25,
        "STRICTLY FOR RELIABILITY ENGINEERING & CI/CD VERIFICATION USE",
    )
    self.setStrokeColor(colors.HexColor("#cbd5e1"))
    self.setLineWidth(0.5)
    self.line(36, 35, 576, 35)
    self.restoreState()


def build_deepeval_pdf(
    output_filename="deepeval_10_concepts_mastery_guide.pdf",
):
  doc = SimpleDocTemplate(
      output_filename,
      pagesize=letter,
      leftMargin=36,
      rightMargin=36,
      topMargin=45,
      bottomMargin=45,
  )

  styles = getSampleStyleSheet()

  # Custom typography hierarchy
  title_style = ParagraphStyle(
      "DocTitle",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=22,
      leading=26,
      textColor=colors.HexColor("#0f172a"),
  )
  subtitle_style = ParagraphStyle(
      "DocSubTitle",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=11,
      leading=15,
      textColor=colors.HexColor("#475569"),
  )
  h1_style = ParagraphStyle(
      "Heading1_Custom",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=13,
      leading=17,
      textColor=colors.HexColor("#0f172a"),
      spaceBefore=12,
      spaceAfter=4,
      keepWithNext=True,
  )
  h2_style = ParagraphStyle(
      "Heading2_Custom",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=10,
      leading=13,
      textColor=colors.HexColor("#0369a1"),
      spaceBefore=6,
      spaceAfter=2,
      keepWithNext=True,
  )
  body_style = ParagraphStyle(
      "Body_Custom",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=9,
      leading=12.5,
      textColor=colors.HexColor("#334155"),
      spaceAfter=4,
  )
  code_style = ParagraphStyle(
      "Code_Custom",
      parent=styles["Normal"],
      fontName="Courier",
      fontSize=8,
      leading=10.5,
      textColor=colors.HexColor("#0f172a"),
  )
  table_header_style = ParagraphStyle(
      "TableHeader",
      parent=styles["Normal"],
      fontName="Helvetica-Bold",
      fontSize=8,
      leading=10.5,
      textColor=colors.white,
  )
  table_cell_style = ParagraphStyle(
      "TableCell",
      parent=styles["Normal"],
      fontName="Helvetica",
      fontSize=7.5,
      leading=9.5,
      textColor=colors.HexColor("#1e293b"),
  )

  story = []

  # Title Banner
  story.append(
      Paragraph(
          "DeepEval Mastery: The 10-Concept Enterprise Reference", title_style
      )
  )
  story.append(
      Paragraph(
          "Comprehensive Architecture Cheat Sheet for AI Agent & Reliability"
          " Engineers",
          subtitle_style,
      )
  )
  story.append(Spacer(1, 8))
  story.append(
      HRFlowable(
          width="100%",
          thickness=1.5,
          color=colors.HexColor("#0284c7"),
          spaceBefore=2,
          spaceAfter=8,
      )
  )

  # Concept 1
  story.append(
      Paragraph(
          "Concept 1: The LLMTestCase Primitive & Assertion Mechanics", h1_style
      )
  )
  story.append(
      Paragraph(
          "<b>LLMTestCase</b> encapsulates test data: <b>input</b> (user"
          " query), <b>actual_output</b> (LLM response), <b>retrieval_context</b>"
          " (RAG chunks), <b>expected_output</b> (golden truth), and"
          " <b>tools_called</b> / <b>expected_tools</b> (agent tool execution"
          " traces).<br/>"
          "<b>assert_test()</b> halts immediately with <code>AssertionError</code>"
          " (exit code 1) on metric failure for CI gates. <b>evaluate()</b> runs"
          " across entire datasets without throwing exceptions, outputting"
          " macro telemetry.",
          body_style,
      )
  )

  # Concept 2
  story.append(
      Paragraph(
          "Concept 2: The RAG Triad (Generation vs. Retrieval Metrics)", h1_style
      )
  )
  story.append(
      Paragraph(
          "Decouples evaluation between the <b>Retriever (Shopper)</b> and the"
          " <b>Generator (Chef)</b>:<br/>"
          "• <b>FaithfulnessMetric:</b> Measures hallucination (actual_output"
          " verified strictly against retrieval_context). Ground truth ="
          " retrieval_context.<br/>"
          "• <b>AnswerRelevancyMetric:</b> Evaluates if actual_output addresses"
          " input without topic drift.<br/>"
          "• <b>ContextualRecallMetric:</b> Measures retrieval completeness"
          " (facts in expected_output found in retrieval_context). Completely"
          " ignores actual_output.<br/>"
          "• <b>ContextualPrecisionMetric:</b> Evaluates retrieval ranking."
          " Penalizes irrelevant chunks outranking relevant ones, mitigating"
          " the <i>'Lost in the Middle'</i> attention degradation effect.",
          body_style,
      )
  )

  # Concept 3
  story.append(
      Paragraph(
          "Concept 3: The G-Eval Framework (Custom LLM-as-a-Judge)", h1_style
      )
  )
  story.append(
      Paragraph(
          "Replaces arbitrary integer (1-5) prompting with a two-phase engine:"
          " <b>Auto-CoT Step Generation</b> (synthesizing structured evaluation"
          " steps from criteria) and <b>Probability Normalization</b> (measuring"
          " score token log probabilities to calculate expected value: Score ="
          " Σ i × P(Score = i)). Drastically eliminates integer scoring bias"
          " and flakiness.",
          body_style,
      )
  )

  # Concept 4
  story.append(
      Paragraph(
          "Concept 4: Synthetic Data Generation & Evolution (Synthesizer)",
          h1_style,
      )
  )
  story.append(
      Paragraph(
          "Solves golden dataset cold-starts by parsing raw knowledge documents"
          " and mutating seed prompts into multi-hop queries, reasoning tasks,"
          " and constrained edge-case tests, guaranteeing grounded reference"
          " test suites.",
          body_style,
      )
  )

  # Concept 5
  story.append(
      Paragraph(
          "Concept 5: Agentic Evaluation & Tool-Call Verification", h1_style
      )
  )
  story.append(
      Paragraph(
          "Audits intermediate agent tool trajectories using"
          " <b>ToolCorrectnessMetric</b> and <b>ToolCallParams</b>. Validates"
          " tool selection and parameter schema adherence, preventing"
          " end-to-end output masking from hiding internal execution"
          " regressions.",
          body_style,
      )
  )

  # Page 1 Break
  story.append(PageBreak())

  # Concept 6
  story.append(
      Paragraph(
          "Concept 6: Automated Red Teaming & Vulnerability Scanning", h1_style
      )
  )
  story.append(
      Paragraph(
          "Automates adversarial attack probes: Direct/Indirect Prompt"
          " Injection, PII leakage, toxicity, and jailbreaks. Uses attack"
          " enhancements (Base64 obfuscation, persona simulation) to verify"
          " application guardrails before release.",
          body_style,
      )
  )

  # Concept 7
  story.append(
      Paragraph(
          "Concept 7: Deterministic Unit Guardrails & Custom BaseMetric",
          h1_style,
      )
  )
  story.append(
      Paragraph(
          "Subclassing <b>BaseMetric</b> enables zero-token, low-latency"
          " (&lt;5ms) Python assertions (regex validation, JSON schema checks,"
          " token count limits, PII filters) without invoking an expensive"
          " LLM judge.",
          body_style,
      )
  )

  # Concept 8
  story.append(
      Paragraph(
          "Concept 8: Production Observability, Live Tracing & Continuous Eval"
          " Flywheel",
          h1_style,
      )
  )
  story.append(
      Paragraph(
          "Avoids 100% judge evaluation costs on live traffic through a tiered"
          " architecture: 100% deterministic heuristic filters, 2%–5%"
          " asynchronous reference-free judge sampling, and 100% user-downvoted"
          " trace capture. Anomalous traces are anonymized, converted to"
          " deterministic LLMTestCase fixtures, and added to the CI regression"
          " suite.",
          body_style,
      )
  )

  # Concept 9
  story.append(
      Paragraph(
          "Concept 9: Model Benchmarking, Evaluation Datasets & Trade-Offs",
          h1_style,
      )
  )
  story.append(
      Paragraph(
          "Leverages <b>EvaluationDataset</b> to benchmark model updates across"
          " the enterprise Pareto frontier: measuring accuracy (Faithfulness /"
          " GEval) against p95 latency and token cost per 1,000 requests.",
          body_style,
      )
  )

  # Concept 10
  story.append(
      Paragraph(
          "Concept 10: Multi-Turn Conversational Evaluation & Memory Drift",
          h1_style,
      )
  )
  story.append(
      Paragraph(
          "Uses <b>ConversationalTestCase(turns=[...])</b> to audit dialogue"
          " trajectories turn-by-turn. Prevents single-turn string"
          " concatenation from hiding failures, identifies Dialogue Memory"
          " Drift, and audits conversational query rewriters resolving"
          " anaphora (pronoun references).",
          body_style,
      )
  )

  # CI/CD Implementation Code Block
  story.append(Spacer(1, 4))
  story.append(
      Paragraph(
          "Enterprise CI/CD Pytest Implementation Pattern",
          h2_style,
      )
  )

  code_text = (
      "# tests/evals/test_agent_reliability.py\n"
      "import pytest\n"
      "from deepeval import assert_test\n"
      "from deepeval.test_case import LLMTestCase, ToolCallParams\n"
      "from deepeval.metrics import FaithfulnessMetric, ToolCorrectnessMetric\n\n"
      "@pytest.fixture\n"
      "def agent_trace():\n"
      "    return LLMTestCase(\n"
      '        input="Query refund window for Enterprise Tier.",\n'
      '        actual_output="Enterprise licenses have a 45-day refund window.",\n'
      '        retrieval_context=["Enterprise licenses have a 45-day refund window."],\n'
      '        tools_called=[ToolCallParams(name="fetch_policy", input_parameters={"tier": "enterprise"})],\n'
      '        expected_tools=[ToolCallParams(name="fetch_policy", input_parameters={"tier": "enterprise"})]\n'
      "    )\n\n"
      "def test_agent_regression(agent_trace):\n"
      "    faithfulness = FaithfulnessMetric(threshold=0.8, include_reason=True)\n"
      "    tool_check = ToolCorrectnessMetric()\n"
      "    assert_test(agent_trace, [faithfulness, tool_check])\n"
  )

  code_table = Table(
      [[Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]],
      colWidths=[540],
  )
  code_table.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
          ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
          ("LEFTPADDING", (0, 0), (-1, -1), 8),
          ("RIGHTPADDING", (0, 0), (-1, -1), 8),
          ("TOPPADDING", (0, 0), (-1, -1), 6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
      ])
  )
  story.append(code_table)

  # Page 2 Break
  story.append(PageBreak())

  # Master Matrix Table
  story.append(
      Paragraph(
          "Master Architecture & Metric Decision Matrix",
          h1_style,
      )
  )
  story.append(Spacer(1, 4))

  matrix_data = [
      [
          Paragraph("Metric / Component", table_header_style),
          Paragraph("Target Subsystem", table_header_style),
          Paragraph("Required Fields", table_header_style),
          Paragraph("Ref Needed?", table_header_style),
          Paragraph("Primary Failure Mode Detected", table_header_style),
      ],
      [
          Paragraph("<b>FaithfulnessMetric</b>", table_cell_style),
          Paragraph("Generator (LLM)", table_cell_style),
          Paragraph("actual_output, retrieval_context", table_cell_style),
          Paragraph("No", table_cell_style),
          Paragraph(
              "Hallucinations, ungrounded claims, factual contradictions",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>AnswerRelevancyMetric</b>", table_cell_style),
          Paragraph("Generator (LLM)", table_cell_style),
          Paragraph("input, actual_output", table_cell_style),
          Paragraph("No", table_cell_style),
          Paragraph(
              "Incomplete answers, topic drift, evasive responses",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>ContextualRecallMetric</b>", table_cell_style),
          Paragraph("Retriever (Vector DB)", table_cell_style),
          Paragraph("expected_output, retrieval_context", table_cell_style),
          Paragraph("Yes (Golden)", table_cell_style),
          Paragraph(
              "Retriever omitted key factual chunks from context",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>ContextualPrecisionMetric</b>", table_cell_style),
          Paragraph("Retriever / Re-ranker", table_cell_style),
          Paragraph(
              "input, expected_output, retrieval_context", table_cell_style
          ),
          Paragraph("Yes (Golden)", table_cell_style),
          Paragraph(
              "Irrelevant chunks ranked above relevant ones", table_cell_style
          ),
      ],
      [
          Paragraph("<b>ToolCorrectnessMetric</b>", table_cell_style),
          Paragraph("Agent Tool Execution", table_cell_style),
          Paragraph("tools_called, expected_tools", table_cell_style),
          Paragraph("Yes (Tools)", table_cell_style),
          Paragraph(
              "Invalid tool call, schema divergence, skipped actions",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>GEval</b>", table_cell_style),
          Paragraph("Custom / Domain Logic", table_cell_style),
          Paragraph("Declared in evaluation_params", table_cell_style),
          Paragraph("Configurable", table_cell_style),
          Paragraph(
              "Policy violations, tone drift, custom business rule breaks",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>ConversationalTestCase</b>", table_cell_style),
          Paragraph("Multi-Turn Dialogue", table_cell_style),
          Paragraph("Ordered list of LLMTestCase turns", table_cell_style),
          Paragraph("Per-turn", table_cell_style),
          Paragraph(
              "Dialogue memory drift, pronoun/anaphora resolution bugs",
              table_cell_style,
          ),
      ],
      [
          Paragraph("<b>BaseMetric (Custom)</b>", table_cell_style),
          Paragraph("Deterministic Heuristics", table_cell_style),
          Paragraph("Programmatic Python properties", table_cell_style),
          Paragraph("Optional", table_cell_style),
          Paragraph(
              "Malformed JSON, regex mismatch, PII leakage, latency caps",
              table_cell_style,
          ),
      ],
  ]

  matrix_table = Table(
      matrix_data, colWidths=[100, 95, 120, 65, 160], repeatRows=1
  )
  matrix_table.setStyle(
      TableStyle([
          ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
          ("ALIGN", (0, 0), (-1, -1), "LEFT"),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 4),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
          ("LEFTPADDING", (0, 0), (-1, -1), 5),
          ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
          (
              "ROWBACKGROUNDS",
              (0, 1),
              (-1, -1),
              [colors.white, colors.HexColor("#f8fafc")],
          ),
      ])
  )
  story.append(matrix_table)

  doc.build(story, canvasmaker=NumberedCanvas)
  print(f"Successfully generated PDF: {output_filename}")
  return output_filename


if __name__ == "__main__":
  build_deepeval_pdf()
