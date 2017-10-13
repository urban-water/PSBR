import os
import time 
from time import sleep
import datetime 
import serial


import serial
ser1 = serial.Serial('COM7', 115200, timeout=.1)
ser = serial.Serial('COM5', 9600, timeout=.1)
time.sleep(1)

ser1.write("192\r\n")#phConstant
ser1.write("0.3\r\n")

ser1.write("193\r\n")#phConstant
ser1.write("0.3\r\n")

time.sleep(5)
ts = time.time()
day=datetime.datetime.fromtimestamp(ts).strftime('%d')
hr=datetime.datetime.fromtimestamp(ts).strftime('%H')
minutes=datetime.datetime.fromtimestamp(ts).strftime('%M')

sample_r1_hr=[13,15,17,19,20,21,22,23]
sample_r1_min=[30,30,30,40,30,30,30,30]

sample_r2_hr=[13,15,17,19,20,21,22,23]
sample_r2_min=[53,40,40,48,40,40,40,40]

ph_control_on_hr=12



ph_control_off_r1_hr=20
ph_control_off_r1_min=25

ph_control_off_r2_hr=20
ph_control_off_r2_min=35

mlvss_hr=0
mlvss_min=2

count_r1=0
count_r2=0


ser.write("195\r\n")#R1 pH Controller Off
ser.write("197\r\n")#R2 pH Controller Off


if(int(hr)>=ph_control_on_hr and int(hr)<=ph_control_off_r1_hr):
  ser.write("194\r\n")#R1 pH Controller On
  ser.write("196\r\n")#R2 pH Controller On


if(int(hr)>sample_r1_hr[0] and int(hr)<=sample_r1_hr[1]):
  count_r1=1
  count_r2=1

if(int(hr)>sample_r1_hr[1] and int(hr)<=sample_r1_hr[2]):
  count_r1=2
  count_r2=2
  

if(int(hr)>sample_r1_hr[2] and int(hr)<=sample_r1_hr[3]):
  count_r1=3
  count_r2=3
  

if(int(hr)>sample_r1_hr[3] and int(hr)<=sample_r1_hr[4]):
  count_r1=4
  count_r2=4
  

if(int(hr)>sample_r1_hr[4] and int(hr)<=sample_r1_hr[5]):
  count_r1=5
  count_r2=5
  

if(int(hr)>sample_r1_hr[5] and int(hr)<=sample_r1_hr[6]):
  count_r1=6
  count_r2=6
  

if(int(hr)>sample_r1_hr[6] and int(hr)<=sample_r1_hr[7]):
  count_r1=7
  count_r2=7
  
print count_r1
print count_r2


ser.write("190\r\n")#phSetpoint
ser.write("7.5\r\n")#Send phSetpoint value after cmd phsetpoint

ser.write("191\r\n")#phSetpoint
ser.write("7.5\r\n")#Send phSetpoint value after cmd phsetpoint

ser.write("198\r\n")#R1 Light On
ser.write("203\r\n")#R2 Light On

ser.write("212\r\n")#Mixer R1 On
ser.write("214\r\n")#Mixer R2 on



 
temp_day=day
file_name="D:/UW/Data/%s.csv"%(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
file = open(file_name, "a")
 
if day!=temp_day and os.stat(file_name).st_size == 0:
 file_name="D:/UW/Data/%s.csv"%(datetime.datetime.fromtimestamp(ts).strftime('%m-%d'))
 file = open(file_name, "a")
 file.write("Time,Data,pH,Remark\n")
 temp_day=day

                                     
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


x1=[10]
if os.stat(file_name).st_size == 0:
        file.write("Time,Data,pH,Remark\n")
count=-5

t_end = time.time() + 60 * 60*8

while time.time() < t_end:
 x=ser.readline()
 x1=x.split(':')

 y=ser1.readline()
 y1=y.split(':')
 
 
 if len(x1) == 2:
  print x1
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  hr=datetime.datetime.fromtimestamp(ts).strftime('%H')
  minutes=datetime.datetime.fromtimestamp(ts).strftime('%M')

  if isfloat(x1[1]):
   txt="%s,%s,%s,%s"%(ts,st,x1[0],x1[1])       
   file.write(txt)
   file.flush()
  else:
   count=count+1
   txt="%s,%s,,%s"%(ts,st,x1[1])       
   file.write(txt)
   file.flush()

 if len(y1) == 2:
  print y1
  ts = time.time()
  st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  hr=datetime.datetime.fromtimestamp(ts).strftime('%H')
  minutes=datetime.datetime.fromtimestamp(ts).strftime('%M')

  if isfloat(y1[1]):
   txt="%s,%s,%s,%s"%(ts,st,y1[0],y1[1])       
   file.write(txt)
   file.flush()
   
   if (float(y1[1])>7.5 and y1[0]=='pH1'):
    ser.write("230\r\n")#R1 Acid Pump
    ser.write("2\r\n")#2 sec pump on
    
   if (float(y1[1])>7.5 and y1[0]=='pH2'):
    ser.write("231\r\n")#R1 Acid Pump
    ser.write("2\r\n")#2 sec pump on
    
  else:
   count=count+1
   txt="%s,%s,,%s"%(ts,st,y1[1])       
   file.write(txt)
   file.flush()



 if(int(hr)==sample_r1_hr[count_r1] and int(minutes)==sample_r1_min[count_r1]):
    ser.write("195\r\n")
    ser.write("213\r\n")#
    time.sleep(300)
    ser.write("222\r\n")#
    time.sleep(40)
    ser.write("223\r\n")#
    ser.write("212\r\n")#
    if(count_r1<3):
      ser.write("194\r\n")#
    count_r1=count_r1+1
    
 if(int(hr)==sample_r2_hr[count_r2] and int(minutes)==sample_r2_min[count_r2]):
    ser.write("197\r\n")#
    ser.write("215\r\n")#
    time.sleep(300)
    ser.write("224\r\n")#
    time.sleep(50)
    ser.write("225\r\n")#
    ser.write("214\r\n")#
    if(count_r1<3):
      ser.write("196\r\n")#
    count_r2=count_r2+1

 if(int(hr)==ph_control_off_r1_hr and int(minutes)==ph_control_off_r1_min):
      ser.write("220\r\n")#
      ser.write("195\r\n")#
      
    

 if(int(hr)==ph_control_off_r2_hr and int(minutes)==ph_control_off_r2_min):
      ser.write("221\r\n")#
      ser.write("197\r\n")#
      
 if(int(hr)==mlvss_hr and int(minutes)==mlvss_min):
      ser.write("206\r\n")#
      ser.write("208\r\n")#
      time.sleep(250)
      ser.write("207\r\n")#
      ser.write("209\r\n")#
      

ser.write("201\r\n")#R1 Light On
ser.write("205\r\n")#R2 Light On

ser.write("213\r\n")#Mixer R1 On
ser.write("215\r\n")#Mixer R2 on
time.sleep(1800)

ser.write("216\r\n")#Mixer R2 on
time.sleep(1500)
ser.write("217\r\n")#Mixer R2 on

ser.write("218\r\n")#Mixer R2 on
time.sleep(1500)
ser.write("219\r\n")#Mixer R2 on


ser.close() 
print " Quit" 

