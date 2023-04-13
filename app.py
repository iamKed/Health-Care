from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
import os
from keras.utils import load_img,img_to_array
from keras.models import load_model
from keras.preprocessing import image
import warnings
from sklearn.preprocessing import StandardScaler
from sqlalchemy import Engine, create_engine, select 
warnings.filterwarnings('ignore')
model= pickle.load(open("Trained_Models/heart.pkl",'rb'))
model_diabetes=pickle.load(open("Trained_Models/diebites_model_best.pkl",'rb'))
from gevent.pywsgi import WSGIServer 
# engine=create_engine('sqlite:///database.db')
from werkzeug.utils import secure_filename
mri_model=load_model(r'Trained_Models\BrainTumor.h5')
app=Flask(__name__)
app.secret_key = b'82736781_@*@&(796*5&^5)'
covid_19_model=load_model(r"Trained_Models\covid_model.h5")
bone_model=load_model(r"Trained_Models\best_model_bone.h5")
skin_model=load_model(r"Trained_Models\skin_d.h5")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['LOGIN_STATUS']=False
app.config['USERNAME']=str('')
answer=''
app.config['UPLOAD_FOLDER']=r'static/files'
class Mainn(db.Model):
    mail=db.Column(db.String, primary_key=True)
    age=db.Column(db.Integer,nullable=False)
    cp=db.Column(db.String(300),nullable=False)
    cardio=db.Column(db.String, nullable=False)
    hr=db.Column(db.Integer, nullable=False)
    bs=db.Column(db.String, nullable=False)
    bp=db.Column(db.Integer,nullable=False)
    sc=db.Column(db.Integer, nullable=False)
    enduced=db.Column(db.String, nullable=False)

class Old_Authentication(db.Model):
    email=db.Column(db.String, primary_key=True )
    password=db.Column(db.String, nullable=False)

class New_Authentication(db.Model):
    name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, primary_key=True)
    password=db.Column(db.String,nullable=False)
    gender=db.Column(db.String, nullable=False)
    age=db.Column(db.Integer, nullable=False)
#preprocessing codes

#preprocessing for brain Tumor module
def preprocess_img_mri(img_path):
    xtest_image = load_img(img_path, target_size=(150,150,3))
    xtest_image = img_to_array(xtest_image)
    xtest_image = np.expand_dims(xtest_image, axis = 0)
    predictions = (mri_model.predict( xtest_image)> 0.5).astype("int32")
    return predictions
    
@app.route('/login',methods=['GET','POST'])
def login_user():
    if request.method=='POST':
        mail=request.form['mail']
        password=request.form['password']
        print(mail,password)
        user = New_Authentication.query.filter_by(email=mail).first()

        if user:
            tag=''
            with db.engine.connect() as conn:
                result = conn.execute(select(New_Authentication.password).where(New_Authentication.email==mail))
                passw=(str(result.all()[0][0]))
                name = conn.execute(select(New_Authentication.name).where(New_Authentication.email==mail))
                app.config['USERNAME']=(str(name.all()[0][0]))
                print(app.config['USERNAME'],passw)

            if passw==password:
                app.config['LOGIN_STATUS']=True
                print(app.config['USERNAME'])
                return redirect('/')
            
            else:
                app.config['USERNAME']=''
                tag="Wrong password"
                return render_template('login.html',alrmsg=tag)
            
        else:
            tag='No such User Exists! Please Register Yourself!'
            # tag="No such User Exists!Please Register Yourself!"
            return render_template('login.html',alrmsg=tag)
    return render_template('login.html')


@app.route('/logout',methods=['GET','POST'])
def logout_user():
    app.config['LOGIN_STATUS']=False
    app.config['USERNAME']=''
    return redirect('/')

@app.route('/')
def refresh():
    print("Ked",app.config['USERNAME'],app.config['USERNAME'])
    return render_template("homepage.html",status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/registration',methods=['GET', 'POST'])
def registration():
    if request.method=='POST':
        fn=request.form['fname']
        ln=request.form['lname']
        email=request.form['email']
        gender=request.form['inlineRadioOptions']
        age=int(request.form['age'])
        password=request.form['password']
        name=fn+' '+ln
        print(name,email,password,email,gender)
        new_auth=New_Authentication(name=name,email=email,password=password,gender=gender,age=age)
        db.session.add(new_auth)
        db.session.commit()
        print("Committed")
        return redirect('/login')
    else:
        return render_template('registration.html')
    

@app.route('/Covid_19')
def Covid_19():
    return render_template("Covid_19.html",status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/Heart_Disease_Prediction')
def Heart_Disease_Prediction():
    return render_template("Heart_Disease.html",status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/diabetes',methods=['GET','POST'])
def diabetes():
    if request.method=='POST':
        # diver code for testing the model
        para=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
               'HeartDiseaseorAttack', 'PhysActivity', 'Veggies', 'HvyAlcoholConsump',
               'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Age', 'Education',
               'Income']
        tip=[para]
        res=model_diabetes.predict(np.array(tip))
        if res[0]==0:
            answer="Non-Diabetic"
        else:
            answer="Diabetic"
    return render_template('diabetes.html',status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])
@app.route('/Bone_Fracture_Detection')
def Bone_Fracture_Detection():
    return render_template("Bone_Fracture.html",status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/Skin_Cancer')
def Skin_Cancer():
    return render_template('Skin_Cancer.html',status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/Brain_Tumor_Detection')
def Brain_Tumor_Detection():
    return render_template("Brain_Tumor.html",status=app.config['LOGIN_STATUS'],username=app.config['USERNAME'])

@app.route('/getmri',methods=['POST'])
#prediction code for brain tumor detection
def getmri():
    if request.method=='POST':
        labels = ['Brain Tumor type- Glioma', 'Brain Tumor type-Meningioma', "Don't Worry, you don't have tumor", 'Brain Tumor type-Pituitary']
        img=request.files['mri']
        img.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename))
        print(file_path)
        result=preprocess_img_mri(file_path)
        return render_template('answer.html',res=labels[(np.where(result[0]==1))[0][0] ])

@app.route('/getcovidresult',methods=['POST'])
#prediction code for covid-19 module
def getcovidresult():
    if request.method=='POST':
        img=request.files['covid']
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        xtest_image = load_img(file_path, target_size=(100,100,3))
        xtest_image = img_to_array(xtest_image)
        xtest_image = np.expand_dims(xtest_image, axis = 0)
        predictions = (covid_19_model.predict(xtest_image)  ).astype("int32")
        print(predictions)
        predictions=predictions[0][0]
        if predictions==0:
            predictions="Covid 19 Negative"
        elif predictions==1:
            predictions="Covid 19 Positive"
        # return render_template('Covid_19/html',res=predictions)
        return render_template('answer.html',res=predictions)



@app.route('/getskin',methods=['POST'])
def getskin():
    if request.method=='POST':
        img=request.files['skin']
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        img = load_img(file_path,target_size=(224, 224))
        img=img_to_array(img)
        test_image = np.expand_dims(img, axis=0)
        a = np.argmax(skin_model.predict(test_image), axis=1)
        print(a[0])
        disease_list = ["Eczema 1677","Melanoma","Atopic Dermantitis","Basal Cell Carcinoma (BCC)","Mealanocytic Nevi (NV)","Benign Keratosis-like Lessions (BKL)", "Psoriasis pictures lichen Planus and related diseases","Seaborrheic Keratoses and other Benign Tumors","Tinea Ringworm Candidiasis and other fungal infections","Warts Molluscum and other Viral Infections"]
        disease=disease_list[int(a[0]+1)]
        print(disease)
    return render_template ('answer.html',res=disease)

@app.route('/getbone',methods=['POST'])
def getbone():
    if request.method=='POST':
        img=request.files['bone']
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        xtest_image = load_img(file_path, target_size=(224,224))
        xtest_image = img_to_array(xtest_image)
        xtest_image = np.expand_dims(xtest_image, axis = 0)
        predictions=bone_model.predict(xtest_image)
        predictions=np.argmax(predictions,axis=1)
        print(predictions[0])
        if predictions[0]==0:
            predictions='Bone Fractured'
        else:
            predictions='Bone Not Fractured'
        print(predictions)
    return render_template ('answer.html',res=predictions)


@app.route('/getValue',methods=['POST'])
def getValue():
    if request.method=='POST':
        oldpeak=float(request.form['oldpeak'])
        slope=int(request.form['slope'])
        ca=int(request.form['ca'])
        thal=int(request.form['thal'])
        sex=int(request.form['sex'])
        age=int(request.form['age'])
        cp=int(request.form['chaistpain'])
        restecg=int(request.form['wave'])
        thalach=int(request.form['hrate'])
        fbs=int(request.form['bloodsugar'])
        trestbps=int(request.form['bloodpressure'])
        chol=int(request.form['serum'])
        exang=int(request.form['anigna'])
        input_data=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        print(input_data)
        answer=input_data
        input_data=np.array(input_data)
        input_data=input_data.reshape(1,-1)
        print("Input_Data: ",input_data)
        answer=model.predict(input_data)
        print(answer)
        if answer:
            answer="Don't Worry You Don't Have a serious Heart Condition"
        else:
            answer="Sorry to say that you might have a serious heart Condition. Please refer to a Doctor and Get treated!"
        return render_template ('answer.html',res=answer)

if __name__=="__main__":
    app.run(debug=True)
