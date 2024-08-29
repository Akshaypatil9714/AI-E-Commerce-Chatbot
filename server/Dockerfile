# Use Node.js version 21.3.0 as the base image
FROM node:21.3.0

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set the environment variable to define the port for the application
ENV PORT=8080

# Command to run the application, using the PORT environment variable if needed
CMD ["node", "server.js"]
