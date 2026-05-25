import json

from app.standardization.models import CodeGenerationRequest


SYSTEM_PROMPT = """
You are a credit risk data standardization code generation assistant.

Your task is to generate reviewable transformation code for credit risk modelling data preparation.

Important rules:
1. You do not have access to actual data.
2. You must not ask for or assume actual customer/account-level values.
3. Use only the metadata and user-provided descriptions.
4. Generate code only for the selected output language.
5. The generated code must be reviewable by a human before execution.
6. Do not execute code.
7. Do not include destructive operations such as DROP, DELETE, TRUNCATE, UPDATE, or INSERT.
8. Return valid JSON only.

Your JSON response must follow this structure:
{
  "generated_code": "string",
  "explanation": "string",
  "assumptions": ["string"],
  "warnings": ["string"],
  "recommended_quality_checks": ["string"],
  "human_review_required": true
}
"""


def build_code_generation_user_prompt(request: CodeGenerationRequest) -> str:
    payload = {
        "source_variable_name": request.source_variable_name,
        "detected_data_type": request.detected_data_type,
        "current_state_description": request.current_state_description,
        "selected_canonical_variable": request.selected_canonical_variable,
        "target_state_description": request.target_state_description,
        "output_language": request.output_language,
        "additional_instruction": request.additional_instruction,
        "privacy_instruction": (
            "No actual data values are provided. Generate code only from metadata and user description."
        ),
    }

    return f"""
Generate transformation code using the following metadata-only request.

{json.dumps(payload, indent=2)}

Return valid JSON only.
"""