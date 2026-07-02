

source /opt/venv/bin/activate

cd /code
RUN_PORT=${RUN_PORT:-8000}
RUN_HOST=${RUN_HOST:-0.0.0.0}

gunicorn -k uvicorn.workers.UvicornWorker main:app --host $RUN_HOST --port $RUN_PORT


