from subprocess import call
from json import load
from os import remove
from sys import argv

def create_scene_txt_file(start, end, filename, scene_counter):
    with open(f"scene{scene_counter}.txt", "w") as f:
        for input in range(start, end+1):
            if (start == end):
                f.write( f"file '{filename}{start}.png'\n")
            f.write( f"file '{filename}{input}.png'\n")

def create_video_txt_file(number_of_scenes):
    with open("video.txt", "w") as f:
        for input in range(0, number_of_scenes):
            f.write( f"file 'fixed_video{input}.avi'\n")

def get_max_framerate(scenes):
    max_framerate = 0
    for scene in scenes:
        if (scene['fps'] > max_framerate):  max_framerate = scene['fps']
    
    return max_framerate

def compute_fps_for_scene(scenes):
    for scene in scenes:
        if(scene['pngs'][0] == scene['pngs'][1]): scene['fps'] = round(1000/(scene['frame_duration_ms']/2), 2)
        else: scene['fps'] = round(1000/scene['frame_duration_ms'], 2)

def main():
    file = open("scenes.json", "r")
    scenes = load(file)
    file.close()

    compute_fps_for_scene(scenes)

    max_framerate = get_max_framerate(scenes)
    print(scenes)
    
    #Checking if the project name has been inserted
    if (len(argv) < 2): 
        print("ERROR: You forgot the basefile name, try again with: python3 animationsyncer.py animationname")
        print("Where animationname is animationname.png, animationname.png, ecc...")
        return
    filename = argv[1]


    scene_counter = 0

    for scene in scenes:
        create_scene_txt_file(scene['pngs'][0], scene['pngs'][1], filename, scene_counter)
        call(["ffmpeg", "-y", "-r", str(scene['fps']), "-f", "concat", "-i", f"scene{scene_counter}.txt", "-c:v", "libx264rgb", "-crf", "0", f"video{scene_counter}.avi"])

        call(["ffmpeg", "-y", "-i", f"video{scene_counter}.avi", "-r", str(max_framerate), "-c:v", "libx264rgb", "-crf", "0", f"fixed_video{scene_counter}.avi"])

        #removing useless files
        remove(f"video{scene_counter}.avi")
        remove(f"scene{scene_counter}.txt")
        scene_counter+=1

    #Merge avi files
    create_video_txt_file(scene_counter)
    call(["ffmpeg", "-y", "-f", "concat", "-i", "video.txt", "-c:v", "libx264rgb", "-crf", "0", "result.mp4"])

    #remove useless files
    remove(f"video.txt")
    for video in range(0, scene_counter):
        remove(f"fixed_video{video}.avi")

if (__name__ == "__main__"): main()