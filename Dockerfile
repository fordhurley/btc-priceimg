FROM python:2-onbuild

EXPOSE 5002

CMD [ "python", "./serve.py" ]
