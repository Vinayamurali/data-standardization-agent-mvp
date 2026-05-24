from app.config import settings
from app.llm.client import OpenAIClient
from app.llm.parser import LLMResponseParser
from app.llm.prompts import SYSTEM_PROMPT, build_code_generation_user_prompt
from app.standardization.models import CodeGenerationRequest, CodeGenerationResponse


class CodeGenerationService:
    """
    Generates standardization code.

    If LLM is enabled, it calls OpenAI.
    If LLM is disabled, it uses a local fallback template so the MVP can be demoed without an API key.
    """

    def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        if settings.llm_enabled:
            return self._generate_with_llm(request)

        return self._generate_with_local_fallback(request)

    def _generate_with_llm(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        user_prompt = build_code_generation_user_prompt(request)

        response_text = OpenAIClient().generate_text(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        parsed_response = LLMResponseParser().parse_json(response_text)

        return CodeGenerationResponse(
            source_variable_name=request.source_variable_name,
            selected_canonical_variable=request.selected_canonical_variable,
            output_language=request.output_language,
            generated_code=parsed_response.get("generated_code", ""),
            explanation=parsed_response.get("explanation", ""),
            assumptions=parsed_response.get("assumptions", []),
            warnings=parsed_response.get("warnings", []),
            recommended_quality_checks=parsed_response.get("recommended_quality_checks", []),
            human_review_required=parsed_response.get("human_review_required", True),
        )

    def _generate_with_local_fallback(
        self,
        request: CodeGenerationRequest,
    ) -> CodeGenerationResponse:
        if request.output_language == "pyspark":
            generated_code = self._fallback_pyspark_code(request)
        elif request.output_language == "sql":
            generated_code = self._fallback_sql_code(request)
        else:
            generated_code = self._fallback_python_code(request)

        return CodeGenerationResponse(
            source_variable_name=request.source_variable_name,
            selected_canonical_variable=request.selected_canonical_variable,
            output_language=request.output_language,
            generated_code=generated_code,
            explanation=(
                "LLM is currently disabled, so this is a local fallback template. "
                "It is generated only from the variable name, selected canonical variable, "
                "target format, and output language."
            ),
            assumptions=[
                "No actual data values were used.",
                "The generated code is a starting template and must be reviewed before execution.",
                "The user-provided current and target state descriptions are assumed to be correct.",
            ],
            warnings=[
                "LLM is disabled. Output may be less tailored than GPT-generated code.",
                "Review delimiter, casting, null handling, and target format before using in production.",
            ],
            recommended_quality_checks=self._recommended_checks(request),
            human_review_required=True,
        )

    def _fallback_pyspark_code(self, request: CodeGenerationRequest) -> str:
        source = request.source_variable_name
        target = request.selected_canonical_variable

        if target == "dpd_last_36_months":
            return f"""from pyspark.sql.functions import col, split, transform, trim, when, lit

# Converts {source} into {target}
# Assumption: source values are delimiter-separated DPD values.
# Update the delimiter if required.

delimiter = "|"

df = df.withColumn(
    "{target}",
    transform(
        split(col("{source}"), delimiter),
        lambda x: when(trim(x) == "", lit("0")).otherwise(trim(x)).cast("int")
    )
)
"""

        if target == "default_flag":
            return f"""from pyspark.sql.functions import col, when, lit

# Converts {source} into binary default_flag.
# Review the positive/negative values before execution.

df = df.withColumn(
    "{target}",
    when(col("{source}").isin("Y", "Yes", "1", 1, True), lit(1))
    .when(col("{source}").isin("N", "No", "0", 0, False), lit(0))
    .otherwise(None)
)
"""

        if target in {"as_on_date", "default_date"}:
            return f"""from pyspark.sql.functions import col, to_date

# Converts {source} into standardized date field {target}.
# Update date format if required.

df = df.withColumn(
    "{target}",
    to_date(col("{source}"))
)
"""

        return f"""from pyspark.sql.functions import col

# Direct standardization template.
# Review casting and null handling before execution.

df = df.withColumn(
    "{target}",
    col("{source}")
)
"""

    def _fallback_sql_code(self, request: CodeGenerationRequest) -> str:
        source = request.source_variable_name
        target = request.selected_canonical_variable

        if target == "default_flag":
            return f"""CASE
    WHEN {source} IN ('Y', 'Yes', '1', 1) THEN 1
    WHEN {source} IN ('N', 'No', '0', 0) THEN 0
    ELSE NULL
END AS {target}"""

        if target in {"as_on_date", "default_date"}:
            return f"""CAST({source} AS DATE) AS {target}"""

        if target == "dpd":
            return f"""CAST({source} AS INTEGER) AS {target}"""

        return f"""{source} AS {target}"""

    def _fallback_python_code(self, request: CodeGenerationRequest) -> str:
        source = request.source_variable_name
        target = request.selected_canonical_variable

        if target == "dpd_last_36_months":
            return f"""# Converts {source} into {target}
# Assumption: values are pipe-separated. Update delimiter if required.

delimiter = "|"

df["{target}"] = (
    df["{source}"]
    .fillna("")
    .astype(str)
    .str.split(delimiter)
    .apply(lambda values: [int(v.strip()) if v.strip() else 0 for v in values])
)
"""

        if target == "default_flag":
            return f"""# Converts {source} into binary default_flag.

positive_values = {{"Y", "Yes", "1", 1, True}}
negative_values = {{"N", "No", "0", 0, False}}

def map_default_flag(value):
    if value in positive_values:
        return 1
    if value in negative_values:
        return 0
    return None

df["{target}"] = df["{source}"].apply(map_default_flag)
"""

        if target in {"as_on_date", "default_date"}:
            return f"""df["{target}"] = pd.to_datetime(df["{source}"], errors="coerce")"""

        return f"""df["{target}"] = df["{source}"]"""

    def _recommended_checks(self, request: CodeGenerationRequest) -> list[str]:
        target = request.selected_canonical_variable

        common_checks = [
            "Verify that the transformed field has the expected data type.",
            "Check missing/null values after transformation.",
            "Review a small sample manually before using the output for modelling.",
        ]

        if target == "dpd":
            return common_checks + [
                "Check DPD is numeric.",
                "Check DPD is greater than or equal to 0.",
                "Review unusually high DPD values.",
            ]

        if target == "dpd_last_36_months":
            return common_checks + [
                "Check each row contains exactly 36 DPD values.",
                "Check every DPD value is numeric.",
                "Check every DPD value is greater than or equal to 0.",
            ]

        if target == "default_flag":
            return common_checks + [
                "Check default_flag contains only 0 and 1.",
                "Confirm default definition with the risk/model owner.",
            ]

        if target in {"as_on_date", "default_date"}:
            return common_checks + [
                "Check date parsing failures.",
                "Confirm date format with the source system owner.",
            ]

        return common_checks