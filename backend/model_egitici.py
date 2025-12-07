import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer

def train_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "eğitim_veriseti.csv")
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    
    os.makedirs(MODELS_DIR, exist_ok=True)

    MODEL_OUTPUT_FILE = os.path.join(MODELS_DIR, "astronomy_classifier_v2.joblib")
    IMPUTER_OUTPUT_FILE = os.path.join(MODELS_DIR, "data_imputer_v2.joblib")
    FEATURE_NAMES_FILE = os.path.join(MODELS_DIR, "feature_names_v2.joblib")
    CLASS_NAMES_FILE = os.path.join(MODELS_DIR, "class_names_v2.joblib")
    CONFUSION_MATRIX_FILE = os.path.join(MODELS_DIR, "confusion_matrix_v2.png")

    try:
        df = pd.read_csv(DATA_FILE, encoding='utf-8')
    except Exception as e:
        print(f"HATA: Veri seti okunamadı: {e}")
        return

    print(f"Veri yüklendi: {len(df)} satır.")

    try:
        y = df['label']
        X = df.drop(['label', 'source_file', 'source_object_id'], axis=1)
    except KeyError:
        print("HATA: Gerekli sütunlar eksik.")
        return

    feature_names = list(X.columns)
    
    X = X.replace([np.inf, -np.inf], np.nan)
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    X = pd.DataFrame(X_imputed, columns=feature_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    print("Model eğitiliyor...")
    model = RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=100)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_OUTPUT_FILE)
    joblib.dump(imputer, IMPUTER_OUTPUT_FILE)
    joblib.dump(feature_names, FEATURE_NAMES_FILE)
    joblib.dump(model.classes_, CLASS_NAMES_FILE)
    print(f"Modeller '{MODELS_DIR}' klasörüne kaydedildi.")

    print("\n--- TEST SONUÇLARI ---")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, zero_division=0))

    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title('Karışıklık Matrisi v2')
    plt.savefig(CONFUSION_MATRIX_FILE)
    print(f"Grafik kaydedildi: {CONFUSION_MATRIX_FILE}")

if __name__ == "__main__":
    train_model()