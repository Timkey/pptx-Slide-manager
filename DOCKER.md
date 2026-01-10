# Docker Setup Guide

This project has been containerized to ensure consistent execution across different environments. All scripts and Python code now run inside Docker containers with all required dependencies pre-installed.

## Prerequisites

- **Colima** (recommended for macOS) or Docker Desktop
- Docker Compose (1.29+)

### Install Colima (macOS - Recommended)

```bash
# Install via Homebrew
brew install colima docker docker-compose

# Start Colima
./exec/start-colima.sh

# Or manually with custom settings:
colima start --cpu 2 --memory 4 --disk 20

# Verify it's running
colima status
docker ps
```

**Why Colima?**
- Lightweight alternative to Docker Desktop
- Free and open source
- Lower resource usage
- Native macOS integration

### Install Docker Desktop (Alternative)

**macOS:**
```bash
brew install --cask docker
# Or download from https://www.docker.com/products/docker-desktop
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER  # Add yourself to docker group
# Log out and back in for group changes to take effect
```

## Quick Start

### 1. Build the Docker Image

From the project root:

```bash
# Using docker-compose (recommended)
docker-compose build

# Or using docker directly
docker build -t immerculate-conception:latest .
```

### 2. Verify the Build

```bash
docker images | grep immerculate
```

You should see `immerculate-conception:latest` in the list.

## Usage

### Method 1: Using Wrapper Scripts (Easiest)

The project provides wrapper scripts in the `exec/` folder that automatically execute commands inside Docker:

```bash
# Merge PDFs
./exec/docker-merge-pdfs.sh assets/output/merged.pdf assets/pdfs/blocks/file1.pdf assets/pdfs/blocks/file2.pdf

# Convert PDF to images
./exec/docker-pdf-to-images.sh assets/pdfs/templates/input.pdf assets/output/images

# Convert PDF to PPTX
./exec/docker-pdf-to-pptx.sh assets/pdfs/templates/input.pdf assets/slides/merged/output.pptx

# Run Python scripts
./exec/docker-run-python.sh merge_pptx.py assets/slides/merged/output.pptx assets/slides/blocks/input1.pptx assets/slides/blocks/input2.pptx
```

### Method 2: Using Docker Compose Directly

For more control, use docker-compose commands:

```bash
# Start container in background
docker-compose up -d

# Execute bash scripts
docker-compose exec immerculate /app/scripts/merge_pdfs.sh /app/assets/output/merged.pdf /app/assets/pdfs/blocks/file1.pdf

# Execute Python scripts
docker-compose exec immerculate python /app/src/merge_pptx.py /app/assets/slides/merged/output.pptx /app/assets/slides/blocks/input.pptx

# Interactive shell (for debugging or manual operations)
docker-compose exec immerculate bash

# Stop container
docker-compose down
```

### Method 3: Using Makefile (Simplest)

See [Makefile](Makefile) for available commands:

```bash
# Build the Docker image
make build

# Run tests
make test

# Interactive shell
make shell

# Clean up
make clean
```

### Method 4: One-off Commands

Run a single command without keeping the container running:

```bash
docker-compose run --rm immerculate /app/scripts/merge_pdfs.sh /app/assets/output/test.pdf /app/assets/pdfs/blocks/input.pdf

docker-compose run --rm immerculate python /app/src/merge.py /app/assets/output/result.pptx /app/assets/slides/blocks/slide1.pptx
```

## File Path Mapping

The Docker container mounts your local directories:

| Local Path | Container Path |
|------------|----------------|
| `./assets` | `/app/assets` |
| `./src` | `/app/src` |
| `./scripts` | `/app/scripts` |

**Important:** When using docker-compose directly, use container paths (e.g., `/app/assets/...`). The wrapper scripts handle path translation automatically.

## Installed Tools

The Docker image includes:

- **Python 3.11** with pip
- **python-pptx** (0.6.21+) - PowerPoint manipulation
- **Pillow** (9.0.0+) - Image processing
- **qpdf** - PDF merging (preferred)
- **poppler-utils** - PDF utilities (pdftoppm, pdfunite)
- **ghostscript** - Alternative PDF tools

## Testing

### Run the Test Suite

```bash
# Using Makefile
make test

# Or directly
./test.sh
```

The test script validates:
- Docker image builds successfully
- All dependencies are installed
- Scripts execute correctly
- Python modules import properly
- PDF tools work as expected

### Manual Testing

```bash
# Start interactive shell
docker-compose run --rm immerculate bash

# Inside container, run commands:
qpdf --version
pdftoppm -v
python -c "from pptx import Presentation; print('python-pptx works!')"
```

## Troubleshooting

### Colima Issues (macOS)

**Colima not running:**
```bash
# Start Colima
./exec/start-colima.sh

# Or manually
colima start

# Check status
colima status
```

**"Cannot connect to Docker daemon" error:**
```bash
# Restart Colima
colima stop
colima start

# Verify Docker socket
ls -la ~/.colima/default/docker.sock
```

**Performance issues:**
```bash
# Stop Colima
colima stop

# Start with more resources
colima start --cpu 4 --memory 8 --disk 30
```

**Colima won't start:**
```bash
# Delete and recreate
colima delete
colima start
```

### Permission Issues

If you encounter permission errors with generated files:

1. **Option 1:** Set user ID in docker-compose.yml:
   ```yaml
   user: "1000:1000"  # Replace with your UID:GID (run `id -u` and `id -g`)
   ```

2. **Option 2:** Fix permissions after execution:
   ```bash
   sudo chown -R $USER:$USER assets/output/
   ```

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Script Not Found

```bash
# Verify scripts are copied to container
docker-compose run --rm immerculate ls -la /app/scripts/

# Ensure scripts are executable
docker-compose run --rm immerculate chmod +x /app/scripts/*.sh
```

### Python Module Not Found

```bash
# Verify Python packages are installed
docker-compose run --rm immerculate pip list

# Reinstall if needed (rebuild image)
docker-compose build --no-cache
```

## Development Workflow

### Modifying Scripts

Scripts and source code are mounted as volumes, so changes are immediately available:

1. Edit `src/*.py` or `scripts/*.sh` locally
2. Run the script through Docker (changes are reflected immediately)
3. No rebuild needed for code changes

### Adding Python Dependencies

1. Edit `src/requirements.txt`
2. Rebuild the Docker image:
   ```bash
   docker-compose build
   ```

### Debugging

```bash
# Enter interactive shell
docker-compose run --rm immerculate bash

# Inside container:
cd /app
python -m pdb src/merge.py  # Python debugger
bash -x scripts/merge_pdfs.sh output.pdf input.pdf  # Shell debugging
```

## Architecture Notes

### Why Docker?

1. **Consistency:** Same environment on macOS, Linux, Windows
2. **Dependency Management:** All PDF tools and Python packages pre-installed
3. **Isolation:** Doesn't pollute your system with packages
4. **Reproducibility:** Easy to share and deploy

### Container Design

- **Base Image:** `python:3.11-slim-bookworm` (Debian 12)
- **Multi-stage Build:** Not used here, but can be added for optimization
- **Volume Mounts:** Keeps data persistent and allows live code editing
- **Non-root User:** Can be configured in docker-compose.yml

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Run tests
        run: docker-compose run --rm immerculate /app/test.sh
```

### GitLab CI Example

```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker-compose build
    - docker-compose run --rm immerculate /app/test.sh
```

## Migration from Non-Docker Setup

### Old Way (Local Installation)

```bash
cd src
./setup_env.sh
source .venv/bin/activate
python merge.py output.pptx input1.pptx input2.pptx
```

### New Way (Docker)

```bash
# From project root
./docker-run-python.sh merge.py output.pptx input1.pptx input2.pptx

# Or
make shell
# Inside container:
python /app/src/merge.py /app/assets/output.pptx /app/assets/input1.pptx
```

### What Changed

- ✅ No need to install Python dependencies locally
- ✅ No need to install qpdf, poppler, ghostscript
- ✅ No virtual environment management
- ✅ Works identically on all platforms
- ℹ️ File paths now use `/app/assets/...` prefix (in container)
- ℹ️ Use wrapper scripts or docker-compose commands

## Performance Considerations

- **First build:** Takes 2-5 minutes (downloads base image, installs packages)
- **Subsequent builds:** Faster due to Docker layer caching
- **Runtime:** Minimal overhead (~1-2% vs native execution)
- **Disk usage:** ~500MB for image

## Security Notes

- Container runs as root by default (can be changed in docker-compose.yml)
- No network access required for core functionality
- Only mounts `assets/`, `src/`, `scripts/` directories
- No credentials or secrets in container (add via environment variables if needed)

## Cleanup

```bash
# Remove containers and networks
docker-compose down

# Remove image
docker rmi immerculate-conception:latest

# Remove all unused Docker resources
docker system prune -a
```

## Support

For issues or questions:
1. Check this documentation
2. Review test.sh for working examples
3. Examine wrapper scripts for path handling
4. Use `docker-compose run --rm immerculate bash` for debugging

---

**Last Updated:** January 10, 2026  
**Docker Version:** 20.10+  
**Docker Compose Version:** 1.29+
