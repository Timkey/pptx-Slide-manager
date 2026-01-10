# Multi-stage Dockerfile for immerculate-conception
# Includes Python 3.11, PDF tools (qpdf, poppler, ghostscript), and Python dependencies

FROM python:3.11-slim-bookworm AS base

# Install system dependencies for PDF manipulation
# - qpdf: PDF merging (preferred method)
# - poppler-utils: PDF to image conversion (pdftoppm, pdfunite)
# - ghostscript: Alternative PDF merging
# - libjpeg-dev, zlib1g-dev: Image processing libraries for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    qpdf \
    poppler-utils \
    ghostscript \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
# This layer is cached unless requirements.txt changes
COPY scripts/python/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy all scripts
COPY scripts/ /app/scripts/

# Make scripts executable
RUN chmod +x /app/scripts/bash/*.sh /app/scripts/python/*.py

# Create directories for assets (will be mounted as volumes)
RUN mkdir -p /app/assets/config \
    /app/assets/output \
    /app/assets/pdfs/blocks \
    /app/assets/pdfs/merged \
    /app/assets/pdfs/templates \
    /app/assets/slides/blocks \
    /app/assets/slides/merged \
    /app/assets/slides/templates

# Set PATH to include both bash and python scripts
ENV PATH="/app/scripts/bash:/app/scripts/python:${PATH}"

# Default command opens a bash shell for interactive use
CMD ["/bin/bash"]

# NOTE: To run specific scripts, override CMD:
# docker run --rm -v $(pwd)/assets:/app/assets immerculate merge_pdfs.sh output.pdf in1.pdf in2.pdf
