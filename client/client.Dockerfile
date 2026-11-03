FROM node:25-alpine3.22 AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ARG VITE_SERVER_IP
ARG VITE_SERVER_BACKEND_PORT

ENV VITE_SERVER_IP=$VITE_SERVER_IP
ENV VITE_SERVER_BACKEND_PORT=$VITE_SERVER_BACKEND_PORT

RUN npm run build

FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 80

ENTRYPOINT ["/start.sh"]
