# coding=utf-8
from demo_sms_send import send_sms
import uuid
import json
import requests
import time

#短信发送记录
def log(contain):
    logfile = open("data/log.txt",'a')
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    w = t+","+contain['location']+","+contain['name']+","+contain['weather']+"<br/>\n"
    logfile.write(w)
    logfile.close()


#-----------------短信设置---------------------
#发送短信
def sendmsg(user,key,msg_p):
    #设置短信的business_id
    __business_id = uuid.uuid1()

    #阿里云的短信签名
    signame = "短信签名"

    #阿里云的短信模板CODE
    modelnumber = "短信模板编号"

    #短信设置说明:‘我使用的模板是 ${name},${location}一小时内将有${weather},请注意哦!’ 需要有三个变量
    for i in range(len(user[key]['user'])):
        contain = {"name":user[key]['user'][i]['name'],"location":key,"weather":msg_p}
        print(contain)
        print(send_sms(__business_id,user[key]['user'][i]['phone'],signame,modelnumber,contain))
        log(contain)
	#延迟一秒
        time.sleep(1)
    user[key]['delay']=time.time()


#降水时间函数
def prec_time(forecast,small,middle,heavy,storm):
    #设置降水时间初值为-1
    small_t =-1
    middle_t=-1
    heavy_t =-1
    storm_t =-1

    #获取各级别降水时间
    for i in range(len(forecast)):
        if forecast[i] >= small:
            small_t = i
            break
    for i in range(len(forecast)):
        if forecast[i] >= middle:
            middle_t = i
            break
    for i in range(len(forecast)):
        if forecast[i] >= heavy:
            heavy_t = i
            break
    for i in range(len(forecast)):
        if forecast[i] >= storm:
            storm_t = i
            break
    return small_t,middle_t,heavy_t,storm_t


#----------------预报设置---------------------
caiyunapi_key="彩云API_KEY" #彩云API_KEY
small_rain = 0.05 #小雨阀值
middle_rain = 0.25 #中雨
heavy_rain = 0.32 #大雨
storm_rain = 0.4 #暴雨
delay_time = 14400 #预警间隔时间，单位秒



#----------------程序开始---------------------
#读取用户文件
userfile = open('data/user.json','r')
user = json.loads(userfile.read())
userfile.close()

for key in user:
    if time.time()-user[key]['delay']>delay_time:
        print('地点:'+key)
        #获取预报
        print('开始连接彩云API')
        page = requests.get("https://api.caiyunapp.com/v2/"+caiyunapi_key+"/"+user[key]["location"]+"/forecast.jsonp?")
        print('连接成功')
        data = json.loads(page.text)
        forecast = data['result']['minutely']['precipitation']
        #print(forecast)
        #获取时间
        st,mt,ht,stt = prec_time(forecast,small_rain,middle_rain,heavy_rain,storm_rain)
        print(st,mt,ht,stt)
        #----开始判断----
        #当前无雨,稍后有雨
        if st>0:
            #有暴雨
            if stt>0:
                print("稍后将有暴雨")
                sendmsg(user,key,"暴雨")

            #有大雨
            elif ht>0:
                print("稍后将有大雨")
                sendmsg(user,key,"大雨")

            #有中雨
            elif mt>0:
                print("稍后有中雨")
                sendmsg(user,key,"中雨")

        #当前只下小雨,稍后有大雨或暴雨
        elif st==0:
            #暴雨
            if stt>0:
                print("当前小雨,稍后有暴雨")
                sendmsg(user,key,"暴雨")
            #大雨
            elif ht>0:
                print("当前小雨,稍后有大雨")
                sendmsg(user,key,"大雨")
            else:
                print("当前小雨,稍后无大雨(不发送)")
        else:
            print("1小时内无雨(不发送)")
    else:
        print("在延迟时间内已预警")
    print("-----------------------")
print("更新用户文件...")
newfile = open('data/user.json','w+')
newfile.write(json.dumps(user,ensure_ascii=False))
newfile.close()
print("程序完成")
