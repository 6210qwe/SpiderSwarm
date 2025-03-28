from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bald_spider",
    version="0.1.2",
    author="MindLullaby",
    author_email="3203939025@qq.com",
    description="A distributed spider framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/6210qwe/SpiderSwarm",
    packages=find_packages(include=['bald_spider', 'bald_spider.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "lxml",
        "loguru",
        "urllib3",
        "curl_cffi",
        "aiomysql",
        "aiohttp",
        "click"
    ],
    entry_points={
        'console_scripts': [
            'bald_spider=bald_spider.cmdline:execute',
        ],
    },
) 