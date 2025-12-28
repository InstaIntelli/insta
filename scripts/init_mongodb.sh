#!/bin/bash
# ============================================
# MongoDB Initialization Script
# ============================================
# This script initializes MongoDB collections and indexes
# Run this inside the mongodb container or via docker-compose exec

set -e

echo "Initializing MongoDB database..."

# Wait for MongoDB to be ready
until mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
  echo "Waiting for MongoDB to be ready..."
  sleep 2
done

echo "MongoDB is ready!"

# Create database and collections
mongosh "${MONGODB_DB:-instaintelli}" --eval "
  db.createCollection('posts');
  db.posts.createIndex({ 'user_id': 1 });
  db.posts.createIndex({ 'created_at': -1 });
  db.posts.createIndex({ 'tags': 1 });
  print('MongoDB collections and indexes created!');
"

echo "MongoDB initialization complete!"

