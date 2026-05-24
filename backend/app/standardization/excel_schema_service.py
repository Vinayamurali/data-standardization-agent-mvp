from fastapi import UploadFile

from app.standardization.models import ExcelColumnSchema, ExcelSchemaResponse


class ExcelSchemaService:
    """
    Placeholder service for Excel schema extraction.

    In the next phase, this will read the uploaded Excel file
    and extract column names and data types without sending data to the LLM.
    """

    async def extract_schema(self, file: UploadFile) -> ExcelSchemaResponse:
        return ExcelSchemaResponse(
            file_name=file.filename or "uploaded_file.xlsx",
            sheet_name=None,
            total_columns=0,
            columns=[
                ExcelColumnSchema(
                    column_name="placeholder_column",
                    detected_data_type="unknown",
                    nullable=None,
                )
            ],
        )