from typing import Type, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUDBase: универсальный класс для работы с SQLAlchemy моделями
        :param model: SQLAlchemy модель
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        """
        Получить объект по ID
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_first(
        self, db: AsyncSession, **filters: dict[str, any]
    ) -> ModelType | None:
        """
        Получить первый объект, удовлетворяющий фильтрам
        """
        query = select(self.model)
        for field, value in filters.items():
            if not hasattr(self.model, field):
                raise ValueError(
                    f"Field '{field}' does not exist in the model '{self.model.__name__}'"
                )
            query = query.where(getattr(self.model, field) == value)

        result = await db.execute(query)

        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        **filters: dict[str, any],
    ) -> list[ModelType]:
        """
        Получить список объектов с фильтрами, поддержкой skip и limit
        """
        query = select(self.model)
        for field, value in filters.items():
            if not hasattr(self.model, field):
                raise ValueError(
                    f"Field '{field}' does not exist in the model '{self.model.__name__}'"
                )
            query = query.where(getattr(self.model, field) == value)
        query = query.order_by(self.model.id).offset(skip).limit(limit)

        result = await db.execute(query)

        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Создать объект
        """
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Обновить объект
        """
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)

        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> ModelType | None:
        """
        Удалить объект по ID
        """
        obj = await self.get(db, id)

        if obj:
            await db.delete(obj)
            await db.commit()

        return obj
