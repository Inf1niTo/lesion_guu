# Используем базовый образ Python
FROM python:3.10

# Копируем код приложения в контейнер
WORKDIR /djangotutorial/
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для доступа к приложению
EXPOSE 8000

# Запускаем приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]