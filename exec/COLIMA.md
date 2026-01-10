# Colima Configuration Notes

This project uses Colima as the Docker runtime on macOS. Colima is a lightweight, open-source alternative to Docker Desktop.

## Quick Reference

### Start/Stop
```bash
# Start Colima with project defaults
./exec/start-colima.sh

# Stop Colima
./exec/stop-colima.sh

# Check status
colima status

# View logs
colima logs
```

### Resource Configuration

The `start-colima.sh` script starts Colima with:
- **CPU**: 2 cores
- **Memory**: 4 GB
- **Disk**: 20 GB
- **Architecture**: x86_64 (Rosetta for Apple Silicon)

Adjust these in [exec/start-colima.sh](exec/start-colima.sh) based on your system resources.

### Manual Start with Custom Settings

```bash
colima start \
    --cpu 4 \
    --memory 8 \
    --disk 30 \
    --arch aarch64 \
    --vm-type=vz
```

## Colima vs Docker Desktop

| Feature | Colima | Docker Desktop |
|---------|--------|----------------|
| **License** | Free/Open Source | Free for personal use |
| **Resource Usage** | Lower (~500MB) | Higher (~1-2GB) |
| **Speed** | Fast | Moderate |
| **GUI** | CLI only | GUI + CLI |
| **Updates** | Manual | Automatic |

## Architecture Notes

### Apple Silicon (M1/M2/M3)

Colima can run in two modes:

1. **Native ARM64** (faster, but some images may not be compatible):
   ```bash
   colima start --arch aarch64
   ```

2. **x86_64 with Rosetta** (slower, but better compatibility):
   ```bash
   colima start --arch x86_64 --vz-rosetta
   ```

The project uses x86_64 with Rosetta by default for maximum compatibility.

### VM Types

- **vz**: Virtualization framework (macOS 13+, faster)
- **qemu**: QEMU-based (compatible with older macOS)

## Common Commands

```bash
# List running containers
colima list

# SSH into Colima VM
colima ssh

# Delete Colima instance (removes all data)
colima delete

# Restart Colima
colima restart

# Get VM IP address
colima ip
```

## Troubleshooting

### Issue: "colima is not running"
```bash
./exec/start-colima.sh
```

### Issue: "Cannot connect to Docker daemon"
```bash
# Check if Colima is running
colima status

# Verify socket exists
ls -la ~/.colima/default/docker.sock

# Restart if needed
colima restart
```

### Issue: Out of disk space
```bash
# Stop Colima
colima stop

# Delete and recreate with more disk
colima delete
colima start --disk 50
```

### Issue: Performance issues
```bash
# Increase resources
colima stop
colima start --cpu 4 --memory 8
```

### Issue: Network problems
```bash
# Restart networking
colima restart
```

## Environment Variables

Colima sets Docker environment automatically. Verify with:

```bash
echo $DOCKER_HOST
# Should show: unix:///Users/<username>/.colima/default/docker.sock
```

## Updates

```bash
# Update Colima via Homebrew
brew upgrade colima

# Check version
colima version
```

## Uninstall

```bash
# Stop and delete
colima stop
colima delete

# Uninstall via Homebrew
brew uninstall colima
```

## Advanced Configuration

Edit `~/.colima/default/colima.yaml` for persistent settings:

```yaml
cpu: 4
memory: 8
disk: 30
arch: x86_64
vmType: vz
rosetta: true
```

Then restart:
```bash
colima restart
```

## Resources

- **Colima GitHub**: https://github.com/abiosoft/colima
- **Documentation**: https://github.com/abiosoft/colima/blob/main/docs/FAQ.md

---

**Note**: Colima is specifically for macOS and Linux. Windows users should use Docker Desktop or WSL2.
