FROM node:18

# Set working directory
WORKDIR /app

# Accept the VITE_BASE_API_URL as a build argument
ARG VITE_BASE_API_URL
ENV VITE_BASE_API_URL=${VITE_BASE_API_URL}

# Copy application code
COPY . ./

# Install dependencies
RUN npm install

# Build the project
RUN npm run build

# Install a lightweight static file server
RUN npm install -g serve

# Expose the frontend port
EXPOSE 5173

# Serve the built project
CMD ["serve", "-s", "dist", "-l", "5173"]