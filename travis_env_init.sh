#!/bin/bash

__COMMENTS__='
# OS: ubuntu 14.04 trusty
# python: 3.5
# pip: 8.1.2 for python3.5
# sudo: required
'

echo "python environment pre install start."
python --version
pip -V

# Scientific computation packages
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-numpy
sudo apt-get install -y python3-scipy
pip install scipy
sudo apt-get install -y python3-matplotlib
pip install matplotlib

# Audio process packages
ProjectFolder=$(pwd)
PortaudioPackage=pa_stable_v19_20140130.tgz

sudo apt-get install -y libasound-dev
cd ..
wget http://portaudio.com/archives/$PortaudioPackage
tar -zxvf $PortaudioPackage
cd portaudio/
./configure && make
sudo make install
cd ..
rm -f $PortaudioPackage
rm -rf portaudio/
cd $ProjectFolder
sudo apt-get install -y python3-pyaudio
pip install pyaudio

# Curl packages
sudo apt-get install -y libcurl4-gnutls-dev
sudo apt-get install -y python3-pycurl
sudo apt-get install -y python3-pycurl-dbg
pip install pycurl

# Unit test and conver test packages
pip install --upgrade nose
pip install coverage
pip install coveralls

echo "python environment pre install complete OK."
