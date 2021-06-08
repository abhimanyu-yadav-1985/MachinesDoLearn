FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y gnupg2
RUN apt-get install -y g++

RUN apt install curl -y

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update

RUN ACCEPT_EULA=Y apt install -y msodbcsql17

RUN ACCEPT_EULA=Y apt install -y mssql-tools

RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bashrc'
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bash_profile'

RUN apt-get install -y unixodbc-dev

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app/


ENTRYPOINT [ "python3" ]
CMD ["app.py"]