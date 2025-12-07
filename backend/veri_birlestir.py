import os
import json
import pandas as pd

def aggregate_labeled_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    FEATURES_DIR = os.path.join(BASE_DIR, "outputs", "features")
    OUTPUT_CSV_FILE = os.path.join(BASE_DIR, "eğitim_veriseti.csv")

    if not os.path.exists(FEATURES_DIR):
        print(f"HATA: '{FEATURES_DIR}' klasörü bulunamadı. Önce star_detector.py'yi çalıştırın.")
        return

    all_labeled_objects = []
    print(f"'{FEATURES_DIR}' klasörü taranıyor...")

    for filename in os.listdir(FEATURES_DIR):
        if filename.lower().endswith('.json'):
            try:
                with open(os.path.join(FEATURES_DIR, filename), 'r', encoding='utf-8') as f:
                    objects = json.load(f)
                
                for obj in objects:
                    if "label" in obj:
                        flat = {'label': obj['label']}
                        cols = ['area', 'perimeter', 'circularity', 'aspect_ratio', 
                                'solidity', 'eccentricity', 'mean_intensity_gray', 
                                'std_dev_intensity_gray', 'peak_intensity_gray', 
                                'mean_b', 'mean_g', 'mean_r']
                        for k in cols: flat[k] = obj.get(k)
                        
                        flat['source_file'] = filename
                        flat['source_object_id'] = obj.get('object_id')
                        all_labeled_objects.append(flat)

            except Exception as e:
                print(f"Hata ({filename}): {e}")

    if not all_labeled_objects:
        print("Uyarı: Hiç etiketli veri bulunamadı.")
        return

    df = pd.DataFrame(all_labeled_objects)
    df.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig')

    print(f"\nBaşarılı! Toplam {len(df)} etiketli veri '{OUTPUT_CSV_FILE}' dosyasına kaydedildi.")
    print("\nSınıf Dağılımı:")
    print(df['label'].value_counts())

if __name__ == "__main__":
    aggregate_labeled_data()