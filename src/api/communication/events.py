from typing import Iterable
from queue import Queue


class Observer:
    def notify(self):
        raise NotImplementedError


class Observable:
    def __init__(self):
        self.subscribers = Queue()

    def send_notifications(self):
        for subscriber in self.subscribers:
            subscriber.notify()

    def subscribe(self, observer):
        return self.subscribers.put(observer)

    def unsubscribe(self, observer):
        return self.subscribers.get(observer)


class EventListener(Observer):
    def on_event(self, event):
        raise NotImplementedError

class EventHandler:
    def __init__(self):
        self.subscribers = Queue()  # type: It[EventListener]

    def handle(self, event):
        for subscriber in self.subscribers:
            subscriber.on_event(event)


class EventSource(Observable):
    pass

