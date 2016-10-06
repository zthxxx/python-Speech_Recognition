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
apt-get install -y python3-dev
apt-get install -y python3-numpy
apt-get install -y python3-scipy
pip install scipy
apt-get install -y python3-matplotlib
pip install matplotlib

# Audio process packages
ProjectFolder=$(pwd)
PortaudioPackage=pa_stable_v19_20140130.tgz

apt-get install -y libasound-dev
cd ..
wget http://portaudio.com/archives/$PortaudioPackage
tar -zxvf $PortaudioPackage
cd portaudio/
./configure && make
make install
cd ..
rm -f $PortaudioPackage
rm -rf portaudio/
cd $ProjectFolder
apt-get install -y python3-pyaudio
pip install pyaudio

# Curl packages
apt-get install -y libcurl4-gnutls-dev
apt-get install -y python3-pycurl
apt-get install -y python3-pycurl-dbg
pip install pycurl

# Unit test and conver test packages
pip install --upgrade nose
pip install coverage
pip install coveralls

echo "python environment pre install complete OK."