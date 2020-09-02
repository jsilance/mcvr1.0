sudo apt-get install screen -y
sudo apt-get install python3-tk -y

wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103 -y
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libjasper-dev -y

sudo pip3 install pillow --upgrade

wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

sudo pip install opencv-contrib-python==4.1.0.25


sudo cp testgui.py /home/pi/Desktop/testgui.py
cd /home/pi/Desktop
python3.7 testgui.py