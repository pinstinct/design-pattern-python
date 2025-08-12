from abc import ABC, abstractmethod
from typing import Optional


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    모든 구상 핸들러에 공통적인 인터페이스를 선언한다.
    일반적으로 요청을 처리하기 위한 단일 메서드만 포함하지만,
    때로는 체인의 다음 핸들러를 세팅하기 위한 다른 메서드가 있을 수도 있다.
    """

    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler class.
    선택적 클래스이며 여기에 모든 핸들러 클래스에 공통적인 상용구 코드를 넣는다.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


"""
All concrete Handlers either handle a request or pass it to the next handler the chain.
요청을 처리하기 위한 실제 코드가 포함된다.
각 핸들러는 요청을 받으면 이 요청을 처리할지와 함께 체인을 따라 전달할지를 결정한다.
일반적으로 자체 포함형이고, 생성자를 통해 필요한 모든 데이터를 한 번만 받는다.
"""


class MonkeyHandler(AbstractHandler):

    def handle(self, request) -> str:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        else:
            return super().handle(request)


class SquirrelHandler(AbstractHandler):

    def handle(self, request) -> str:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        else:
            return super().handle(request)


class DogHandler(AbstractHandler):

    def handle(self, request) -> str:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    """
    The client code is usually suited to work with a single handler.
    In most cases, it is not even aware that the handler is part of a chain.
    """
    for food in ["Nut", "Banana", "Cup of coffee"]:
        print(f"\nClient: Who wants a {food}?")
        result = handler.handle(food)
        if result:
            print(f" {result}", end="")
        else:
            print(f" {food} was left untouched.", end="")


if __name__ == "__main__":
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)
    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)
    print("\n")

    print("Subchain: Squirrel > Dog")
    client_code(squirrel)
