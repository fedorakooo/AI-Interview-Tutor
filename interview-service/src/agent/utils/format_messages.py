from src.agent.domain.value_objects.conversation_role import ConversationRole


def format_messages(messages: list[tuple[ConversationRole, str]]) -> str:
    lines = []
    for message in messages:
        role, content = message
        lines.append(f"{str(role)}: {content}")
    return "\n".join(lines)
