from database.base import get_test_database
import pytest

async def init():
    await get_test_database()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield