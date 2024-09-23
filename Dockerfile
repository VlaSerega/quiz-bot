# Используем официальный образ Python в качестве базового
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /quiz

# Копируем файл зависимостей
COPY requirements.txt /quiz/

RUN apt-get -y update
RUN apt-get -y upgrade

# Устанавливаем зависимости Python
RUN pip install --progress-bar off -r requirements.txt

# Копируем код приложения в контейнер
COPY . /quiz/

# Команда для запуска приложения
CMD ["python3", "main.py"]

