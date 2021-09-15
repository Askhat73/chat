FROM node:14.17.6-alpine as build

# Set the working directory
WORKDIR /usr/local/app

# Add the source code to app
# COPY . /usr/local/app/
COPY package*.json ./

# Install all the dependencies
RUN npm install -g @angular/cli @angular-devkit/build-angular --unsafe-perm=true && npm install --unsafe-perm=true

# Expose port 4200
EXPOSE 4200
CMD ["npm", "start"]
