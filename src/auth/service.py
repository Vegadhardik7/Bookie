from src.auth.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generated_pswd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def get_all_user(self, session: AsyncSession):
        async with session.begin():
            statement = select(User)
            result = await session.exec(statement)
            return result.all()

    async def get_user_by_email(self, email: str, session: AsyncSession):
        async with session.begin():
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            usr = result.first()
            return usr
    
    async def user_exists(self, email: str, session: AsyncSession):
        usr = await self.get_user_by_email(email, session)
        return True if usr is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        usr_data_dict = user_data.model_dump()

        new_user = User(**usr_data_dict)
        new_user.password = generated_pswd_hash(user_data.password)
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user