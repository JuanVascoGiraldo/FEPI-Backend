import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_sse(self) -> str:
        return f"event: {self.type}\ndata: {json.dumps({**self.payload, 'timestamp': self.timestamp})}\n\n"


class EventBus:
    def __init__(self) -> None:
        self._group_queues: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, group: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._group_queues.setdefault(group, []).append(q)
        return q

    def unsubscribe(self, group: str, q: asyncio.Queue) -> None:
        if group in self._group_queues:
            self._group_queues[group] = [x for x in self._group_queues[group] if x is not q]

    async def publish(self, group: str, event: Event) -> None:
        for q in self._group_queues.get(group, []):
            await q.put(event)
