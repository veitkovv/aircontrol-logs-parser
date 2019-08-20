# The instructions for the first stage
FROM node:alpine as builder

COPY package*.json ./

RUN npm install

# The instructions for second stage
FROM node:alpine

WORKDIR /opt/alp/frontend

COPY --from=builder node_modules node_modules

ADD . .

RUN npm run build

CMD [ "npm", "run", "serve" ]
