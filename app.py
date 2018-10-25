
from flask import Flask, render_template, flash, request, redirect, url_for,jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_wtf.csrf import CSRFProtect
import os
import threadcam
import dbops,register,hashlib
from thread import start_new_thread as newthread
import capture as cap
# App config.
csrf = CSRFProtect()
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 

@app.route('/',methods=['GET'])
def home():
    form = ReusableForm(request.form)
 
    print form.errors
    print request.form 
    return render_template('hello.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def signup():
    form = ReusableForm(request.form)
    print form.errors
    print request.form
    attr={}
    if request.method == 'POST':
        attr['fname']=request.form['fname']
        attr['lname']=request.form['lname']
        attr['empid']=request.form['empID']
        password=request.form['password']
        phash=hashlib.sha256()
        hashobj=register.twoWordHash(attr['empid'],password)
        attr['PassHash']=hashobj.getHash()
        message=register.signup(attr)
        print message
        return render_template('hello.html', form=form, status_msg=message)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = ReusableForm(request.form)
    print form.errors
    print request.form
    attr={}
    global init_flag
    try:
       init_flag
    except Exception as e:
        cap.init()
        init_flag=True
    if request.method=='POST':
        attr['empid']=request.form['empID']
        password=request.form['password']
        print str(attr)+" "+str(password)
        cameraStatus=cap.statusUpdate()
        authResult=register.authcreds(attr['empid'],password) 
        if authResult and attr['empid']!='admin':
            return render_template('demo.html', form=form, cap_image="./images/image_icon.png",
                                   analysis_image="./images/image_icon.png",camStatus=cameraStatus,
                                   user=attr['empid'])
        elif authResult and attr['empid']=='admin':
            return render_template('admin.html', form=form, cap_image="./images/image_icon.png",
                                   camStatus=cameraStatus,user=attr['empid'])
        else:
            return render_template('hello.html', form=form, auth_msg="Authentication Failed")

@app.route("/capture",methods=['GET'])
def capture():
    cap_image = "./images/image_icon.png"
    analysis_image = "./images/image_icon.png"
    form=ReusableForm(request.form)
    print form.errors
    print request.form
    cap_status,cap_image,analysis_image=cap.captureAnalyse(request.args['empid'])

    if not(cap_status):
         # return render_template('demo.html', form=form, cap_image="./images/image_icon.png",analysis_image="./images/image_icon.png",status_msg=cap_status)
        cap_image = "./images/image_icon.png"
        analysis_image = "./images/image_icon.png"
        response = {"cap_image": cap_image, "analysisImage": analysis_image}
        print response
        return jsonify(response)
    else:
        # return render_template('demo.html', form=form, cap_image=img_path,analysis_image=anlysis_image_path)
        response = {"cap_image": cap_image, "analysisImage": analysis_image}
        print response
        return jsonify(response)

@app.route("/refresh_Camera",methods=['GET'])
def refresh_Camera():
    form=ReusableForm(request.form)
    print form.errors
    print request.form
    message=cap.init()
    print message
    return message
    # return  render_template('demo.html', form=form, cap_image="./images/image_icon.png",analysis_image="./images/image_icon.png",camStatus=message)

@app.route("/capture_ref",methods=['GET'])
def capture_ref():
    form = ReusableForm(request.form)
    print form.errors
    print request.form
    cap_status, img_path, anlysis_image_path = cap.captureAnalyse(request.args['empid'])
    if not (cap_status):
         cap_image="./images/image_icon.png"
         return cap_image
    else:
        return img_path

@app.route('/getIcons',methods=['GET'])
def getIcons():
        imgpath='./images/image_icon.png'
        return imgpath
    # return redirect(url_for('refresh_Camera'),cap_image="./images/image_icon.png",analysis_image="./images/image_icon.png",camStatus=message)
if __name__ == "__main__":
    app.run()
    

