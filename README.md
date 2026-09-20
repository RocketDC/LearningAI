# DeepEval Enterprise Architecture & Mastery Project

A working reference implementation of DeepEval's 10 foundational concepts for enterprise LLM evaluation, agentic auditing, RAG triad metrics, production flywheel tracing, and CI/CD Pytest automation.

---

## 🌟 10 Foundational Concepts Covered

1. **LLMTestCase & Assertion Mechanics**: Core primitive for prompts, context, actual output, golden reference, and tool call parameters. Unit assertions (`assert_test`) vs dataset evaluations (`evaluate`).
2. **RAG Triad Architecture**: Decoupled evaluation between Retriever (`ContextualRecallMetric`, `ContextualPrecisionMetric`) and Generator (`FaithfulnessMetric`, `AnswerRelevancyMetric`).
3. **G-Eval Framework**: Two-phase LLM-as-a-judge engine featuring Auto-CoT rubric step generation and log probability continuous score normalization.
4. **Synthetic Test Data Generation & Evolution**: Cold-start dataset generation with `Synthesizer` using Multi-Hop, Reasoning, and Constraint mutation algorithms.
5. **Agentic Evaluation & Tool-Call Verification**: Trajectory auditing with `ToolCallParams` and `ToolCorrectnessMetric`.
6. **Automated Red Teaming**: Vulnerability scanning across direct/indirect prompt injection, PII leakage, toxicity, and base64 jailbreak mutations.
7. **Deterministic Unit Guardrails**: Subclassing `BaseMetric` for low-latency (<5ms), zero-token Python assertions (`ValidJSONMetric`, `RegexGuardrailMetric`, `LatencyCapMetric`, `BlacklistPIIMetric`).
8. **Production Observability & Continuous Eval Flywheel**: 3-Tier production telemetry and automatic conversion of user downvotes/anomalies into PII-redacted CI regression test fixtures.
9. **Model Benchmarking & EvaluationDatasets**: Pareto frontier trade-off evaluation (Accuracy vs Latency vs Token Cost) using versioned `EvaluationDataset` instances.
10. **Multi-Turn Conversational Evaluation**: Dialogue session auditing turn-by-turn with `ConversationalTestCase` to detect dialogue memory drift and anaphora resolution bugs.

---

## 📁 Project Structure

```
DeepEval/
├── generate_pdf.py                      # ReportLab PDF compiler for 10-concept reference guide
├── deepeval_10_concepts_mastery_guide.pdf # Generated master PDF reference artifact
├── requirements.txt                     # Project dependencies
├── .env.example                         # Environment template for LLM judge API keys
├── src/
│   ├── __init__.py
│   ├── custom_metrics.py                # Concept 7: Deterministic Custom BaseMetrics
│   ├── rag_pipeline.py                  # Concept 2: RAG Triad architecture implementation
│   ├── agent_execution.py               # Concept 5: Agent execution with ToolCallParams
│   ├── synthesizer_engine.py            # Concept 4: Synthetic data evolution algorithms
│   ├── production_observability.py     # Concept 8: Production telemetry & Continuous Eval Flywheel
│   └── red_teaming.py                  # Concept 6: Automated red-teaming attack harness
└── tests/
    ├── test_concept1_primitives.py      # LLMTestCase & assert_test vs evaluate
    ├── test_concept2_rag_triad.py       # RAG Triad metric sources of truth
    ├── test_concept3_geval.py           # GEval configuration & Auto-CoT steps
    ├── test_concept5_agent_tools.py     # ToolCorrectnessMetric & ToolCallParams
    ├── test_concept7_custom_guardrails.py # Zero-cost BaseMetric guardrails
    ├── test_concept8_flywheel.py        # Telemetry trace ingestion & PII redaction
    ├── test_concept9_benchmarks.py      # EvaluationDataset benchmarking
    ├── test_concept10_multiturn.py      # ConversationalTestCase multi-turn auditing
    └── evals/
        └── test_agent_reliability.py    # CI/CD Pytest integration suite
```

---

## 🚀 Quickstart & Usage

### 1. Setup Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Master Architecture Reference PDF
```bash
python generate_pdf.py
```
Outputs `deepeval_10_concepts_mastery_guide.pdf` with styled tables, code formatting, running headers/footers, and page numbers.

### 3. Execute Test Suites
Run the entire test suite using `pytest`:
```bash
pytest tests/
```

Run CI/CD eval suite using `deepeval test run`:
```bash
deepeval test run tests/evals/test_agent_reliability.py
```
