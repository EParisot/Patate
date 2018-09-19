# Patate42
An autonomous RC car to compete the IronCar Challenge...

![](IMG_20180210_150832.jpg)

Patate42 won the first (and third) french IronCar race edition !!!

# Installation :

## on Raspberry :

```
git clone https://github.com/EParisot/Patate.git
cd Patate
pip install -r requirement.txt
```

To use a Xbox gamepad :
```
sudo apt-get install xboxdrv
```

## on Computer :

```
git clone https://github.com/EParisot/Patate.git
cd Patate/Data_processing/Training
pip install -r requirement.txt
```

# Usage :

## Collect Data (manual drive + take images/labels) (RPi) :

```
cd Data_processing
sudo python Auto_datamining_pad.py 0.1
```
to take one picture every 0.1 sec (to just control without taking pictures, don't specify any value)

If you don't have Xbox Gamepad, you can use the computer keyboard (opencv needed, to install opencv on your RPi : https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)

```
cd Data_processing
python Auto_datamining_key.py 0.1
```

Or you can use the built-in car controler and labelise by hand later:

```
cd Data_processing
python Manual_datamining.py
```

## Train model (Computer) :

```
cd Patate/Data_processing/Training
jupyter notebook
```

## AutoPilot (RPi) :

```
cd Patate
python patateScript_threaded.py myModel.h5
```

