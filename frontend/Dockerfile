FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR proj/frontend/

COPY . /proj/frontend/

RUN npm install

RUN npm run build

EXPOSE 8080

CMD [ "http-server", "dist" ]
