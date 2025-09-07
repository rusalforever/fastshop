from src.users.models.pydantic import UserModel


async def get_current_user() -> UserModel:
    return UserModel(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone_number="+380001112233",
    )