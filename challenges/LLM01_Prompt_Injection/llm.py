"""Ollama access for LLM01 levels 1-7.

Every model call for levels 1-7 goes through chat(), so the levels share pinned
model versions and fixed sampling options. The pinned tags have the same
digests as `mistral:latest` (6577803aa9a0) and `granite3-guardian:latest`
(ba81a177bd23) at the time the levels were tuned, so a newer `latest` can't
silently change how the levels behave.

Level 8 (the original challenge) keeps its own calls in app1.py.
"""
import ollama

TARGET_MODEL = "mistral:7b-instruct-v0.3-q4_K_M"
JUDGE_MODEL = TARGET_MODEL
GUARDIAN_MODEL = "granite3-guardian:2b-q8_0"  # same digest as the `latest` tag level 8 uses

OLLAMA_OPTIONS = {
    "temperature": 0,  # always pick the most likely token: same prompt, same reply
    "seed": 42,        # reproducible sampling if a call ever uses temperature > 0
    "num_ctx": 4096,   # fixed context size, so long prompts are always cut the same way
}

TARGET_MAX_TOKENS = 300  # keeps the worst-case reply to a few seconds
JUDGE_MAX_TOKENS = 5     # verdicts are a single word


def chat(model, messages, max_tokens=None):
    """Send messages to an Ollama model and return the reply text."""
    options = dict(OLLAMA_OPTIONS)
    if max_tokens is not None:
        options["num_predict"] = max_tokens
    response = ollama.chat(model=model, messages=messages, options=options)
    return response["message"]["content"]
