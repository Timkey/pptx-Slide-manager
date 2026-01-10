#!/usr/bin/env bash
# Quick reference card for immerculate-conception Docker setup
# Run this anytime you need a reminder of available commands

cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║         IMMERCULATE CONCEPTION - QUICK REFERENCE             ║
╚═══════════════════════════════════════════════════════════════╝

🚀 SETUP (First Time)
───────────────────────────────────────────────────────────────
  ./exec/start-colima.sh          # Start Colima (Docker runtime)
  make build                       # Build Docker image
  make test                        # Verify everything works

📦 DAILY USAGE
───────────────────────────────────────────────────────────────
  MERGE PDFs:
    ./exec/docker-merge-pdfs.sh assets/output/merged.pdf \
        assets/pdfs/blocks/file1.pdf assets/pdfs/blocks/file2.pdf

  PDF → IMAGES:
    ./exec/docker-pdf-to-images.sh assets/pdfs/input.pdf \
        assets/output/images/

  PDF → PPTX:
    ./exec/docker-pdf-to-pptx.sh assets/pdfs/input.pdf \
        assets/slides/output.pptx

  RUN PYTHON:
    ./exec/docker-run-python.sh merge_pptx.py output.pptx \
        input1.pptx input2.pptx

🛠️  MAKEFILE COMMANDS
───────────────────────────────────────────────────────────────
  make build          Build Docker image
  make test           Run test suite (20 tests)
  make shell          Interactive bash shell in container
  make up             Start container in background
  make down           Stop container
  make clean          Remove all Docker resources
  make rebuild        Clean rebuild from scratch
  make logs           Show container logs
  make help           Show all available commands

🐳 DOCKER COMMANDS
───────────────────────────────────────────────────────────────
  docker-compose up -d                    # Start in background
  docker-compose exec immerculate bash    # Interactive shell
  docker-compose down                     # Stop everything
  docker-compose logs                     # View logs

🖥️  COLIMA COMMANDS (macOS)
───────────────────────────────────────────────────────────────
  ./exec/start-colima.sh          Start Colima
  ./exec/stop-colima.sh           Stop Colima
  colima status                   Check if running
  colima restart                  Restart Colima
  colima list                     List instances

🔧 TROUBLESHOOTING
───────────────────────────────────────────────────────────────
  ERROR: "colima is not running"
    → ./exec/start-colima.sh

  ERROR: "Cannot connect to Docker daemon"
    → colima restart

  ERROR: Script fails
    → make clean && make rebuild

  ERROR: Permission issues
    → sudo chown -R $USER:$USER assets/

  NEED MORE RESOURCES:
    → Edit exec/start-colima.sh (increase CPU/memory)
    → ./exec/stop-colima.sh && ./exec/start-colima.sh

📚 DOCUMENTATION
───────────────────────────────────────────────────────────────
  README.md                       Project overview
  DOCKER.md                       Complete Docker guide
  exec/COLIMA.md                  Colima setup & troubleshooting
  exec/REORGANIZATION_SUMMARY.md  What changed & why
  Makefile                        All available commands

📁 PROJECT STRUCTURE
───────────────────────────────────────────────────────────────
  exec/           Execution scripts & docs
  assets/         Input/output files (shared with container)
  src/            Python source code (live-editable)
  scripts/        Bash scripts (live-editable)

💡 TIPS
───────────────────────────────────────────────────────────────
  • All files in src/ and scripts/ are live-mounted
    → Edit locally, run immediately (no rebuild)
  
  • Add Python packages to src/requirements.txt
    → Then run: make rebuild
  
  • Place input files in assets/ subdirectories
    → Results appear in assets/output/
  
  • Use 'make shell' to debug interactively
    → Full access to container environment

📊 CURRENT STATUS
───────────────────────────────────────────────────────────────
EOF

# Dynamic status checks
echo -n "  Colima:          "
if colima status >/dev/null 2>&1; then
    echo "✅ Running"
else
    echo "❌ Not running (run ./exec/start-colima.sh)"
fi

echo -n "  Docker Image:    "
if docker images immerculate-conception:latest | grep -q immerculate; then
    echo "✅ Built"
else
    echo "❌ Not built (run make build)"
fi

echo -n "  Container:       "
if docker-compose ps | grep -q immerculate; then
    echo "✅ Running"
else
    echo "ℹ️  Stopped (optional, use make up to start)"
fi

cat << 'EOF'

🎯 NEXT STEPS
───────────────────────────────────────────────────────────────
  1. Ensure Colima is running
  2. Place your files in assets/
  3. Run the appropriate exec/ script
  4. Find results in assets/output/

Need help? Run: make help

EOF
