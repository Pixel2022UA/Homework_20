__Для ДЗ №24 ( API для продажу книг )__

1. Создание ордера и плучение ссылки (POST /orders)
    - https://mylibrary-e460551407b2.herokuapp.com/api/orders/
    - В body необходимо указать id книги и ее количество или их список. Пример: {"order": [{"book_id": 1,"quantity": 19 }, {"book_id": 4,"quantity": 500 }]}
    - по ссылке с GET запросом можно увидеть что статус ордера "create".
   
2. Далее переходим по ссылке и заполняем платежную форму. Можно аопользоватся этими данными: 
   - Номер карты: 5148048444679915, Срок дейтсвия: 12/26, CVV: 123
   - по ссылке с GET запросом можно увидеть что статус ордера изменился на "processing"

3. Далее на странице нажимаем "Подтверждаю". После по ссылке с GET запросом можно увидеть что статус ордера изменился на "created"

__Для ДЗ №23 ( API Auth )__

- #Список ссылок для проверки ДЗ:
- :exclamation: __В Postman для корректной работы в конце каждой URL необходимо добавлять "/"__ :exclamation:

1. Регистрация и получение токена ( POST/register/)
- Можно использовать Postman или генератор запроса через Swagger.
- Получаем токен, для этого нужно создать логин и пароль в теле запроса.
- Пример: {"username":"user123", "password":"123456789"}

- После получения токена в Postman во вкладке Headers в поле Key=Authorization, а в поле Value вписать ваш токен, :exclamation:НО перед токеном написать Token, ниже пример.
- ![](https://github.com/Pixel2022UA/Homework_20/blob/main/images/image1.png)

- :exclamation: Используя Swagger при авторизации необходимо так же прописывать Token перед самим токеном.

2. Получаем список всех книг (GET /books) - для всех пользователей:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/
- 1.1. Фильтрация по названию, после знака "=", в конце ссылки, необходимо написать название книги(title):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?title=
- 1.2. Фильтрация по автору, после знака "=", в конце ссылки, необходимо написать имя автора:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?author=
- 1.3. Фильтрация по жанру, после знака "=", в конце ссылки, необходимо написать жанр книг:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?genre=

3. Получаем конкретную книгу по ID (GET /books/{id}) - для всех пользователей:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

4. Добавляем новую книгу (POST /books) - __только для зарегестрированных пользователей__:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/
   - Для примера можно использовать этот шаблон: 
{"title": "Third book", "author": "Ilon", "genre": "Thriller", "publication_date": "2019-02-04"}

5. Обновляем данные определенной книги по ID (PUT /books/{id}) - __только для зарегестрированных пользователей__:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)
   - Для примера можно использовать этот шаблон: 
{"title": "Third book", "author": "Ilon", "genre": "Thriller", "publication_date": "2019-02-04"}
   - __Можно изменить как все данные так и часть данных__, к примеру только {"author": "Ilon"}

6. Удаление книги по ID (DELETE /books/{id}) - __только для зарегестрированных пользователей__:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

7. Получаем список всех авторов (GET /authors) - для всех пользователей: 
   - https://mylibrary-e460551407b2.herokuapp.com/api/authors
- 6.1. Фильтрация по имени автора, после знака "=", в конце ссылки, необходимо написать имя:
   - https://mylibrary-e460551407b2.herokuapp.com/api/authors/?name=   

8. Полчаем информацию об авторе по ID (GET /authors/{id}) - для всех пользователей:
    - https://mylibrary-e460551407b2.herokuapp.com/api/authors/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

9. Для запуска тестов необходимо:
   - Скопируйте проект по ссылке: https://github.com/Pixel2022UA/Homework_20
   - Откройте проект в PyCharm и установите необходимые зависимости из файла requirements.txt, используя команду pip install -r requirements.txt
   - Создаем базу данных командами python manage.py makemigrations, python manage.py migrate (:exclamation: __В PyCharm убедитесь, что вы находитесь в директории, где расположены файлы проекта и файл manage.py__)
   - Для запуска тестов введите команду python manage.py test

-------------------------------------------------------------------------------------

__Для ДЗ №22 ( Docker-изація )__
1. Скопируйте проект по ссылке:
    - https://github.com/Pixel2022UA/Homework_20

2. Откройте проект в PyCharm и убедитесь, что вы находитесь в директории, где расположены файлы проекта и файл manage.py

3. __Скопируйте прикрепленный в LMS Hillel файл .env в корневую директорию проекта (в директорию с фалом manage.py).__

4. Для создания образа проекта выполните команду:
    - docker compose up

5. После создания образа, для проверки проекта, можно воспользоваться ссылкой http://0.0.0.0:8000/ .  Postgres и Redis подключены к Heroku
используя .env файл переданный в LMS hillel.


-------------------------------------------------------------------------------------
__Для ДЗ №20-21 ( API & Opne API )__
- #Список ссылок для проверки ДЗ:
- :exclamation: __В Postman для корректной работы в конце каждой URL необходимо добавлять "/"__ :exclamation:

1. Получаем список всех книг (GET /books):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/
- 1.1. Фильтрация по названию, после знака "=", в конце ссылки, необходимо написать название книги:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?title=
- 1.2. Фильтрация по автору, после знака "=", в конце ссылки, необходимо написать имя автора:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?author=
- 1.3. Фильтрация по жанру, после знака "=", в конце ссылки, необходимо написать жанр книг:
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/?genre=

2. Получаем конкретную книгу по ID (GET /books/{id}):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

3. Добавляем новую книгу (POST /books):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/
   - Для примера можно использовать этот шаблон: 
{"title": "Third book", "author": "Ilon", "genre": "Thriller", "publication_date": "2019-02-04"}

4. Обновляем данные определенной книги по ID (PUT /books/{id}):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)
   - Для примера можно использовать этот шаблон: 
{"title": "Third book", "author": "Ilon", "genre": "Thriller", "publication_date": "2019-02-04"}
   - __Можно изменить как все данные так и часть данных__, к примеру только {"author": "Ilon"}

5. Удаление книги по ID (DELETE /books/{id}):
   - https://mylibrary-e460551407b2.herokuapp.com/api/books/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

6. Получаем список всех авторов (GET /authors): 
   - https://mylibrary-e460551407b2.herokuapp.com/api/authors
- 6.1. Фильтрация по имени автора, после знака "=", в конце ссылки, необходимо написать имя:
   - https://mylibrary-e460551407b2.herokuapp.com/api/authors/?name=   

7. Полчаем информацию об авторе по ID (GET /authors/{id}):
    - https://mylibrary-e460551407b2.herokuapp.com/api/authors/   __(В конце ссылки ввести число-ID книги)__  (не забываем "/" в конце)

8. Для запуска тестов необходимо:
   - Скопируйте проект по ссылке: https://github.com/Pixel2022UA/Homework_20
   - Откройте проект в PyCharm и установите необходимые зависимости из файла requirements.txt, используя команду pip install -r requirements.txt
   - Создаем базу данных командами python manage.py makemigrations, python manage.py migrate (:exclamation: __В PyCharm убедитесь, что вы находитесь в директории, где расположены файлы проекта и файл manage.py__)
   - Для запуска тестов введите команду python manage.py test