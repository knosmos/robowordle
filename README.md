# RoboWordle

3D Printer plays Wordle


https://user-images.githubusercontent.com/30610197/156936611-31ae89e9-2f76-4c8c-8465-29292354509c.mov

# Capabilities
- [X] Precise 3D printer movement
- [X] 3D printed stylus holder and camera mount for keypresses and image acquiration
- [X] Fiducial detection and dewarping to make system robust against suboptimal camera position / angle
- [X] Image processing with OpenCV for color identification

# Installation
This project is not designed for widespread use, but if you do want to make it, here are the setup instructions.
### Dependencies
- `opencv-python`
- `printrun`
- `numpy`
- `pyserial`

### Assembly
1. Print out [the fiducial sheet](https://github.com/knosmos/robowordle/blob/master/assets/april.png) (must be original size, otherwise the scale will be wrong) and attach to 3D printer
2. Attach stylus to the print head (I designed [this mount](https://github.com/knosmos/robowordle/blob/master/assets/mount.stl), but it will differ depending on the printer and stylus you use). Note that the stylus must be in contact with a sufficiently large conductive object for the capacitive touch to work (I used an alligator clip attached to the printer frame)
3. Mount the camera (placement does not need to be precise as long as all four fiducials are clearly visible).
4. *The following step is only necessary if you are calibrating for a device that has dimensions different from my iPhone 6*
    - Place the phone on the fiducial sheet and run [dewarp.py](https://github.com/knosmos/robowordle/blob/master/dewarp.py); this will produce a dewarped image like this: ![dewarped](https://user-images.githubusercontent.com/30610197/156937382-6b345fbe-0ba6-48ad-9353-af39108b8c47.png)
    - Run [testing/marker.py](https://github.com/knosmos/robowordle/blob/master/testing/marker.py) to determine the location of each key. Click each key on the in order to mark the position; once all 27 keys (delete key is not used) are selected, copy-paste the positions to [config.py](https://github.com/knosmos/robowordle/blob/master/config.py)
    - Run [testing/grid-finder.py](https://github.com/knosmos/robowordle/blob/master/testing/grid-finder.py); click the top-left and lower-right corners of the wordle grid, then copy-paste the positions to config.py as well.
5. Connect the 3D printer to your laptop, cross your fingers, and run (main.py)[https://github.com/knosmos/robowordle/blob/master/main.py].


# Future plans
- [ ] automatic end-of-game detection
- [ ] more robust color detection
- [ ] support for more devices