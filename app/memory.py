from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SessionMemory:
    messages: dict[str, list[dict[str, str]]] = field(default_factory=dict)

    def add(self, session_id: str, role: str, content: str) -> None:
        self.messages.setdefault(session_id, []).append(
            {"role": role, "content": content}
        )

    def get(self, session_id: str) -> list[dict[str, str]]:
        return list(self.messages.get(session_id, []))
