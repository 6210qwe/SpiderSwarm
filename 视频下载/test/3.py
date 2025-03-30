from hs_m3u8 import M3u8Downloader
import asyncio
import os
from pathlib import Path

# 获取桌面路径
desktop_path = Path.home() / "Desktop"
url = "https://encrypt-k-vod.xet.tech/522ff1e0vodcq1252524126/dab666141397757905719800962/playlist_eof.m3u8?sign=ba3e7a322000935d7ad80f4f690282b3&t=67e822f6&us=bAyTWrDXAL&time=1743223325350&uuid=u_65d66599d5049_zHFstwoMln"
name = "03 初识Java编程课-2025-02-23-夏洛"


async def main():
    dl = M3u8Downloader(
        m3u8_url=url,
        save_path=str(desktop_path / name),  # 将 Path 对象转换为字符串
        max_workers=64
    )
    await dl.run(del_hls=False, merge=True)


if __name__ == "__main__":
    asyncio.run(main())
