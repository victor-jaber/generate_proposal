FROM node:18-alpine AS build-deps

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . ./

RUN npm run build

# Stage 2 - the production environment
FROM nginx:1.19.2-alpine

COPY --from=build-deps /usr/src/app/.next /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

