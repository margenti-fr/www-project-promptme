import time

from flask import request, render_template, jsonify
from app import app
from app.utils.llm06_2025_utils.llm06_2025_service import process_user_input
from app.utils.llm06_2025_utils.box_utils import FOLDERS

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/llm06_2025_chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    start_time = time.perf_counter()
    response = process_user_input(user_message)
    elapsed_seconds = time.perf_counter() - start_time

    payload = response.get_json()
    payload['processing_time'] = round(elapsed_seconds, 2)
    return jsonify(payload)


@app.route('/submit-flag', methods=['POST'])
def submit_flag():
    submitted_flag = (request.json or {}).get('flag', '')
    # Read live so the check always matches the on-disk flag, never a hardcoded copy.
    actual_flag = (FOLDERS["restricted"] / "flag.txt").read_text().strip()
    if submitted_flag.strip() == actual_flag:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"})