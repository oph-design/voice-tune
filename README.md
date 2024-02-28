<h1 align="center">VoiceTune</h1>

<p align="center">
  <img src="https://github.com/oph-design/voice-tune/assets/106475996/324721b7-815f-4b9d-9a43-22c134ce74f2" alt="Logo resized">
</p>

VoiceTune is an innovative application designed to enhance the driving experience by allowing users to adjust in-vehicle settings through voice commands. Our goal is to make driving safer and more convenient for everyone by minimizing distractions and enabling drivers to keep their focus on the road.

## Features

- **Voice-Activated Controls**: Easily adjust your car's settings without lifting a finger.
- **Safety First**: Designed with safety in mind to ensure that you can use all the features without taking your eyes off the road.

## How to use VoiceTune
1. Install requirements
   ```
   pip install -r requirements.txt
   ```
2. Install databroker / kuksa client
   ```
   docker run -it --rm --net=host ghcr.io/eclipse/kuksa.val/databroker:master --insecure
   ```
3. Run program
   ```
   python src/harmony.py
   ```
4. Use a voice command for the in-vehicle settings to change, e.g. "Move the seat back by 15 degrees"
5. See the values being adjusted


## VoiceTune Initial Thoughts
![image](https://github.com/oph-design/voice-tune/assets/106475996/50c50e08-30af-454f-9d1a-781a02d112a4)

## VoiceTune Final Concept
![VoiceTune](https://github.com/oph-design/voice-tune/assets/106475996/17994715-e897-4214-bca8-e3878ff18fff)

## VoiceTune Future Features
- **Acceleration**
- **Cabin**
- **CO2 Emissions**
- **Connectivity**
- **Current Location**
- **Infotainment**
- **Service**
- **Vehicle Identification**

## Team Members
- Ole - [@oph-design](https://github.com/oph-design)
- Ismail - [@ipatel4](https://github.com/ipatel4)
- Flavia - [@dendeaisd](https://github.com/dendeaisd)
- Ramy - [@letsgogeeky](https://github.com/letsgogeeky)
- Raffael - [@Raffael-Passion](https://github.com/Raffael-Passion)
