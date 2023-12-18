# Stage 1: Build the application
FROM node:latest as build
#RUN npm install -g yarn
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
ARG SERVER_ADDRESS
ENV VITE_SERVER_ADDRESS $SERVER_ADDRESS
RUN yarn build

# Stage 2: Serve the application
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]