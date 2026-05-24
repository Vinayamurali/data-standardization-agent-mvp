import json
import re
from typing import Any


class LLMResponseParser:
    """
    Parses JSON returned by the LLM.
    """

    def parse_json(self, response_text: str) -> dict[str, Any]:
        cleaned = self._strip_markdown_code_fence(response_text)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM response was not valid JSON. Raw response: {response_text}"
            ) from exc

    def _strip_markdown_code_fence(self, text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            text = re.sub(r"^```json", "", text, flags=re.IGNORECASE).strip()
            text = re.sub(r"^```", "", text).strip()
            text = re.sub(r"```$", "", text).strip()

        return text