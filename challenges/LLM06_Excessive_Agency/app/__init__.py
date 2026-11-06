import os

from flask import Flask

app = Flask(__name__)

# app6_mitigated.py sets this before importing the package to serve the
# hardened version of the challenge instead of the vulnerable one.
MITIGATED = os.environ.get("PROMPTME_LLM03_MITIGATED") == "1"

if MITIGATED:
    from app import mitigated_routes  # noqa: E402,F401
else:
    from app import routes  # noqa: E402,F401
