from typing import List, Literal, Optional
from pydantic import BaseModel, Field


OutputLanguage = Literal["sql", "pyspark", "python"]


class CanonicalVariable(BaseModel):
    name: str
    display_name: str
    description: str
    expected_data_type: str
    example_use_case: str


class ExcelColumnSchema(BaseModel):
    column_name: str
    detected_data_type: str
    nullable: Optional[bool] = None


class ExcelSchemaResponse(BaseModel):
    file_name: str
    sheet_name: Optional[str] = None
    available_sheets: List[str] = Field(default_factory=list)
    total_rows: int
    total_columns: int
    columns: List[ExcelColumnSchema]


class CodeGenerationRequest(BaseModel):
    source_variable_name: str
    detected_data_type: Optional[str] = None
    current_state_description: str
    selected_canonical_variable: str
    target_state_description: str
    output_language: OutputLanguage
    additional_instruction: Optional[str] = None


class CodeGenerationResponse(BaseModel):
    source_variable_name: str
    selected_canonical_variable: str
    output_language: OutputLanguage
    generated_code: str
    explanation: str
    assumptions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    recommended_quality_checks: List[str] = Field(default_factory=list)
    human_review_required: bool = True