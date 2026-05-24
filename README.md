# Data Standardization Agent MVP

This project contains a standalone MVP module for a metadata-only Data Standardization Agent.

The agent is designed to be integrated into an existing AI Mesh platform.

## Purpose

The agent helps users generate reviewable SQL, PySpark, or Python code to standardize raw credit risk modelling variables into approved canonical variables.

The LLM does not receive actual data values. It only receives metadata and user-provided transformation instructions.

## MVP Capabilities

- Upload Excel file and extract schema only
- Display column names and detected data types
- Provide predefined credit risk canonical variables
- Let user select a variable for transformation
- Let user describe current and target format
- Generate transformation code in SQL, PySpark, or Python
- Return assumptions, warnings, and recommended quality checks

## Current API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health check |
| `GET /standardization/canonical-variables` | Returns predefined canonical variables |
| `POST /standardization/excel-schema` | Extracts schema from uploaded Excel file |
| `POST /standardization/generate-code` | Generates transformation code |

## Privacy Design

The LLM does not receive:

- actual Excel rows
- customer IDs
- account IDs
- balances
- DPD values
- default flags
- any raw data records

The LLM receives only:

- selected source variable name
- detected data type
- user-provided current state description
- selected canonical variable
- user-provided target state description
- selected output language
- optional user instruction

## Local Run

```powershell
cd backend
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload