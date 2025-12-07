import requests
import json
import base64
import os

# test etmek istediginiz goruntunun yolunu buraya yazin
IMAGE_TO_TEST = r"deneme.jpeg" # ornek yol

API_URL = "http://127.0.0.1:5000/classify"
DEBUG_IMAGE_OUTPUT = "api_response_debug.jpg"

print(f"'{API_URL}' adresine test isteği gönderiliyor...")
print(f"Test görüntüsü: {IMAGE_TO_TEST}")

try:
    with open(IMAGE_TO_TEST, 'rb') as f:
        files = {'image': (os.path.basename(IMAGE_TO_TEST), f, 'image/jpeg')}
        
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            print("\nBaşarılı! (HTTP 200). Sunucudan yanıt alındı.")
            
            data = response.json()
            
            print("\n--- SINIFLANDIRMA ÖZETİ ---")
            print(f"Toplam {data['object_count']} nesne bulundu.")
            print("Sınıf Dağılımı:")
            print(json.dumps(data['class_counts'], indent=2, ensure_ascii=False))
            
            if 'debug_image_base64' in data:
                img_data = base64.b64decode(data['debug_image_base64'])
                with open(DEBUG_IMAGE_OUTPUT, 'wb') as f_out:
                    f_out.write(img_data)
                print(f"\nDebug görüntüsü '{DEBUG_IMAGE_OUTPUT}' olarak kaydedildi.")
                
        else:
            print(f"\nHATA: Sunucu {response.status_code} koduyla yanıt verdi.")
            print("Sunucu Hatası:", response.text)

except requests.exceptions.ConnectionError:
    print("\nBAĞLANTI HATASI: Sunucuya bağlanılamadı.")
    print(f"Lütfen 'image_service.py' script'inin başka bir terminalde çalıştığından emin olun.")
except FileNotFoundError:
    print(f"\nHATA: Test görüntüsü '{IMAGE_TO_TEST}' bulunamadı.")
    print("Lütfen 'IMAGE_TO_TEST' değişkenini geçerli bir görüntü yolu ile güncelleyin.")
except Exception as e:
    print(f"\nBeklenmeyen bir hata oluştu: {e}")