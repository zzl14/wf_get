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
|	|_____server.py			#在指定ip：port提供web上传服务
|
|-plugins
|	|_____json2time.py  #将datetime类型转换，方便json转换上传
|
|-readme.md		#wf_get项目说明
|_data.txt		#记录上次没上传成功的数据
```

## 程序流程

```
流程图    		
    		开始执行
######################################    
      		__
			||
    		\/
        是否有data.txt,数据添加到all_data
        	||				
			||				
    		\/ 				
    	获取数据到packet
    	是否上传数据?
    ||			|			
	||			|	  
	\/			否-->packet存到本地数据库
    是					   
 packet存到all_data
 每隔n秒，all_data是否有数据 
    ||			 	  |	
	||				  |	 				
	\/				 否------->继续获取数据
    是							/\
本地文件web上传到server  			||
	||							||
  web上传成功？					 ||
	||	  |						||					
	||	  |						||					
	\/	  否——保存数据到data.txt———-
    是		
删除本地all_data    
########################################  
```



> 查看本地是否有data.txt
> 有的话json.loads(line)加入self.all_data，文件清空
>
> while True:
> 	获取数据
>     符合格式，加入packet
>     packet不为空，写入本地数据库，
>     		如果相同mac超过3秒，存入本地数据库
>         	转换time格式，加入all_data
>     每隔5秒上传数据
>     		从all_data获取数据，json.dumps()后上传
>         	上传成功。all_data赋为空
>             失败，all_data保存到data.txt，all_data赋为空



## 使用说明

```sh
run with `-m <monitor> -p <probemac> -t <time> -s <server>` to get and upload information 
run with ` -webserver 0.0.0.0:5001` to run web server
```



```sh
optional arguments:
  -h, --help            show this help message and exit
  -m MONITOR, --monitor MONITOR
                        type the monitor name you have
  -s SERVER, --server SERVER
                        type the url of your server to upload
  -webserver WEBSERVER  run your web server<ip:port>
  -t FLUSH_DATA_TIME, --flush_data_time FLUSH_DATA_TIME
                        get same mac_packet until <time> seconds later
  -p PROBEMAC, --probemac PROBEMAC
                        type <probemac> to location

```

