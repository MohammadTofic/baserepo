from flask import Flask ,render_template
import numpy as np
import cv2
from flask import request as rq
from werkzeug import secure_filename
# just serve all the static files under root
app = Flask(__name__, static_folder='.', static_url_path='')

# for / root, return Hello Word
@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('main.html')



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if rq.method == 'POST':
      f = rq.files['file']
      face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
      eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
      #f.save('input.png')
      img = cv2.imdecode(np.fromstring(f.read(), np.uint8), cv2.IMREAD_UNCHANGED)
      cv2.imwrite('input.png',img) 
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
      for (x,y,w,h) in faces:
          img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
          roi_gray = gray[y:y+h, x:x+w]
          roi_color = img[y:y+h, x:x+w]
          eyes = eye_cascade.detectMultiScale(roi_gray)
          for (ex,ey,ew,eh) in eyes:
              cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
      cv2.imwrite('output.png',img)        
      #cv2.imshow('img',img)
      #cv2.waitKey(0)
      #cv2.destroyAllWindows()

      return render_template('out.html')



















# Remember from flask import request
# for /request and POST method
@app.route('/request',methods=['POST'])
def request():
  payload=request.data
  # if accept json object as string
  data = json.loads(payload)
  # if accept normal string
  data = payload
  # After process
  
  # If still return json, Remember using jsonify(data) to return.
  # Do not need to return status, and mimetype. jsonify has
  # already helped you do that.
  return jsonify(data)
  return data, 200, {'Content-Type': 'application/json'}
  
  
  # Otherwise, just return with status and type
  # The mimetype can be text/xml, text/html.
  return data, 200, {'Content-Type': 'text/txt'}
  
  
  
  
# start listening
if __name__ == "__main__":
    app.run(debug=True, port='3110', host='0.0.0.0')
    
    