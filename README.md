# web-project

# 特点
1. 使用starlette ASGI框架， 最流行的框架之一。但框架不重要，只要改api/__init__.py就可以换成其他任何框架
2. 类rpc风格，不使用路径参数，只使用GET/POST，通过自定义动词method区分调用的service。 
3. 类golang error风格，大部分函数返回值最后一个参数
4. 目录结构遵循DDD领域驱动架构。
5. 支持同步请求和后台请求，后台请求通过最佳轻量级实践线程池实现
6. 内置请求审计功能
7. 内置log/metric/trace可观测性功能
7. 

# 构建
docker build --platform linux/amd64 -t app .

# 运行
docker run -p 8000:8000 -it app bash