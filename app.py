import os
import uuid

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

import chat_core

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

conversations: dict[str, list[dict]] = {}


def _get_session_id() -> str:
    sid = session.get("sid")
    if not sid:
        sid = str(uuid.uuid4())
        session["sid"] = sid
    return sid


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    user_message = data.get("message", "")

    sid = _get_session_id()
    if sid not in conversations:
        conversations[sid] = []

    messages = conversations[sid]
    messages.append({"role": "user", "content": user_message})

    try:
        result = chat_core.chat(messages)

        answer = result.get("answer", "")
        search_used = result.get("search_used", False)
        search_query = result.get("search_query")

        messages.append({"role": "assistant", "content": answer})

        return jsonify(
            {
                "answer": answer,
                "search_used": bool(search_used),
                "search_query": search_query,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
