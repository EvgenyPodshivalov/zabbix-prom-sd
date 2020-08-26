FROM python:3.7.4-buster

WORKDIR /app

RUN apt -y update
RUN apt -y install libsasl2-dev python-dev libldap2-dev libssl-dev

COPY . /app
RUN pip3 install --requirement /app/requirements.txt

CMD [ "sleep 60", "&&", "python", "./zbxDiscovery.py" ]
