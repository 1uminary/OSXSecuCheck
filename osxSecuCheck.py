# -*- coding: utf-8 -*-
import os
import datetime
import time
import re
import json

host = {}
stat = {}

def nameDateTime():
    """이 함수는 host list 에 PC 의 hostname 과 현재날짜, 현재시간을 기록함.
    
    예제:
        다음과 같이 사용:
        >>> nameDatetime()
    """
    result = []
    h = os.popen("hostname").readline().split()
    hostname = h[0]
    result.append(hostname)
    print(hostname)

    dayTime = str(datetime.datetime.now())
    dt = dayTime.split()
    result.append(dt[0])
    result.append(dt[1])
    print(dt[0])
    print(dt[1])

    return result

ndt = nameDateTime()
host["name"] = ndt[0]
host["date"] = ndt[1]
host["time"] = ndt[2]

print(u"PC-01 패스워드 주기적 변경 and PC-02 패스워드 정책이 해당 기관의 보안 정책에 적합하게 설정")
resultCheck = 0
resultCheck1 = 0
result = os.popen("pwpolicy getglobalpolicy").read()
result = result.split()
if not result:
    resultCheck += 1
    resultCheck += 1
else: 
    for r in result:
        r = r.split('=')
        stat[r[0]] = r[1]
        if r[0] == "requiresAlpha":
            if int(r[1]) < 1: resultCheck1 += 1
        elif r[0] == "maxMinutesUntilChangePassword":
            if int(r[1]) > 129600: resultCheck += 1
        elif r[0] == "equiresNumeric":
            if int(r[1]) < 1: resultCheck1 += 1
        elif r[0] == "minChars":
            if int(r[1]) < 8: resultCheck1 += 1
host["pwPolicy"] = stat
if resultCheck == 0 : host["PC-01"] = "true"
else: host["PC-01"] = "false"
if resultCheck1 == 0 : host["PC-02"] = "true"
else: host["PC-02"] = "false"

print(u"PC-04 공유 폴더 제거")
host["PC-04"] = "null"

print(u"PC-05 불필요한 서비스 제거")
host["PC-05"] = "null"

print(u"PC-07 파일 시스템을 NTFS로 포맷")
host["PC-07"] = "null"

print(u"PC-11 최신 서비스팩 적용")
result = os.popen("sw_vers | grep ProductVersion").read()
r = result.split()
host["version"] = r[1]
if r[1] == "10.13.4" : host["PC-11"] = "true"
else: host["PC-11"] = "false"

print(u"PC-15 OS에서 제공하는 침입차단 기능 활성화")
result = os.popen("defaults read /Library/Preferences/com.apple.alf globalstate").read()
result = re.findall("\d+", result)[0]
host["firewallEnable"] = result
if result == "0" : host["PC-15"] = "false"
elif result == "1" : host["PC-15"] = "true" 

print(u"PC-16 화면보호기 대기 시간 설정 및 재시작 시 암호 보호 설정")
result = os.popen("defaults -currentHost read com.apple.screensaver | grep idleTime").read()
result = int(re.findall("\d+", result)[0])
host["screenSaverIdelTime"] = result
if result in range(1,601) : host["PC-16"] = "true"
elif result > 600 : host["PC-16"] = "false"

stringOfJsonData = json.dumps(host, indent=4, sort_keys=False)
fileName = ndt[0] + "_" + ndt[1] + ".json"
f = open(fileName, 'w')
f.write(stringOfJsonData)
f.close()
