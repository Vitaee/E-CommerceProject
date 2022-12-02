from tortoise.signals import pre_save, pre_delete, post_delete, post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient
from models.users import User

@pre_save(User)
async def signal_pre_save(sender: "Type[User]", instance: User, using_db, update_fields):
    """might set default avatar from this signal"""
    print("signal pre save : ", sender, instance)


@post_save(User)
async def signal_post_save(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    """might send welcome email from this signal"""
    print('message_post_save: ', sender, instance, using_db, update_fields)


@pre_delete(User)
async def signal_pre_delete(sender: "Type[User]", instance: User, using_db: "Optional[BaseDBAsyncClient]") -> None:
    print('message_pre_delete: ', sender, instance, using_db)


@post_delete(User)
async def signal_post_delete(sender: "Type[User]", instance: User, using_db: "Optional[BaseDBAsyncClient]") -> None:
    """might send information email from this signal"""
    print('message_post_delete: ', sender, instance, using_db)