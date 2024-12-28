import os, time

while True:
    time.sleep(19)
    for dir in os.listdir("public"):    
        complist = []
        fulllist = []
        for file in dir.listdir():
            if file.startswith("c-"):
                complist.append(file)
            else:
                fulllist.append(file)
        for file in fulllist:
            if "c-" + file not in complist:
                try:
                    os.remove(f"public/{dir}/{file}")
                except:
                    pass