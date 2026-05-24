


# Frontend Contract: Data Standardization Agent

## 1. Purpose

The Data Standardization Agent helps users generate reviewable SQL, PySpark, or Python code to standardize raw credit-risk modelling variables into approved canonical variables.

The agent is metadata-only. Actual data values should not be sent to the LLM.

---

## 2. High-Level User Flow

```text
User opens Data Standardization Agent
        ↓
Uploads Excel file
        ↓
Frontend calls /standardization/excel-schema
        ↓
Schema preview is displayed
        ↓
User selects one source variable
        ↓
User selects target canonical variable
        ↓
User describes current format and target format
        ↓
User selects output language: SQL / PySpark / Python
        ↓
Frontend calls /standardization/generate-code
        ↓
Generated code, assumptions, warnings, and checks are displayed