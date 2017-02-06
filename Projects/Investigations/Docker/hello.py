from flask import Flask
app = Flask(__name__) # create the application instance :)

@app.route('/')
def hello_world():
    return 'Hello, World! - dockerized version'

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')