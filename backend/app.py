from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/test", methods=["POST"])
def test():
    
    clicked=None
    if request.method == "POST":
        
        data = request.get_json()
        print(data)

        
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()