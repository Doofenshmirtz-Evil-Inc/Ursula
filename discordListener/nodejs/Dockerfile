FROM node:14.4.0

WORKDIR /nodejs
ADD index.js /nodejs/index.js
ADD package.json /nodejs/package.json
ADD keys.json /nodejs/keys.json
RUN ["npm", "install", "discord.js-commando", "--save", "-g"]
RUN ["npm", "install", "/nodejs", "-f"]
CMD [ "node", "/nodejs/index.js"]