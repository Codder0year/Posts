Ваша задача — разработать приложение, в котором пользователи могут писать посты и комментировать их.
Создайте модели и соответствующие точки API для взаимодействия с ними.

Технические требования:

Python 3.8+
Django 3+
DRF 3.10+
PostgreSQL 10+
Структура приложения
Задача 1
МОДЕЛИ
Модель пользователя
логин
пароль
номер
дата рождения
дата создания
дата редактирования
Модель поста
заголовок
текст
изображение (если есть)
автор
комментарии
дата создания
дата редактирования
Модель комментария
автор
текст
дата создания
дата редактирования
Примечание: связи между моделями определите самостоятельно.
Задача 2
ЭНДПОИНТЫ
Реализуйте CRUD для каждой модели.

Пользователь:
CREATE: все пользователи (регистрация).
READ: администратор/авторизованные пользователи.
UPDATE: администратор/пользователь может редактировать только себя./
DELETE: администратор.
Пост:
CREATE: авторизованные пользователи.
READ: все пользователи.
UPDATE: администратор/пользователь может редактировать только себя.
DELETE: администратор/пользователь может удалять свои посты.
Комментарий:
CREATE: авторизованные пользователи.
READ: все пользователи.
UPDATE: администратор/пользователь может редактировать только себя.
DELETE: администратор/пользователь может удалять свои комментарии.
Задача 3
ВАЛИДАТОРЫ
Модель пользователя

Реализуйте валидатор для пароля (должен быть не менее 8 символов, должен включать цифры).

Реализуйте валидатор для почты (разрешены домены: mail.ru, yandex.ru).

Модель поста

Реализуйте проверку того, что автор поста достиг возраста 18 лет.

Реализуйте проверку, что автор в заголовок не вписал запрещенные слова: ерунда, глупость, чепуха.

Задача 4
АДМИН. ПАНЕЛЬ
Добавьте в объекте поста ссылку на автора.

Добавьте фильтр по дате создания поста.

Руководство по использованию проекта
Клонируйте репозиторий:git clone

https://github.com/elenaludina0573/Post_and_comments

Установите зависимости:

pip install -r requirements.txt

Примените миграции:

python manage.py makemigrations

python manage.py migrate

Создайте суперпользователя:

python manage.py csu

Запустите сервер разработки:

python manage.py runserver