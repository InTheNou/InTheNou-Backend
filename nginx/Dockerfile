FROM nginx
ARG config
RUN rm /etc/nginx/conf.d/default.conf
RUN echo ${config}

COPY ${config} /etc/nginx/conf.d/

ADD ssl /etc/nginx/ssl/
RUN chown -R root:root /etc/nginx/ssl
RUN chmod -R 700 /etc/nginx/ssl