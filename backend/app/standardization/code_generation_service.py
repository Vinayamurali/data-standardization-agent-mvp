from app.standardization.models import CodeGenerationRequest, CodeGenerationResponse


class CodeGenerationService:
    """
    Placeholder service for code generation.

    In a later phase, this will call the LLM.
    For now, it returns a safe placeholder response.
    """

    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        generated_code = (
            f"# Placeholder code for standardizing {request.source_variable_name} "
            f"to {request.selected_canonical_variable}\n"
            f"# Output language selected: {request.output_language}\n"
            f"# LLM integration will be added in a later phase."
        )

        return CodeGenerationResponse(
            source_variable_name=request.source_variable_name,
            selected_canonical_variable=request.selected_canonical_variable,
            output_language=request.output_language,
            generated_code=generated_code,
            explanation=(
                "This is a placeholder response. The final version will generate "
                "reviewable transformation code using only metadata and user-provided instructions."
            ),
            assumptions=[
                "No actual data is sent to the LLM.",
                "The user will review generated code before implementation."
            ],
            warnings=[
                "This placeholder does not perform actual code generation yet."
            ],
            recommended_quality_checks=[
                "Validate output data type after transformation.",
                "Check missing values after transformation.",
                "Review transformation logic before using it for modelling."
            ],
            human_review_required=True,
        )