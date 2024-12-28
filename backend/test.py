import os, time
name = "zydtmoh3qq"
user = "wind"
while True:
    time.sleep(.1)
    try:
        os.remove(f"./public/{user}/{name}.mp4")
        # os.rename(f"./tempvids/{user}-{name}.mp4", f"./public/{user}/{name}.mp4")
    except:
        continue
    break 