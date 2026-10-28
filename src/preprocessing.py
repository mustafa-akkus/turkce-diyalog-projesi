import os
import re
import sys
import json
import random
from collections import Counter

# Windows terminalinde Türkçe karakterlerin düzgün görünmesi için UTF-8 ayarı
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Tekrarlanabilirlik (Reproducibility) için sabit tohum değeri
RANDOM_SEED = 42


def turkce_kucuk_harf(metin):
    """
    Neden kullanıyoruz?
    Python'daki standart .lower() fonksiyonu Türkçe 'I' harfini 'i'ye veya
    'İ' harfini bozuk bir karaktere dönüştürebilir. Türkçe morfolojisini
    bozmamak için önce I -> ı ve İ -> i dönüşümü yapıyoruz.
    """
    if not isinstance(metin, str):
        return ""
    metin = metin.replace("İ", "i").replace("I", "ı")
    return metin.lower()


def metin_temizle(metin):
    """
    Neden kullanıyoruz?
    1. Türkçe uyumlu küçük harfe çevirerek 'Kitap' ve 'kitap' kelimelerinin
       farklı kelimeler gibi algılanmasını önleriz.
    2. Noktalama işaretlerini, markdown sembollerini (*, # vb.) ve gereksiz
       boşlukları temizleyerek TF-IDF matrisinin gürültüden arınmasını sağlarız.
    """
    metin = turkce_kucuk_harf(metin)
    # Sadece harfleri (Türkçe karakterler dahil), rakamları ve boşlukları tut
    metin = re.sub(r"[^a-z0-9çğıöşü\s]", " ", metin)
    # Fazla boşlukları ve satır sonlarını tek boşluğa indir
    metin = re.sub(r"\s+", " ", metin).strip()
    return metin


def veri_yukle_ve_bol(kaynak_json_yolu, cikti_klasoru, seed=RANDOM_SEED):
    """
    Veri setini yükler, tekrar eden (duplicate) soruları temizleyerek veri
    sızıntısını (data leakage) önler ve %80 Eğitim, %10 Doğrulama, %10 Test
    olarak böler.
    """
    print(f"[1/3] Veri seti okunuyor: {kaynak_json_yolu}")
    with open(kaynak_json_yolu, "r", encoding="utf-8") as f:
        ham_veri = json.load(f)

    print(f"      Toplam ham örnek sayısı: {len(ham_veri)}")

    # Tekrar eden soruları temizleme (Veri sızıntısını önlemek için)
    gorulen_sorular = set()
    temiz_veri = []

    for kayit in ham_veri:
        soru = kayit.get("input", "").strip()
        cevap = kayit.get("output", "").strip()

        if not soru or not cevap:
            continue

        temiz_soru = metin_temizle(soru)
        if not temiz_soru:
            continue

        # Eğer aynı soru daha önce eklendiyse atla (Data Leakage önlemi)
        if temiz_soru in gorulen_sorular:
            continue

        gorulen_sorular.add(temiz_soru)
        temiz_veri.append({
            "input": soru,
            "output": cevap,
            "clean_input": temiz_soru,
            "clean_output": metin_temizle(cevap)
        })

    print(f"      Tekrar eden sorular temizlendikten sonra kalan örnek: {len(temiz_veri)}")

    # Sabit random seed ile karıştırma
    random.seed(seed)
    random.shuffle(temiz_veri)

    # %80 Eğitim (Train), %10 Doğrulama (Validation), %10 Test bölünmesi
    toplam = len(temiz_veri)
    train_bitis = int(toplam * 0.80)
    val_bitis = int(toplam * 0.90)

    train_veri = temiz_veri[:train_bitis]
    val_veri = temiz_veri[train_bitis:val_bitis]
    test_veri = temiz_veri[val_bitis:]

    print(f"[2/3] Veri bölündü -> Eğitim: {len(train_veri)}, Doğrulama: {len(val_veri)}, Test: {len(test_veri)}")

    os.makedirs(cikti_klasoru, exist_ok=True)
    for dosya_adi, veri in [("train.json", train_veri), ("val.json", val_veri), ("test.json", test_veri)]:
        dosya_yolu = os.path.join(cikti_klasoru, dosya_adi)
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)

    print(f"      Bölünmüş veri setleri '{cikti_klasoru}' klasörüne kaydedildi.")
    return train_veri, val_veri, test_veri


def eda_yap(veri_listesi, sonuc_klasoru):
    """
    Keşifsel Veri Analizi (EDA):
    Cümle uzunluk dağılımlarını, kelime haznesi (vocabulary) boyutunu hesaplar
    ve histogram grafiklerini oluşturup results/ klasörüne kaydeder.
    """
    print("[3/3] Keşifsel Veri Analizi (EDA) yapılıyor...")
    os.makedirs(sonuc_klasoru, exist_ok=True)

    soru_kelime_sayilari = []
    cevap_kelime_sayilari = []
    soru_kelime_sayaci = Counter()
    tum_kelimeler = set()

    for kayit in veri_listesi:
        soru_kelimeler = kayit["clean_input"].split()
        cevap_kelimeler = kayit["clean_output"].split()

        soru_kelime_sayilari.append(len(soru_kelimeler))
        cevap_kelime_sayilari.append(len(cevap_kelimeler))

        soru_kelime_sayaci.update(soru_kelimeler)
        tum_kelimeler.update(soru_kelimeler)
        tum_kelimeler.update(cevap_kelimeler)

    ort_soru_uzunlugu = sum(soru_kelime_sayilari) / len(soru_kelime_sayilari)
    ort_cevap_uzunlugu = sum(cevap_kelime_sayilari) / len(cevap_kelime_sayilari)

    ozet_metin = (
        "=== KEŞİFSEL VERİ ANALİZİ (EDA) ÖZETİ ===\n"
        f"Toplam Benzersiz Örnek Sayısı : {len(veri_listesi)}\n"
        f"Toplam Kelime Haznesi (Vocab) : {len(tum_kelimeler)} benzersiz kelime\n"
        f"Ortalama Soru Uzunluğu        : {ort_soru_uzunlugu:.2f} kelime (Min: {min(soru_kelime_sayilari)}, Maks: {max(soru_kelime_sayilari)})\n"
        f"Ortalama Cevap Uzunluğu       : {ort_cevap_uzunlugu:.2f} kelime (Min: {min(cevap_kelime_sayilari)}, Maks: {max(cevap_kelime_sayilari)})\n\n"
        "Sorularda En Sık Geçen 15 Kelime:\n"
    )
    for kelime, frekans in soru_kelime_sayaci.most_common(15):
        ozet_metin += f"  - {kelime}: {frekans}\n"

    ozet_yolu = os.path.join(sonuc_klasoru, "eda_ozet_istatistikler.txt")
    with open(ozet_yolu, "w", encoding="utf-8") as f:
        f.write(ozet_metin)

    # Matplotlib ile grafik çizimi
    try:
        import matplotlib.pyplot as plt

        # Aşırı uç değerlerin (outlier) grafiği sıkıştırmaması için %99'luk aralığı çizelim
        soru_grafik_veri = [x for x in soru_kelime_sayilari if x <= 35]
        cevap_grafik_veri = [x for x in cevap_kelime_sayilari if x <= 250]

        # Grafik 1: Soru ve Cevap Kelime Sayısı Dağılımı (Histogram)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        axes[0].hist(soru_grafik_veri, bins=25, color="#3b82f6", edgecolor="black", alpha=0.8)
        axes[0].set_title("Soru (Input) Kelime Sayısı Dağılımı (0-35 Kelime)")
        axes[0].set_xlabel("Kelime Sayısı")
        axes[0].set_ylabel("Örnek Sayısı (Frekans)")

        axes[1].hist(cevap_grafik_veri, bins=30, color="#10b981", edgecolor="black", alpha=0.8)
        axes[1].set_title("Cevap (Output) Kelime Sayısı Dağılımı (0-250 Kelime)")
        axes[1].set_xlabel("Kelime Sayısı")
        axes[1].set_ylabel("Örnek Sayısı (Frekans)")

        plt.tight_layout()
        grafik1_yolu = os.path.join(sonuc_klasoru, "eda_uzunluk_dagilimi.png")
        plt.savefig(grafik1_yolu, dpi=150)
        plt.close()

        # Grafik 2: En Sık Geçen 15 Kelime
        en_sik = soru_kelime_sayaci.most_common(15)
        kelimeler = [k for k, _ in en_sik][::-1]
        sayilar = [s for _, s in en_sik][::-1]

        plt.figure(figsize=(8, 5))
        plt.barh(kelimeler, sayilar, color="#f59e0b", edgecolor="black", alpha=0.85)
        plt.title("Sorularda En Sık Geçen 15 Kelime")
        plt.xlabel("Frekans")
        plt.tight_layout()
        grafik2_yolu = os.path.join(sonuc_klasoru, "eda_en_sik_kelimeler.png")
        plt.savefig(grafik2_yolu, dpi=150)
        plt.close()

        print(f"      EDA istatistikleri ve grafikleri '{sonuc_klasoru}' klasörüne kaydedildi.")
    except ImportError:
        print("      [Uyarı] matplotlib yüklü olmadığı için sadece metin özeti kaydedildi.")


if __name__ == "__main__":
    # Proje ana dizinini bul
    proje_dizini = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Önce data/data.json var mı bak, yoksa masaüstündeki data.json'u kullan
    yerel_veri = os.path.join(proje_dizini, "data", "data.json")
    masaustu_veri = os.path.join(os.path.dirname(proje_dizini), "data.json")

    kaynak_yol = yerel_veri if os.path.exists(yerel_veri) else masaustu_veri
    veri_klasoru = os.path.join(proje_dizini, "data")
    sonuc_klasoru = os.path.join(proje_dizini, "results")

    train_v, val_v, test_v = veri_yukle_ve_bol(kaynak_yol, veri_klasoru)
    eda_yap(train_v + val_v + test_v, sonuc_klasoru)
