# -*- coding: utf-8 -*-

#                Bad Craft Launcher                #
# Copyright (C) 2025 DCR Studio.All right reserved #

import re
import os
import sys
import hashlib
import subprocess
import threading
import time
import psutil
import uvicorn
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import win32api
import tempfile



# ==================== 配置日志 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"launch_check.log"),  # 日志输出到文件
        logging.StreamHandler()  # 日志输出到控制台
    ]
)
logger = logging.getLogger(__name__)

# ======================提权=======================
# 提权部分在正式发布期间需要注释或删除并在pyinstaller封装时加"--uac"参数
def administrator():
    try:
        testfile = os.path.join(os.getenv('windir'),"get_permission.txt")
        open(testfile,"w").close()
    except OSError:
        return False
    else:
        os.remove(testfile)
        return True

# ==================== 硬件检测 ====================

def get_windows_version():
    """
    获取Windows操作系统的版本信息，返回一个元组(major_version, minor_version, build_number)
    """
    version_info = sys.getwindowsversion()
    major_version = version_info.major
    minor_version = version_info.minor
    build_number = version_info.build
    return major_version, minor_version, build_number

def is_unsupported_windows_version():
    """
    检查当前Windows版本是否为不支持的版本
    """
    if sys.platform != "win32":
        # 如果不是Windows系统，直接返回False
        return False

    major_version, minor_version, build_number = get_windows_version()

    # 检查是否为Windows 8 (build 9200) 或更低版本
    if (major_version == 6 and minor_version <= 2 and (build_number == 9200 or minor_version < 2)) or \
            (major_version < 6):
        return True

    return False

def check_hardware_software():
    """
    检查硬件和软件环境
    """
    if is_unsupported_windows_version():
        logger.warning("This computer may not be supported and there may be issues. It is recommended to run on Windows 8.1 and above operating systems.")
    else:
        logger.info("Windows version is supported.")

    # 检查内存
    memory = psutil.virtual_memory()
    logger.info(f"Total memory: {memory.total / 1024**2} MB")
    if memory.total / 1024**2 < 2048:
        logger.error("The installed memory of the computer is insufficient (less than 2048 MB).")
        sys.exit(1)
    else:
        logger.info("Memory check passed.")

    # 检查磁盘空间
    current_file_path = os.path.abspath(__file__)
    disk_root = os.path.splitdrive(current_file_path)[0] + '\\'
    disk_usage = psutil.disk_usage(disk_root)
    logger.info(f"Disk free space: {disk_usage.free / 1024**3} GB")
    if disk_usage.free / 1024**3 < 4:
        logger.error("This disk does not have enough free space (less than 4 GB).")
        sys.exit(1)
    else:
        logger.info("Disk space check passed.")

    # 检查 Python 是否安装
    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Python Installed: {result.stdout.strip()}")
        else:
            logger.error("Python not found.")
            sys.exit(1)
    except FileNotFoundError:
        logger.error("Python not found.")
        sys.exit(1)

# ==================== 路径检测 ====================
def is_in_temp():
    # 获取当前程序的绝对路径
    current_file = os.path.abspath(__file__)
    
    # 获取系统临时目录路径
    temp_dir = tempfile.gettempdir()
    
    # 判断程序路径是否位于临时目录中
    try:
        return os.path.commonpath([current_file, temp_dir]) == temp_dir
    except ValueError:
        # 如果路径不在同一个盘符（Windows 下可能出现），直接返回 False
        return False
def contains_chinese(path):
    """
    检查路径中是否包含中文字符
    """
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(chinese_pattern.search(path))

def check_path():
    """
    检查当前路径是否包含中文字符
    """
    current_directory = os.getcwd()
    logger.debug(f"Current directory: {current_directory}")
    if contains_chinese(current_directory):
        logger.error("The file path should not contain Chinese characters.")
        sys.exit(1)
    else:
        logger.info("Path check passed.")

# ==================== CURL检测 ====================

app = FastAPI()

def generate_1kb_file(filename):
    """
    生成 1KB 的文件
    """
    content = "a" * 1024  # 1KB 的内容
    with open(filename, "w") as f:
        f.write(content)
    logger.info(f"Generated 1KB file: {filename}")
    return filename

def calculate_sha256(filename):
    """
    计算文件的 SHA256 校验值
    """
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    logger.info(f"Calculated SHA256 for file: {filename}")
    return sha256_hash.hexdigest()

@app.get("/download")
def download_file():
    """
    文件下载路由
    """
    filename = generate_1kb_file("1kb_file.txt")
    logger.info(f"Serving file for download: {filename}")
    return FileResponse(filename, filename="cdown.txt")

@app.get("/verify")
def verify_file():
    """
    校验文件路由
    """
    original_file = "1kb_file.txt"
    downloaded_file = "cdown.txt"

    if not os.path.exists(downloaded_file):
        logger.error("Downloaded file does not exist.")
        return {"error": "File not found."}

    original_hash = calculate_sha256(original_file)
    downloaded_hash = calculate_sha256(downloaded_file)

    if original_hash == downloaded_hash:
        logger.info("File verification successful: Hashes match.")
        return {"message": "The verification of file SHA256 is the consistent.", "original_hash": original_hash, "downloaded_hash": downloaded_hash}
    else:
        logger.error("File verification failed: Hashes do not match.")
        return {"message": "The verification of file SHA256 is the inconsistent.", "original_hash": original_hash, "downloaded_hash": downloaded_hash}

@app.get("/shutdown")
def shutdown_server():
    """
    关闭 FastAPI 服务
    """
    import os
    import signal
    logger.info("Shutting down FastAPI server...")
    os.kill(os.getpid(), signal.SIGINT)
    return {"message": "Server is shutting down..."}

def curl(url, output):
    """
    模拟 curl 下载
    """
    logger.info(f"Downloading file from {url} to {output}")
    subprocess.run(["curl", "-o", output, url], check=True)

def main():
    """
    主函数
    """
    # 启动 FastAPI 服务
    threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()
    logger.info("FastAPI Service started!")

    # 等待服务启动
    time.sleep(2)

    # 下载文件
    curl("http://127.0.0.1:8000/download", "cdown.txt")

    # 校验文件
    result = verify_file()
    logger.info(f"Verification result: {result}")

    # 关闭 FastAPI 服务
    requests.get("http://127.0.0.1:8000/shutdown")

# ==================== 主程序 ====================
#print(administrator())
#if administrator():
#    logger.info("Successfully get Administrator permission")
#    if __name__ == "__main__":
#        check_hardware_software()
#
#        if is_in_temp==False:
#            logger.info("IS NOT IN TEMP CHECK PASS")
#        elif is_in_temp==True:
#            logger.error("IS NOT IN TEMP CHECK FAIL")
#        check_path()
#
#        main()
#else:
#    logger.error("Failed get Administrator permission")
#    win32api.ShellExecute(None,"runas",sys.executable,__file__,None,1)
if __name__ == "__main__":
    check_hardware_software()
    logger.info(f"Program in temp folder:{is_in_temp()}")
    if is_in_temp==False:
        logger.info('PITCheck Pass')
    if is_in_temp==True:
        logger.error('PITCheck FAIL')
    check_path()
    main()
