FROM nginx

RUN apt-get update; exit 0

RUN apt-get -y install vim

RUN apt-get -y install links

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/

