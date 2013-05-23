import os, sys
import settings
from flask import Flask, request, redirect, url_for, render_template, flash, g, make_response
from werkzeug import secure_filename
import speciesd as pFast

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt'])
 
app = Flask(__name__)
app.secret_key = settings.secret_key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROPAGATE_EXCEPTIONS'] = True

#TODO
#Anweisungen fuer upload/text field
#check/validate upload
#check/validate text field

from flask import g

def after_this_request(f):
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []
    g.after_request_callbacks.append(f)
    return f

@app.after_request
def call_after_request_callbacks(response):
    for callback in getattr(g, 'after_request_callbacks', ()):
        response = callback(response)
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#always called, with every request?
#@app.before_request
#def set_FileName(filename):
#    response.set_cookie('filename', filename)
#        @after_this_request
#        def remember_language(response):
#            response.set_cookie('filename', language)
#    g.language = language

@app.route("/download", methods=['GET'])
def download():
    if request.method == 'GET':
        render_template('download.html')
        name = request.cookies.get('filename')
        print('checker' + name)
        resultList = pFast.main(UPLOAD_FOLDER + name, name.rsplit('.', 1)[0])
        print('results')
        print(resultList)
        return render_template('download.html', pdf=resultList[2], resultImage1=resultList[0], resultImage2=resultList[1])
        # there should be a redirect for broken/not working fastq files & txt files not being fastq

@app.route("/", methods=['GET', 'POST'])   
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        #flash('Uploading the file...This may take some time according to your file size.', 'upload')
        print(request.files.get('file')) #!use get for multiple requests at the same time
        textInput = request.form.get('comments', None)
        fileEnding=''
        try:
#            fileEnding = request.files.get('file').filename.rsplit('.', 1)[1]
            fileName = request.files.get('file').filename
            fileEnding = fileName.rsplit('.', 1)[1]
        except:
            fileEnding=''
        if fileEnding == 'txt':
##            if textInput != None:
##                flash('Please decide on whether to upload a file or to use the text box. Only one can be processed at a time.', 'upload')
##                return redirect(url_for('index'))
            file = request.files.get('file')
            if file and allowed_file(file.filename):                
                filename = secure_filename(file.filename)
                fileFolder = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('You have successfile uploaded your file', 'upload')
#                set_FileName(filename)
                resp = make_response(redirect(url_for('download')))
                print(filename)
                resp.set_cookie('filename', '')
                resp.set_cookie('filename', fileName)
                return resp
#                return redirect(url_for('download'))
                # check unicode/format -> in the other script -> forward to this script ?
                # have db or dict for returning the right jobs
                # let some processing happen here (SCRIPT)
        elif fileEnding == '' and textInput == None:
            flash('Please specify your file\'s location first.', 'upload')
            return redirect(url_for('index'))
        elif fileEnding != 'txt' and textInput == None:
            flash('Only .txt is allowed as input.', 'upload')
            return redirect(url_for('index'))
        if textInput != '':
            flash(textInput.swapcase(), 'process') #use SCRIPT here
            return '''could redirect here'''
            #redirect(url_for('index'))
        return redirect(url_for('index')) #just in case
 
if __name__ == "__main__":
    filename=''
    app.run(port=80, debug=True)
