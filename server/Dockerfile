FROM python:3.11.7

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m", "architext.entrypoints.socketio.socketio_server"]
