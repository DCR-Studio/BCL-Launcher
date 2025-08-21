<h1 align="center">BCL Launcher</h1>

<p align="center">
  <img src="./assets/logo.svg" alt="BCL-Launcher Logo" width="150">
</p>

<div style="text-align: center; margin: 10px 0;">
  <a href="../README.md" style="margin: 0 15px;">简体中文</a>
  <a href="README_ENG.md" style="margin: 0 15px;">English</a>
  <a href="README_RUS.md" style="margin: 0 15px;">Русский</a>
</div>

<h3 align="center">輕量化 · 可定制 · 開放 · 以使用者為中心的 Minecraft 啟動器</h3>

---

## ❓ BCL Launcher 是什麼？
**BCL Launcher**（全名 **Bad Craft Launcher**），由 [DCR Studio[↗]](https://github.com/DCR-Studio) 開發的 **輕量化、可定制的 Minecraft 啟動器**，秉持「以使用者為中心」理念。  

- 使用 **Rust + Python** 混合開發  
- 我們提供 **完全 Rust 編寫的核心內核** [HyperLightBCLCore[↗]](https://github.com/DCR-Studio/OpenBCLCore)  
- 完全 **開源**，任何人皆可參與  

---

## 🚀 特點與優勢
### 🔒 安全  
- 使用非對稱加密與系統級密鑰存儲器保護使用者敏感資料  
- Rust 記憶體安全 + Python 層的可控邏輯  

### 👍 穩定可靠  
- Rust 保證核心模組穩定運行  
- 即使在低配環境下也能順暢執行  

### 💻 跨平台  
- 支援多平台（Windows / Linux / macOS）  
- Python 負責 UI 與邏輯，快速適配不同系統  

### ✨ 靈活擴展  
- 支援插件（Plugin）與腳本系統  
- 豐富的第三方庫生態，開發者可快速擴充功能  

### 🧩 模組化設計 + Plugin 介面  
- 核心性能模組由 **Rust** 編寫，保證速度與安全  
- 各模組間透過 **IPC（進程間通訊）** 聯絡，確保高效與安全的資料交換  
- 高層邏輯、設定與擴充功能由 **Python** 編寫，靈活易維護  
- 模組解耦，方便快速迭代、除錯與替換  
- 開發者可依需求單獨修改或新增元件，而無須大幅改動整個專案  

---

## 📦 安裝與使用
### 下載
> [!IMPORTANT]  
> ❌**目前專案仍在開發階段，暫時未放出 Release**
- [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases)

### 啟動
#### 對於 Windows
- Windows 通常以 zip 壓縮檔形式發行。
1. 從 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下載 `BadCraftLauncher-版本號-Windows-系統架構.zip`，下方為檔名示例（目前開發中，尚未發行 Release）
```
檔名示例
BadCraftLauncher-1.0RC1-Windows-x86\_64.zip
```
2. 開啟可執行檔

#### 對於 Linux
> [!IMPORTANT]
> - Linux 的啟動流程與 Windows 不同，發行形式為 **原始碼 + 安裝腳本 (.sh)**  
> - 您需先下載原始碼包，再執行腳本完成建置與啟動  
> - 系統需安裝 Python3（建議 ≥3.10）與 Rust（建議 ≥1.80）
1. 從 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下載 `BadCraftLauncher-版本號-Linux-系統架構.tar.gz`，下方為檔名示例（目前開發中，尚未發行 Release）  
```
#檔名示例
BadCraftLauncher-1.0RC1-Linux-x86\_64.tar.gz
````

2. 解壓原始碼包  
```bash
# 以實際下載的檔名為準
tar -xvzf BadCraftLauncher-1.0RC1-Linux-x86_64.tar.gz
cd BadCraftLauncher-1.0RC1
````

3. 執行安裝/啟動腳本

```bash
sh run.sh
```

4. 若需開發模式啟動，可手動執行

```bash
pip install -r requirements.txt
cargo build --release
python main.py
```

#### 對於 macOS

> \[!IMPORTANT]
>
> * macOS 發行方式與 Linux 類似，提供 **原始碼 + 啟動腳本 (.sh)**
> * 使用者可透過腳本快速啟動，未來可能提供 `.dmg` 安裝包
> * macOS 系統需安裝 Python3 (建議 ≥3.10) 與 Rust (建議 ≥1.80)
> * Apple Silicon (M1/M2/M3/M4) 使用 arm64 架構版本，Intel CPU 使用 amd64 架構版本

1. 從 [GitHub Release[↗]](https://github.com/DCR-Studio/BCL-Launcher/releases) 下載 `BadCraftLauncher-版本號-macOS-系統架構.tar.gz`，下方為檔名示例（目前開發中，尚未發行 Release）

```
# 檔名示例
BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
BadCraftLauncher-1.0RC1-macOS-x86_64.tar.gz
```

2. 解壓原始碼包

```bash
# 以實際下載的檔名為準
tar -xvzf BadCraftLauncher-1.0RC1-macOS-arm64.tar.gz
cd BadCraftLauncher-1.0RC1
```

3. 執行安裝/啟動腳本

```bash
sh run.sh
```

4. 若需開發模式啟動，可手動執行

```bash
pip install -r requirements.txt
cargo build --release
python main.py
```

---

## 📜 版權與開源協議

BCL Launcher 由 **DCR Studio** 開發，版權所有 ©2025 DCR Studio。保留所有權利。

本專案使用 **GPL-3.0** 開源協議，任何人在遵守協議條款下皆可使用、修改與發佈軟體。
詳細協議內容請參見 [LICENSE[↗]](./LICENSE) 文件。

> \[!WARNING]
>
> * 可自由使用與修改 BCL Launcher，但必須保留原作者署名
> * 禁止移除本版權聲明用於閉源商業發佈

此繁體中文文件由 ChatGPT 翻譯
	