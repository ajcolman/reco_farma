import os
import joblib
import cv2
from flask import Blueprint, json, render_template
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import dlib

class CustomSVM:
    def __init__(self):
        self.model = svm.SVC(kernel='linear')
        self.le = preprocessing.LabelEncoder()

    def train(self, X, y):
        # Codificar etiquetas
        y_encoded = self.le.fit_transform(y)

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42)

        # Entrenar el modelo
        self.model.fit(X_train, y_train)

        # Evaluar el modelo
        accuracy = self.model.score(X_test, y_test)
        print(f'Accuracy: {accuracy}')

    def save_model(self, file_path):
        # Guardar el modelo y el codificador de etiquetas
        joblib.dump({'model': self.model, 'le': self.le}, file_path)

    def load_model(self, file_path):
        # Cargar el modelo y el codificador de etiquetas
        data = joblib.load(file_path)
        self.model = data['model']
        self.le = data['le']

    def predict(self, img):
        # Preprocesar la imagen
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (64, 64))
        img = img.astype(np.float32) / 255.0
        img = img.reshape(-1, 64 * 64 * 3)

        # Realizar la predicción
        prediction = self.model.predict(img)
        predicted_label = self.le.inverse_transform(prediction)[0]

        return predicted_label


class C_IA_Trainer():
    ia = Blueprint('ia', __name__)

    @ia.route('/ia_trainer')
    def ia_trainer():
        return render_template('v_ia_trainer.html', title="Entrenamiento de Modelo de IA")

    @ia.route('/train')
    def train():
        C_IA_Trainer.train_model()
        return json.dumps('Modelo entrenado correctamente')

    def train_model():
        # Obtener una lista de los directorios en el directorio `static/uploads`
        directories = os.listdir('app/static/uploads/people_photo')

        # Crear listas para almacenar las imágenes y sus etiquetas
        X = []
        y = []

        # Leer las imágenes y sus etiquetas
        for directory in directories:
            # Obtener las imágenes en el directorio
            files = os.listdir(f'app/static/uploads/people_photo/{directory}')
            # Leer las imágenes y sus etiquetas
            for file in files:
                # Obtener la imagen
                img = cv2.imread(
                    f'app/static/uploads/people_photo/{directory}/{file}')

                # Convertir la imagen a un vector y agregar a X
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (64, 64))
                img = img.astype(np.float32) / 255.0
                img = img.reshape(-1, 64 * 64 * 3)
                X.append(img)

                # Agregar la etiqueta a y
                y.append(directory)

        # Convertir las listas a arreglos numpy
        X = np.concatenate(X)
        y = np.array(y)

        # Entrenar el modelo SVM
        custom_svm = CustomSVM()
        custom_svm.train(X, y)

        # Guardar el modelo entrenado
        custom_svm.save_model('model_weights.joblib')

    @ia.route('/identify')
    def identify():
        prediction = C_IA_Trainer.identify_person()
        return str(prediction)

    def identify_person():
        # Inicializar el detector de caras de dlib
        face_detector = dlib.get_frontal_face_detector()

        # Obtener una imagen de la webcam
        cap = cv2.VideoCapture(0)
        ret, webcam_img = cap.read()

        # Cargar el modelo con joblib
        custom_svm = CustomSVM()
        custom_svm.load_model('model_weights.joblib')

        # Convertir la imagen de la webcam a escala de grises para el detector de caras
        gray_webcam_img = cv2.cvtColor(webcam_img, cv2.COLOR_BGR2GRAY)

        # Detectar caras en la imagen de la webcam
        faces = face_detector(gray_webcam_img)

        if not faces:
            return "No se detectaron caras en la webcam"

        # Tomar la primera cara detectada (puedes ajustar esto según tus necesidades)
        face = faces[0]

        # Ajustar las coordenadas de la cara para capturar un área más grande
        x, y, w, h = face.left() - 30, face.top() - 30, face.width() + \
            60, face.height() + 60

        # Asegurar que las coordenadas no sean negativas
        x, y = max(x, 0), max(y, 0)

        # Recortar la cara de la imagen de la webcam
        cropped_webcam_img = webcam_img[y:y+h, x:x+w]

        # Predecir la etiqueta de la cara recortada
        prediction = custom_svm.predict(cropped_webcam_img)

        # Verificar si la predicción es desconocida
        if prediction == "unknown":
            return "Persona desconocida"

        # Devolver la etiqueta
        return prediction