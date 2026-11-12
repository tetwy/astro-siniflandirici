# 🌌 Astronomik Nesne Sınıflandırıcı (Astro Classifier)

> **Derin uzay fotoğraflarını analiz eden, gök cisimlerini tespit edip sınıflandıran Yapay Zeka destekli Full-Stack web uygulaması.**

![Status](https://img.shields.io/badge/Status-Tamamlandı-success?style=flat-square)
![Version](https://img.shields.io/badge/Version-v2.0-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

<p align="center">
  <img src="docs/onizleme.png" alt="Astro Classifier Uygulama Arayüzü" width="100%" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);">
</p>

<!-- TODO: demo GIF -->

## 📖 Proje Hakkında

Bu proje, amatör veya profesyonel astronomi fotoğraflarını işleyerek içerisindeki nesneleri **Yıldız, Galaksi, Bulutsu, Gezegen** gibi sınıflara ayıran uçtan uca (end-to-end) bir çözümdür.

Python (Flask) tabanlı güçlü bir görüntü işleme arka ucu ve React (Vite) ile geliştirilmiş modern, uzay temalı bir ön yüze sahiptir.

### 🚀 Temel Özellikler

* **🔍 Akıllı Nesne Tespiti:** OpenCV kullanarak görüntüdeki ışık kaynaklarını arka plandan ayırır ve segmentlere böler.
* **🧠 Yapay Zeka Sınıflandırma:** Eğitilmiş **RandomForest (v2)** modeli ile nesneleri 6 farklı sınıfa ayırır.
* **🎨 Renkli Görselleştirme:** Tespit edilen nesneleri sınıflarına göre farklı renklerle (Örn: Galaksi=Mor, Yıldız=Mavi) çerçeveler.
* **📊 İstatistiksel Analiz:** Görüntüdeki dağılımı interaktif grafikler (Halka Grafik) ve detaylı listelerle sunar.
* **✨ Modern Arayüz:** Sürükle-bırak destekli, karanlık mod (dark mode) ve "glassmorphism" etkili şık tasarım.

---

## 🛠️ Teknolojiler

### Backend
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?logo=opencv&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?logo=pandas&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-Type%20Safety-3178C6?logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-06B6D4?logo=tailwindcss&logoColor=white)

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/tetwy/astro-siniflandirici.git
cd astro-siniflandirici
```

### 2\. Backend Kurulumu (Terminal 1)

Önce Python sanal ortamını oluşturun ve gerekli kütüphaneleri yükleyin.

```bash
cd backend

python -m venv venv
# Windows için aktivasyon:
venv\Scripts\activate
# Mac/Linux için aktivasyon:
# source venv/bin/activate

# Bağımlılıkları yükleyin
pip install flask flask-cors opencv-python scikit-learn pandas numpy joblib

# Yalnızca modeli yeniden eğitmek için (model_egitici.py) gerekli:
# pip install matplotlib seaborn

# API Sunucusunu başlatın
python image_service.py
```

*Backend `http://localhost:5000` adresinde çalışır (`/classify` uç noktası). Eğitilmiş v2 modelleri `backend/models` içinde hazır gelir.*

### 3\. Frontend Kurulumu (Terminal 2)

Yeni bir terminal penceresi açın ve React uygulamasını başlatın.

```bash
cd frontend

# Paketleri yükleyin
npm install

# Uygulamayı başlatın
npm run dev
```

*Frontend `http://localhost:8080` adresinde açılır (`frontend/vite.config.ts`) ve API'ye `http://127.0.0.1:5000/classify` üzerinden bağlanır.*

### 4\. Modeli Yeniden Eğitme (isteğe bağlı)

```bash
# backend/ klasöründe
python star_detector.py   # assets/ altındaki görüntülerden outputs/features/ içine özellik JSON'ları üretir
python veri_birlestir.py  # etiketli nesneleri eğitim_veriseti.csv dosyasında birleştirir
python model_egitici.py   # models/ klasörüne v2 modelini yazar
```

-----

## 📂 Proje Yapısı

```text
astro-siniflandirici/
├── backend/                 # Python API ve AI Modelleri
│   ├── assets/              # Eğitim için ham görüntüler
│   ├── models/              # Eğitilmiş .joblib modelleri (v2)
│   ├── outputs/             # star_detector.py çalışınca oluşan debug görüntüleri ve özellik JSON'ları (git'te izlenmez)
│   ├── image_service.py     # Flask API Sunucusu (Giriş Noktası)
│   ├── star_detector.py     # Görüntü İşleme Modülü
│   ├── model_egitici.py     # Model Eğitim Scripti
│   └── veri_birlestir.py    # Veri Seti Oluşturucu
│
├── frontend/                # React Web Arayüzü
│   ├── src/                 # Kaynak kodlar
│   ├── public/              # Statik dosyalar
│   └── ...                  # Config dosyaları
│
└── docs/                    # Dokümantasyon görselleri
```

## 📄 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır.

MIT Lisansı, bu yazılımın kopyasını alan herhangi bir kişiye; yazılımı kullanma, kopyalama, değiştirme, birleştirme, yayımlama, dağıtma, alt lisans verme ve/veya satma haklarını sınırsız bir şekilde verir.

Daha fazla detay için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
