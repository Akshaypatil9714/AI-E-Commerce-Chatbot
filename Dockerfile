# Use Node.js version 21.3.0 as the base image
FROM node:21.3.0

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install server app dependencies
COPY server/package*.json ./
RUN npm install

# Copy the server source code
COPY server/. .

# # Build the frontend if needed
# ARG REACT_APP_API_URL
# ENV REACT_APP_API_URL=${REACT_APP_API_URL}
# RUN npm run build
# RUN npm

# Expose the port your app runs on
EXPOSE 8080

# Set the environment variable to define the port for the application
ENV PORT=8080

# Run the application
CMD ["node", "server.js"]