from collections import defaultdict

class EventBus:
    """Simple event dispatcher. Listeners are callables registered by event type."""
    def __init__(self):
        self._listeners = defaultdict(list)
        self._approval_listener = None
    
    def on(self, event_type, callback) -> None:
        """Call `callback(event)` whenever an event of `event_type` is emitted. eg bus.on(ToolFinished, show_result)"""
        self._listeners[event_type].append(callback)

    def emit(self, event) -> None:
        """Hand the event to every callback registered for its type."""
        for callback in self._listeners[type(event)]:
            callback(event)
    
    def on_approval(self, callback) -> None:
        """Register approval_lister as callback function"""
        self._approval_listener = callback
    
    def emit_approval(self, event) -> bool:
        self.emit(event)

        if self._approval_listener is None:
            return True

        return self._approval_listener(event) is not False # as may return none too 

