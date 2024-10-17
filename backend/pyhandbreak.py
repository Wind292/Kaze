import subprocess, string, random



def gen_rand(length=10):
    characters = string.ascii_lowercase + '123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def formatvid(inputdir, user, bitrate=1000, framerate=None, codec="mp4", name=None):
    if not name: name = gen_rand()
    command = f'HandBrakeCLI.exe -i {inputdir} -o "./public/{user}/{name}.mp4" -f av_{codec} -b {bitrate} -e nvenc_h265'
    if framerate: command += ' -r ' + str(framerate)

    result = subprocess.run(command, capture_output=True, text=True)
    print("Saved: " + name)

if __name__ == "__main__":
    formatvid("vid2.mp4", "wind", bitrate=5000, framerate=60, name='nvida5k')
