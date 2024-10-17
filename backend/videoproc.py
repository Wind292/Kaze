from flask import Flask, jsonify, request

app = Flask(__name__)

# Example of handling POST requests
@app.route('/handle-upload', methods=['POST'])
def upload():
    data = request.json

        

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
