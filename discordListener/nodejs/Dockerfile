FROM node:14.5.0

WORKDIR /nodejs
ADD index.js /nodejs/index.js
ADD package.json /nodejs/package.json
ADD keys.json /nodejs/keys.json
# RUN ["npm", "install", "/nodejs", "-f"]
RUN ["npm", "install", "/nodejs"]
CMD [ "node", "/nodejs/index.js"]