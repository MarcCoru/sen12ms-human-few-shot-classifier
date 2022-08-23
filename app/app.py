from flask import Flask, render_template, request
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import os
from datetime import datetime
import json
from waitress import serve


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
#cors = CORS(app, resources={r"/predict_petal_length": {"origins": "*"}})

JSON_RECORDS_FILE = "app/static/records.json"

@app.route('/')
def index():
    userid = request.args.get('userid')
    if userid is None:
        userid = ""
    return render_template("index.html", userid=userid)

"""
@app.route('/generateimages')
def generateimages():

    ways=4
    shots=2
    num_batches=1000

    testtasks, stats = sample_testtasks(data_root="/ssd/sen12ms128", ways=ways, shots=shots, num_batches=num_batches)

    # delete previous images
    dirpath = os.path.join("app","static","img")
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        os.makedirs(dirpath)

    def save_png(image, path):
        import numpy as np
        from PIL import Image
        arr = (image * 255).transpose(0,2).numpy().astype(np.uint8)
        im = Image.fromarray(arr)
        im.save(path)

    for idx in range(num_batches):
        row = stats.iloc[idx]

        train_X, train_y, train_meta = testtasks[idx][1]["train"]
        test_X, test_y, test_meta = testtasks[idx][1]["test"]
        (train_meta)

        os.makedirs(os.path.join("app","static","img",str(idx), "train"), exist_ok=True)
        os.makedirs(os.path.join("app","static","img",str(idx), "test"), exist_ok=True)

        i = 0
        for class_id in range(ways):
            for shot in range(shots):

                path = os.path.join("app","static","img",str(idx), "train",f"{class_id}-{shot}.png") #train_meta[i][0].replace("/","-") +
                with open(os.path.join("app","static","img",str(idx), "train", "meta.txt"), 'a') as f:
                    print(class_id, shot, train_meta[i][0], file=f)
                save_png(train_X[0,i], path)

                path = os.path.join("app","static","img",str(idx), "test", f"{class_id}-{shot}.png")
                with open(os.path.join("app","static","img",str(idx), "test", "meta.txt"), 'a') as f:
                    print(class_id, shot, test_meta[i][0], file=f)
                save_png(test_X[0,i], path)

                i += 1


    return "generating images"
"""

def append_record(record):
    if os.path.exists(JSON_RECORDS_FILE):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    print(append_write)
    with open(JSON_RECORDS_FILE, append_write) as f:
        json.dump(record, f)
        f.write(os.linesep)

@app.route('/dropevent', methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['data']
    data = json.loads(jsdata)
    data["timestamp"] = datetime.now().isoformat()
    data["ip"] = request.environ['REMOTE_ADDR']
    print(data)
    append_record(data)
    #x = mongocollection.insert_one(data)

    return jsdata

@app.route('/plot')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

if __name__ == "__main__":
#   app.run(host='0.0.0.0', ssl_context='adhoc') ##Replaced with below code to run it using waitress
   serve(app, host='0.0.0.0', port=80)
