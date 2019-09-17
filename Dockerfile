FROM python:alpine

LABEL Name=algotrading-api Version=0.0.1
EXPOSE 8080

WORKDIR /app
ADD . /app

ENV SECRET_KEY dev
ENV SQL_DB sqlite:////tmp/test.db

ENV DISCORD_CRAWLER_HOOK http://yeet.this
ENV DISCORD_API_HOOK http://yeet.this
ENV DISCORD_TRAINING_HOOK http://yeet.this
ENV DISCORD_OPS_HOOK http://yeet.this
ENV DISCORD_TEST_HOOK http://yeet.this

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "-m", "start_api.py"]
