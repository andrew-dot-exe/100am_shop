# 100am_shop
not one-week project. Stack: FastAPI, SQLAlchemy, PostgreSQL

## Постановка задачи. Первое приближение
Реализовать REST-ful интернет магазин
Для функционирования сервиса понадобятся:
- реализовать работу с пользователями, разграничение прав доступа (покупатель, администратор), реализовать регистрацию;
    - роли продавца не будет, т.к. это не маркетплейс, но можно записать в TODO.
- реализовать работу с товарами, корзину и оплату
    - в качестве оплаты сделать заглушку

###  Приближение два. Сторона пользователей
Теперь более подробно о каждом из пунктов. Для начала, как вообще должен работать сервис для пользователя.
Пользователь входит при помощи логина и пароля, либо регистрируется в нем. После входа/регистрации он выбирает товары и помещает их в свою корзину. При переходе в корзину, пользователь может увеличить/уменьшить количество товара в его исчисляемой единице (кг, штук, etc.), удалить товар, а также оформить заказ. При оформлении заказа, пользователь вводит данные, выбирает пункт выдачи, "оплачивает" товар и получает уникальный номер заказа и QR-код для его выдачи.
Пользователь может посмотреть историю заказов, какие товары были заказаны
Администратор добавляет тот или иной товар, его наличие в магазинах, но не имеет доступ к личным данным покупателей (Ф.И., номер телефона).
    
### Приближение три. Сторона сервера
Здесь уже техническая реализация, без оглядки на фронтенд
Сервер через отдельный API Endpoint получает пару логин-пароль и выдает JWT-токен пользователя, который хранит в себе то, что это - юзер. Пользователь на фронтенде выбирает товары, которые попадают в его корзину, содержимое которой хранится в базе данных (интересно, насколько это эффективно и нужно ли noSQL), При переходе пользователя на фронтенде в корзину, пользователь может удалить или изменить состав корзины, либо оформить заказ. После оформления заказа, корзина очищается.
Оформление заказа происходит так: эндпоинт передает стоимость заказа шлюзу оплаты, бронирует (уменьшает на выбранное пользователем количество товаров из корзины в общем числе наличия), передает на шлюз оплаты стоимость заказа, получает ответ от шлюза, и, либо отменяет заказ в случае неудачной оплаты, либо возвращает номер заказа и формирует QR-код для заказа.
Администратор получает свой JWT-токен с ролью админа и может с эти токеном вызывать эндпоинты для добавления, редактирования и удаления тех или иных товаров.

### Товар, карточка товара, что в нее входит
У каждого товара есть артикул, название и стоимость. Дополнительно у товара может быть фотография и описание товара. Артикул - первичный ключ.
Категорий пока не будет.

### База данных
Будет использоваться Postgres, работа с базой через ORM. База будет создаваться по описанию модели в SQLAlchemy. Пароли будут хранится в зашифрованном виде.
Сущности: пользователь, товар, заказы, заказнные товары (ассоциативная сущность), корзина (ассоциативная сущность), магазины, наличие товара в магазине (ассоциативная сущность). 
Сумма корзины будет вычисляться на сервере при изменении количества товара и получения содержимого корзины. 
Схема данных выглядит так:
![Схема данных](/readme-content/database.jpg)
