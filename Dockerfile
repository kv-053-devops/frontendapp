FROM python:3.6-alpine

COPY server_flask.py forms.py requirments.txt /home/app/
COPY templates/* /home/app/templates/

RUN adduser -D -h /home/app app && pip3 install -r /home/app/requirments.txt

WORKDIR /home/app

USER app

ENTRYPOINT ["python3", "server_flask.py"]
