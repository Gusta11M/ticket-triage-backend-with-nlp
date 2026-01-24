from select import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreateSchema

async def create_category(db : AsyncSession, category : CategoryCreateSchema):

    db_category = Category(
        category_name = category.category_name
    )

    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_category_by_id(db : AsyncSession, category_id : int):

    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    return result.scalars().first()

async def get_all_categories(db : AsyncSession):

    result = await db.execute(select(Category))

    return result.scalars().all()


async def update_category(db : AsyncSession, category_id : int, category_name : str):

    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    db_category = result.scalars().first()

    if db_category:
        db_category.category_name =  category_name

        await db.commit()
        await db.refresh(db_category)
    return db_category


async def delete_category(db : AsyncSession, category_id : int):

    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    db_category = result.scalars().first()

    if db_category:
        await db.delete(db_category)
        await db.commit()
    return db_category