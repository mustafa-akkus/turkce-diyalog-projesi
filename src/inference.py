import os
import sys
from model import TfidfRetrievalBaseline

# Windows terminalinde emoji ve özel karakterlerin hata vermemesi için UTF-8 ayarı
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")


def ornek_sorulari_test_et(model):
    """Komut satırından hızlı test için örnek soruları çalıştırır."""
    ornek_sorular = [
        "İngilizce öğreniyorum ama konuşmaya utanıyorum ne yapmalıyım?",
        "Evde ekipmansız nasıl spor yapabilirim?",
        "Evden çalışırken odaklanmak için ne önerirsin?",
        "Güzel bir komedi filmi önerir misin?",
        "Anksiyete ve stresle nasıl başa çıkabilirim?"
    ]
    print("\n=== ÖRNEK SORU - CEVAP TESTİ (DEMO) ===")
    for soru in ornek_sorular:
        sonuc = model.cevap_bul(soru)
        print("-" * 70)
        print(f"Kullanıcı Sorusu      : {sonuc['sorgu']}")
        print(f"Eşleşen Eğitim Sorusu : {sonuc['eslesen_egitim_sorusu']}")
        print(f"Kosinüs Benzerliği    : %{sonuc['benzerlik_skoru'] * 100:.2f}")
        print(f"Modelin Yanıtı        :\n{sonuc['tahmin_cevap']}\n")


def canli_sohbet(model):
    """Kullanıcının terminalden soru sorabileceği interaktif döngü."""
    print("\n" + "=" * 65)
    print("  TÜRKÇE DİYALOG AJANI (TF-IDF + KOSİNÜS BENZERLİĞİ BASELINE)")
    print("  Çıkmak için 'q' veya 'çıkış' yazabilirsiniz.")
    print("=" * 65)

    while True:
        try:
            soru = input("\nSiz: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSohbet sonlandırıldı.")
            break

        if not soru:
            continue
        if soru.lower() in ["q", "quit", "exit", "çıkış", "cikis"]:
            print("Sohbet sonlandırıldı. İyi çalışmalar!")
            break

        sonuc = model.cevap_bul(soru)
        print(f"\n[Eşleşen Soru: '{sonuc['eslesen_egitim_sorusu']}' | Benzerlik: %{sonuc['benzerlik_skoru']*100:.1f}]")
        print(f"Bot: {sonuc['tahmin_cevap']}")


if __name__ == "__main__":
    proje_dizini = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_yolu = os.path.join(proje_dizini, "models", "tfidf_baseline.pkl")

    if not os.path.exists(model_yolu):
        print("Eğitilmiş model bulunamadı! Lütfen önce 'python src/train.py' komutunu çalıştırın.")
        sys.exit(1)

    baseline_model = TfidfRetrievalBaseline.yukle(model_yolu)

    if "--demo" in sys.argv:
        ornek_sorulari_test_et(baseline_model)
    else:
        canli_sohbet(baseline_model)
