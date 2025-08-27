import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.agent.data.sample_data import SAMPLE_CV
from src.api.v1.managers.interview_manager import interview_manager
from src.domain.models.user_profile import UserProfile
from src.logger import app_logger

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user: UserProfile):
    cv_data = SAMPLE_CV

    user_id = str(user.id)

    await interview_manager.start_interview(websocket, user, cv_data)

    await websocket.send_text(
        json.dumps(
            {
                "type": "interview_started",
                "user_id": user_id,
            }
        )
    )

    try:
        while True:
            data = await websocket.receive_text()

            message_data = json.loads(data)
            message_type = message_data.get("type", "message")

            if message_type == "user_message":
                content = message_data.get("content", "")
                if content:
                    await interview_manager.handle_user_message(user_id, content)
                else:
                    await websocket.send_text(json.dumps({"type": "error", "message": "Message content is required"}))

            elif message_type == "end_interview":
                await interview_manager.end_interview(user_id)
                break

            elif message_type == "get_status":
                status = interview_manager.get_interview_status(user_id)
                if status:
                    await websocket.send_text(json.dumps({"type": "interview_status", "status": status}))

            else:
                content = message_data.get("content", data)
                await interview_manager.handle_user_message(user_id, content)

    except WebSocketDisconnect:
        app_logger.info(f"WebSocket disconnected for interview {user_id}")
        interview_manager.disconnect_user(user_id)

    await websocket.close()
