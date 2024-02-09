class OutBox:
    """
    Provides list of email messages sent
    The class is used for testing purposes
    """
    outbox: list = []


class Mediator:
    """
    Mediator between class that provides lists of email
    messages and class that implements mail-sending interface
    for test purposes
    """
    def __init__(self):
        self._outbox = OutBox.outbox

    def add_data_to_outbox(self, data) -> None:
        self._outbox.append(data)

    def clear_outbox(self) -> None:
        self._outbox.clear()

    def get_outbox(self) -> list:
        return self._outbox


def get_mediator() -> Mediator:
    """
    Instance of Mediator that is common and used
    both in tests and in a class that implements
    mail-sending interface for test purposes
    """
    return Mediator()
