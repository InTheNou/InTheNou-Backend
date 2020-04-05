FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

ADD ssl /etc/nginx/ssl/
RUN chown -R root:root /etc/nginx/ssl
RUN chmod -R 700 /etc/nginx/ssl