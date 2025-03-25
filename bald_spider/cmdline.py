import sys
import click
from pathlib import Path
from loguru import logger
import os

def execute(argv=None, settings=None):
    """执行命令行命令"""
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        click.echo("请使用以下命令：")
        click.echo("  bald_spider startproject <project_name>")
        click.echo("  bald_spider create_spider <spider_name> <domain>")
        click.echo("  bald_spider run <spider_file>")
        return

    command = argv[1]
    if command == "startproject":
        if len(argv) < 3:
            click.echo("请指定项目名称：")
            click.echo("  bald_spider startproject <project_name>")
            return
        create_project(argv[2])
    elif command == "create_spider":
        if len(argv) < 4:
            click.echo("请指定爬虫名称和域名：")
            click.echo("  bald_spider create_spider <spider_name> <domain>")
            return
        create_spider(argv[2], argv[3])
    elif command == "run":
        if len(argv) < 3:
            click.echo("请指定爬虫文件：")
            click.echo("  bald_spider run <spider_file>")
            return
        run_spider(argv[2])
    else:
        click.echo(f"未知命令: {command}")
        click.echo("可用命令：")
        click.echo("  bald_spider startproject <project_name>")
        click.echo("  bald_spider create_spider <spider_name> <domain>")
        click.echo("  bald_spider run <spider_file>")

def create_project(project_name):
    """创建新项目"""
    project_dir = Path(project_name)
    if project_dir.exists():
        click.echo(f"错误: 目录 {project_name} 已存在")
        return

    # 创建基本目录结构
    project_dir.mkdir()
    
    # 创建目录时使用固定的顺序
    dirs = ["spiders", "items", "middleware", "pipeline", "settings"]
    for dir_name in dirs:
        (project_dir / dir_name).mkdir()

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
    "middleware.user_agent_middleware.RandomUserAgentMiddleware",
    "middleware.proxy_middleware.ProxyMiddleware",
]

# 管道配置
PIPELINE = [
    "pipeline.database_pipeline.DatabasePipeline",
]
""")

    # 创建items初始文件
    items_file = project_dir / "items" / "__init__.py"
    with open(items_file, "w", encoding="utf-8") as f:
        f.write("""from bald_spider import Item, Field

class ExampleItem(Item):
    title = Field()
    link = Field()
    content = Field()
    created_at = Field()
""")

    # 创建middleware初始文件
    middleware_file = project_dir / "middleware" / "__init__.py"
    with open(middleware_file, "w", encoding="utf-8") as f:
        f.write("""from bald_spider import Middleware
from loguru import logger

class BaseMiddleware(Middleware):
    def process_request(self, request):
        pass

    def process_response(self, response):
        return response

    def process_exception(self, request, exception):
        logger.error(f"请求异常: {exception}")
        return request
""")

    # 创建pipeline初始文件
    pipeline_file = project_dir / "pipeline" / "__init__.py"
    with open(pipeline_file, "w", encoding="utf-8") as f:
        f.write("""from bald_spider import Pipeline
from loguru import logger

class BasePipeline(Pipeline):
    def process_item(self, item):
        logger.info(f"处理数据: {item}")
        return item

    def open_spider(self, spider):
        logger.info(f"爬虫 {spider.name} 启动")

    def close_spider(self, spider):
        logger.info(f"爬虫 {spider.name} 关闭")
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
│   └── __init__.py  # 数据模型定义
├── middleware/      # 中间件
│   └── __init__.py  # 中间件定义
├── pipeline/        # 数据处理管道
│   └── __init__.py  # 管道定义
└── settings/        # 配置文件
```

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 创建新的爬虫：
```bash
bald_spider create_spider example example.com
```

3. 运行爬虫：
```bash
bald_spider run spiders/example_spider.py
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
    
    # 显示主目录
    click.echo(f"{project_name}/")
    
    # 按照创建顺序显示目录
    for dir_name in dirs:
        dir_path = project_dir / dir_name
        click.echo(f"    {dir_name}/")
        # 显示目录下的文件
        for file in dir_path.iterdir():
            if file.is_file():
                click.echo(f"        {file.name}")

def create_spider(spider_name, domain):
    """创建新的爬虫文件"""
    # 检查是否在项目目录中
    if not Path("spiders").exists():
        click.echo("错误: 请在项目目录中运行此命令")
        return

    # 创建爬虫文件
    spider_file = Path("spiders") / f"{spider_name}_spider.py"
    if spider_file.exists():
        click.echo(f"错误: 爬虫文件 {spider_file} 已存在")
        return

    with open(spider_file, "w", encoding="utf-8") as f:
        f.write(f"""from bald_spider import Spider, Request
from loguru import logger

class {spider_name.capitalize()}Spider(Spider):
    name = "{spider_name}"
    allowed_domains = ["{domain}"]
    
    def start_requests(self):
        urls = []
        for url in urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # 解析页面
        pass

""")

    click.echo(f"爬虫 {spider_file} 创建成功！")

def run_spider(spider_file):
    """运行爬虫"""
    try:
        # 导入爬虫文件
        import importlib.util
        spec = importlib.util.spec_from_file_location("spider", spider_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 获取爬虫类
        spider_class = None
        for attr in dir(module):
            obj = getattr(module, attr)
            if (isinstance(obj, type) and 
                issubclass(obj, Spider) and 
                obj != Spider):
                spider_class = obj
                break
        
        if not spider_class:
            click.echo("错误: 未找到爬虫类")
            return
            
        # 运行爬虫
        spider = spider_class()
        spider.start_spider()
        
    except Exception as e:
        click.echo(f"错误: {str(e)}")
        logger.exception("运行爬虫时出错") 