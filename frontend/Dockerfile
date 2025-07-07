# Use official Nginx image as the base
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Remove default static files
RUN rm -rf ./*

# Copy static build files into the container
COPY . .

# Optional: override default nginx config for single-page app support
COPY nginx.conf /etc/nginx/conf.d/default.conf