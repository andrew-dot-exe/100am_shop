import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from dto.shop_items import ShopItem as DTOShopItem
from models.shop_item import ShopItem  # Абсолютный импорт
from services.shop_item import ShopController  # Абсолютный импорт

# Настройка тестовой базы данных (SQLite в памяти)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Фикстура для создания асинхронной сессии
@pytest_asyncio.fixture
async def async_session():
    # Создаем асинхронный движок
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    # Создаем таблицы
    async with engine.begin() as conn:
        await conn.run_sync(ShopItem.metadata.create_all)
    # Создаем фабрику сессий
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture
async def create_items(async_session):
    async with async_session.begin():
        for i in range(1, 6):  # Добавляем 5 записей
            item = ShopItem(article=i, name=f"Item {i}", price=100.0 * i, description=f"Description {i}")
            async_session.add(item)
        await async_session.commit()

@pytest.mark.asyncio
async def test_get_nth_items(async_session, create_items):
    # Создаем тестовые данные

    # Создаем экземпляр контроллера
    controller = ShopController(async_session)
    # Вызываем метод и проверяем результат
    result = await controller.get_nth_items(3)
    assert len(result) == 3  # Проверяем, что вернулось 3 записи
    assert result[0].article == 1  # Проверяем первую запись
    assert result[1].name == "Item 2"  # Проверяем вторую запись
    assert result[2].price == 300.0  # Проверяем третью запись

@pytest.mark.asyncio
async def test_get_item_info(async_session, create_items):
    # Создаем экземпляр контроллера
    controller = ShopController(async_session)
    # Вызываем метод и проверяем результат
    result = await controller.get_nth_items(3)
    assert len(result) == 3  # Проверяем, что вернулось 3 записи
    assert result[0].article == 1  # Проверяем первую запись
    assert result[1].name == "Item 2"  # Проверяем вторую запись
    assert result[2].price == 300.0  # Проверяем третью запись


@pytest.mark.asyncio
async def test_add_item(async_session, create_items):
    controller = ShopController(async_session)
    item = DTOShopItem(
        name="test_item",
        price=999.99,
        description="test description",
        path_to_photo=None
    )
    test_result = await controller.add_item(item)
    async with async_session.begin():
        query = await async_session.execute(select(ShopItem).filter(ShopItem.name == item.name))
        result = query.scalars().one()
    assert test_result == None
    assert result.name == item.name
    assert result.price == item.price
    assert result.description == item.description


@pytest.mark.asyncio
async def test_edit_item(async_session, create_items):
    # Создаем экземпляр контроллера
    controller = ShopController(async_session)

    # Получаем объект для редактирования
    item_to_edit = await controller.get_nth_items(1)  # Берем первый элемент

    if not item_to_edit:
        pytest.fail("No items found for editing")

    item_to_edit = item_to_edit[0]  # Получаем первый элемент из списка

    # Обновляем информацию о товаре
    updated_data = DTOShopItem(
        article=item_to_edit.article,
        name="Updated Item",
        price=999.99,
        description="Updated Description",
        path_to_photo=None
    )

    await controller.update_item(updated_data)

    # Проверяем, что изменения сохранены
    async with async_session.begin():
        query = await async_session.execute(select(ShopItem).filter(ShopItem.name == item_to_edit.name))
        result = query.scalars().one()

    assert result.name == updated_data.name
    assert result.price == updated_data.price
    assert result.description == updated_data.description


@pytest.mark.asyncio
async def test_delete_item(async_session, create_items):
    controller = ShopController(async_session)
    item_to_delete = await controller.get_nth_items(1)
    if not item_to_delete:
        pytest.fail("No items found for deletion")
    item_to_delete = item_to_delete[0]
    await controller.delete_item(item_to_delete.article)
    async with async_session.begin():
        query = await async_session.execute(select(ShopItem).filter(ShopItem.article == item_to_delete.article))
        result = query.scalars().all()

    assert len(result) == 0, "SHOP CONTROLLER: DELETE OK" # Ожидаем, что результат пустой после удаления
