FROM node:alpine

ENV NODE_ENV development
ENV NODE_OPTIONS=--openssl-legacy-provider
COPY ./frontend/package.json ./
RUN apk update && npm install --save --legacy-peer-deps

ENV HOST 0.0.0.0
EXPOSE 3000