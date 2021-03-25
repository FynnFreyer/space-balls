from typing import List, Mapping, Type
from queue import Queue
from abc import ABC, abstractmethod


class Event(ABC):
    source: object


class EventListener(ABC):
    @abstractmethod
    def on_event(self, event):
        raise NotImplementedError()


class EventHandler(ABC):
    event_type: Type[Event]

    def __init__(self):
        self.listeners = list()  # type: List[EventListener]

    def handle(self, event):
        if type(event) == self.event_type:
            for listener in self.listeners:
                listener.on_event(event)

    def subscribe(self, listener):
        self.listeners.append(listener)


class EventSource(ABC):
    handlers: List[EventHandler]

    def __init__(self):
        self.handlers = list()  # type: List[EventHandler]

    def hand_off(self, event):
        for handler in self.handlers:
            handler.handle(event)

    def subscribe(self, handler):
        return self.handlers.append(handler)

    def unsubscribe(self, handler):
        return self.handlers.remove(handler)
