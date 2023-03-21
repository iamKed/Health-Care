
        # print(prediction)
        # return render_template('Covid_19.html',res=prediction)

@app.route('/Heart_Disease_Prediction')
def Heart_Disease_Prediction():
    return render_template("Heart_Disease.html")

@app.route('/Bone_Fracture_Detection')
def Bone_Fracture_Detection():
    return render_template("Bone_Fracture.html")
