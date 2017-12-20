FROM python:2.7
MAINTAINER Jiming_Ye

RUN mkdir -p /usr/src/myapp

WORKDIR /usr/src/myapp

COPY requirements.txt /usr/src/myapp
RUN pip install -r requirements.txt

COPY . /usr/src/myapp

EXPOSE 5000

CMD ["python", "test.py"]