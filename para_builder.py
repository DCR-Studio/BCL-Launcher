# Parameter Builder v1.0
# (C)2025 DCR Studio.

import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime

now=datetime.now()
formatted_date=now.strftime("%Y-%m-%d %H-%M-%S")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=f"bcl_para_builder-{formatted_date}.log"
)

def validate_minecraft_path(path: str) -> bool:
    # 校验Minecraft主文件路径合法
    try:
        path = Path(path).resolve()
        return path.exists() and path.is_dir()
    except Exception:
        return False

def build_minecraft_command(
        game_path:str,
        version:str,
        use_modloader:bool,
        min_mem:int,
        max_mem:int,
        java_path:str,
        username:str,
        token:str,
) -> list[str]:
    # 校验参数
    if not validate_minecraft_path(game_path):
        raise ValueError("Invalid game path.")
    if min_mem > max_mem:
        raise ValueError("Min mem must <= max mem.")

    java_bin =Path(java_path) / "bin" / "java.exe"
    if not java_bin.exists():
        raise FileNotFoundError('Java binary not found') 

    command=[
        str(java_bin),
        f"-Xms{min_mem}M",
        f"-Xmx{max_mem}M",
        f"-Djava.library.path={Path(game_path)/'versions'/version/'natives'}",
        "-cp",
        f"{Path(game_path)/'libraries'}/*;{Path(game_path)/'versions'/version/f'{version}.jar'}",
        "net.minecraft.client.main.Main",
        "--username",username.strip(),
        "--version",version,
        "--gameDir",game_path,
        "--assetsDir",f"{Path(game_path)/'assets'}",
        "--assetsIndex",version.split('.')[0],
        "--accessToken",token,  #危险项，尽快处理
        "--userType","mojang",
    ]

    logged_command = command.copy()
    logged_command[logged_command.index("--accessToken") + 1] = "[Hidden]"
    logging.debug('START COMMAND: ')
    logging.debug(' '.join(logged_command))

    return command

try:
    cmd = build_minecraft_command(
        game_path="<PATH>",
        version="<VERSION>",
        use_modloader=False,
        min_mem="<MEM>",
        max_mem="<MEM>",
        java_path="<PATH>",
        username="<NAME>",
        token="<TOKEN>",
    )
    logging.info("Successfully build parameter.")
except Exception as exc:
    logging.error(f"FAIL: {exc}")
    print(f"FAIL: {exc}")
