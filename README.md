# Wireless Signal Strength Meter (wssm)

This is a quick and dirty app I wrote while teaching myself PyQt. 

I wrote this while I was in a remote conference and struggling with random and non-linear wireless network throughput with 500-700 of my colleagues. 

While moving from conference room to confernece room in a large hotel setting, roaming signal strength varies wildly, from distance to the associated AP to walls and doors and other frequency obstructions. 


## Installing
To install this, simply follow these steps: 

```
sudo apt install python3-venv
cd /tmp/
git clone github.com/desrod/wssm
cd wssm
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
./wssm.py
```

If you got all of the dependnecies correct, you should now see something that looks like this: 

![Starting wssm](wssm_gui.png "wssm Interface")


## Running and Monitoring
Click "Start Monitoring" to begin the scanning and monitoring of your WiFi adapter's signal strength. Now you should see something that looks like this: 

![wssm Monitoring](wssm_gui_live.gif "wssm Live")

