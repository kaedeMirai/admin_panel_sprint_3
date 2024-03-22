# Проект "Онлайн Кинотеатр"

## Сервис ETL

Репозиторий для сервиса ETL (Extract, Transform, Load), отвечающего за передачу данных из базы данных PostgreSQL в хранилище Elastic. Этот сервис часть проекта "Онлайн Кинотеатр" и обеспечивает обновление поискового индекса с информацией о фильмах, жанрах, актёрах и других сущностях.

## Содержание:

- [Django Admin Panel](https://github.com/kaedeMirai/new_admin_panel_sprint_1) - **Панель администратора для управления контентом**
- [ETL](https://github.com/kaedeMirai/admin_panel_sprint_3) - **Перенос данных из PostgreSQL в ElasticSearch для реализации полнотекстового поиска.**
- [Auth](https://github.com/kaedeMirai/Auth_sprint_1-2) - **Аутентификация и авторизация пользователей на сайте с системой ролей.**
- [UGC](https://github.com/kaedeMirai/ugc_sprint_1) - **Сервис для удобного хранения аналитической информации и UGC.**
- [UGC +](https://github.com/kaedeMirai/ugc_sprint_2) - **Улучшение функционала UGC внедрением CI/CD процессов и настройкой системы логирования Setnry и ELK.**
- [Notification service](https://github.com/kaedeMirai/notifications_sprint_1) - **Отправка уведомлений пользователям о важных событиях и акциях в кинотеатре.**
- [Watch Together service](https://github.com/kaedeMirai/graduate_work) - **Позволяет пользователям смотреть фильмы совместно в реальном времени, обеспечивая синхронизацию видео и чата.**

## Примечания
1. Если уже есть заполненная база Postgresql, то можно указать **volume**, в котором она лежит. Иначе база будет создана и заполнена с нуля с помощью дампа, который лежит в проекте.

## Запуск проекта
1. Склонировать репозиторий
    ```
    git clone https://github.com/Munewxar/new_admin_panel_sprint_3.git
    ```
2. Скопировать .env.example в .env и заполнить его
3. Запустить приложение
    ```
    docker compose up
    ```
