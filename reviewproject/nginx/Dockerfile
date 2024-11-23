FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY ./cert.pem /etc/nginx/cert.pem 
COPY ./private.key /etc/nginx/private.key
COPY ./nginx.conf /etc/nginx/conf.d