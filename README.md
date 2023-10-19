# AsepriteImagesMergerScript
Python script that automatically merges PNGs files into a lossless MP4 video file.

## Why?
Aseprite allows you to export animations in GIF files, these have a huge limitation allowing only 256 colours max, so gradients are essentially broken when exported with Aseprite.
This script solves it merging every single PNG file into a single lossless MP4, to adjust frame durations you need to fill a configuration file `scenes.json` when you describe every single scene in your animation and the frame duration for every frame.

## How
This script assumes you have `ffmpeg` installed and available on your PATH, doesn't matter on what platform you're running this. Ffmpeg allows us to encode multiple static images into a single video, modifying the framerate but keeping the correct pacing.

## Example
Let's say I have an animation where the first 15 frames (1, 15) have a frame duration of 100ms, then from frames 16 to 20 we have a frame duration of 600ms, and then again from 21 to 25 of 100ms, scenes.json will look like this:
```json
[
    {
        "pngs": [1, 15],
        "frame_duration_ms": 100
    },
    {
        "pngs": [16, 20],
        "frame_duration_ms": 600
    },
    {
        "pngs": [21, 25],
        "frame_duration_ms": 100
    }
]
```

That's it, run the `animationsyncer.py` script inside the folder with all PNGs and it will generate the MP4 file automatically, using the scene with highest framerate as the result video framerate.


## Todo
- [ ] Multithread implementation
- [X] Pass PNGs base file name as an argument, without changing the python script

