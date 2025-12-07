import flask
from flask import request, jsonify
from flask_cors import CORS
import joblib
import cv2
import numpy as np
import pandas as pd
import base64
import collections
import os

try:
    from star_detector import preprocess_image, detect_and_extract_features
except ImportError:
    print("HATA: star_detector.py dosyası bulunamadı.")
    exit()

app = flask.Flask(__name__)
CORS(app)

CLASS_COLORS = {
    'Yıldız': (235, 150, 50), 
    'Bulutsu': (80, 160, 255),
    'Galaksi': (255, 100, 255),
    'Kuyruklu Yıldız': (100, 255, 100),
    'Gezegen': (255, 255, 100),
    'Gürültü': (100, 100, 255)
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

print(f"API sunucusu başlıyor... Modeller '{MODELS_DIR}' klasöründen yükleniyor...")

try:
    MODEL = joblib.load(os.path.join(MODELS_DIR, 'astronomy_classifier_v2.joblib'))
    IMPUTER = joblib.load(os.path.join(MODELS_DIR, 'data_imputer_v2.joblib'))
    FEATURE_NAMES = joblib.load(os.path.join(MODELS_DIR, 'feature_names_v2.joblib'))
    CLASS_NAMES = joblib.load(os.path.join(MODELS_DIR, 'class_names_v2.joblib'))
    print("v2 Modelleri başarıyla yüklendi.")
except FileNotFoundError as e:
    print(f"HATA: Model dosyası bulunamadı: {e}")
    print("Lütfen 'models' klasöründe v2 dosyalarının olduğundan emin olun.")
    exit()

@app.route("/classify", methods=["POST"])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Görüntü dosyası bulunamadı'}), 400

    file = request.files['image']
    
    try:
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        img_color = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img_color is None: raise ValueError("Görüntü okunamadı.")
    except Exception as e:
        return jsonify({'error': f'Hata: {e}'}), 400

    print(f"\nİşleniyor: {file.filename}")

    img_processed, img_gray, img_color_original = preprocess_image(img_color)
    
    features_list, _, contours = detect_and_extract_features(
        img_processed, img_gray, img_color_original
    )

    if not features_list:
        return jsonify({
            'message': 'Nesne bulunamadı.',
            'object_count': 0,
            'predictions': [],
            'class_counts': {}
        })

    df_predict = pd.DataFrame(features_list)
    X_predict = df_predict.reindex(columns=FEATURE_NAMES).fillna(0)
    X_imputed = IMPUTER.transform(X_predict)
    predictions = MODEL.predict(X_imputed)
    
    try:
        probabilities = MODEL.predict_proba(X_imputed)
    except:
        probabilities = None

    img_result = img_color_original.copy()
    results = []
    class_counts = collections.Counter()

    for i, (features, label, cnt) in enumerate(zip(features_list, predictions, contours)):
        class_counts[label] += 1
        color = CLASS_COLORS.get(label, (255, 255, 255))
        cv2.drawContours(img_result, [cnt], -1, color, 2)
        
        obj_result = {
            'object_id': features['object_id'],
            'predicted_class': label,
            'center': features.get('center', 'N/A')
        }
        if probabilities is not None:
            class_index = np.where(CLASS_NAMES == label)[0][0]
            obj_result['confidence'] = round(float(probabilities[i][class_index]), 4)
        
        results.append(obj_result)

    print(f"Tamamlandı. Dağılım: {dict(class_counts)}")

    _, buffer = cv2.imencode('.jpg', img_result)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'message': 'Sınıflandırma başarılı',
        'object_count': len(results),
        'class_counts': dict(class_counts),
        'predictions': results,
        'debug_image_base64': img_base64
    })

if __name__ == "__main__":
    print("Flask sunucusu http://127.0.0.1:5000 adresinde başlatılıyor...")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)