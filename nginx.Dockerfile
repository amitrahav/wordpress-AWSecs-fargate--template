FROM nginx:latest

COPY ./site /var/www/html
COPY ./config/nginx /etc/nginx/conf.d