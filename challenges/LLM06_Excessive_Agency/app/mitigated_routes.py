"""Routes for the mitigated Excessive Agency challenge.

Admin privilege is granted only by POST /login with the admin password and is
stored server-side in the signed Flask session. The chat endpoint reads the
role from that session and passes it to the file tool.
"""

import hmac
import os
import secrets
import time

from flask import jsonify, render_template, request, session

from app import app
from app.utils.llm06_2025_utils.box_utils import FOLDERS
from app.utils.llm06_2025_utils.llm06_2025_mitigated_service import (
    ROLE_ADMIN,
    ROLE_ANONYMOUS,
    process_user_input,
)

# Fresh signing key per run: sessions do not survive a restart, which is fine for a lab.
app.secret_key = os.environ.get("PROMPTME_LLM03_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

ADMIN_PASSWORD = os.environ.get("PROMPTME_LLM03_ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    ADMIN_PASSWORD = secrets.token_urlsafe(12)
    # Goes to the challenge log (logs/challenge_<port>.log) for the lab facilitator.
    print(f"[mitigated] Generated admin password: {ADMIN_PASSWORD}", flush=True)


def current_role():
    return ROLE_ADMIN if session.get("role") == ROLE_ADMIN else ROLE_ANONYMOUS


@app.route("/")
def home():
    return render_template("index.html", mitigated=True, role=current_role())


@app.route("/session", methods=["GET"])
def session_info():
    return jsonify({"role": current_role()})


@app.route("/login", methods=["POST"])
def login():
    password = str((request.get_json(silent=True) or {}).get("password", ""))
    if hmac.compare_digest(password.encode(), ADMIN_PASSWORD.encode()):
        session.clear()
        session["role"] = ROLE_ADMIN
        return jsonify({"status": "success", "role": ROLE_ADMIN})
    # Small delay to slow down guessing.
    time.sleep(0.5)
    return jsonify({"status": "fail", "role": current_role()}), 401


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "success", "role": ROLE_ANONYMOUS})


@app.route("/llm06_2025_chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", ""))
    start_time = time.perf_counter()
    response = process_user_input(user_message, current_role())
    elapsed_seconds = time.perf_counter() - start_time
    payload = response.get_json()
    payload["processing_time"] = round(elapsed_seconds, 2)
    payload["role"] = current_role()
    return jsonify(payload)


@app.route("/submit-flag", methods=["POST"])
def submit_flag():
    submitted_flag = str((request.get_json(silent=True) or {}).get("flag", ""))
    actual_flag = (FOLDERS["restricted"] / "flag.txt").read_text().strip()
    if submitted_flag.strip() == actual_flag:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})
