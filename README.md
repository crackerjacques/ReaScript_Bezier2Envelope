# ReaScript_Bezier2Envelope

Draw Bezier curve to Reaper envelope.

![GIF](https://github.com/crackerjacques/ReaScript_Bezier2Envelope/blob/main/bezier.gif?raw=true)

# How to Use

Download or clone this repo.

```
git clone https://github.com/crackerjacques/Easing_ReaScript.git
```

and put 2 of scripts in your reaper's scripts dir.

```
pip install pygame numpy tk reapy_boost
```

Launch Reaper then


```
python -c "import reapy_boost; reapy_boost.configure_reaper()"
```

and load  bezier2envelope.py from Action List or type


```
python  bezier2env_main.py 
```

# Problem

It does not yet support decibel scale envelopes, 
and if you want to use it, write once and then run this envelope multiplier.

https://github.com/crackerjacques/Easing_ReaScript/tree/main/Envelope_utility

In addition, reproducibility may be questionable for some curve shapes.
These will be implemented as soon as we come up with a way to improve them.
