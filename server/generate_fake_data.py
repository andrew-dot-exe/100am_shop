import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Numeric, Text, select
from faker import Faker
import random
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение строки подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_CONN_STRING")

# Определение базы данных и модели
Base = declarative_base()

class ShopItem(Base):
    __tablename__ = "shop_items"
    article = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(Numeric(16, 2), nullable=False)
    description = Column(Text, nullable=True)
    path_to_photo = Column(String, nullable=True)

# Настройка подключения к базе данных (например, PostgreSQL с асинхронным движком)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Инициализация Faker для генерации случайных данных
fake = Faker('ru_RU')

# Список брендов и категорий для продакт-плейсмента
brands = [
    "Nike", "Adidas", "Puma", "Reebok", "Levi's", "Zara", "H&M",
    "Samsung", "LG", "Sony", "Apple", "Xiaomi", "Philips", "Bosch",
    "Under Armour", "New Balance", "Converse", "Tommy Hilfiger", "Calvin Klein",
    "Asics", "Fila", "Vans", "Champion", "North Face",
    "Dell", "HP", "Acer", "Lenovo", "MSI",
    "Canon", "Nikon", "GoPro", "Panasonic", "Olympus",
    "JBL", "Beats", "Sennheiser", "Bose", "Sony Audio",
    "Huawei", "OnePlus", "Google", "Motorola", "Asus",
    "Whirlpool", "Electrolux", "Midea", "Haier", "Toshiba",
]

clothing_categories = [
    "Футболка", "Джинсы", "Куртка", "Кроссовки", "Платье", "Юбка", "Пальто", "Рубашка",
    "Шорты", "Свитер", "Брюки", "Толстовка", "Пиджак", "Плащ", "Плавки", "Носки",
    "Перчатки", "Шапка", "Шарф", "Пояс"
]

electronics_categories = [
    "Смартфон", "Ноутбук", "Планшет", "Телевизор", "Наушники", "Умные часы", "Камера",
    "Монитор", "Проектор", "Принтер", "МФУ", "Компьютер", "Игровая консоль", "Гарнитура",
    "Фитнес-трекер", "Портативная колонка", "Электробритва", "Эпилятор", "Фен", "Мультиварка"
]

colors = ["Красный", "Синий", "Зеленый", "Черный", "Белый", "Желтый", "Фиолетовый", "Серый",
          "Оранжевый", "Розовый", "Коричневый", "Бежевый", "Голубой", "Бирюзовый", "Салатовый"]

models = {
    "Nike": ["Air Max", "Blazer", "Cortez", "Air Force 1", "Jordan"],
    "Adidas": ["Superstar", "Stan Smith", "Ultraboost", "NMD", "Yeezy"],
    "Puma": ["RS-X", "Suede", "Basket Classic", "Cali", "Thunder"],
    "Reebok": ["Classic Leather", "Club C", "Freestyle Hi", "Aztrek", "DMX Series"],
    "Levi's": ["501", "511", "514", "505", "512"],
    "Zara": ["Basic Fit", "Slim Fit", "Relaxed Fit", "Oversized", "Skinny"],
    "H&M": ["Regular Fit", "Slim Fit", "Loose Fit", "Straight Fit", "Baggy"],
    "Samsung": ["Galaxy S", "Galaxy A", "Galaxy Note", "Galaxy M", "Galaxy Z"],
    "LG": ["G Series", "V Series", "K Series", "Q Series", "NanoCell"],
    "Sony": ["Xperia X", "Xperia L", "Xperia Z", "Xperia Pro", "Xperia 1"],
    "Apple": ["iPhone", "iPad", "MacBook", "iMac", "Apple Watch"],
    "Xiaomi": ["Mi", "Redmi", "Poco", "Black Shark", "Mi Mix"],
    "Philips": ["Serie 500/XMLSchema", "Serie 7000", "Serie 9000", "Serie 2000", "Serie 3000"],
    "Bosch": ["Series 4", "Series 6", "Series 8", "Series 2", "Series 10"],
    "Under Armour": ["HOVR", "Charged", "Speedform", "HeatGear", "ColdGear"],
    "New Balance": ["Fresh Foam", "FuelCell", "574", "990", "327"],
    "Converse": ["Chuck Taylor", "One Star", "Jack Purcell", "Pro Blaze", "Weapon"],
    "Tommy Hilfiger": ["Essential", "Signature", "Iconic", "Heritage", "Modern Prep"],
    "Calvin Klein": ["Modern Cotton", "Seductive Comfort", "Invisible", "Microfiber", "Perfectly Fit"],
    "Asics": ["Gel-Kayano", "Gel-Nimbus", "GT-2000", "Gel-Cumulus", "Gel-Quantum"],
    "Fila": ["Disruptor", "Ray", "Grant Hill", "Original Fitness", "V94M"],
    "Vans": ["Old Skool", "Authentic", "Sk8-Hi", "Slip-On", "Era"],
    "Champion": ["Reverse Weave", "Powerblend", "Graphic Tee", "Absolute Leggings", "Retro Shorts"],
    "North Face": ["Thermoball", "Denali", "Ventrix", "Fusion", "Apex"],
    "Dell": ["XPS", "Inspiron", "Alienware", "Latitude", "Precision"],
    "HP": ["Pavilion", "Spectre", "Envy", "OMEN", "ProBook"],
    "Acer": ["Aspire", "Predator", "Nitro", "Swift", "TravelMate"],
    "Lenovo": ["ThinkPad", "Yoga", "Legion", "IdeaPad", "Flex"],
    "MSI": ["GS", "GE", "GP", "GL", "GF"],
    "Canon": ["EOS", "PowerShot", "IXUS", "EF", "RF"],
    "Nikon": ["D", "Z", "COOLPIX", "AF-S", "Nikkor"],
    "GoPro": ["Hero", "Max", "Fusion", "Session", "Omni"],
    "Panasonic": ["Lumix", "HC", "AG", "GH", "G"],
    "Olympus": ["OM-D", "PEN", "Stylus", "SP", "TG"],
    "JBL": ["Flip", "Charge", "Clip", "Endurance", "Reflect"],
    "Beats": ["Solo", "Studio", "Powerbeats", "Pro", "Flex"],
    "Sennheiser": ["Momentum", "CX", "HD", "IE", "Amperior"],
    "Bose": ["QuietComfort", "SoundLink", "Noise Cancelling", "Sleepbuds", "Frames"],
    "Sony Audio": ["WH", "WF", "MDR", "IER", "EXTRA BASS"],
    "Huawei": ["P", "Mate", "Nova", "Enjoy", "Y"],
    "OnePlus": ["8", "7", "6", "5", "Nord"],
    "Google": ["Pixel", "Nest", "Daydream", "Stadia", "Fitbit"],
    "Motorola": ["Moto G", "Moto E", "Moto Z", "One", "Edge"],
    "Asus": ["ROG", "ZenBook", "VivoBook", "TUF", "Chromebook"],
    "Whirlpool": ["Affresh", "Cabrio", "Wash2Dry", "EveryDrop", "Swash"],
    "Electrolux": ["EcoInverter", "PureSteam", "UltraMix", "OptiSense", "QuickPro"],
    "Midea": ["CoolWind", "EasyClean", "FreshFlow", "SmartSensing", "TurboCool"],
    "Haier": ["Cube", "Direct Motion", "Crystal", "AquaSpin", "Dual Drum"],
    "Toshiba": ["Dynabook", "Canvio", "FlashAir", "TransMemory", "Encore"]
}

def generate_product_name():
    if random.random() > 0.5:
        # Генерируем товар из категории одежды
        brand = random.choice(brands[:20])  # Бренды одежды
        category = random.choice(clothing_categories)
        color = random.choice(colors)
        model = random.choice(models.get(brand, ["Model"]))  # Если у бренда нет моделей, используем заглушку
        return f"{brand} {model} {category} ({color})"
    else:
        # Генерируем товар из категории электроники
        brand = random.choice(brands[20:])  # Бренды электроники
        category = random.choice(electronics_categories)
        model = random.choice(models.get(brand, ["Model"]))  # Если у бренда нет моделей, используем заглушку

        if category == "Смартфон":
            memory = random.choice(["64GB", "128GB", "256GB", "512GB"])
            return f"{brand} {model} {category} ({memory})"
        elif category == "Телевизор":
            size = random.choice(["43''", "55''", "65''", "75''"])
            return f"{brand} {model} {category} ({size})"
        elif category == "Ноутбук":
            ram = random.choice(["8GB", "16GB", "32GB"])
            storage = random.choice(["256GB SSD", "512GB SSD", "1TB HDD"])
            return f"{brand} {model} {category} ({ram}, {storage})"
        elif category == "Монитор":
            size = random.choice(["24''", "27''", "32''", "34''"])
            return f"{brand} {model} {category} ({size})"
        elif category == "Проектор":
            resolution = random.choice(["1080p", "4K", "720p"])
            return f"{brand} {model} {category} ({resolution})"
        elif category == "Принтер":
            type_print = random.choice(["Лазерный", "Струйный", "МФУ"])
            return f"{brand} {model} {category} ({type_print})"
        elif category == "Компьютер":
            cpu = random.choice(["Intel i5", "Intel i7", "AMD Ryzen 5", "AMD Ryzen 7"])
            return f"{brand} {model} {category} ({cpu})"
        elif category == "Игровая консоль":
            version = random.choice(["Standard", "Pro", "Lite"])
            return f"{brand} {model} {category} ({version})"
        elif category == "Гарнитура":
            connection = random.choice(["Bluetooth", "Wired"])
            return f"{brand} {model} {category} ({connection})"
        elif category == "Фитнес-трекер":
            features = random.choice(["Heart Rate", "GPS", "Waterproof"])
            return f"{brand} {model} {category} ({features})"
        elif category == "Портативная колонка":
            battery = random.choice(["10h", "20h", "30h"])
            return f"{brand} {model} {category} ({battery})"
        elif category == "Электробритва":
            blades = random.choice(["3 Blades", "5 Blades", "Rotary"])
            return f"{brand} {model} {category} ({blades})"
        elif category == "Эпилятор":
            speed = random.choice(["Fast", "Slow", "Variable"])
            return f"{brand} {model} {category} ({speed})"
        elif category == "Фен":
            power = random.choice(["1000W", "1500W", "2000W"])
            return f"{brand} {model} {category} ({power})"
        elif category == "Мультиварка":
            capacity = random.choice(["3L", "5L", "7L"])
            return f"{brand} {model} {category} ({capacity})"
        else:
            return f"{brand} {model} {category}"

def generate_description(product_name):
    if any(category in product_name for category in clothing_categories):
        # Описание для одежды
        return fake.sentence(nb_words=10) + f" Эта {product_name.lower()} изготовлена из высококачественных материалов и разработана для комфорта и стиля."
    else:
        # Описание для техники
        if "Смартфон" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} предлагает мощную производительность благодаря своим передовым функциям и стильному дизайну."
        elif "Ноутбук" in product_name or "Компьютер" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивает отличную производительность и портативность, идеально подходящую для работы и развлечений."
        elif "Телевизор" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивает потрясающее качество изображения и погружает вас в звук, улучшая ваш опыт просмотра."
        elif "Наушники" in product_name or "Гарнитура" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивают исключительное качество звука и комфорт, делая их идеальными для любителей музыки."
        elif "Умные часы" in product_name or "Фитнес-трекер" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} сочетают стиль и функциональность, помогая вам оставаться на связи и следить за временем."
        elif "Камера" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} позволяет делать потрясающие фотографии и видео благодаря своим передовым функциям и простоте использования."
        elif "Монитор" in product_name or "Проектор" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивает четкое изображение и удобство использования для различных задач."
        elif "Принтер" in product_name or "МФУ" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} предоставляет надежные возможности печати для дома и офиса."
        elif "Игровая консоль" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} предлагает захватывающий игровой опыт с множеством эксклюзивных игр."
        elif "Портативная колонка" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивает качественный звук и мобильность для ваших мероприятий."
        elif "Электробритва" in product_name or "Эпилятор" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} обеспечивает эффективное удаление волос и комфортное использование."
        elif "Фен" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} предлагает быстрое высыхание и защиту ваших волос."
        elif "Мультиварка" in product_name:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} позволяет готовить вкусные блюда легко и быстро."
        else:
            return fake.sentence(nb_words=10) + f" {product_name.lower()} является надежным и универсальным устройством, которое удовлетворяет всем вашим потребностям."

async def is_unique_name(session, name):
    result = await session.execute(select(ShopItem).where(ShopItem.name == name))
    return result.scalar() is None

async def generate_shop_items(num_items=100000):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    added_articles = set()  # Для уникальности артикулов

    async with AsyncSessionLocal() as session:
        for _ in range(num_items):
            while True:
                article = random.randint(1000, 99999)  # Генерируем случайный артикул
                if article not in added_articles:
                    added_articles.add(article)
                    break

            while True:
                name = generate_product_name()  # Генерируем осмысленное имя товара
                if await is_unique_name(session, name):
                    break

            price = round(random.uniform(100, 100000), 2)  # Генерируем случайную цену от 100 до 100,000 рублей
            description = generate_description(name)  # Генерируем осмысленное описание товара
            path_to_photo = ""  # Путь до фото оставляем пустым

            shop_item = ShopItem(
                article=article,
                name=name,
                price=price,
                description=description,
                path_to_photo=path_to_photo
            )

            session.add(shop_item)

        try:
            await session.commit()
            print(f"Успешно добавлено {num_items} товаров.")
        except Exception as e:
            await session.rollback()
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(generate_shop_items(1000))
