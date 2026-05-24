from io import BytesIO

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_excel_schema_api_returns_column_metadata():
    df = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "as_on_date": pd.to_datetime(["2023-01-31", "2023-02-28"]),
            "dpd": [0, 30],
            "outstanding_balance": [1000.5, 2000.75],
        }
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="loan_data")

    excel_buffer.seek(0)

    response = client.post(
        "/standardization/excel-schema",
        files={
            "file": (
                "sample.xlsx",
                excel_buffer.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["file_name"] == "sample.xlsx"
    assert data["sheet_name"] == "loan_data"
    assert data["total_rows"] == 2
    assert data["total_columns"] == 4

    column_names = [column["column_name"] for column in data["columns"]]

    assert "customer_id" in column_names
    assert "as_on_date" in column_names
    assert "dpd" in column_names
    assert "outstanding_balance" in column_names


def test_excel_schema_api_rejects_non_excel_file():
    response = client.post(
        "/standardization/excel-schema",
        files={
            "file": (
                "sample.txt",
                b"not an excel file",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400