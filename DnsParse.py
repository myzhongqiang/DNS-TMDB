import datetime
import json
import platform
import requests
from subprocess import Popen, PIPE

# dns解析用到的api
api = "http://api.ip33.com/dns/resolver"

# 待解析的域名
hosts = ["api.themoviedb.org", "image.tmdb.org", "www.themoviedb.org"]

# dns服务商
dnsProvider = ["156.154.70.1", "208.67.222.222"]

# host文件的位置
hostLocate = "/etc/hosts"

# 批量ping
def pingBatch(ips):
    if ips is not None and type(ips) == list:
        for ip in ips[:]:  # 使用[:]复制ips列表，以避免在迭代时修改原列表
            result = pingIp(ip)
            if not result:
                ips.remove(ip)

# ping ip返回ip是否连通
def pingIp(ip) -> bool:
    try:
        ping_process = Popen(["ping", "-c", "1", ip], stdout=PIPE, stderr=PIPE)
        ping_output, ping_error = ping_process.communicate()
        if ping_process.returncode == 0:
            print(f"[√] IP:{ip}  可以ping通")
            return True
        else:
            print(f"[×] IP:{ip}  无法ping通")
            return False
    except Exception as e:
        print(f"Ping IP:{ip} 出错：{str(e)}")
        return False

# 返回host对应domain的解析结果列表
def analysis(domain, dns) -> list:
    params = {
        "domain": domain,
        "type": "A",
        "dns": dns
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"
    }
    try:
        response = requests.post(url=api, data=params, headers=headers)
        ipDics = json.loads(response.text)["record"]
        ips = [dic["ip"] for dic in ipDics]
        return ips
    except Exception as e:
        print("解析dns出错：")
        print(e)

# 写入host信息
def hostWritor(hostDic):
    platInfo = platform.platform().upper()
    if "LINUX" in platInfo:
        hostFile = "/etc/hosts"
    else:
        print("未能识别当前操作系统，且用户未指定host文件所在目录！")
        return

    origin = ""
    with open(hostFile, "r", encoding="utf-8") as f:
        # 之前是否已经写过dns信息
        flag = False
        for eachLine in f.readlines():
            if r"###start###" in eachLine:
                flag = True
            elif r"###end###" in eachLine:
                flag = False
            else:
                if not flag:
                    origin = origin + eachLine
        # 写入新的host记录
        origin = origin.strip()
        origin = origin + "\n###start###\n"
        for eachHost in hostDic:
            for eachIp in hostDic[eachHost]:
                origin = origin + eachIp + "\t" + eachHost + "\n"
        origin = origin + "###最后更新时间:%s###\n" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin = origin + "###end###\n"

    with open(hostFile, "w", encoding="utf-8") as f:
        f.write(origin)

if __name__ == '__main__':
    resultDic = {}
    for host in hosts:
        for dns in dnsProvider:
            records = analysis(host, dns)
            pingBatch(records)
            if records is not None and len(records) > 0:
                if host not in resultDic:
                    resultDic[host] = records
                else:
                    resultDic[host] += records
    hostWritor(resultDic)
