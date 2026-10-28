import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import metin_temizle


class TfidfRetrievalBaseline:
    """
    TF-IDF + Kosinüs Benzerliği Tabanlı Bilgi Getirme (Retrieval) Referans Modeli.

    Çalışma Mantığı:
    1. Eğitim setindeki tüm sorular TF-IDF vektörlerine dönüştürülür.
    2. Kullanıcıdan yeni bir soru geldiğinde, aynı TF-IDF uzayına çevrilir.
    3. Gelen soru ile eğitimdeki tüm sorular arasında Kosinüs Benzerliği hesaplanır.
    4. En yüksek benzerliğe sahip eğitim sorusunun cevabı çıktı olarak döndürülür.
    """

    def __init__(self, ngram_range=(1, 2), max_features=25000):
        # Hem tek kelimeleri (1-gram) hem de ikili kelime gruplarını (2-gram) alır.
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            sublinear_tf=True
        )
        self.egitim_tfidf_matrisi = None
        self.egitim_sorulari = []
        self.egitim_cevaplari = []
        self.egitim_temiz_cevaplari = []

    def fit(self, egitim_verisi):
        """
        Modeli eğitim verisi (train.json) üzerindeki sorularla eğitir (TF-IDF matrisini kurar).
        """
        temiz_sorular = [kayit["clean_input"] for kayit in egitim_verisi]
        self.egitim_sorulari = [kayit["input"] for kayit in egitim_verisi]
        self.egitim_cevaplari = [kayit["output"] for kayit in egitim_verisi]
        self.egitim_temiz_cevaplari = [kayit["clean_output"] for kayit in egitim_verisi]

        # Soruları TF-IDF matrisine dönüştür
        self.egitim_tfidf_matrisi = self.vectorizer.fit_transform(temiz_sorular)
        print(f"      TF-IDF Matrisi Boyutu: {self.egitim_tfidf_matrisi.shape}")

    def cevap_bul(self, kullanici_sorusu):
        """
        Tek bir kullanıcı sorusu için en yakın eğitim sorusunu ve cevabını döndürür.
        """
        temiz_sorgu = metin_temizle(kullanici_sorusu)
        sorgu_vektoru = self.vectorizer.transform([temiz_sorgu])

        # Sorgu vektörü ile tüm eğitim soruları arasındaki kosinüs benzerliğini hesapla
        benzerlikler = cosine_similarity(sorgu_vektoru, self.egitim_tfidf_matrisi).flatten()

        en_iyi_indeks = int(np.argmax(benzerlikler))
        en_yuksek_skor = float(benzerlikler[en_iyi_indeks])

        return {
            "sorgu": kullanici_sorusu,
            "eslesen_egitim_sorusu": self.egitim_sorulari[en_iyi_indeks],
            "tahmin_cevap": self.egitim_cevaplari[en_iyi_indeks],
            "tahmin_temiz_cevap": self.egitim_temiz_cevaplari[en_iyi_indeks],
            "benzerlik_skoru": en_yuksek_skor
        }

    def toplu_tahmin(self, temiz_sorular_listesi, batch_boyutu=500):
        """
        Değerlendirme (evaluate) aşamasında yüzlerce soruyu hızlıca tahmin etmek için
        mini-batch halinde kosinüs benzerliği hesaplar.
        """
        sorgu_matrisi = self.vectorizer.transform(temiz_sorular_listesi)
        en_iyi_indeksler = []
        en_yuksek_skorlar = []

        toplam = sorgu_matrisi.shape[0]
        for baslangic in range(0, toplam, batch_boyutu):
            bitis = min(baslangic + batch_boyutu, toplam)
            alt_matris = sorgu_matrisi[baslangic:bitis]

            benzerlik_matrisi = cosine_similarity(alt_matris, self.egitim_tfidf_matrisi)
            indeksler = np.argmax(benzerlik_matrisi, axis=1)
            skorlar = benzerlik_matrisi[np.arange(len(indeksler)), indeksler]

            en_iyi_indeksler.extend(indeksler.tolist())
            en_yuksek_skorlar.extend(skorlar.tolist())

        return en_iyi_indeksler, en_yuksek_skorlar

    def kaydet(self, dosya_yolu):
        """Modeli diske kaydeder."""
        joblib.dump(self, dosya_yolu)

    @staticmethod
    def yukle(dosya_yolu):
        """Kaydedilmiş modeli diskten yükler."""
        return joblib.load(dosya_yolu)
