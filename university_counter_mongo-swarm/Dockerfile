FROM python:3.8.10-alpine

WORKDIR /app

RUN pip3 install pymongo
RUN pip3 install flask

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["flask", "run"]