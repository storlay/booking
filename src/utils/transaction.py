from abc import ABC
from abc import abstractmethod
from typing import Callable

from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class BaseManager(ABC):
    users: UsersRepository
    hotels: HotelsRepository
    rooms: RoomsRepository

    @abstractmethod
    def __init__(self):
        """Initializing the manager"""
        pass

    @abstractmethod
    async def __aenter__(self):
        """Enter the asynchronous context"""
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        """Exit the asynchronous context"""
        pass

    @abstractmethod
    async def commit(self):
        """Commit the transaction"""
        pass


class TransactionManager(BaseManager):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
