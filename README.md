### for reviewer:
foodgram_domain: https://nemnogofoodgram.ddns.net

admin_login: admin2

admin_password: 20001013zzz

### ------------------------------------------------------------

# Проект foodgram

Проект доступен по адресу:

https://nemnogofoodgram.ddns.net


## Описание
Проект foodgram создан в рамках учёбы в Практикуме на курсе backend-разработчика.

Данный проект является соц.сетью, где пользователи могут делится своими рецептами, а также изучать рецепты других пользователей.
У пользователей есть возможности подписываться друг на друга, добавлять рецепты в избранное, постить собственные рецепты, а также сохранять рецепты в список покупок с последующим скачиванием списка с формате PDF.

## Стек технологий, использованных в проекте:
- Python
- Django
- DRF
- Docker
- PostgreSQL
- nginx
- gunicorn
- GitHub Actions

## Как запустить проект локально:

### Клонируйте репозиторий

```bash
git clone git@github.com:nemnogospaal/foodgram-project-react.git
```

### В репозитории перейдите в /infra

Находясь в /infra, выполните команду:

```bash
docker compose up
```

Затем откройте новый терминал и соберите необходимую статику:

```bash
docker compose exec backend python manage.py collectstatic
```

```bash
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```

Выполните миграции:

```bash
docker compose exec backend python manage.py migrate
```

Создайте суперпользователя:

```bash
docker compose exec backend python manage.py createsuperuser
```

Заполните базу данных ингредиентами:

```bash
docker compose exec backend python manage.py loaddata
```

## Примеры запросов к API:


### Запросы к пользователям/регистрации

```bash
GET /api/users/ - получение списка пользователей
POST /api/users/ - регистрация нового пользователя
GET /api/users/{id}/ - профиль пользователя
GET /api/users/me/ - текущий пользователь
POST /api/users/set_password/ - изменение пароля
```

### Запросы к рецептам/тегам/избранным рецептам/списку покупок

```bash
GET /api/recipes/ - получение списка рецептов
POST /api/recipes/ - создание рецепта
GET /api/recipes/{id}/ - получение отдельного рецепта
DELETE /api/recipes/{id}/ - удаление рецепта
PATCH /api/recipes/{id}/ - обновление рецепта
```

```bash
GET /api/recipes/download_shopping_cart/ - скачать список покупок
POST /api/recipes/{id}/shopping_cart/ - добавление рецепта в список покупок
DELETE /api/recipes/{id}/shopping_cart/ - удаление рецепта из списка покупок
```

```bash
POST /api/recipes/{id}/favorite/ - добавление рецепта в избранное
DELETE /api/recipes/{id}/favorite/ - удаление рецепта из избранного
```

```bash
GET /api/tags/ - получение списка тегов
GET /api/tags/{id}/ - получение отдельного тега
```

### Автор:

Ивлев Павел
г. Владивосток
telegram: @pashkmsnv
