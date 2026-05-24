from io import BytesIO

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.standardization.models import ExcelColumnSchema, ExcelSchemaResponse


class ExcelSchemaService:
    """
    Extracts schema from an uploaded Excel file.

    Important:
    - The file is read only by the backend.
    - Actual data rows are not returned.
    - Actual data rows are not sent to the LLM.
    - Only column names, inferred data types, nullable flag, and row/column counts are returned.
    """

    SUPPORTED_EXTENSIONS = {".xlsx", ".xls"}

    async def extract_schema(self, file: UploadFile) -> ExcelSchemaResponse:
        file_name = file.filename or "uploaded_file.xlsx"

        self._validate_file_extension(file_name)

        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded Excel file is empty."
            )

        try:
            excel_file = pd.ExcelFile(BytesIO(file_bytes))
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to read Excel file. Error: {str(exc)}"
            ) from exc

        if not excel_file.sheet_names:
            raise HTTPException(
                status_code=400,
                detail="Excel file does not contain any sheets."
            )

        selected_sheet = excel_file.sheet_names[0]

        try:
            df = pd.read_excel(
                BytesIO(file_bytes),
                sheet_name=selected_sheet,
                engine="openpyxl"
            )
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to parse sheet '{selected_sheet}'. Error: {str(exc)}"
            ) from exc

        columns = []

        for column_name in df.columns:
            column_series = df[column_name]

            columns.append(
                ExcelColumnSchema(
                    column_name=str(column_name),
                    detected_data_type=str(column_series.dtype),
                    nullable=bool(column_series.isna().any()),
                )
            )

        return ExcelSchemaResponse(
            file_name=file_name,
            sheet_name=selected_sheet,
            available_sheets=excel_file.sheet_names,
            total_rows=int(len(df)),
            total_columns=int(len(df.columns)),
            columns=columns,
        )

    def _validate_file_extension(self, file_name: str) -> None:
        lower_file_name = file_name.lower()

        if not any(lower_file_name.endswith(ext) for ext in self.SUPPORTED_EXTENSIONS):
            raise HTTPException(
                status_code=400,
                detail="Only .xlsx and .xls files are supported."
            )