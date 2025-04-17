import os
import time
import uuid
import threading
import logging
from typing import Any
import socketio
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


async def call_director(
    text_message: str, session_id: str | None = None, collection_id: str = "default"
) -> dict[str, Any]:
    """
    Orchestrates specialized agents within the VideoDB server to efficiently handle multimedia and video-related queries.
    
    Args:
        text_message (str): The natural language query that Director will interpret and delegate to appropriate agents.
        session_id (str | None, optional): A session identifier to maintain continuity across multiple requests. If a previous response from this method included a `session_id`, it is MANDATORY to include it in subsequent requests.
    """
    url = os.getenv("DIRECTOR_API_URL")
    timeout = 300
    headers = {"x-access-token": os.getenv("VIDEO_DB_API_KEY")}
    sio = socketio.Client()
    response_data = None
    response_event = threading.Event()

    def on_connect():
        logger.info("Connected to Director agent")
        message = {
            "msg_type": "input",
            "sender": "user",
            "conv_id": str(int(time.time() * 1000)),
            "msg_id": str(int(time.time() * 1000) + 1),
            "session_id": session_id if session_id else str(uuid.uuid4()),
            "content": [{"type": "text", "text": text_message}],
            "agents": [],
            "collection_id": collection_id,
        }
        sio.emit("chat", message, namespace="/chat")

    def on_message(data):
        nonlocal response_data
        if isinstance(data, dict) and data.get("status") != "progress":
            response_data = data
            response_event.set()

    sio.on("connect", on_connect, namespace="/chat")
    sio.on("chat", on_message, namespace="/chat")

    try:
        logger.info(f"Connecting to Director agent at {url}")
        sio.connect(
            url,
            namespaces=["/chat"],
            headers=headers,
        )
        received = response_event.wait(timeout=timeout)
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return {"error": f"Connection failed: {e}"}
    finally:
        sio.disconnect()

    if received:
        return response_data or {"error": "No data received"}
    else:
        logger.warning(f"Timeout waiting for response after {timeout} seconds")
        return {"error": "Timeout waiting for response"}

