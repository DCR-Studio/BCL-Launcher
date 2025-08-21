<h1 align="center">BCL Launcher</h1>

<p align="center">
  <img src="./docs/assets/logo.svg" alt="BCL-Launcher Logo" width="150">
</p>

<p align="center">
  <b><a href="./docs/README_ZHTW.md">繁體中文</a> | <a href="./docs/README_ENG.md">English</a> | <a href="./docs/README_RUS.md">Русский</a></b>
</p>


<h3 align="center">轻量化 · 可定制 · 开放 · 以用户为中心的 Minecraft 启动器</h3>

---

## ❓ BCL Launcher 是什么？
**BCL Launcher**（全称 **Bad Craft Launcher**），是由 [DCR Studio[↗]](https://github.com/DCR-Studio) 开发的 **轻量化、可定制的 Minecraft 启动器**，秉持「以用户为中心」的理念。  

- 使用 **Rust + Python** 混合编写  
- 我们提供 **完全 Rust 编写的内核** [HyperLightBCLCore[↗]](https://github.com/DCR-Studio/OpenBCLCore)  
- 完全 **开源**，任何人都可以参与  

---

## 🚀 特点与优势
### 🔒 安全  
- 使用非对称加密和系统级密钥存储器处理用户的敏感数据  
- Rust 内存安全 + Python 层的可控逻辑  

### 👍 稳定可靠  
- Rust 保证核心模块的稳定运行  
- 即使在低配置环境下也能流畅运行  

### 💻 跨平台  
- 跨平台支持（Windows / Linux / macOS）  
- Python 负责 UI 与逻辑，可快速适配不同系统  

### ✨ 灵活扩展  
- 支持插件（Plugin）与脚本系统  
- 丰富的第三方库生态，开发者可快速扩展功能  

### 🧩 模块化设计+Plugin接口   
- 核心性能模块由 **Rust** 编写，保证速度与安全  
- 各模块之间通过 **IPC（进程间通信）** 联系，保证高效与安全的数据交互 
- 高层逻辑、配置与扩展功能由 **Python** 编写，保证灵活与易维护  
- 模块之间解耦，便于快速迭代、调试和替换  
- 开发者可根据需求独立修改或新增组件，而无需大幅度改动整个项目
 

---

## 📦 安装与使用
### 下载
> [!IMPORTANT]  
> ❌**目前项目还处于开发阶段，暂时没有放出Release**
- [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases)

### 启动
#### 对于Windwos
- Windows一般以zip压缩文件形式发行。
1. 从 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下载为`BadCraftLauncher-版本号-Windows-系统架构.zip`，见下方文件名示例（目前正在开发阶段，没有Release被发行）
```
# 文件名示例
BadCraftLauncher-1.0RC1-Windows-x86_64.zip
```
2. 打开可执行文件

#### 对于 Linux
> [!IMPORTANT]
> - Linux 的启动过程与 Windows 不同，发行形式为 **源码 + 安装脚本 (.sh)**。  
> - 您需要先下载源码包，然后执行脚本进行构建与启动。  
> - 您的计算机上需要安装Python3(建议高于3.10)和Rust(建议高于1.80)
1. 从 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下载为`BadCraftLauncher-版本号-Linux-系统架构.tar.gz`，见下方文件名示例（目前正在开发阶段，没有 Release 被发行）  
```
# 文件名示例
BadCraftLauncher-1.0RC1-Linux-x86_64.tar.gz
```

2. 解压源码包  
```bash
# 以实际下载的文件名为准
tar -xvzf BadCraftLauncher-1.0RC1-Linux-x86_64.tar.gz
cd BadCraftLauncher-1.0RC1
```

3. 运行安装/启动脚本
```bash
sh run.sh
```

4. 如果需要开发模式启动，可以手动执行
```bash
pip install -r requirements.txt
cargo build --release
python main.py
```
#### 对于 macOS
> [!IMPORTANT]
> - macOS 的发行形式与 Linux 类似，提供 **源码 + 启动脚本 (.sh)**。  
> - 用户可以通过脚本快速运行，未来可能提供 `.dmg` 安装包。
> - macOS 用户需确保系统已安装 Python3 (推荐≥3.10) 与 Rust (推荐≥1.80)  
> - Apple Silicon (M1/M2/M3/M4) 需要使用 arm64 构建版本，Intel CPU使用amd64构建版本
 
1. 从 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下载为`BadCraftLauncher-版本号-macOS-系统架构.tar.gz`，见下方文件名示例（目前正在开发阶段，没有 Release 被发行）  
```
文件名示例
BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
BadCraftLauncher-1.0RC1-macOS-x86_64.tar.gz
```

2. 解压源码包  
```bash
# 以实际下载的文件名为准
tar -xvzf BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
cd BadCraftLauncher-1.0RC1
```
3. 运行安装/启动脚本
```bash
sh run.sh
```

4. 如果需要开发模式启动，可以手动执行
```
pip install -r requirements.txt
cargo build --release
python main.py
```  

## 📜 版权与开源协议

BCL Launcher 由 **DCR Studio** 开发，版权所有 ©2025 DCR Studio。  保留所有权利。

本项目使用 **GPL-3.0** 开源协议，任何人均可在遵循协议条款的前提下使用、修改和分发本软件。  
详细协议内容请参见 [LICENSE[↗]](./LICENSE) 文件。

> [!WARNING]
> - 你可以自由使用和修改 BCL Launcher，但必须保留原作者署名。  
> - 禁止去除本版权声明用于闭源商业分发。