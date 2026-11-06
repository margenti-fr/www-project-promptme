"""Entry point for the mitigated Excessive Agency challenge (OWASP 2026 LLM03)."""

import os

os.environ["PROMPTME_LLM03_MITIGATED"] = "1"

from app import app  # noqa: E402

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5106, debug=False)
