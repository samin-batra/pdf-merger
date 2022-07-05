import flask
from flask import Flask,render_template, flash
import os
import PyPDF2

app = Flask(__name__)
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return filename.split(".")[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload",methods=['POST'])
def upload():
    print(f"Upload: {UPLOAD_PATH}")
    print(flask.request.files.getlist("files"))
    uploaded_files = flask.request.files.getlist("files")
    print(uploaded_files)
    if not uploaded_files:
        app.logger.info("No files were uploaded")
        flash("Please upload a file to continue")
    else:
        mergeFile = PyPDF2.PdfFileMerger()
        merged_file_name = ""
        for file in uploaded_files:
            file_name = file.filename
            if allowed_file(file_name):
                merged_file_name += "" + file_name.split(".")[0]
                mergeFile.append(PyPDF2.PdfFileReader(file.stream))
        mergeFile.write(UPLOAD_PATH + f"\\{merged_file_name}" + ".pdf")
        return flask.send_from_directory(app.config['UPLOAD_FOLDER'],merged_file_name+".pdf")

            # file.save(UPLOAD_PATH+)
    # return "hello"


if __name__=='__main__':
    app.run(debug=True)