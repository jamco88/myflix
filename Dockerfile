FROM python:3.6-alpine

RUN adduser -D james

WORKDIR /home/myflix

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY myflix.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP myflix.py

RUN chown -R james:james ./
USER james

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
