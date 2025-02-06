from pydantic_ai import (
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    SystemPromptPart,
    TextPart,
)
from app.chat.message.schemas import (
    Message,
    Role,
    REQ_ROLES,
    RES_ROLES,
    MessageMetadata,
    CreateMessage,
)


class HistoryAdapter:
    """
    Implements logic to transform history data to pydantic_ai chat_history
    """

    @staticmethod
    def wrap(stored: list[Message]) -> list[ModelRequest | ModelResponse]:
        ai_history: list[ModelRequest | ModelResponse] = []

        seq_type = "req" if stored and stored[0].meta_data.role in REQ_ROLES else "res"
        temp = []
        for msg in stored:
            if seq_type == "req" and msg.meta_data.role in REQ_ROLES:
                if msg.meta_data.role == Role.user:
                    temp.append(
                        UserPromptPart(
                            content=msg.content,
                            timestamp=msg.created_at,
                            part_kind="user-prompt",
                        )
                    )
                elif msg.meta_data.role == Role.system:
                    temp.append(
                        SystemPromptPart(
                            content=msg.content,
                            dynamic_ref=None,
                            part_kind="system-prompt",
                        )
                    )
            elif seq_type == "res" and msg.meta_data.role in RES_ROLES:
                temp.append(
                    TextPart(
                        content=msg.content,
                        part_kind="text",
                    )
                )
            else:
                if msg.meta_data.role == Role.user:
                    temp.append(
                        UserPromptPart(
                            content=msg.content,
                            timestamp=msg.created_at,
                            part_kind="user-prompt",
                        )
                    )
                elif msg.meta_data.role == Role.system:
                    temp.append(
                        SystemPromptPart(
                            content=msg.content,
                            dynamic_ref=None,
                            part_kind="system-prompt",
                        )
                    )
                else:
                    temp.append(
                        TextPart(
                            content=msg.content,
                            part_kind="text",
                        )
                    )

                if temp:
                    if seq_type == "req":
                        ai_history.append(ModelRequest(parts=temp))
                    else:
                        ai_history.append(ModelResponse(parts=temp))
                    temp = []
                seq_type = "res" if seq_type == "req" else "req"

        if len(temp) > 0:
            if seq_type == "req":
                ai_history.append(ModelRequest(parts=temp))
            else:
                ai_history.append(ModelResponse(parts=temp))

        return ai_history

    def unwrap(
        ai_history: list[ModelRequest | ModelResponse], connection_id: int
    ) -> list[Message]:
        messages: list[Message] = []

        for item in ai_history:
            for part in item.parts:
                if isinstance(part, UserPromptPart):
                    messages.append(
                        CreateMessage(
                            id=None,
                            content=part.content,
                            meta_data=MessageMetadata(role=Role.user),
                            connection_id=connection_id,
                        )
                    )
                elif isinstance(part, SystemPromptPart):
                    messages.append(
                        CreateMessage(
                            id=None,
                            content=part.content,
                            meta_data=MessageMetadata(role=Role.system),
                            connection_id=connection_id,
                        )
                    )
                elif isinstance(part, TextPart):
                    messages.append(
                        CreateMessage(
                            id=None,
                            content=part.content,
                            meta_data=MessageMetadata(
                                role=Role.assistant, name=item.model_name
                            ),
                            connection_id=connection_id,
                            created_at=item.timestamp,
                        )
                    )

        return messages
