Базовая настройка проекта

1. Установка виртуального окружения и всех необходимых пакетов

````
python -m venv venv
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
````

2. Настройка переменных окружения в файле `setenv.sh` (Токен для Телеграм бота и данные для подключения к базе данных)
3. Установка переменных окружения
````
./setenv.sh
````
4. Создание и применение миграций моделей
````
python manage.py makemigrations
python manage.py migrate
````
5. Установка и настройка веб-сервера(nginx, apache или любой другой сервер) и Gunicorn
6. Сбор статических файлов
````
python manage.py collectstatic
````

Настройка 