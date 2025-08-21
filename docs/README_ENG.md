<h1 align="center">BCL Launcher</h1>

<p align="center">
  <img src="./assets/logo.svg" alt="BCL-Launcher Logo" width="150">
</p>

<div style="text-align: center; margin: 10px 0;">
  <a href="../README.md" style="margin: 0 15px;">简体中文</a>
  <a href="README_ZHTW.md" style="margin: 0 15px;">繁体中文</a>
  <a href="README_RUS.md" style="margin: 0 15px;">Русский</a>
</div>

<h3 align="center">Lightweight · Customizable · Open · User-Centric Minecraft Launcher</h3>

---

## ❓ What is BCL Launcher?
**BCL Launcher** (full name **Bad Craft Launcher**) is a **lightweight, customizable Minecraft launcher** developed by [DCR Studio[↗]](https://github.com/DCR-Studio), following a "user-centric" philosophy.  

- Developed using **Rust + Python**  
- We provide a **fully Rust-based core** [HyperLightBCLCore[↗]](https://github.com/DCR-Studio/OpenBCLCore)  
- Fully **open-source**, anyone can contribute  

---

## 🚀 Features & Advantages
### 🔒 Security  
- Uses asymmetric encryption and system-level key storage to protect user sensitive data  
- Rust memory safety + Python layer for controlled logic  

### 👍 Stability & Reliability  
- Rust ensures core modules run stably  
- Runs smoothly even on low-end hardware  

### 💻 Cross-Platform  
- Supports multiple platforms (Windows / Linux / macOS)  
- Python handles UI and logic for rapid adaptation across systems  

### ✨ Flexible & Extensible  
- Supports plugins and script system  
- Rich third-party library ecosystem allows developers to extend functionality quickly  

### 🧩 Modular Design + Plugin Interface  
- Core performance modules written in **Rust** ensure speed and security  
- Modules communicate via **IPC (inter-process communication)**, ensuring efficient and safe data exchange  
- High-level logic, configuration, and extensions are written in **Python** for flexibility and maintainability  
- Modules are decoupled, making iteration, debugging, and replacement easy  
- Developers can independently modify or add components without major changes to the whole project  

---

## 📦 Installation & Usage
### Download
> [!IMPORTANT]  
> ❌**The project is still in development; no release has been published yet**
- [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases)

### Launch
#### For Windows
- Windows is usually distributed as a zip archive.
1. Download from [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) as `BadCraftLauncher-Version-Windows-Architecture.zip`, example file names below (still in development, no release available yet)
```

# Example file name

BadCraftLauncher-1.0RC1-Windows-x86\_64.zip

```
2. Open the executable file

#### For Linux
> [!IMPORTANT]
> - Linux launch process differs from Windows; distribution is **source code + installation script (.sh)**  
> - You need to download the source package first, then run the script to build and launch  
> - Ensure Python3 (≥3.10 recommended) and Rust (≥1.80 recommended) are installed
1. Download from [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) as `BadCraftLauncher-Version-Linux-Architecture.tar.gz`, example file names below (still in development, no release available yet)
```

# Example file name

BadCraftLauncher-1.0RC1-Linux-x86\_64.tar.gz

````

2. Extract the source package  
```bash
# Use the actual downloaded file name
tar -xvzf BadCraftLauncher-1.0RC1-Linux-x86_64.tar.gz
cd BadCraftLauncher-1.0RC1
````

3. Run the installation/launch script

```bash
sh run.sh
```

4. For development mode, run manually

```bash
pip install -r requirements.txt
cargo build --release
python main.py
```

#### For macOS

> \[!IMPORTANT]
>
> * macOS distribution is similar to Linux, providing **source code + launch script (.sh)**
> * Users can quickly run via script; `.dmg` installer may be provided in future
> * Ensure Python3 (≥3.10 recommended) and Rust (≥1.80 recommended) are installed
> * Apple Silicon (M1/M2/M3/M4) should use arm64 build; Intel CPU should use amd64 build

1. Download from [GitHub Release\[↗\]](https://github.com/DCR-Studio/BCL-Launcher/releases) as `BadCraftLauncher-Version-macOS-Architecture.tar.gz`, example file names below (still in development, no release available yet)

```
# Example file names
BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
BadCraftLauncher-1.0RC1-macOS-x86_64.tar.gz
```

2. Extract the source package

```bash
tar -xvzf BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
cd BadCraftLauncher-1.0RC1
```

3. Run the installation/launch script

```bash
sh run.sh
```

4. For development mode, run manually

```bash
pip install -r requirements.txt
cargo build --release
python main.py
```

---

## 📜 Copyright & Open Source License

BCL Launcher is developed by **DCR Studio**, ©2025 DCR Studio. All rights reserved.

This project is licensed under **GPL-3.0**, allowing anyone to use, modify, and distribute the software under the terms of the license.
See [LICENSE[↗]](./LICENSE) for full license details.

> \[!WARNING]
>
> * You are free to use and modify BCL Launcher but must retain the original author attribution
> * Removing this copyright notice for closed-source commercial distribution is prohibited

This English document is translated by ChatGPT
