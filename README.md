# Immerculate Conception

A containerized toolkit for PDF and PowerPoint manipulation. All operations run inside Docker containers for consistent, reproducible results across platforms.

## 🚀 Quick Start

### Prerequisites
- **Colima** (recommended for macOS) or Docker Desktop
- Docker Compose (1.29+)

### Quick Reference

Run this anytime for a command cheat sheet:
```bash
./exec/quick-ref.sh
```

### Setup with Colima (macOS)

```bash
# Install Colima if not already installed
brew install colima

# Start Colima
./exec/start-colima.sh

# Verify Docker is running
docker ps
```

### Build & Test

```bash
# Build the Docker image
make build

# Run tests to verify everything works
make test

# Open interactive shell
make shell
```

## 📦 What's Included

This project provides tools for:
- **PDF Merging**: Combine multiple PDFs into one
- **PDF to Images**: Convert PDF pages to PNG images
- **PDF to PowerPoint**: Convert PDFs to PPTX presentations
- **PowerPoint Merging**: Combine multiple PPTX files
- **Output Validation**: Comprehensive validation of merged files
- **Organized Outputs**: Script-specific subdirectories for easy management

### Output Organization

All merge scripts save outputs to organized subdirectories:
```
assets/output/
├── merge_pptx/          # PowerPoint merge outputs
├── merge_pdfs/          # PDF merge outputs
├── merge_template/      # Template-based merge outputs
└── merge_images/        # Image-based merge outputs
```

### Automatic Validation

All merge operations include automatic validation:
- ✅ File integrity checks (ZIP structure for PPTX, header/EOF for PDF)
- ✅ Content validation (slide count, layout verification)
- ✅ Size and completeness checks
- ✅ Immediate feedback after each merge

All tools are containerized and ready to use with zero local setup!

## 🎯 Usage

### Method 1: Wrapper Scripts (Easiest)

```bash
# Merge PDFs
./exec/docker-merge-pdfs.sh assets/output/merged.pdf assets/pdfs/blocks/file1.pdf assets/pdfs/blocks/file2.pdf

# Convert PDF to images
./exec/docker-pdf-to-images.sh assets/pdfs/templates/input.pdf assets/output/images

# Convert PDF to PPTX
./exec/docker-pdf-to-pptx.sh assets/pdfs/templates/input.pdf assets/slides/merged/output.pptx

# Run Python scripts
./exec/docker-run-python.sh merge_pptx.py output.pptx input1.pptx input2.pptx
```

### Method 2: Makefile Commands

```bash
make build      # Build Docker image
make test       # Run test suite
make shell      # Interactive bash shell
make clean      # Remove containers & images
make help       # Show all commands
```

### Method 3: Docker Compose

```bash
# Start container
docker-compose up -d

# Execute commands
docker-compose exec immerculate /app/scripts/merge_pdfs.sh /app/assets/output/test.pdf /app/assets/pdfs/input.pdf

# Interactive shell
docker-compose exec immerculate bash

# Stop container
docker-compose down
```

## 📁 Project Structure

All scripts are now organized under `scripts/` directory:
- `scripts/bash/` - Shell scripts for PDF operations
- `scripts/python/` - Python scripts for PPTX operations
- `assets/` - Input/output files (shared with container)
- `exec/` - Docker wrapper scripts for easy execution

```
.
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── Makefile               # Common commands
├── test.sh                # Test suite
├── DOCKER.md              # Detailed Docker docs
├── README.md              # This file
│
├── exec/                  # Execution scripts
│   ├── start-colima.sh    # Start Colima (macOS)
│   ├── stop-colima.sh     # Stop Colima
│   ├── docker-merge-pdfs.sh
│   ├── docker-pdf-to-images.sh
│   ├── docker-pdf-to-pptx.sh
│   └── docker-run-python.sh
│
├── assets/                # Data directory (mounted in container)
│   ├── config/
│   ├── output/            # Organized merged files
│   │   ├── merge_pptx/    # PowerPoint merge outputs
│   │   ├── merge_pdfs/    # PDF merge outputs
│   │   ├── merge_template/# Template-based outputs
│   │   └── merge_images/  # Image-based outputs
│   ├── pdfs/
│   │   ├── blocks/        # Input PDFs
│   │   ├── merged/        # Legacy location (use output/)
│   │   └── templates/     # PDF templates
│   └── slides/
│       ├── blocks/        # Input PPTX
│       ├── merged/        # Merged PPTX
│       └── templates/
│
└── scripts/               # All scripts (mounted as volume)
    ├── bash/              # Bash scripts
    │   ├── merge_pdfs.sh
    │   ├── pdf_to_images.sh
    │   ├── pdf_to_pptx.sh
    │   └── pptx_to_pdf.sh
    ├── python/            # Python scripts
    │   ├── merge.py
    │   ├── merge_pptx.py
    │   ├── pdf_images_to_pptx.py
    │   ├── test_merge_templates.py
    │   └── requirements.txt
    └── setup_env.sh
```

## 🛠️ Available Tools

The Docker container includes:

- **Python 3.11** with pip
- **python-pptx** (PowerPoint manipulation)
- **Pillow** (Image processing)
- **qpdf** (PDF merging - preferred)
- **poppler-utils** (PDF utilities: pdftoppm, pdfunite)
- **ghostscript** (Alternative PDF tools)

## 📖 Documentation

- **[DOCKER.md](DOCKER.md)**: Complete Docker setup guide, troubleshooting, and advanced usage
- **[VALIDATION_GUIDE.md](exec/VALIDATION_GUIDE.md)**: Output validation and organization
- **[AUTO_FILENAME_GUIDE.md](exec/AUTO_FILENAME_GUIDE.md)**: Auto-generated filename usage
- **[Makefile](Makefile)**: See all available make commands
- **[test.sh](test.sh)**: Test script with examples

## ✅ Validation

Validate merged outputs for corruption:

```bash
# Validate all outputs (inside container)
./exec/docker-validate-output.sh

# Validate specific directory
./exec/docker-validate-output.sh assets/output/merge_pptx

# Run comprehensive merge & validation test
./test-merge-validation.sh
```

Validation checks:
- File integrity (ZIP structure, PDF headers)
- Content accessibility (slides, shapes, layouts)
- Completeness (size, EOF markers)
- Metadata (dimensions, slide counts)

## 🧪 Testing

Run the full test suite:

```bash
./test.sh
```

Or use Make:

```bash
make test
```

Tests validate:
- ✅ Docker image builds correctly
- ✅ All dependencies installed
- ✅ Scripts are executable
- ✅ Python modules import properly
- ✅ PDF tools work correctly
- ✅ Volume mounts configured
- ✅ Wrapper scripts functional

## 🔧 Development

### Modifying Code

Source code and scripts are mounted as volumes, so changes take effect immediately:

1. Edit files in `src/` or `scripts/`
2. Run through Docker (no rebuild needed)
3. Changes are reflected instantly

### Adding Python Dependencies

1. Edit `src/requirements.txt`
2. Rebuild: `make rebuild`

### Debugging

```bash
# Interactive shell
make shell

# Inside container:
python -m pdb /app/src/merge.py         # Python debugger
bash -x /app/scripts/merge_pdfs.sh      # Shell debugging
```

## 🚨 Troubleshooting

### Permission Issues

If generated files have wrong ownership:

```bash
# Fix permissions
sudo chown -R $USER:$USER assets/output/

# Or configure in docker-compose.yml:
# user: "1000:1000"  # Your UID:GID (run `id -u` and `id -g`)
```

### Container Won't Build

```bash
# Clean rebuild
make rebuild

# Or manually:
docker-compose down
docker-compose build --no-cache
```

### Script Not Found

```bash
# Verify scripts in container
docker-compose run --rm immerculate ls -la /app/scripts/
```

See [DOCKER.md](DOCKER.md) for more troubleshooting tips.

## 📝 Migration Notes

### Before (Local Setup)
```bash
cd src
./setup_env.sh
source .venv/bin/activate
pip install -r requirements.txt
python merge.py output.pptx input.pptx
```

### After (Docker + Colima)
```bash
# Start Colima (macOS)
./exec/start-colima.sh

# Build and run
make build
./exec/docker-run-python.sh merge.py output.pptx input.pptx
```

**Benefits:**
- ✅ No local Python environment needed
- ✅ No system dependencies to install
- ✅ Works identically on macOS, Linux, Windows
- ✅ Isolated from system packages
- ✅ Easy to share and deploy

## 🔐 Security

- Container runs with minimal privileges
- No network access required for core operations
- Only mounts necessary directories
- No credentials stored in container

## 🧹 Cleanup

```bash
# Remove containers and networks
make down

# Remove everything including image
make clean

# Remove all Docker resources
docker system prune -a
```

## 📊 Performance

- **First build**: 2-5 minutes
- **Subsequent builds**: Seconds (cached layers)
- **Runtime overhead**: ~1-2% vs native
- **Disk usage**: ~500MB for image

## 🤝 Contributing

1. Make changes to code or scripts
2. Test with `make test`
3. Document changes
4. Ensure Docker setup still works

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

Built with:
- Python & python-pptx
- qpdf, Poppler, Ghostscript
- Docker & Docker Compose

---

**Docker-First Project** | Last Updated: January 10, 2026

For detailed Docker documentation, see [DOCKER.md](DOCKER.md)
