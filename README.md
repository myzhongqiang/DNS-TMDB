群晖系统，自动更新访问TMDB API的DNS，支持写入到群晖系统hosts文件，搭配群晖任务技术实现自动更新。(用某位大佬的代码基础上结合ai修改得到的，忘记那位大佬的一下子搜索不到）

一、套件安装Python

二、 把”DnsParse.py“下载下来，导入到群晖群晖的你想放的文件夹里面。

三、查询自己的PY目录
SHH命令查询如下

which python
which python3

四、打开控制面板，任务计划新建任务，用户账户类型：Root，计划每天某个时间点就行，任务设置-运行命令用户自定义脚本写入

/bin/python3 /volume1/docker/DnsParse.py，

其中“/bin/python3”替换自己which python which python3查询得到的目录；

其中“/volume1/docker/DnsParse.py”修改为自己的存放的DnsParse.py文件的路径。

四、ssh命令查询是否修改成功，输入
cat /etc/hosts
