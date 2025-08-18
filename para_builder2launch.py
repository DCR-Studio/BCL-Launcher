# -*- coding: utf-8 -*-
# Parameter Builder2Launch v1.1
# Bad Craft Launcher Core Component.
# (C)2025 DCR Studio.

import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime
import json

# 初始化日志 Initialize log
now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H-%M-%S")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=f"bcl_para_builder-{formatted_date}.log"
)

def validate_minecraft_path(path: str) -> bool:
    try:
        path = Path(path).resolve()
        return path.exists() and path.is_dir()
    except Exception:
        return False

def detect_main_class(version_dir: Path, version: str) -> str:
    version_json = version_dir / f"{version}.json"
    if version_json.exists():
        try:
            data = json.loads(version_json.read_text(encoding='utf-8'))
            # 使用arguments.client解析更精确的启动参数，保证声音和语言资源被正确加载
            # Use <arguments.client> to resolve precise startup paraments to ensure that all game files are loaded normally.
            return data.get('mainClass', 'net.minecraft.client.main.Main')
        except Exception:
            return 'net.minecraft.client.main.Main'
    return 'net.minecraft.client.main.Main'

def build_classpath(game_path: Path, version: str) -> str:
    version_dir = game_path / "versions" / version
    version_jar = version_dir / f"{version}.jar"

    if not version_jar.exists():
        raise FileNotFoundError(f"版本 JAR 文件不存在 The version JAR file does not exist: {version_jar}")

    jars = [str(j) for j in (game_path / "libraries").rglob("*.jar")]
    jars.append(str(version_jar))

    sep = ";" if os.name == "nt" else ":"
    cp_string = sep.join(jars)
    return cp_string

def get_assets_info(game_path: Path, version: str):
    version_json = game_path / "versions" / version / f"{version}.json"
    if not version_json.exists():
        return None, None
    try:
        data = json.loads(version_json.read_text(encoding='utf-8'))
        asset_index = data.get("assetIndex", {})
        # 使用id字段保证对应版本精确调用资源
        # Use the ID field to ensure precise invocation of the corresponding version's resources.
        assets_index = asset_index.get("id", data.get("assets", "legacy"))
        return str(game_path / "assets"), assets_index
    except Exception:
        return None, None

def build_minecraft_command(
        game_path: str,
        version: str,
        use_modloader: bool,
        min_mem: int,
        max_mem: int,
        java_path: str,
        username: str,
        token: str,
) -> list[str]:
    if not validate_minecraft_path(game_path):
        raise ValueError("Invalid game path.")
    if min_mem > max_mem:
        raise ValueError("Min mem must <= max mem.")

    java_bin = Path(java_path) / "bin" / ("java.exe" if os.name == "nt" else "java")
    if not java_bin.exists():
        raise FileNotFoundError('找不到Java二进制文件 Java binary not found')

    version_dir = Path(game_path) / "versions" / version
    main_class = detect_main_class(version_dir, version)
    cp_string = build_classpath(Path(game_path), version)

    assets_dir, assets_index = get_assets_info(Path(game_path), version)
    # 构建一个启动参数列表 Build a list of startup parameters.
    command = [
        str(java_bin),
        f"-Xms{min_mem}M",
        f"-Xmx{max_mem}M",
        f"-Djava.library.path={version_dir/'natives'}",
        "-cp", cp_string,
        main_class,
        "--username", username.strip(),
        "--version", version,
        "--gameDir", game_path,
        "--uuid", "00000000-0000-0000-0000-000000000000",
        "--accessToken", token,
        "--userType", "offline",
        "--versionType", "BadCraftLauncher",
        "--assetIndex", assets_index,  # 强制传入assetsIndex，保证文件正常加载
        "--assetsDir", assets_dir,
        #"--demo" #以测试版打开(可选)
    ]

    logged_command = command.copy()
    if "--accessToken" in logged_command:
        logged_command[logged_command.index("--accessToken") + 1] = "[Hidden]"
    logging.debug('START COMMAND: ')
    logging.debug(' '.join(logged_command))

    return command

try:
    cmd = build_minecraft_command(
        game_path=r"D:\BCL_Testmc\.minecraft", # 开发人员需要将其更换为自己的具体的.minecraft的路径，注意不是.minecraft/.minecraft
        version="1.14.4", # 你是什么版本你就填什么
        use_modloader=False, # 现在没有模组加载器的支持，开发人员请使用原版测试
        min_mem=2048, # 最小内存
        max_mem=4096, # 最大内存
        java_path=r"D:\JDK\jdk-24.0.2", # 定位到自己的Java文件夹(找到你的java.exe[Win]或者java[Linux/macOS])
        username="SteveOffline", # 符合Minecraft命名规范，不得出现中文，不得出现违规符号如./\-[]()<>?'";:!@#$%^&*+=——，只允许出现_(下划线)符号
        token="0", # 离线用户没有AccessToken
    )
    logging.info("参数构建成功 Successfully build parameter.")
except Exception as exc:
    logging.error(f"FAIL: {exc}")
    print(f"FAIL: {exc}")
    cmd = []

# 通过subprocess执行启动命令 Use <subprocess> library to execute the startup command.
if cmd:
    process = subprocess.Popen(cmd)
    process.wait()