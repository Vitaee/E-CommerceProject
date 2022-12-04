import pytest
from models.users import User
from database.base import get_test_database
import pytest_asyncio

data = {
    'firstname': 'Can',
    'lastname': 'Test',
    'username': 'vitae',
    'phone': '+905542128844',
    'email': 'test@example.com',
    'password': '123456',
}

#@pytest.mark.asyncio
@pytest.mark.anyio
async def test_create_user():
    await User.all().delete()

    user = await User.create(**data)

    assert user.email == data['email']

    assert await User.filter(email=user.email).count() == 1


"""

@pytest.mark.asyncio
async def test_update_user():
    user = await User.filter(email=data['email']).first()
    assert user is not None
    user.username = 'testusername'
    update_data = {'username': 'testusername'}
    await user.update_from_dict(update_data)
    assert user.username != data['username']
    assert user.username is not None


@pytest.mark.asyncio
async def test_remove_user():
    await User.filter(email=data['email']).delete()
    assert await User.filter(email=data['email']).count() == 0

"""