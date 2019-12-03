from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/test", methods=["POST"])
def test():
    name_of_slider = request.form["name_of_slider"]
    print(name_of_slider)
    return render_template('index.html', slider = name_of_slider)

if __name__ == '__main__':
    app.run()