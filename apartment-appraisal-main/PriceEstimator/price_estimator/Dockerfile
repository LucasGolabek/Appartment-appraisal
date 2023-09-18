FROM node:latest
ENV NODE_ENV=production
WORKDIR /frontend
COPY . /frontend/
RUN npm install -g n
RUN n 16.15.0
RUN n use 16.15.0
RUN npm install --production
