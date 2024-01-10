FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./proxy-runner.sh /proxy-runner.sh

RUN apk add --no-cache openssl bash
RUN chmod +x /proxy-runner.sh

VOLUME /vol/www

CMD ["/proxy-runner.sh"]

EXPOSE 80
