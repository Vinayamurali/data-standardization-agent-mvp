# AI Mesh Integration Notes: Data Standardization Agent

## 1. Purpose

This module provides a metadata-only Data Standardization Agent that can be integrated into the existing AI Mesh platform.

The agent allows users to:

1. Upload an Excel file.
2. Extract schema metadata.
3. View column names and detected data types.
4. Select a variable for standardization.
5. Select an approved canonical credit-risk variable.
6. Describe the current and target format.
7. Generate reviewable SQL, PySpark, or Python transformation code.

The LLM does not receive actual data values.

---

## 2. Backend Components

The key backend folders are:

```text
backend/app/standardization/
backend/app/llm/