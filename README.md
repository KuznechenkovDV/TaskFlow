# TaskFlow

TaskFlow — это веб-приложение для управления проектами и задачами с гибкой системой ролей (Администратор, Менеджер проекта, Исполнитель). Приложение реализовано на Django и включает функции аутентификации, регистрации пользователей, управления проектами, задачами, комментариями, загрузки файлов и интеграции с социальными сетями (Google, Yandex, VK).

## Особенности

- **Управление проектами и задачами:**  
  Администратор может создавать, редактировать, просматривать и удалять все проекты и задачи. Менеджер проекта работает только с проектами и задачами, назначенными ему. Исполнитель может просматривать и обновлять статус назначенных задач.
  
- **Фильтрация и сортировка:**  
  Возможность поиска проектов и задач по различным параметрам, сортировка по названию, дате начала, приоритету и т.д.

- **Комментарии и файлы:**  
  Возможность добавления комментариев к задачам с поддержкой AJAX, загрузка файлов и изображений.

- **Профили пользователей и система ролей:**  
  При регистрации автоматически создаётся профиль пользователя, где задаётся роль (по умолчанию – Исполнитель). Администратор имеет возможность редактировать профиль и менять роль.

- **Социальная аутентификация:**  
  Авторизация через Google (с возможностью дальнейшего расширения для Yandex и VK).

- **Интерфейс:**  
  Используется Bootstrap 5 для адаптивного дизайна и отображения данных в виде карточек, форм и таблиц. Карточки проектов оформлены в виде «товаров» с изображением, статусом, назначенным менеджером и датой начала.

## Установка и запуск

TaskFlow использует SQLite в качестве базы данных по умолчанию. Для запуска проекта настройте параметры базы данных, статики и медиа в файле настроек Django, выполните миграции и создайте суперпользователя.

После настройки запустите сервер разработки, и приложение будет доступно по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Использование

- **Регистрация и авторизация:**  
  Пользователи могут регистрироваться через форму или авторизовываться через Google. После входа в систему пользователь попадает в свой профиль, где отображаются его проекты, задачи и другая информация.

- **Управление проектами:**  
  - Администратор может редактировать все проекты.  
  - Менеджер проекта видит и редактирует только свои проекты.  
  На странице списка проектов проекты выводятся в виде карточек с изображением, статусом, именем менеджера и датой начала.

- **Редактирование проектов и задач:**  
  При переходе на страницу деталей проекта или задачи пользователь с нужной ролью может редактировать объект.

## Структура проекта

**TaskFlow/** – главный каталог проекта:
  - **TaskFlow/settings.py** – настройки Django.
  - **TaskFlow/urls.py** – URL-конфигурация проекта.
  - **TaskFlow/wsgi.py** – WSGI-конфигурация.
  - **TaskFlow/asgi.py** – ASGI-конфигурация.

**projects/** – приложение для управления проектами и задачами:
  - **models.py** – модели: Project, Task, Comment, Profile, TaskFile.
  - **views.py** – представления для обработки запросов.
  - **forms.py** – формы для ввода и валидации данных.
  - **urls.py** – маршрутизация URL.
  - **admin.py** – регистрация моделей в админке.
  - **tests.py** – тесты для проверки функциональности.
  - **migrations/** – файлы миграций базы данных.

**media/** – каталог для загруженных файлов:
  - **profile_photos/** – фотографии профиля пользователей.
  - **default_project.jpg** – изображение проекта по умолчанию.

**static/** – статические файлы:
  - **css/** – стили CSS.
  - **js/** – скрипты JavaScript.

**templates/** – HTML-шаблоны:
  - **account/** – шаблоны для работы с аккаунтами:
    - **edit_profile.html** – редактирование профиля.
    - **profile.html** – просмотр профиля.
    - **register.html** – регистрация пользователя.
    - **register_done.html** – подтверждение регистрации.
  - **projects/** – шаблоны для проектов и задач:
    - **project_list.html** – список проектов.
    - **project_detail.html** – детали проекта.
    - **project_form.html** – форма проекта.
    - **task_detail.html** – детали задачи.
    - **task_form.html** – форма задачи.
  - **registration/** – шаблоны для аутентификации:
    - **login.html** – страница входа.
  - **base.html** – базовый шаблон.
  - **index.html** – главная страница.



## Заключение

TaskFlow — это гибкое и расширяемое приложение для управления проектами, которое позволяет пользователям с различными ролями эффективно работать с проектами и задачами, добавлять комментарии и файлы, а также использовать социальную авторизацию через Google. Это стартовая версия, которую можно дорабатывать и расширять в соответствии с потребностями.