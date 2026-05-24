from typing import List

from fastapi import APIRouter, File, UploadFile

from app.standardization.canonical_variables import get_canonical_variables
from app.standardization.code_generation_service import CodeGenerationService
from app.standardization.excel_schema_service import ExcelSchemaService
from app.standardization.models import (
    CanonicalVariable,
    CodeGenerationRequest,
    CodeGenerationResponse,
    ExcelSchemaResponse,
)

router = APIRouter(
    prefix="/standardization",
    tags=["Data Standardization Agent"]
)


@router.get("/canonical-variables", response_model=List[CanonicalVariable])
def list_canonical_variables():
    return get_canonical_variables()


@router.post("/excel-schema", response_model=ExcelSchemaResponse)
async def extract_excel_schema(file: UploadFile = File(...)):
    service = ExcelSchemaService()
    return await service.extract_schema(file)


@router.post("/generate-code", response_model=CodeGenerationResponse)
def generate_standardization_code(request: CodeGenerationRequest):
    service = CodeGenerationService()
    return service.generate_code(request)