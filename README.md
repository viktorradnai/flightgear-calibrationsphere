# flightgear-calibrationsphere

This project is an "aircraft" addon for Flightgear which can be used for screen calibration. The aircraft model is a sphere with the pilot's viewpoint located in the centre of it. This makes it possible to use the pilot view for screen calibration. On a flat display, lens distortion is visualised. On a spherical or cylindrical display (if you have one), you should not see any distortion.

<div align="center">
<img src="https://raw.githubusercontent.com/viktorradnai/flightgear-calibrationsphere/master/Splash/screenshot1.png" width="600">
<img src="https://raw.githubusercontent.com/viktorradnai/flightgear-calibrationsphere/master/Splash/example1.png" width="600">
<img src="https://raw.githubusercontent.com/viktorradnai/flightgear-calibrationsphere/master/Splash/example2.png" width="600">
</div>

The included Python script `sphere.py` can be used to convert an AC3D file (the format used by Flightgear) to a combination of two materials with a chessboard pattern. This script was used to convert a plain sphere created in Blender to the 3D model used.
