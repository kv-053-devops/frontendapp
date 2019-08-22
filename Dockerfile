FROM python:3.6-alpine

COPY server_flask.py forms.py requirements.txt /home/app/
COPY templates/* /home/app/templates/

RUN adduser -D -h /home/app app && pip3 install -r /home/app/requirements.txt

WORKDIR /home/app

USER app

ENTRYPOINT ["python3", "server_flask.py"]
