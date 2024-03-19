import os
import sys
import typing
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from contextlib import contextmanager

FILE_PATH = Path(os.path.realpath(__file__)).parent


class ConversationState(Enum):
    STARTED = "started"
    ENDED = "ended"


@dataclass
class Conversation:
    _state: typing.Final = ConversationState.STARTED

    @property
    def state(self) -> ConversationState:
        return self._state

    @state.setter
    def state(self, value: ConversationState):
        self._state = value


def read_previous_conversation(file_path: Path) -> typing.Optional[Conversation]:
    if not file_path.exists():
        return None

    with open(file_path, "r") as file:
        state = file.read().strip()
        return Conversation(state=ConversationState(state))


def write_conversation(file_path: Path, conversation: Conversation):
    with open(file_path, "w") as file:
        file.write(conversation.state.value)


@contextmanager
def conversation_context(file_path: Path) -> typing.Generator[Conversation
