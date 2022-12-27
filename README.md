# HRMS_Timekeeper


## <b>Connection - SSH</b>
2 way:
* Lan
* wifi
### Step by step
Easy way:
* Connect Lan cable
* Check connected client at 192.168.1.1 or use [Advanced IP Scanner](https://www.advanced-ip-scanner.com/) (use VPN if can not access)
* Get IP with named Raspberry pi foundation
* Open CMD or terminal and run\
```ssh pi@<<IP>>```\
or use PUTTY to ssh
account infor: pi/lemon

### <b>Desktop remote</b>
2 way:
* via VNC
* via window remote desktop

### VIA VNC:
* ssh to pi
* run sudo raspi-config
* select ```Interfacing Options```
* Enable ```VNC```

## Main source
run 
```python3 as608.py``` for auto run app\
run
```python3 as608_feature.py``` for default feature\
other file can be ignored

## datasheet

raspberry pi 3: [datasheet](https://www.google.com/search?q=raspberrypi+datasheet&rlz=1C1ONGR_enVN955VN955&sxsrf=ALiCzsYWzLzl-t-SZeTuW4CP2ZT47-M6nA:1672135704235&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj456r1xpn8AhU4QPUHHZyNB9IQ_AUoAXoECAEQAw&biw=1920&bih=937&dpr=1#imgrc=AlEeh-fnVD2uDM)