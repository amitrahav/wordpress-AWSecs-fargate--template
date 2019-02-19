FROM ${php-fpm-image/wp-engine}:latest

COPY ./site /var/www/html
COPY ./config/php-fpm /usr/local/etc/php-fpm.d
COPY ./config/php-fpm/logs.ini /usr/local/etc/php/conf.d/logs.ini