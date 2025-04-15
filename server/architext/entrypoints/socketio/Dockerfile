FROM python:3.12.8

WORKDIR /usr/src/app

COPY ./server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./server .

ENV NODE_ENV=production

CMD [ "python3", "-m", "architext.entrypoints.socketio.server"]