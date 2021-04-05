FROM node:lts-buster-slim
WORKDIR /src

COPY package.json /src
COPY yarn.lock /src

RUN npm install yarn
RUN yarn install

CMD ["yarn", "start"]