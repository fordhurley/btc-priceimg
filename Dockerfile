FROM python:2.7.9

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 5002

CMD [ "python", "./serve.py" ]
