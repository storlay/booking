from src.db.database import async_session_null_pool
from src.utils.transaction import TransactionManager


async def get_bookings_for_notify_checkin():
    async with TransactionManager(session_factory=async_session_null_pool) as transaction:
        await transaction.bookings.get_bookings_for_notify_checkin()
        ...
