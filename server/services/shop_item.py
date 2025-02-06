# shop items logic
# @andrew-dot-exe, 2025

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dto.shop_items import ShopItem as DTOShopItem
from dto.shop_items import ShopItemShort as ShortDTOItem
from models.shop_item import ShopItem


class ShopController:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_nth_items(self, count: int) -> list:
        result = []
        query = select(ShopItem).limit(count)
        async with self.session.begin():  # Начинаем транзакцию
            exec = await self.session.execute(query)  # Выполняем запрос
            response = exec.scalars().all()  # Получаем все результаты
            for row in response:
                # результаты должны быть в формате DTO
                converted = ShortDTOItem(
                    article=row.article,
                    name=row.name,
                    price=row.price
                )
                result.append(converted.model_dump_json())  # Добавляем каждый результат в список
        return result

    async def get_item_info(self, article: int):
        query = select(ShopItem).where(ShopItem.article==article)
        async with self.session.begin():
            exec = await self.session.execute(query)
            response = exec.scalars().one()
            conv = DTOShopItem(
                article=response.article,
                name=response.name,
                price= response.price,
                description=response.description,
                path_to_photo=response.path_to_photo
            )
            return conv


    async def add_item(self, item: DTOShopItem):
        add_item = ShopItem(
            name = item.name,
            price = item.price,
            description=item.description,
            path_to_photo=item.path_to_photo
        )
        async with self.session.begin():
            self.session.add(add_item)
            await self.session.commit()

    async def update_item(self, item: DTOShopItem):
        async with self.session.begin():
            fnd_item = await self.session.execute(select(ShopItem).filter(ShopItem.article==item.article))
            try:
                editable = fnd_item.scalars().one()
            except NoResultFound:
                raise Exception("Item not found.")
            editable.name = item.name
            editable.price = item.price
            editable.description = item.description
            editable.path_to_photo = item.path_to_photo

            await self.session.commit()

    async def delete_item(self, article: int):
        async with self.session.begin():
            item = await self.session.execute(select(ShopItem).filter(ShopItem.article==article))
            try:
                to_delete = item.scalars().one()
                await self.session.delete(to_delete)
                await self.session.commit()
            except NoResultFound:
                raise Exception("Item not found")
