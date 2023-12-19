# Use an official Node.js runtime as a parent image
FROM node:16-slim

WORKDIR /app
COPY . /app
RUN npm install
CMD [ "npm", "run", "build" ]
