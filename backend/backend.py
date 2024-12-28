from flask import Flask, request, jsonify, send_from_directory, abort
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
import pyhandbreak
from flask import Flask
from flask_cors import CORS
import threading
import sqlite3
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './public'
USER_LIST_FILE = './userlist.json'
PASSWORDS_FILE = './passwords.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def valid_username(username):
    return username.isalnum() or '_' in username

def gen_rand_name(length=10):
    import random
    characters = 'abcdefghijklmnopqrstuvwxyz123456789'
    return ''.join(random.choice(characters) for _ in range(length))



def auth(username, password):
    try:
        connection = sqlite3.connect('userinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE userid = ?", (username,))
        result = cursor.fetchone()

        if result and result[0] == password:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        connection.close()

def add_vid_json(username, new_element):
    try:
        connection = sqlite3.connect('userinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT videos FROM users WHERE userid = ?", (username,))
        result = cursor.fetchone()

        if not result:
            print("User not found in database.")
            return

        videos = json.loads(result[0])
        videos.append(new_element)

        cursor.execute("UPDATE users SET videos = ? WHERE userid = ?", (json.dumps(videos), username))
        connection.commit()

        print("New element added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()



@app.route('/')
def home():
    return 'Stop doing that'

@app.route('/pullvid', methods=['POST', "GET"])
def pullvid():
    request_username = request.args.get('u')  # For GET requests
    request_video = request.args.get('v')

    if request.method == 'POST':
        # For POST requests, fetch data from the body
        request_username = request.form.get('u') or request_username
        request_video = request.form.get('v') or request_video

    if not request_username or not request_video:
        return abort(400, "Missing username or video")

    file_path = f"C:/Rand/git/Kaze/backend/public/{request_username}"
    file_name = f"{request_video}.mp4"
    
    try:
        return send_from_directory(file_path, file_name, as_attachment=True)
    except FileNotFoundError:
        return abort(404, "File not found")
    
# @app.route('/startnc', methods=['GET'])
# def start_nc():
#     if not compque:
#         return jsonify({"message": "No tasks"}), 204

#     task = compque.pop(0)
#     return jsonify({"message": task}), 200

# @app.route('/finishnc', methods=['POST'])
# def finish_nc():
#     if 'file' not in request.files:
#         return 'No file uploaded.', 400

#     file = request.files['file']
#     path = request.form.getlist('path')

#     if not path or len(path) < 2:
#         return 'Invalid path.', 400

#     save_path = os.path.join(app.config['UPLOAD_FOLDER'], path[0], path[1])
#     os.makedirs(os.path.dirname(save_path), exist_ok=True)

#     file.save(save_path)
#     return f"File {file.filename} uploaded successfully.", 200

@app.route('/iscompressed', methods=['GET'])
def is_compressed():
    username = request.args.get('u')
    video_id = request.args.get('v')

    try:
        connection = sqlite3.connect('userinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT videos FROM users WHERE userid = ?", (username,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "User not found"}), 404

        videos = json.loads(result[0])
        for video in videos:
            if video["id"] == video_id or video["id"] == f"c-{video_id}":
                return jsonify({"compressed": video["compressed"]})

        return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error"}), 500
    finally:
        connection.close()


@app.route('/usrinfo/<username>', methods=['GET'])
def usr_info(username):
    try:
        connection = sqlite3.connect('userinfo.db')
        cursor = connection.cursor()

        cursor.execute("SELECT displayname, bio, videos FROM users WHERE userid = ?", (username,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "User not found"}), 404

        user_info = {
            "userid": username,
            "display_name": result[0],
            "bio": result[1],
            "videos": json.loads(result[2])
        }
        return jsonify(user_info)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error"}), 500
    finally:
        connection.close()

@app.route('/passwordcheck', methods=['GET'])
def password_check():
    username = request.args.get('username')
    password = request.args.get('password')

    if auth(username, password):
        return "Ok"
    return "Invalid username or password"

@app.route('/createaccount', methods=['GET'])
def create_account():
    connection = sqlite3.connect('userinfo.db')
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT NOT NULL PRIMARY KEY,
        displayname TEXT NOT NULL,
        bio TEXT,
        password TEXT NOT NULL,
        videos TEXT NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    
    bio = request.args.get('bio')
    raw_id = request.args.get('id', '').lower()
    display_name = request.args.get('disname')
    password = request.args.get('password')

    if not valid_username(raw_id):
        return 'Not a valid User ID, tip: User IDs can only be numbers, lowercase letters, and _'

    try:
        cursor.execute("SELECT userid FROM users WHERE userid = ?", (raw_id,))
        if cursor.fetchone():
            return 'Username already taken'

        cursor.execute("INSERT INTO users (userid, displayname, bio, password, videos) VALUES (?, ?, ?, ?, ?)",
                       (raw_id, display_name, bio, password, json.dumps([])))
        connection.commit()

        print("Account created")
        return 'Ok'
    except Exception as e:
        print(f"Error: {e}")
        return 'Internal Server Error', 500
    finally:
        connection.close()

@app.route('/uploadvideo', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"message": "No video uploaded"}), 400

    video = request.files['video']
    username = request.form.get('user', 'unknown')
    password = request.form.get('password')
    title = request.form.get('title')

    if not auth(username, password):
        return jsonify({"message": "Incorrect and/or missing credentials"}), 401

    user_dir = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_dir, exist_ok=True)

    file_id = gen_rand_name()
    filename = file_id + ".mp4"
    file_path = os.path.join(user_dir, filename)

    video.save(file_path)

    add_vid_json(username, {"name": title, "id": file_id, "compressed": False})
    
    data = ""
    compQ_item = {
        "user": username,
        "video": file_id
    }
    with open("downscaleQ.json", 'r') as file:
        data = json.load(file)

    data["videos"].append(compQ_item)

    with open("downscaleQ.json", 'w') as file:
        json.dump(data, file, indent=4)

    comp_thread = threading.Thread(target=pyhandbreak.formatvid, args=(file_path, username, file_id))
    comp_thread.start()

    return jsonify({"message": "Video uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)
