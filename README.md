# Nomi

## 🛠 Setup Instructions

### 1. Create Project Structure

```bash
mkdir -p ~/Repos/nomi/{utils}
cd ~/Repos/nomi

touch nomi.py brain.py memory.py startup.py config.yaml
touch utils/__init__.py utils/cli.py
echo "{}" > memory.json

# Make main script executable with a shebang
echo '#!/usr/bin/env python3' | cat - nomi.py > temp && mv temp nomi.py
chmod +x nomi.py
