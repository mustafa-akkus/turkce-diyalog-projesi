import os
import sys
import json
from preprocessing import veri_yukle_ve_bol, eda_yap
from model import TfidfRetrievalBaseline

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def modeli_egit():
    proje_dizini = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    veri_klasoru = os.path.join(proje_dizini, "data")
    model_klasoru = os.path.join(proje_dizini, "models")
    sonuc_klasoru = os.path.join(proje_dizini, "results")

    train_yolu = os.path.join(veri_klasoru, "train.json")

    # Eğer bölünmüş eğitim verisi henüz oluşturulmadıysa önce ön işleme adımını çalıştır
    if not os.path.exists(train_yolu):
        print("Bölünmüş veri seti bulunamadı, önce ön işleme (preprocessing) başlatılıyor...")
        yerel_veri = os.path.join(veri_klasoru, "data.json")
        masaustu_veri = os.path.join(os.path.dirname(proje_dizini), "data.json")
        kaynak_yol = yerel_veri if os.path.exists(yerel_veri) else masaustu_veri

        train_veri, val_veri, test_veri = veri_yukle_ve_bol(kaynak_yol, veri_klasoru)
        eda_yap(train_veri + val_veri + test_veri, sonuc_klasoru)
    else:
        print(f"Eğitim verisi yükleniyor: {train_yolu}")
        with open(train_yolu, "r", encoding="utf-8") as f:
            train_veri = json.load(f)

    print("TF-IDF + Kosinüs Benzerliği Baseline Modeli kuruluyor...")
    baseline_model = TfidfRetrievalBaseline(ngram_range=(1, 2), max_features=25000)
    baseline_model.fit(train_veri)

    os.makedirs(model_klasoru, exist_ok=True)
    kayit_yolu = os.path.join(model_klasoru, "tfidf_baseline.pkl")
    baseline_model.kaydet(kayit_yolu)
    print(f"Model başarıyla eğitildi ve kaydedildi: {kayit_yolu}")


if __name__ == "__main__":
    modeli_egit()
