FROM python:3.8
RUN apt-get update

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app/

CMD ["gunicorn", "--reload"  , "--bind", "0.0.0.0:80", "app:server"]
