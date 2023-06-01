FROM nginxinc/nginx-unprivileged:1.19-alpine

USER root

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /usr/share/nginx/html/static

COPY ./vol/static /usr/share/nginx/html/static
RUN chown -R nginx:nginx /usr/share/nginx/html

