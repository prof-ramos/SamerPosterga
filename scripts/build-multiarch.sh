#!/bin/bash
# scripts/build-multiarch.sh

set -e

IMAGE_NAME="ghcr.io/prof-ramos/juridic-bot"
VERSION="${1:-latest}"

echo "🏗️ Building multi-architecture Docker image..."

# Create buildx builder if not exists
docker buildx inspect multiarch-builder >/dev/null 2>&1 || \
docker buildx create --name multiarch-builder --use

# Build and push multi-arch image
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "${IMAGE_NAME}:${VERSION}" \
  --tag "${IMAGE_NAME}:latest" \
  --push \
  --file Dockerfile.optimized \
  .

echo "✅ Multi-arch build completed: ${IMAGE_NAME}:${VERSION}"