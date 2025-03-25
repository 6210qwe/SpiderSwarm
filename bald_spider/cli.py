import os
import click
import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"

@click.group()
def main():
    """Bald Spider 命令行工具"""
    pass

@main.command()
@click.argument('project_name')
def create(project_name):
    """创建新的爬虫项目"""
    # 创建项目目录
    project_dir = Path(project_name)
    if project_dir.exists():
        click.echo(f"错误: 目录 {project_name} 已存在")
        return

    # 创建基本目录结构
    project_dir.mkdir()
    (project_dir / "spiders").mkdir()
    (project_dir / "items").mkdir()
    (project_dir / "middleware").mkdir()
    (project_dir / "pipeline").mkdir()
    (project_dir / "settings").mkdir()

    # 创建配置文件
    settings_file = project_dir / "settings" / "settings.py"
    with open(settings_file, "w", encoding="utf-8") as f:
        f.write("""# 爬虫配置
SPIDER_NAME = "my_spider"
SPIDER_DOMAIN = "example.com"

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "spider_db",
    "user": "root",
    "password": "password"
}

# 并发配置
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# 中间件配置
MIDDLEWARE = [
    "bald_spider.middleware.RandomUserAgentMiddleware",
    "bald_spider.middleware.ProxyMiddleware",
]

# 管道配置
PIPELINE = [
    "bald_spider.pipeline.DatabasePipeline",
]
""")

    # 创建爬虫文件
    spider_file = project_dir / "spiders" / "example_spider.py"
    with open(spider_file, "w", encoding="utf-8") as f:
        f.write("""from bald_spider import Spider, Request
from loguru import logger

class ExampleSpider(Spider):
    name = "example_spider"
    allowed_domains = ["example.com"]
    
    def start_requests(self):
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # 解析页面
        items = response.xpath("//div[@class='item']")
        for item in items:
            yield {
                "title": item.xpath(".//h2/text()").get(),
                "link": item.xpath(".//a/@href").get(),
            }
""")

    # 创建项目说明文件
    readme_file = project_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"""# {project_name}

这是一个使用 Bald Spider 框架创建的爬虫项目。

## 项目结构

```
{project_name}/
├── spiders/          # 爬虫文件
├── items/           # 数据模型
├── middleware/      # 中间件
├── pipeline/        # 数据处理管道
└── settings/        # 配置文件
```

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行爬虫：
```bash
python -m bald_spider run spiders/example_spider.py
```
""")

    # 创建依赖文件
    requirements_file = project_dir / "requirements.txt"
    with open(requirements_file, "w", encoding="utf-8") as f:
        f.write("""bald-spider>=0.1.1
requests>=2.31.0
lxml>=4.9.3
loguru>=0.7.2
aiomysql>=0.2.0
aiohttp>=3.9.1
""")

    click.echo(f"项目 {project_name} 创建成功！")
    click.echo(f"目录结构：")
    for root, dirs, files in os.walk(project_dir):
        level = root.replace(str(project_dir), '').count(os.sep)
        indent = ' ' * 4 * level
        click.echo(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            click.echo(f"{subindent}{f}")

if __name__ == '__main__':
    main() 