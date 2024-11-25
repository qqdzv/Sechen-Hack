FROM python:3.11

RUN apt-get update && apt-get install -y libgl1

WORKDIR /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Устанавливаем рабочую директорию
COPY . /app

# Копируем файлы проекта в контейнер
COPY . .