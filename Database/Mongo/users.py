from . import db

usersdb = db.users

async def add_user(a: int):
    found = usersdb.find_one({"a": a})
    if not found:
        await usersdb.insert_one({"a": a})

async def get_users():
    List
    users = usersdb.find({"a": {"$gt": 0}})
    if not users:
        return []
    for user in await users.to_list(length=1000000000):
        List.append(user)
    return List

async def is_user(a: int):
    is_ = usersdb.find_one({"a": a})
    if is_:
        return True
    return False
