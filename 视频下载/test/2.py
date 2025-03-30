from hs_m3u8 import M3u8Downloader
import asyncio
import os
from pathlib import Path

# 获取桌面路径
desktop_path = Path.home() / "Desktop"
url = "https://htv-tos.xet.tech/522ff1e0vodcq1252524126/bb8f7f5a1397757904919688611/playlist_eof.m3u8?sign=9ba84ef710fe60e9a65cd9866dd2dba3&t=67e88165&us=omMmcNluZn"
name = "测试"


async def main():
    dl = M3u8Downloader(
        m3u8_url=url,
        save_path=str(desktop_path / name),  # 将 Path 对象转换为字符串
        max_workers=64
    )
    await dl.run(del_hls=True, merge=True)


if __name__ == "__main__":
    asyncio.run(main())
