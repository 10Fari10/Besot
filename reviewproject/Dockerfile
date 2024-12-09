FROM python:3.12

ENV HOME /home/app
ENV APP_HOME /home/app/web
RUN mkdir $HOME
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static_files
RUN mkdir $APP_HOME/media

WORKDIR $APP_HOME

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput --clear && python manage.py runserver 0.0.0.0:8080