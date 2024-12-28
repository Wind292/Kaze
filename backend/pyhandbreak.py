import os
import subprocess, string, random, json, sqlite3

def remove_video_by_id( video_id):
    json_data = ""
    with open("./downscaleQ.json", 'r') as f:
        json_data = json.load(f)

    # Convert the string into a JSON object if it's a string
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    # Iterate through the videos list and remove the video with the matching ID
    updated_videos = [video for video in json_data["videos"] if video["video"] != video_id]
    
    # Update the videos list
    json_data["videos"] = updated_videos
    
    with open("./downscaleQ.json", 'w') as f:
        json.dump(json_data, f, indent=2)

def gen_rand(length=10):
    characters = string.ascii_lowercase + '123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def formatvid(inputdir: str, user: str, id: str, bitrate=1000, framerate=None, codec="mp4"):
    print("Starting to compress")

    # Build HandBrakeCLI command
    handbrake_command = [
        "HandBrakeCLI",
        "-i", f"./public/{user}/{id}.mp4",
        "-o", f"./public/{user}/c-{id}.mp4",
        "--preset", "Creator 1080p60",
        "-b", str(bitrate),
    ]

    if framerate:
        handbrake_command.extend(["--rate", str(framerate)])

    try:
        result = subprocess.run(handbrake_command, capture_output=True, text=True, check=True)
        print("Compression completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Compression failed: {e.stderr}")
        return

    print("Saved:", id)

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('userinfo.db')
        cursor = connection.cursor()

        # Fetch the user's videos JSON from the database
        cursor.execute("SELECT videos FROM users WHERE userid = ?", (user,))
        result = cursor.fetchone()

        if result is None:
            print("User not found in the database.")
            return

        videos_json = result[0]
        videos = json.loads(videos_json)

        # Update the video entry
        video_found = False
        for video in videos:
            if video["id"] == id:
                video["id"] = f"c-{id}"
                video["compressed"] = True
                video_found = True
                break

        if not video_found:
            print("Video ID not found in the user's video list.")
            return

        # Update the database with the modified videos JSON
        cursor.execute("UPDATE users SET videos = ? WHERE userid = ?", (json.dumps(videos), user))

        connection.commit()
        print("Database updated successfully.")

    except sqlite3.Error as db_error:
        print(f"Database error: {db_error}")

    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    formatvid("vid2.mp4", "wind", bitrate=5000, framerate=60, id='nvida5k')
