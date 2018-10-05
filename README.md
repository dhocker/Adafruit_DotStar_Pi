# Fork of Adafruit_DotStar_Pi

DotStar module for Python on Raspberry Pi using Python 3.

# Overview
The current [Adafruit_Dotstar_Pi](https://github.com/adafruit/Adafruit_DotStar_Pi.git) 
package only runs with Python 2 (e.g. 2.7).
This fork supports Python 3, specifically Python 3.6. It may work with
other Python 3 versions (e.g. works with Python 3.5). However, the plan is to keep
this fork working on the latest Python version. Your mileage may vary.

**This fork WILL NOT work on Python 2.**

# Installation
Installation into a VENV is unfortunately manual.

1. Activate the VENV containing Python 3.6
2. make clean (if rebuilding)
3. make or make python3.5 or make python3.6
4. python setup.py install

# Credits
Thanks to the following contributors who have done the real work of getting
Adafruit_Dotstar_Pi to workon on Python 3. This fork mostly combined their pull
requests.

[thomasthiriez](https://github.com/thomasthiriez)
Who fixed up [setup.py](https://github.com/adafruit/Adafruit_DotStar_Pi/pull/22/commits/b613fee2ce5ea03f66ea123c684bb2147e1990c3).

[retroj](https://github.com/retroj)
Who did the heavy lifting reworking dotstar.c for Python 3. 
See [Python 3 compatibility #24](https://github.com/adafruit/Adafruit_DotStar_Pi/issues/24#issuecomment-406747387)
for details.