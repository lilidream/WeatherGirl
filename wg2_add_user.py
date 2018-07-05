# coding=utf-8
import json

new_name = input("请输入新用户用户名：")
new_phone = input("请输入新用户手机号码：")


#读取用户文件
datafile = open("data/user.json",'r')
data = json.loads(datafile.read())
datafile.close()

print("列出已存有地点:")
print("-------------------")
for key in data:
    print(key)
print("-------------------")
new_l = input("新用户地点是否已经存在?(y/n)")

#地点已存在
if new_l == 'y' or new_l == 'Y':
    location = input("请输入地点：")
    new = {'name':new_name,'phone':new_phone}
    data[location]['user'].append(new)

#地点未存在
else:
    location = input("请输入新增的地点名称：")
    ll = input("请输入新增地点的经纬度(例如：116.7901,31.3124)：")
    new = {'location':ll,'delay':0,'user':[{'name':new_name,'phone':new_phone}]}
    data[location] = new

#写入文件
newfile = open("data/user.json",'w+')
newfile.write(json.dumps(data,ensure_ascii=False))
newfile.close()

print("新增用户完成")
