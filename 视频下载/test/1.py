from hs_m3u8 import M3u8Downloader
import asyncio
import os
from pathlib import Path

# 获取桌面路径
desktop_path = Path.home() / "Desktop"
url = "https://encrypt-k-vod.xet.tech/522ff1e0vodcq1252524126/b42717b31397757906176056942/playlist_eof.m3u8?sign=75eecce1d1b919cbd31a54108797cb45&t=67e87884&us=PUpcTvKkfo&time=1743245227007&uuid=u_65d66599d5049_zHFstwoMln"
url = "https:\/\/v-tos-k.xiaoeknow.com\/522ff1e0vodcq1252524126\/bb8f7f5a1397757904919688611\/playlist_eof.m3u8?sign=5dce718520c83bd8658dd84140cb0869&t=67e88165&us=HavPCkWpaH"
name = "05 数据结构学习-2025-02-27-夏洛"


async def main():
    dl = M3u8Downloader(
        m3u8_url=url,
        save_path=str(desktop_path / name),  # 将 Path 对象转换为字符串
        max_workers=64
    )
    await dl.run(del_hls=False, merge=True)


if __name__ == "__main__":
    asyncio.run(main())
