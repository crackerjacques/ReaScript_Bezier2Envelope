# ReaScript_Bezier2Envelope

Draw Bezier curve to Reaper envelope.

![GIF](https://github.com/crackerjacques/ReaScript_Bezier2Envelope/blob/main/bezier.gif?raw=true)

# How to Use

Download or clone this repo.

```
git clone https://github.com/crackerjacques/ReaScript_Bezier2Envelope
```
and put 2 of scripts in your reaper's scripts dir.


Install the required packages.
```
pip install pygame numpy tk reapy_boost
```

Launch Reaper then

```
python -c "import reapy_boost; reapy_boost.configure_reaper()"
```

and load  bezier2envelope.py from Action List or 


```
python  bezier2env_main.py 
```
type in your terminal.

# Problem

It does not yet support decibel scale envelopes, 
and if you want to use it with Volume fader, write once and then run this envelope multiplier.

https://github.com/crackerjacques/Easing_ReaScript/tree/main/Envelope_utility


In addition, reproducibility may be questionable for some curve shapes.
These will be implemented as soon as I come up with a way to improve them.
