# myproject

这是一个使用 Bald Spider 框架创建的爬虫项目。

## 项目结构

```
myproject/
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
