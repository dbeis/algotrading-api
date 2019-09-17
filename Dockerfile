FROM python:alpine

LABEL Name=algotrading-api Version=0.0.1
EXPOSE 8080

WORKDIR /app
ADD . /app

ENV SECRET_KEY dev
ENV SQL_DB sqlite:////tmp/test.db

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "-m", "start_api.py"]
