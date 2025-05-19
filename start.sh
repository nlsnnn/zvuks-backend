set -e

echo "Выполняю миграции..."
alembic upgrade head

echo "Запускаю приложение..."
exec uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8080