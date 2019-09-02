# The instructions for the first stage
FROM node:stretch as builder

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y openssh-server

COPY package*.json ./

RUN npm install

# The instructions for second stage
FROM node:stretch

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y openssh-server

WORKDIR /opt/alp/frontend

COPY --from=builder node_modules node_modules

ADD . .

RUN npm run build

CMD [ "npm", "run", "serve" ]
