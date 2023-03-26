from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle
import os
import cv2
from keras.utils import load_img,img_to_array
from keras.models import load_model
from keras.preprocessing import image
import warnings
warnings.filterwarnings('ignore')

# with open(r"Python\Health-Care\Trained_Models\model_HD.h5",'rb') as fe_data_file:
#     model = pickle.load(fe_data_file)
#Trained_Models\modelHD.h5
model= load_model(r"Trained_Models\modelHD.h5")
#C:\Users\asus\OneDrive\Ked data\VS Code\Python\Health-Care\Trained_Models\modelHD.h5
model_diabetes=load_model(r'Trained_Models\modelDibt.h5')
from gevent.pywsgi import WSGIServer 
from werkzeug.utils import secure_filename
mri_model=load_model(r'Trained_Models\BrainTumor.h5')
app=Flask(__name__)
covid_19_model=load_model(r"Trained_Models\covid_model.h5")
# bone_model=load_model(r"Trained_Models\bone_fracture.h5")
skin_model=load_model(r"Trained_Models\skin_d.h5")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///heart.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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
#         return "Sorry to say that you might have a serious heart Condition. Please refer to a Doctor and Get treated!"



#preprocessing for brain Tumor module
def preprocess_img_mri(img_path):
    xtest_image = load_img(img_path, target_size=(150,150,3))
    xtest_image = img_to_array(xtest_image)
    xtest_image = np.expand_dims(xtest_image, axis = 0)
    predictions = (mri_model.predict( xtest_image)> 0.5).astype("int32")
    return predictions
    


@app.route('/')
def refresh():
    print(app.root_path)
    return render_template("homepage.html")

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
        return render_template('Covid_19/html',res=predictions)



@app.route('/getskin',methods=['POST'])
def getskin():
    if request.method=='POST':
        img=request.files['skin']
        print(str(img))
        test_image = load_img(os.path.join(app.config['UPLOAD_FOLDER'],img),target_size=(224, 224))
        file_path=(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(img.filename)))
        img.save(file_path)
        # print(str(file_path))
        # test_image = np.asarray(file_path)
        # print(type(img))
        # cv2.imshow(img)

        # model = load_model("skin_d.h5")
        # img = load_img(img,target_size=(224, 224))
        
        test_image=test_image.resize((224,224))
        test_image = np.expand_dims(test_image, axis=0)
        a = np.argmax(model.predict(test_image), axis=1)
        print(a)

        
        # preprocessed_img=preprocess_img_skin(img)
        # result=skin_model.predict(preprocessed_img)
    # return render_template('Skin _Cancer.html',res=result)

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
        pass
        oldpeak=1.055555556
        slope=0.602693603
        ca=0.676767677
        thal=0.835016835
        sex=0
        age=request.form['age']
        cp=request.form['chaistpain']
        restecg=request.form['wave']
        thalach=request.form['hrate']
        fbs=request.form['bloodsugar']
        trestbps=request.form['bloodpressure']
        chol=request.form['serum']
        exang=request.form['anigna']
        # print(age)
        # print(restecg)
        # print(fbs)
        # print(chol)
        # print(trestbps)
        # print(exang)
        # print(thalach)
        input_data=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        input_data=tuple(input_data)
        input_data=np.asarray(input_data)
        input_data=input_data.reshape(1,-1)
        pred=model.predict(input_data)
        print(pred)
        # answer=predict_heart_condition(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
        # print(answer)
        # return render_template ('Heart_Disease.html',ans=answer)

if __name__=="__main__":
    app.run(debug=True)
