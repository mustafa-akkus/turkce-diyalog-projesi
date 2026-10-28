import os
import sys
import json
import math
from collections import Counter
from model import TfidfRetrievalBaseline

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def ngram_olustur(kelimeler, n):
    """Kelime listesinden n-gram'ları üretir."""
    return [tuple(kelimeler[i:i + n]) for i in range(len(kelimeler) - n + 1)]


def bleu_hesapla(referans_kelimeler, tahmin_kelimeler, max_n=4):
    """
    Standart BLEU-N (BLEU-1, BLEU-2, BLEU-4) hesaplaması.
    Kısalık cezası (Brevity Penalty) ve sıfır bölünmesini önleyen yumuşatma (smoothing) içerir.
    """
    if not tahmin_kelimeler or not referans_kelimeler:
        return 0.0

    # Kısalık Cezası (Brevity Penalty)
    ref_uzunluk = len(referans_kelimeler)
    tahmin_uzunluk = len(tahmin_kelimeler)
    if tahmin_uzunluk > ref_uzunluk:
        bp = 1.0
    else:
        bp = math.exp(1.0 - (ref_uzunluk / max(tahmin_uzunluk, 1)))

    log_toplam = 0.0
    for n in range(1, max_n + 1):
        tahmin_ngrams = ngram_olustur(tahmin_kelimeler, n)
        ref_ngrams = ngram_olustur(referans_kelimeler, n)

        if not tahmin_ngrams:
            return 0.0

        tahmin_sayac = Counter(tahmin_ngrams)
        ref_sayac = Counter(ref_ngrams)

        # Kırpılmış (Clipped) eşleşme sayısı
        eslesme = sum(min(sayi, ref_sayac[gram]) for gram, sayi in tahmin_sayac.items())

        # Smoothing (n > 1 için 0 çıkmasını önlemek adına küçük +0.1 ekleme)
        if n == 1:
            kesinlik = eslesme / len(tahmin_ngrams)
        else:
            kesinlik = (eslesme + 0.1) / (len(tahmin_ngrams) + 0.1)

        if kesinlik <= 0:
            return 0.0
        log_toplam += math.log(kesinlik) / max_n

    return bp * math.exp(log_toplam)


def rouge_n_hesapla(referans_kelimeler, tahmin_kelimeler, n=1):
    """
    ROUGE-N (ROUGE-1 ve ROUGE-2) F1 ve Recall (Hatırlama) skoru hesaplaması.
    """
    if not referans_kelimeler or not tahmin_kelimeler:
        return 0.0

    ref_ngrams = ngram_olustur(referans_kelimeler, n)
    tahmin_ngrams = ngram_olustur(tahmin_kelimeler, n)

    if not ref_ngrams or not tahmin_ngrams:
        return 0.0

    ref_sayac = Counter(ref_ngrams)
    tahmin_sayac = Counter(tahmin_ngrams)

    ortak = sum(min(sayi, tahmin_sayac[gram]) for gram, sayi in ref_sayac.items())

    recall = ortak / len(ref_ngrams)
    precision = ortak / len(tahmin_ngrams)

    if recall + precision == 0:
        return 0.0
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def en_uzun_ortak_altdizi_uzunlugu(x, y):
    """
    ROUGE-L için iki kelime dizisi arasındaki En Uzun Ortak Alt-Dizi (LCS) uzunluğunu bulur.
    Performans için ilk 75 kelime üzerinden hesaplanır.
    """
    x = x[:75]
    y = y[:75]
    m, n = len(x), len(y)
    onceki = [0] * (n + 1)

    for i in range(1, m + 1):
        simdiki = [0] * (n + 1)
        xi = x[i - 1]
        for j in range(1, n + 1):
            if xi == y[j - 1]:
                simdiki[j] = onceki[j - 1] + 1
            else:
                simdiki[j] = onceki[j] if onceki[j] >= simdiki[j - 1] else simdiki[j - 1]
        onceki = simdiki

    return onceki[n]


def rouge_l_hesapla(referans_kelimeler, tahmin_kelimeler):
    """ROUGE-L (LCS tabanlı F1 skoru) hesaplar."""
    if not referans_kelimeler or not tahmin_kelimeler:
        return 0.0

    lcs = en_uzun_ortak_altdizi_uzunlugu(referans_kelimeler, tahmin_kelimeler)
    recall = lcs / min(len(referans_kelimeler), 75)
    precision = lcs / min(len(tahmin_kelimeler), 75)

    if recall + precision == 0:
        return 0.0
    return (2 * precision * recall) / (precision + recall)


def veri_setini_degerlendir(model, veri_listesi, veri_adi="Test"):
    """Verilen veri seti üzerinde BLEU ve ROUGE metriklerini hesaplar."""
    print(f"{veri_adi} seti ({len(veri_listesi)} örnek) üzerinde tahmin yapılıyor...")
    temiz_sorular = [k["clean_input"] for k in veri_listesi]
    indeksler, benzerlik_skorlari = model.toplu_tahmin(temiz_sorular)

    bleu1_list, bleu2_list, bleu4_list = [], [], []
    rouge1_list, rouge2_list, rougel_list = [], [], []
    detayli_sonuclar = []

    for i, kayit in enumerate(veri_listesi):
        en_iyi_idx = indeksler[i]
        benzerlik = benzerlik_skorlari[i]

        ref_kelimeler = kayit["clean_output"].split()
        tahmin_kelimeler = model.egitim_temiz_cevaplari[en_iyi_idx].split()

        b1 = bleu_hesapla(ref_kelimeler, tahmin_kelimeler, max_n=1)
        b2 = bleu_hesapla(ref_kelimeler, tahmin_kelimeler, max_n=2)
        b4 = bleu_hesapla(ref_kelimeler, tahmin_kelimeler, max_n=4)

        r1 = rouge_n_hesapla(ref_kelimeler, tahmin_kelimeler, n=1)
        r2 = rouge_n_hesapla(ref_kelimeler, tahmin_kelimeler, n=2)
        rl = rouge_l_hesapla(ref_kelimeler, tahmin_kelimeler)

        bleu1_list.append(b1)
        bleu2_list.append(b2)
        bleu4_list.append(b4)
        rouge1_list.append(r1)
        rouge2_list.append(r2)
        rougel_list.append(rl)

        detayli_sonuclar.append({
            "test_sorusu": kayit["input"],
            "gercek_cevap": kayit["output"],
            "eslesen_egitim_sorusu": model.egitim_sorulari[en_iyi_idx],
            "tahmin_cevap": model.egitim_cevaplari[en_iyi_idx],
            "kosinus_benzerligi": benzerlik,
            "bleu1": b1,
            "rouge1": r1,
            "rougel": rl
        })

    n = len(veri_listesi)
    ozet_metrikler = {
        "BLEU-1": (sum(bleu1_list) / n) * 100,
        "BLEU-2": (sum(bleu2_list) / n) * 100,
        "BLEU-4": (sum(bleu4_list) / n) * 100,
        "ROUGE-1": (sum(rouge1_list) / n) * 100,
        "ROUGE-2": (sum(rouge2_list) / n) * 100,
        "ROUGE-L": (sum(rougel_list) / n) * 100,
        "Ortalama Kosinüs Benzerliği": (sum(benzerlik_skorlari) / n) * 100
    }
    return ozet_metrikler, detayli_sonuclar


def hata_analizi_kaydet(detayli_sonuclar, dosya_yolu):
    """
    Yönerge Madde 14 (Error Analysis):
    En başarılı 5 örneği ve en başarısız 5 örneği seçip raporlar.
    """
    # ROUGE-1 ve Kosinüs benzerliği ortalamasına göre sırala
    sirali = sorted(
        detayli_sonuclar,
        key=lambda x: (x["rouge1"] + x["kosinus_benzerligi"]) / 2,
        reverse=True
    )

    en_iyi_5 = sirali[:5]
    # En kötü 5 için tamamen boş olmayan ama alakasız eşleşen örnekleri al
    en_kotu_5 = [x for x in reversed(sirali) if x["kosinus_benzerligi"] > 0.05][:5]

    metin = "=== ZORUNLU HATA ANALİZİ (ERROR ANALYSIS): 5 DOĞRU VE 5 HATALI ÖRNEK ===\n\n"
    metin += "------------------------------------------------------------------------\n"
    metin += "BÖLÜM A: BAŞARILI / DOĞRU YANITLANAN 5 ÖRNEK\n"
    metin += "------------------------------------------------------------------------\n"

    for idx, ornek in enumerate(en_iyi_5, 1):
        metin += (
            f"\n[Doğru Örnek #{idx}]\n"
            f"- Test Sorusu            : {ornek['test_sorusu']}\n"
            f"- Eşleşen Eğitim Sorusu  : {ornek['eslesen_egitim_sorusu']}\n"
            f"- Kosinüs Benzerliği     : %{ornek['kosinus_benzerligi']*100:.2f} | ROUGE-1: %{ornek['rouge1']*100:.2f}\n"
            f"- Gerçek Cevap (Özet)    : {ornek['gercek_cevap'][:220]}...\n"
            f"- Modelin Cevabı (Özet)  : {ornek['tahmin_cevap'][:220]}...\n"
        )

    metin += "\n\n------------------------------------------------------------------------\n"
    metin += "BÖLÜM B: HATALI / Yetersiz YANITLANAN 5 ÖRNEK VE HATA NEDENLERİ\n"
    metin += "------------------------------------------------------------------------\n"

    for idx, ornek in enumerate(en_kotu_5, 1):
        metin += (
            f"\n[Hatalı Örnek #{idx}]\n"
            f"- Test Sorusu            : {ornek['test_sorusu']}\n"
            f"- Eşleşen Eğitim Sorusu  : {ornek['eslesen_egitim_sorusu']}\n"
            f"- Kosinüs Benzerliği     : %{ornek['kosinus_benzerligi']*100:.2f} | ROUGE-1: %{ornek['rouge1']*100:.2f}\n"
            f"- Gerçek Cevap (Özet)    : {ornek['gercek_cevap'][:220]}...\n"
            f"- Modelin Cevabı (Özet)  : {ornek['tahmin_cevap'][:220]}...\n"
            f"- Hata Analizi Yorumu    : TF-IDF modeli anlamsal (semantik) bağlamı bilmediği için sadece yüzeysel kelime/ek eşleşmesine bakarak farklı bağlamdaki bir sorunun cevabını getirmiştir.\n"
        )

    with open(dosya_yolu, "w", encoding="utf-8") as f:
        f.write(metin)


def ana_degerlendirme():
    proje_dizini = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    veri_klasoru = os.path.join(proje_dizini, "data")
    model_yolu = os.path.join(proje_dizini, "models", "tfidf_baseline.pkl")
    sonuc_klasoru = os.path.join(proje_dizini, "results")

    os.makedirs(sonuc_klasoru, exist_ok=True)

    print(f"Model yükleniyor: {model_yolu}")
    model = TfidfRetrievalBaseline.yukle(model_yolu)

    with open(os.path.join(veri_klasoru, "val.json"), "r", encoding="utf-8") as f:
        val_veri = json.load(f)
    with open(os.path.join(veri_klasoru, "test.json"), "r", encoding="utf-8") as f:
        test_veri = json.load(f)

    val_metrikler, _ = veri_setini_degerlendir(model, val_veri, "Doğrulama (Validation)")
    test_metrikler, test_detaylar = veri_setini_degerlendir(model, test_veri, "Test")

    rapor = "=== TF-IDF + KOSİNÜS BENZERLİĞİ BASELINE MODEL SONUÇLARI ===\n\n"
    rapor += "1. Doğrulama (Validation) Seti Metrikleri (%):\n"
    for k, v in val_metrikler.items():
        rapor += f"   - {k:<28}: %{v:.2f}\n"

    rapor += "\n2. Test Seti Nihai Metrikleri (%):\n"
    for k, v in test_metrikler.items():
        rapor += f"   - {k:<28}: %{v:.2f}\n"

    rapor += (
        "\nNot: Perplexity (PPL) metriği olasılıksal dil modellerine (Transformer vb.) özgüdür;\n"
        "TF-IDF bilgi getirme (retrieval) modeli kelime olasılık dağılımı üretmediği için PPL hesaplanmaz.\n"
    )

    print("\n" + rapor)

    metrik_yolu = os.path.join(sonuc_klasoru, "baseline_metrikler.txt")
    with open(metrik_yolu, "w", encoding="utf-8") as f:
        f.write(rapor)

    hata_yolu = os.path.join(sonuc_klasoru, "hata_analizi_ornekleri.txt")
    hata_analizi_kaydet(test_detaylar, hata_yolu)
    print(f"Metrikler '{metrik_yolu}' dosyasına kaydedildi.")
    print(f"5 doğru / 5 hatalı örnek analizi '{hata_yolu}' dosyasına kaydedildi.")


if __name__ == "__main__":
    ana_degerlendirme()
