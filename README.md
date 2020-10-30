# wf_get
获取开启wifi设备探测帧信息
# 三个模块 && `mysql`

> 依赖 `ubuntu16.04`,`python3`

`argparse`用来解析命令行

`scapy`通过网卡用来获取数据

`sqlalchemy`用`ORM`模型与数据库交互

`mysql`存储数据

## argparse

支持python2,3

https://docs.python.org/3/library/argparse.html?highlight=parse_arg

## scapy

> 2.4及以上版本支持python3
>
> 版本兼容python2

https://scapy.readthedocs.io/en/latest/introduction.html

## sqlalchemy

> 1.2及以下版本支持python2
>
> 1.3及以上版本支持python3

https://www.sqlalchemy.org/blog/#sqlalchemy-1.3.19-released

# `wf_get`

> 文件结构

```sh
|-setup.sh	#建立环境，安装依赖
|-menu.py		#初始界面设置，解析命令,开始运行，获取数据并上传
|-fetch
|	|____ fetch_client.py  #定义client表，解析数据包，定义相同mac时间间隔等
|
|-readme.md		#wf_get项目说明
```

> 文件说明

```python
>>> menu.py
def main():
    设置解析命令行参数
class Wf_get:    
	def init
    	初始数据 执行 go
	def go:
        获取数据，上传数据
        self.get_data()
		self.write_local_db()
	def get_data:
        sniff获取数据，packeteer解析
    def packeteer:
    	解析合适的数据存到列表
    def write_local_db:
        从列表里获取解析过的数据,过滤一定时间相同mac数据，上传	
```

```python
>>> fetch_client.py
engine=create_engine()
Session_client = sessionmaker(bind=engine)
#建立对应数据库连接   
class client:
    定义对应表
def flush_data:
    过滤一定时间相同mac数据的函数
def get_next_id:
    直接上传到数据库，获取id字段
def proc_packet:
    初步解析包，获取需要的数据
```

> 使用说明

```
wf_get -m <monitor>		#用monitor监听数据，并上传到本地数据库
```



```sh
usage: wf_get [-h] [-m MONITOR] [-t TIME] [-p PROBEMAC]

positional arguments:
  g                     get information default(true)

optional arguments:
  -h, --help            show this help message and exit
  -m MONITOR, --monitor MONITOR
                        type the monitor name you have
  -t TIME, --time TIME  get same mac_packet until <time> seconds later
  -p PROBEMAC, --probemac PROBEMAC
                        type <probemac> to location

run with `-m <monitor> -p <probemac> ` to get information
```

截图

![image-20201025213730828](/home/zzl/.config/Typora/typora-user-images/image-20201025213730828.png)
