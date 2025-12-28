# ============================================
# INSTAINTELLI - Frontend Dockerfile
# ============================================
# React + Vite Frontend Container
# Uses Node.js 18 for compatibility

FROM node:18-alpine

WORKDIR /app

# Install dependencies first (for better caching)
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run development server with hot-reload
# --host 0.0.0.0 allows access from outside container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

