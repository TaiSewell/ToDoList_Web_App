# Stage 1: Build the React app
FROM node:18 as build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

RUN dir /app/src/pages

# Build the React app
RUN npm run build

# Stage 2: Serve the React app with Nginx
FROM nginx:alpine

# Copy the build output to Nginx's HTML directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
