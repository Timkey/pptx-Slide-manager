# Makefile for immerculate-conception Docker operations
# Simplifies common Docker tasks

.PHONY: help build up down shell test clean rebuild logs ps

# Default target
help:
	@echo "Immerculate Conception - Docker Commands"
	@echo "========================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make build      - Build the Docker image"
	@echo "  make up         - Start container in background"
	@echo "  make down       - Stop and remove containers"
	@echo "  make shell      - Open interactive bash shell in container"
	@echo "  make test       - Run test suite"
	@echo "  make clean      - Remove containers, images, and volumes"
	@echo "  make rebuild    - Clean and rebuild from scratch"
	@echo "  make logs       - Show container logs"
	@echo "  make ps         - Show running containers"
	@echo ""
	@echo "Examples:"
	@echo "  make build && make test"
	@echo "  make shell"
	@echo "  make clean && make build"

# Build Docker image
build:
	@echo "Building Docker image..."
	docker-compose build

# Start container in background
up:
	@echo "Starting container..."
	docker-compose up -d
	@echo "Container started. Use 'make shell' to access it."

# Stop and remove containers
down:
	@echo "Stopping containers..."
	docker-compose down

# Open interactive shell
shell:
	@echo "Opening interactive shell..."
	docker-compose run --rm immerculate bash

# Run test suite
test:
	@echo "Running test suite..."
	@if [ -f ./test.sh ]; then \
		./test.sh; \
	else \
		echo "Test script not found. Running basic smoke tests..."; \
		docker-compose run --rm immerculate python --version; \
		docker-compose run --rm immerculate qpdf --version; \
		docker-compose run --rm immerculate pdftoppm -v; \
		docker-compose run --rm immerculate python -c "from pptx import Presentation; print('✓ python-pptx works')"; \
		docker-compose run --rm immerculate python -c "from PIL import Image; print('✓ Pillow works')"; \
	fi

# Clean up all Docker resources for this project
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down --volumes --remove-orphans
	@echo "Removing Docker image..."
	docker rmi immerculate-conception:latest 2>/dev/null || true
	@echo "Cleanup complete."

# Rebuild from scratch
rebuild: clean build
	@echo "Rebuild complete."

# Show container logs
logs:
	docker-compose logs -f

# Show running containers
ps:
	docker-compose ps

# Quick test of PDF merge
test-merge-pdf:
	@echo "Testing PDF merge..."
	docker-compose run --rm immerculate bash -c "cd /app && qpdf --version && echo 'qpdf is ready'"

# Quick test of Python PPTX
test-python-pptx:
	@echo "Testing python-pptx..."
	docker-compose run --rm immerculate python -c "from pptx import Presentation; print('✓ python-pptx imports successfully')"

# Quick test of PDF to images
test-pdf-images:
	@echo "Testing pdftoppm..."
	docker-compose run --rm immerculate pdftoppm -v

# Run interactive Python REPL
python:
	@echo "Starting Python REPL..."
	docker-compose run --rm immerculate python

# Display Docker image info
info:
	@echo "Docker Image Information:"
	@docker images immerculate-conception:latest
	@echo ""
	@echo "Container Status:"
	@docker-compose ps

# Export Docker image to tar file (for sharing)
export:
	@echo "Exporting Docker image to immerculate-conception.tar..."
	docker save immerculate-conception:latest -o immerculate-conception.tar
	@echo "Image exported. Share immerculate-conception.tar with others."

# Import Docker image from tar file
import:
	@if [ -f immerculate-conception.tar ]; then \
		echo "Importing Docker image..."; \
		docker load -i immerculate-conception.tar; \
		echo "Image imported successfully."; \
	else \
		echo "Error: immerculate-conception.tar not found."; \
		exit 1; \
	fi
