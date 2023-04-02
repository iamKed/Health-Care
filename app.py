from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
import os
import cv2
from keras.utils import load_img,img_to_array
from keras.models import load_model
from keras.preprocessing import image
import warnings
from sklearn.preprocessing import StandardScaler as std_scaler
warnings.filterwarnings('ignore')
model= load_model(r"Trained_Models\modelHD.h5")
model_diabetes=load_model(r'Trained_Models\modelDibt.h5')
from gevent.pywsgi import WSGIServer 
from werkzeug.utils import secure_filename
mri_model=load_model(r'Trained_Models\BrainTumor.h5')
app=Flask(__name__)
app.secret_key = b'82736781_@*@&(796*5&^5)'
covid_19_model=load_model(r"Trained_Models\covid_model.h5")
# bone_model=load_model(r"Trained_Models\bone_fracture.h5")
skin_model=load_model(r"Trained_Models\skin_d.h5")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
LOGIN_STATUS=False
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



#preprocessing and prediction code for heart_disease_prediction module
# def predict_heart_condition(age1,sex1,cp1,trestbps1,chol1,fbs1,restecg1,thalach1,exang1,oldpeak1,slope1,ca1,thal1):
#     age=age1
#     sex=sex1
#     cp_list=['Typical Angina','Atypical Angina','Non-Anginal pain','Asymptomatic']
#     restecg_list=['Normal','Having ST-T wave abnormality','Showing probable or definite left ventricular hypertrophy']
#     cp=cp_list.index(cp1)
#     restecg=restecg_list.index(restecg1)
#     thalach=thalach1
#     fbs_list=['Fasting blood sugar < 120','Fasting blood sugar > 120']
#     fbs=fbs_list.index(fbs1)
#     trestbps=trestbps1
#     chol=chol1
#     exang_list=['No','Yes']
#     exang=exang_list.index(exang1)
#     input_data=[int(age),int(sex),int(cp),int(trestbps),int(chol),int(fbs),int(restecg),int(thalach),int(exang),int(oldpeak1),slope1,int(ca1),int(thal1)]
#     print(i for i in input_data)
#     input_data=tuple(input_data)
#     input_data=np.asarray(input_data)
#     input_data=input_data.reshape(1,-1)
#     print(input_data)
#     Prediction=model.predict(input_data)
#     if Prediction==[0]:
#         return "Don't Worry You Don't Have a serious Heart Condition"
#     else:
#         return ""



#preprocessing for brain Tumor module
def preprocess_img_mri(img_path):
    xtest_image = load_img(img_path, target_size=(150,150,3))
    xtest_image = img_to_array(xtest_image)
    xtest_image = np.expand_dims(xtest_image, axis = 0)
    predictions = (mri_model.predict( xtest_image)> 0.5).astype("int32")
    return predictions
    

@app.route('/login')
def login():
    email=request.form['email']
    password=request.form['password']
    # if condition check:
    return render_template('homepage.html',access=True)

@app.route('/')
def refresh():
    print(app.root_path)
    return render_template("homepage.html")

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/Covid_19')
def Covid_19():
    return render_template("Covid_19.html")

@app.route('/Heart_Disease_Prediction')
def Heart_Disease_Prediction():
    return render_template("Heart_Disease.html")

@app.route('/Bone_Fracture_Detection')
def Bone_Fracture_Detection():
    return render_template("Bone_Fracture.html")

@app.route('/Skin_Cancer')
def Skin_Cancer():
    return render_template('Skin_Cancer.html')

@app.route('/Brain_Tumor_Detection')
def Brain_Tumor_Detection():
    return render_template("Brain_Tumor.html")

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
        return render_template('Brain_Tumor.html',res=labels [(np.where(result[0]==1))[0][0] ])

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
        session['predictions'] = predictions
        # return render_template('Covid_19/html',res=predictions)
        return render_template('answer.html',res=predictions)



@app.route('/getskin',methods=['POST'])
def getskin():
    if request.method=='POST':
        img=request.files['skin']
        # print(str(img))
        # test_image = load_img(os.path.join(app.config['UPLOAD_FOLDER'],img),target_size=(224, 224))
        
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        # test_image=cv2.imread(file_path)
        # test_image.resize((224,224))
        # print(str(file_path))
        # test_image = np.asarray(test_image)
        # test_image=img_to_array(test_image)
        # print(type(img))
        # cv2.imshow(img)
        # model = load_model("skin_d.h5")
        img = load_img(file_path,target_size=(224, 224))
        img=img_to_array(img)
        
        # test_image=test_image.resize((224,224))
        test_image = np.expand_dims(img, axis=0)
        a = np.argmax(skin_model.predict(test_image), axis=1)
        print(a[0])
        disease_list = ["Eczema 1677","Melanoma","Atopic Dermantitis","Basal Cell Carcinoma (BCC)","Mealanocytic Nevi (NV)","Benign Keratosis-like Lessions (BKL)", "Psoriasis pictures lichen Planus and related diseases","Seaborrheic Keratoses and other Benign Tumors","Tinea Ringworm Candidiasis and other fungal infections","Warts Molluscum and other Viral Infections"]
        disease=disease_list[int(a[0]+1)]
        print(disease)
        # preprocessed_img=preprocess_img_skin(img)
        # result=skin_model.predict(preprocessed_img)
    return render_template('Skin_Cancer.html',res=disease)

@app.route('/getbone',methods=['POST'])
def getbone():
    if request.method=='POST':
        labels=['Bone Not Fractured','Bone Fractured']
        img=request.files['bone']
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        xtest_image = load_img(file_path, target_size=(224,224,3))
        xtest_image = img_to_array(xtest_image)
        xtest_image = np.expand_dims(xtest_image, axis = 0)
        # predictions = (bone_model.predict( xtest_image) > 0.5).astype("int32")
        print(labels [(np.where(predictions[0]==1))[0][0] ])
        print(predictions)
        if predictions[0][0]==1:
            predictions='Bone Not Fractured'
        elif predictions[0][1]==1:
            predictions='Bone Fractured'
        print(predictions)
        # result=bone_model.predict(preprocessed_img)
    return render_template('Bone_Fracture.html',res=predictions)


@app.route('/getValue',methods=['POST'])
def getValue():
    if request.method=='POST':
        oldpeak=float(request.form['oldpeak'])
        slope=float(request.form['slope'])
        ca=float(request.form['ca'])
        thal=float(request.form['thal'])
        sex=float(request.form['sex'])
        age=float(request.form['age'])
        cp=float(request.form['chaistpain'])
        restecg=float(request.form['wave'])
        thalach=float(request.form['hrate'])
        fbs=float(request.form['bloodsugar'])
        trestbps=float(request.form['bloodpressure'])
        chol=float(request.form['serum'])
        exang=float(request.form['anigna'])
        input_data=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        print(input_data)
        # input_data=tuple(input_data)
        # input_data=np.asarray(input_data[:])
        # input_data=input_data.reshape(1,-1)
        # input_data=std_scaler.transform(input_data)
        # pred=model.predict(input_data)
        # print(pred)
        # answer=pred[0][0]>0.75
        # # print(answer)
        # if answer:
        #     print("Don't Worry You Don't Have a serious Heart Condition")
        # else:
        #     print("Sorry to say that you might have a serious heart Condition. Please refer to a Doctor and Get treated!")
        # return render_template ('Heart_Disease.html',ans=answer)

if __name__=="__main__":
    app.run(debug=True)