from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_code_api_returns_fallback_pyspark_code():
    payload = {
        "source_variable_name": "dpd_hist_36m",
        "detected_data_type": "string",
        "current_state_description": "The column contains last 36 months DPD values separated by pipe.",
        "selected_canonical_variable": "dpd_last_36_months",
        "target_state_description": "Convert into an array of 36 integer values.",
        "output_language": "pyspark",
        "additional_instruction": "Replace missing values with 0.",
    }

    response = client.post("/standardization/generate-code", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["source_variable_name"] == "dpd_hist_36m"
    assert data["selected_canonical_variable"] == "dpd_last_36_months"
    assert data["output_language"] == "pyspark"
    assert "df.withColumn" in data["generated_code"]
    assert "split" in data["generated_code"]
    assert data["human_review_required"] is True


def test_generate_code_api_returns_fallback_sql_code():
    payload = {
        "source_variable_name": "bad_ind",
        "detected_data_type": "string",
        "current_state_description": "The column contains Y/N default indicator.",
        "selected_canonical_variable": "default_flag",
        "target_state_description": "Convert to binary 1/0 default flag.",
        "output_language": "sql",
        "additional_instruction": "Y means default and N means not default.",
    }

    response = client.post("/standardization/generate-code", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "CASE" in data["generated_code"]
    assert "AS default_flag" in data["generated_code"]