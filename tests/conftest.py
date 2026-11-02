import json
import urllib.request

import pytest

OLLAMA_URL = "http://localhost:11434"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "ollama: live test against a local Ollama server; run with `pytest -m ollama`",
    )


def pytest_collection_modifyitems(config, items):
    """Live tests only run when selected explicitly with `-m ollama`."""
    if "ollama" in (config.getoption("-m") or ""):
        return
    skip = pytest.mark.skip(reason="live Ollama test; run with `pytest -m ollama`")
    for item in items:
        if "ollama" in item.keywords:
            item.add_marker(skip)


_latencies = {}


def record_latency(level, seconds):
    """Collect per-level response times from live tests for the summary below."""
    _latencies.setdefault(level, []).append(seconds)


def pytest_terminal_summary(terminalreporter):
    if not _latencies:
        return
    terminalreporter.section("LLM01 live latency per level")
    for level in sorted(_latencies):
        times = _latencies[level]
        terminalreporter.write_line(
            f"level {level}: {len(times):2d} calls, "
            f"avg {sum(times) / len(times):5.2f}s, max {max(times):5.2f}s"
        )


def installed_ollama_models():
    """Return the installed model tags, or None when Ollama isn't reachable."""
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3) as response:
            return {m["name"] for m in json.load(response)["models"]}
    except Exception:
        return None
