# easyBJUT
软件工程——工大助手，其中python爬虫部分，负责将教务上的信息爬取到本地。

## 功能
1. 登录
2. 查询成绩

## 使用方式
因为要生成excel文件，所以需要对目标文件夹有写操作权限。

文件中用到了BeautifulSoup、xlwt，所以需要相应包的支持。

在命令行中执行如下操作运行程序：
``` python
python easyBJUT
```

可以通过setup.py生成可执行文件，但需要用到py2exe，命令如下：
``` python
python setup.py py2exe
```

## 问题
没有做到相应的问题处理模块，如果在使用过程中有任何问题，请联系bjxx5555@126.com