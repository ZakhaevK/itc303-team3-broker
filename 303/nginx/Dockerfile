FROM nginx:1.24
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/nginx/modules-enabled
COPY ./content/index.html /usr/share/nginx/html/index.html
COPY ./conf/nginx.conf /etc/nginx/nginx.conf
COPY ./conf/60-mqtt-stream.conf /etc/nginx/modules-enabled/60-mqtt-stream.conf
EXPOSE 80
