#Importing the Libraries
import pandas as pd
import numpy as np
from flask import Flask, request,render_template
from flask_cors import CORS
import os
from sklearn.externals import joblib
from keras.models import load_model
import pickle
import flask
from imageio import imread
from PIL import Image
from keras.preprocessing import image
from fatsecret import Fatsecret
fs = Fatsecret('d82e5cd4d5674be99e298020286a1bd5', '823bef07377d4560ba7c3fa4a5c0b521')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import base64
from io import BytesIO

categories = pd.read_csv('category.csv',index_col=['Unnamed: 0'])
#Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app=flask.Flask(__name__,template_folder='templates')

model = joblib.load('model.pkl')

@app.route('/')
def main():
    return render_template('main.html')

#Receiving the input image from user and predicting using the model
@app.route('/predict',methods=['GET','POST'])
def predict():
    img = request.files["Image"]
    img = Image.open(img)
    buffered = BytesIO()
    img.save(buffered, format='JPEG')
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode("utf-8")
    img = img.resize((128,128))
    img = np.array(img)
    img = img.flatten()
    img = img.reshape(1,-1)
    index = model.predict(img/255)
    cat = categories.loc[index[0],'1']
    foods = fs.foods_search(categories.iloc[index[0],0])
    nutrition = foods[0]['food_description']
    return render_template('main.html', prediction_text='Predicted Category: {} \n Nutrition Values: {}'.format(cat, nutrition),user_image=img_str)
    
if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)