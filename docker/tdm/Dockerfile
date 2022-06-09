FROM python:3.7.2

#For Oracle instant client installation

WORKDIR /opt/oracle

ADD ./tdm/instantclient-basic-linux.x64-18.5.0.0.0dbru.zip /opt/oracle

RUN unzip instantclient-basic-linux.x64-18.5.0.0.0dbru.zip

RUN apt-get update

RUN apt-get install libaio1

RUN sh -c "echo /opt/oracle/instantclient_18_5 > /etc/ld.so.conf.d/oracle-instantclient.conf"

RUN ldconfig

COPY ./tdm/tnsnames.ora /opt/oracle/instantclient_18_5/network/admin

#Setting environment variables

ENV PYTHONDONTWRITEBYTECODE 1 #PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to dis

ENV PYTHONUNBUFFERED 1 #PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr

ENV FLASK_APP=run.py

ENV FLASK_ENV=development

#Installing required package for basket_service

WORKDIR /tdm

ADD ./tdm/requirements.txt /tdm

RUN pip3 install --upgrade pip

RUN PATH=$PATH:/usr/pgsql-9.3/bin/ pip3 install psycopg2

RUN pip3 --no-cache-dir install -r requirements.txt

# Configure ssh connections

COPY ./tdm/ssh /root/.ssh

RUN chmod 700 /root/.ssh

RUN chmod 600 /root/.ssh/*

#Add source code to container

ADD ./tdm /tdm

#Change directory to proper file

WORKDIR /tdm/flask_app

EXPOSE 5000

CMD gunicorn -w 10 --bind 0.0.0:5000 run:app --timeout 2500

