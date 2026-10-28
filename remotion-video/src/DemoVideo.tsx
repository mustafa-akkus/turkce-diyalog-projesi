import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
} from "remotion";

const FONT_FAMILY = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif";

// Alt kısımdaki ilerleme çubuğu ve sahne göstergesi
const BottomProgressBar: React.FC<{ sceneTitle: string; stepIndex: number }> = ({
  sceneTitle,
  stepIndex,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = (frame / durationInFrames) * 100;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        height: 68,
        background: "rgba(15, 23, 42, 0.92)",
        borderTop: "1px solid rgba(148, 163, 184, 0.2)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 60px",
        fontFamily: FONT_FAMILY,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            background: "linear-gradient(135deg, #3b82f6, #06b6d4)",
            color: "#fff",
            fontWeight: 700,
            fontSize: 16,
            padding: "6px 14px",
            borderRadius: 8,
          }}
        >
          BÖLÜM {stepIndex} / 5
        </div>
        <span style={{ color: "#e2e8f0", fontSize: 19, fontWeight: 600 }}>
          {sceneTitle}
        </span>
      </div>
      <div style={{ color: "#94a3b8", fontSize: 17 }}>
        Mustafa Can Akkuş (240711004) • Derin Öğrenmeye Giriş Dönem Projesi
      </div>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          height: 5,
          width: `${progress}%`,
          background: "linear-gradient(90deg, #3b82f6, #10b981, #f59e0b)",
        }}
      />
    </div>
  );
};

// SAHNE 1: GİRİŞ VE PROBLEM TANIMI (0 - 180 Kare / 0 - 6 sn)
const Scene1Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 14 } });
  const subtitleOpacity = interpolate(frame, [20, 45], [0, 1], {
    extrapolateRight: "clamp",
  });
  const cardsSlide = spring({
    frame: Math.max(0, frame - 40),
    fps,
    config: { damping: 15 },
  });

  const infoCards = [
    {
      badge: "PROBLEM TANIMI",
      title: "Türkçe Doğal Dil Diyalog Üretimi",
      desc: "Açık uçlu kullanıcı sorularını yorumlayıp bağlama uygun yanıtlar üreten diyalog sistemi tasarımı.",
      color: "#3b82f6",
    },
    {
      badge: "TEMEL ZORLUK",
      title: "Sondan Eklemeli Morfoloji",
      desc: "Türkçede tek bir kökten onlarca kelime türetilmesi, klasik kelime eşleme yöntemlerini zorlar.",
      color: "#f59e0b",
    },
    {
      badge: "İLK AŞAMA HEDEFİ",
      title: "TF-IDF + Kosinüs Referans Modeli",
      desc: "Derin öğrenme (Transformer) modellerinin başarımını kıyaslamak için nesnel alt sınır (baseline) kurulumu.",
      color: "#10b981",
    },
  ];

  return (
    <AbsoluteFill
      style={{
        padding: "70px 80px",
        fontFamily: FONT_FAMILY,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      {/* Üst Üniversite ve Ders Başlığı */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          opacity: subtitleOpacity,
        }}
      >
        <div
          style={{
            background: "rgba(59, 130, 246, 0.15)",
            border: "1px solid rgba(59, 130, 246, 0.4)",
            padding: "10px 22px",
            borderRadius: 999,
            color: "#60a5fa",
            fontWeight: 700,
            fontSize: 20,
            letterSpacing: 0.5,
          }}
        >
          ATATÜRK ÜNİVERSİTESİ • YAPAY ZEKA VE VERİ MÜHENDİSLİĞİ
        </div>
        <div style={{ color: "#cbd5e1", fontSize: 20, fontWeight: 500 }}>
          Öğretim Üyesi: Prof. Dr. Afshin Ebrahimi
        </div>
      </div>

      {/* Ana Başlık */}
      <div
        style={{
          transform: `scale(${interpolate(titleScale, [0, 1], [0.9, 1])})`,
          opacity: titleScale,
          marginTop: 10,
        }}
      >
        <div
          style={{
            fontSize: 24,
            fontWeight: 700,
            color: "#38bdf8",
            marginBottom: 12,
            letterSpacing: 1.5,
          }}
        >
          DERİN ÖĞRENMEYE GİRİŞ PROJESİ — AŞAMA 1 (BASELINE)
        </div>
        <h1
          style={{
            fontSize: 66,
            fontWeight: 800,
            color: "#f8fafc",
            margin: 0,
            lineHeight: 1.15,
          }}
        >
          Türkçe Transformer Tabanlı Diyalog Ajanı
        </h1>
        <p
          style={{
            fontSize: 30,
            color: "#94a3b8",
            marginTop: 16,
            marginBottom: 0,
          }}
        >
          TF-IDF ve Kosinüs Benzerliği Tabanlı Bilgi Getirme (Retrieval) Referans Modeli
        </p>
      </div>

      {/* 3 Bilgi Kartı */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 30,
          marginBottom: 60,
          transform: `translateY(${interpolate(cardsSlide, [0, 1], [50, 0])}px)`,
          opacity: cardsSlide,
        }}
      >
        {infoCards.map((c, i) => (
          <div
            key={i}
            style={{
              background: "rgba(30, 41, 59, 0.78)",
              border: `2px solid ${c.color}55`,
              borderRadius: 20,
              padding: "30px 32px",
              boxShadow: "0 20px 40px rgba(0,0,0,0.3)",
            }}
          >
            <div
              style={{
                display: "inline-block",
                background: `${c.color}22`,
                color: c.color,
                padding: "6px 14px",
                borderRadius: 8,
                fontSize: 16,
                fontWeight: 800,
                marginBottom: 16,
              }}
            >
              {c.badge}
            </div>
            <h3
              style={{
                color: "#f1f5f9",
                fontSize: 28,
                margin: "0 0 12px 0",
                fontWeight: 700,
              }}
            >
              {c.title}
            </h3>
            <p
              style={{
                color: "#cbd5e1",
                fontSize: 21,
                lineHeight: 1.45,
                margin: 0,
              }}
            >
              {c.desc}
            </p>
          </div>
        ))}
      </div>

      <BottomProgressBar
        sceneTitle="Proje Tanımı, Motivasyon ve Baseline Hedefi"
        stepIndex={1}
      />
    </AbsoluteFill>
  );
};

// SAHNE 2: VERİ SETİ VE ÖN İŞLEME HATTI (180 - 390 Kare / 6 - 13 sn)
const Scene2Preprocessing: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const steps = [
    {
      num: "01",
      title: "Ham Veri Seti (data.json)",
      detail: "sixfingerdev/turkish-qa-multi-dialog-dataset",
      stat: "21.282 Soru-Cevap Çifti",
      color: "#38bdf8",
    },
    {
      num: "02",
      title: "Türkçe Uyumlu Ön İşleme",
      detail: "I → ı ve İ → i dönüşümü, noktalama ve gürültü temizliği",
      stat: "58.426 Benzersiz Kelime (Vocab)",
      color: "#a855f7",
    },
    {
      num: "03",
      title: "Veri Sızıntısı (Data Leakage) Önleme",
      detail: "Birebir tekrar eden 1.851 soru bölünmeden önce temizlendi",
      stat: "19.431 Tekil ve Temiz Örnek",
      color: "#10b981",
    },
  ];

  const barProgress = interpolate(frame, [80, 150], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        padding: "65px 80px",
        fontFamily: FONT_FAMILY,
      }}
    >
      <div style={{ color: "#38bdf8", fontSize: 22, fontWeight: 700 }}>
        MODÜL 1 • src/preprocessing.py
      </div>
      <h2
        style={{
          color: "#f8fafc",
          fontSize: 50,
          margin: "8px 0 36px 0",
          fontWeight: 800,
        }}
      >
        Veri Ön İşleme, Sızıntı Önleme ve Bölümleme
      </h2>

      {/* 3 Aşamalı Ön İşleme Akışı */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 28,
          marginBottom: 42,
        }}
      >
        {steps.map((s, idx) => {
          const appear = spring({
            frame: Math.max(0, frame - idx * 20),
            fps,
            config: { damping: 14 },
          });
          return (
            <div
              key={idx}
              style={{
                background: "rgba(30, 41, 59, 0.85)",
                border: `2px solid ${s.color}66`,
                borderRadius: 20,
                padding: "28px 30px",
                transform: `translateY(${interpolate(appear, [0, 1], [40, 0])}px)`,
                opacity: appear,
              }}
            >
              <div
                style={{
                  fontSize: 38,
                  fontWeight: 900,
                  color: s.color,
                  marginBottom: 10,
                }}
              >
                ADIM {s.num}
              </div>
              <div
                style={{
                  fontSize: 27,
                  fontWeight: 700,
                  color: "#f8fafc",
                  marginBottom: 10,
                }}
              >
                {s.title}
              </div>
              <div
                style={{
                  fontSize: 20,
                  color: "#94a3b8",
                  marginBottom: 20,
                  lineHeight: 1.4,
                }}
              >
                {s.detail}
              </div>
              <div
                style={{
                  background: `${s.color}20`,
                  border: `1px solid ${s.color}55`,
                  color: "#f1f5f9",
                  padding: "10px 16px",
                  borderRadius: 12,
                  fontSize: 21,
                  fontWeight: 700,
                }}
              >
                {s.stat}
              </div>
            </div>
          );
        })}
      </div>

      {/* Veri Bölümleme Kutusu */}
      <div
        style={{
          background: "rgba(15, 23, 42, 0.9)",
          border: "2px solid rgba(148, 163, 184, 0.25)",
          borderRadius: 22,
          padding: "30px 36px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 20,
          }}
        >
          <span style={{ color: "#f8fafc", fontSize: 26, fontWeight: 700 }}>
            Veri Kümesi Bölünmesi (Sabit Tohum: RANDOM_SEED = 42)
          </span>
          <span style={{ color: "#94a3b8", fontSize: 20 }}>
            Ortalama Soru: 8.69 kelime | Ortalama Cevap: 29.01 kelime
          </span>
        </div>

        {/* Bölünme Barı */}
        <div
          style={{
            height: 54,
            width: "100%",
            background: "#1e293b",
            borderRadius: 14,
            overflow: "hidden",
            display: "flex",
          }}
        >
          <div
            style={{
              width: `${80 * barProgress}%`,
              background: "linear-gradient(90deg, #2563eb, #3b82f6)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#fff",
              fontWeight: 800,
              fontSize: 21,
            }}
          >
            %80 EĞİTİM (15.544 Örnek)
          </div>
          <div
            style={{
              width: `${10 * barProgress}%`,
              background: "#f59e0b",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#0f172a",
              fontWeight: 800,
              fontSize: 18,
            }}
          >
            %10 VAL (1.943)
          </div>
          <div
            style={{
              width: `${10 * barProgress}%`,
              background: "#10b981",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#0f172a",
              fontWeight: 800,
              fontSize: 18,
            }}
          >
            %10 TEST (1.944)
          </div>
        </div>
      </div>

      <BottomProgressBar
        sceneTitle="Veri Ön İşleme, Tekrar Temizliği ve %80/%10/%10 Bölümleme"
        stepIndex={2}
      />
    </AbsoluteFill>
  );
};

// SAHNE 3: TF-IDF VE KOSİNÜS BENZERLİĞİ MİMARİSİ (390 - 630 Kare / 13 - 21 sn)
const Scene3Architecture: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = Math.sin(frame / 8) * 0.03 + 1;

  const sampleWeights = [
    { token: "stresle", tfidf: 0.58, color: "#38bdf8" },
    { token: "başa çıkabilirim", tfidf: 0.64, color: "#10b981" },
    { token: "nasıl", tfidf: 0.29, color: "#f59e0b" },
    { token: "anksiyete", tfidf: 0.41, color: "#a855f7" },
  ];

  return (
    <AbsoluteFill style={{ padding: "65px 80px", fontFamily: FONT_FAMILY }}>
      <div style={{ color: "#10b981", fontSize: 22, fontWeight: 700 }}>
        MODÜL 2 & 3 • src/model.py & src/train.py
      </div>
      <h2
        style={{
          color: "#f8fafc",
          fontSize: 50,
          margin: "8px 0 34px 0",
          fontWeight: 800,
        }}
      >
        Referans Model Mimarisi: TF-IDF + Kosinüs Benzerliği
      </h2>

      {/* Mimari Akış Diyagramı */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1.15fr 1fr",
          gap: 28,
          alignItems: "stretch",
        }}
      >
        {/* Sol Kutu: TF-IDF Uzayı */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.85)",
            border: "2px solid rgba(56, 189, 248, 0.4)",
            borderRadius: 22,
            padding: 30,
          }}
        >
          <div style={{ color: "#38bdf8", fontWeight: 800, fontSize: 20 }}>
            1. ÖZELLİK ÇIKARIMI (TF-IDF)
          </div>
          <h3 style={{ color: "#f8fafc", fontSize: 28, margin: "10px 0 16px 0" }}>
            Eğitim Matrisi: (15.544 × 25.000)
          </h3>
          <p style={{ color: "#cbd5e1", fontSize: 20, lineHeight: 1.45 }}>
            Eğitim setindeki sorular <b>(1, 2) N-Gram</b> (tekli ve ikili kelime grupları) ile{" "}
            <code>sublinear_tf=True</code> kullanılarak vektörleştirilir.
          </p>

          <div style={{ marginTop: 22 }}>
            <div style={{ color: "#94a3b8", fontSize: 18, marginBottom: 10 }}>
              Örnek Terim Ağırlıkları (TF × IDF):
            </div>
            {sampleWeights.map((item, idx) => {
              const barW = spring({
                frame: Math.max(0, frame - 20 - idx * 12),
                fps,
                config: { damping: 14 },
              });
              return (
                <div key={idx} style={{ marginBottom: 12 }}>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      color: "#e2e8f0",
                      fontSize: 18,
                      marginBottom: 4,
                    }}
                  >
                    <span>"{item.token}"</span>
                    <span style={{ fontWeight: 700 }}>{item.tfidf.toFixed(2)}</span>
                  </div>
                  <div
                    style={{
                      height: 12,
                      background: "#0f172a",
                      borderRadius: 6,
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        width: `${item.tfidf * 100 * barW}%`,
                        height: "100%",
                        background: item.color,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Orta Kutu: Kosinüs Benzerliği */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.95)",
            border: "2px solid rgba(245, 158, 11, 0.6)",
            borderRadius: 22,
            padding: 32,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            transform: `scale(${pulse})`,
          }}
        >
          <div>
            <div style={{ color: "#f59e0b", fontWeight: 800, fontSize: 20 }}>
              2. BENZERLİK HESABI
            </div>
            <h3 style={{ color: "#f8fafc", fontSize: 30, margin: "10px 0 16px 0" }}>
              Kosinüs Benzerliği (Cosine Similarity)
            </h3>
            <p style={{ color: "#cbd5e1", fontSize: 20, lineHeight: 1.45 }}>
              Kullanıcı sorgusu <b>Q</b> ile eğitimdeki her <b>D_i</b> soru vektörü arasındaki açının kosinüsü hesaplanır:
            </p>
          </div>

          <div
            style={{
              background: "rgba(30, 41, 59, 0.9)",
              border: "1px solid rgba(245, 158, 11, 0.4)",
              borderRadius: 16,
              padding: "22px 20px",
              textAlign: "center",
              color: "#fef08a",
              fontSize: 27,
              fontWeight: 700,
              letterSpacing: 1,
            }}
          >
            cos(θ) = (Q · D_i) / (||Q|| × ||D_i||)
          </div>

          <div
            style={{
              background: "rgba(16, 185, 129, 0.15)",
              border: "1px solid rgba(16, 185, 129, 0.4)",
              borderRadius: 14,
              padding: "16px 20px",
              color: "#a7f3d0",
              fontSize: 20,
              fontWeight: 600,
            }}
          >
            En yüksek skoru veren indeks:
            <br />
            <code style={{ color: "#fff", fontSize: 22 }}>
              en_iyi_indeks = np.argmax(benzerlikler)
            </code>
          </div>
        </div>

        {/* Sağ Kutu: Yanıt Getirme */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.85)",
            border: "2px solid rgba(16, 185, 129, 0.4)",
            borderRadius: 22,
            padding: 30,
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
          }}
        >
          <div>
            <div style={{ color: "#10b981", fontWeight: 800, fontSize: 20 }}>
              3. YANIT DÖNDÜRME (RETRIEVAL)
            </div>
            <h3 style={{ color: "#f8fafc", fontSize: 28, margin: "10px 0 16px 0" }}>
              En Yakın Sorunun Cevabı
            </h3>
            <p style={{ color: "#cbd5e1", fontSize: 20, lineHeight: 1.45 }}>
              Model sıfırdan kelime üretmez; eğitim kümesinde en yüksek benzerliğe sahip sorunun doğrulanmış cevabını döndürür.
            </p>
          </div>

          <div
            style={{
              background: "#0f172a",
              borderRadius: 16,
              padding: 22,
              borderLeft: "5px solid #10b981",
            }}
          >
            <div style={{ color: "#94a3b8", fontSize: 17, marginBottom: 6 }}>
              Kaydedilen Model Dosyası:
            </div>
            <div
              style={{
                color: "#38bdf8",
                fontSize: 22,
                fontWeight: 700,
                marginBottom: 14,
              }}
            >
              models/tfidf_baseline.pkl
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 18 }}>
              • CPU üzerinde milisaniyeler içinde çıkarım
              <br />• 500'lük mini-batch matris çarpımı ile hızlı test
            </div>
          </div>
        </div>
      </div>

      <BottomProgressBar
        sceneTitle="Sistem Mimarisi: TF-IDF Vektörleştirme ve Kosinüs Benzerliği"
        stepIndex={3}
      />
    </AbsoluteFill>
  );
};

// SAHNE 4: CANLI DEMO VE HATA ANALİZİ (630 - 870 Kare / 21 - 29 sn)
const Scene4DemoAndError: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const leftAppear = spring({ frame, fps, config: { damping: 14 } });
  const rightAppear = spring({
    frame: Math.max(0, frame - 45),
    fps,
    config: { damping: 14 },
  });

  return (
    <AbsoluteFill style={{ padding: "65px 80px", fontFamily: FONT_FAMILY }}>
      <div style={{ color: "#f59e0b", fontSize: 22, fontWeight: 700 }}>
        MODÜL 4 • src/inference.py & ZORUNLU HATA ANALİZİ
      </div>
      <h2
        style={{
          color: "#f8fafc",
          fontSize: 48,
          margin: "8px 0 30px 0",
          fontWeight: 800,
        }}
      >
        Canlı Soru-Cevap Testi ve Sözlük Dışı (OOV) Hata Analizi
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 32,
        }}
      >
        {/* Sol Terminal: Başarılı Örnek */}
        <div
          style={{
            background: "#090d16",
            border: "2px solid #10b98188",
            borderRadius: 20,
            overflow: "hidden",
            transform: `translateY(${interpolate(leftAppear, [0, 1], [35, 0])}px)`,
            opacity: leftAppear,
          }}
        >
          <div
            style={{
              background: "#1e293b",
              padding: "14px 24px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span style={{ color: "#10b981", fontWeight: 800, fontSize: 20 }}>
              ✓ BAŞARILI ÖRNEK (Benzerlik: %87.04)
            </span>
            <span style={{ color: "#94a3b8", fontSize: 16 }}>src/inference.py</span>
          </div>
          <div style={{ padding: 28, fontSize: 21, lineHeight: 1.5 }}>
            <div style={{ color: "#38bdf8", marginBottom: 14 }}>
              <b>Kullanıcı:</b> "Anksiyete ve stresle nasıl başa çıkabilirim?"
            </div>
            <div style={{ color: "#94a3b8", fontSize: 19, marginBottom: 16 }}>
              <b>Eşleşen Eğitim Sorusu:</b> "Stresle nasıl başa çıkabilirim?"
            </div>
            <div
              style={{
                background: "rgba(16, 185, 129, 0.1)",
                borderLeft: "4px solid #10b981",
                padding: "16px 20px",
                borderRadius: 8,
                color: "#e2e8f0",
                fontSize: 19,
              }}
            >
              <b>Model Yanıtı:</b> Stres yönetimi için etkili yöntemler:
              <br />1. Nefes egzersizleri (4-7-8 tekniği)
              <br />2. Fiziksel aktivite (Günde 30 dk yürüyüş)
              <br />3. Meditasyon ve 7-8 saat kaliteli uyku düzeni
            </div>
          </div>
        </div>

        {/* Sağ Terminal: Hata Analizi Örneği */}
        <div
          style={{
            background: "#090d16",
            border: "2px solid #ef444488",
            borderRadius: 20,
            overflow: "hidden",
            transform: `translateY(${interpolate(rightAppear, [0, 1], [35, 0])}px)`,
            opacity: rightAppear,
          }}
        >
          <div
            style={{
              background: "#1e293b",
              padding: "14px 24px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span style={{ color: "#f87171", fontWeight: 800, fontSize: 20 }}>
              ✗ HATA ANALİZİ: SÖZLÜK DIŞI (OOV) SORUNU
            </span>
            <span style={{ color: "#94a3b8", fontSize: 16 }}>Neden Transformer?</span>
          </div>
          <div style={{ padding: 28, fontSize: 21, lineHeight: 1.5 }}>
            <div style={{ color: "#fca5a5", marginBottom: 14 }}>
              <b>Kullanıcı:</b> "Cinsellik üzerine ne düşünüyorsun"
            </div>
            <div style={{ color: "#94a3b8", fontSize: 19, marginBottom: 16 }}>
              <b>Eşleşen Soru:</b> "Osmanlı'nın başarısızlığı üzerine ne oldu?" (%65.5)
            </div>
            <div
              style={{
                background: "rgba(239, 68, 68, 0.12)",
                borderLeft: "4px solid #ef4444",
                padding: "16px 20px",
                borderRadius: 8,
                color: "#e2e8f0",
                fontSize: 19,
              }}
            >
              <b>Hata Nedeni (Morfoloji & OOV):</b>
              <br />• Eğitimde <code>"cinsel"</code> ve <code>"düşünüyorsunuz"</code> var ancak ek almış <code>"cinsellik"</code> ve <code>"düşünüyorsun"</code> kelimeleri yok!
              <br />• TF-IDF bilmediği kelimeleri silip sadece <b>"üzerine ne"</b> (IDF: 8.86) kalıbına bakarak yanlış soruyu getirir.
            </div>
          </div>
        </div>
      </div>

      <BottomProgressBar
        sceneTitle="Canlı Demo Çıktısı ve Türkçe Morfolojisi / OOV Hata Analizi"
        stepIndex={4}
      />
    </AbsoluteFill>
  );
};

// SAHNE 5: DEĞERLENDİRME METRİKLERİ VE YOL HARİTASI (870 - 1050 Kare / 29 - 35 sn)
const Scene5MetricsAndRoadmap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const countProgress = interpolate(frame, [10, 65], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const metrics = [
    { name: "BLEU-1", val: 11.1, color: "#38bdf8" },
    { name: "BLEU-2", val: 7.03, color: "#60a5fa" },
    { name: "BLEU-4", val: 2.32, color: "#818cf8" },
    { name: "ROUGE-1", val: 13.36, color: "#10b981" },
    { name: "ROUGE-2", val: 5.84, color: "#34d399" },
    { name: "ROUGE-L", val: 12.48, color: "#f59e0b" },
  ];

  const roadmapAppear = spring({
    frame: Math.max(0, frame - 40),
    fps,
    config: { damping: 14 },
  });

  return (
    <AbsoluteFill style={{ padding: "65px 80px", fontFamily: FONT_FAMILY }}>
      <div style={{ color: "#a855f7", fontSize: 22, fontWeight: 700 }}>
        MODÜL 5 • src/evaluate.py & SONRAKİ DERİN ÖĞRENME AŞAMALARI
      </div>
      <h2
        style={{
          color: "#f8fafc",
          fontSize: 48,
          margin: "8px 0 30px 0",
          fontWeight: 800,
        }}
      >
        Test Seti Nicel Metrikleri ve Proje Yol Haritası
      </h2>

      {/* 6 Metrik Kartı */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(6, 1fr)",
          gap: 20,
          marginBottom: 40,
        }}
      >
        {metrics.map((m, idx) => (
          <div
            key={idx}
            style={{
              background: "rgba(30, 41, 59, 0.88)",
              border: `2px solid ${m.color}66`,
              borderRadius: 18,
              padding: "24px 18px",
              textAlign: "center",
            }}
          >
            <div style={{ color: "#94a3b8", fontSize: 20, fontWeight: 700 }}>
              {m.name}
            </div>
            <div
              style={{
                color: m.color,
                fontSize: 42,
                fontWeight: 900,
                marginTop: 10,
              }}
            >
              %{(m.val * countProgress).toFixed(2)}
            </div>
          </div>
        ))}
      </div>

      {/* Yol Haritası Kutusu */}
      <div
        style={{
          background: "rgba(15, 23, 42, 0.92)",
          border: "2px solid rgba(56, 189, 248, 0.35)",
          borderRadius: 22,
          padding: "30px 36px",
          transform: `translateY(${interpolate(roadmapAppear, [0, 1], [30, 0])}px)`,
          opacity: roadmapAppear,
        }}
      >
        <div
          style={{
            color: "#f8fafc",
            fontSize: 26,
            fontWeight: 800,
            marginBottom: 20,
          }}
        >
          Karşılaştırmalı Deneysel Çalışma Yol Haritası
        </div>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 24,
          }}
        >
          <div
            style={{
              background: "rgba(16, 185, 129, 0.15)",
              border: "1px solid #10b981",
              borderRadius: 14,
              padding: 20,
            }}
          >
            <div style={{ color: "#10b981", fontWeight: 800, fontSize: 19 }}>
              ✓ AŞAMA 1 (TAMAMLANDI)
            </div>
            <div
              style={{
                color: "#f8fafc",
                fontSize: 22,
                fontWeight: 700,
                marginTop: 6,
              }}
            >
              TF-IDF + Kosinüs Baseline
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 18, marginTop: 6 }}>
              İstatistiksel bilgi getirme alt sınırı ve 5 doğru / 5 yanlış örnek analizi.
            </div>
          </div>

          <div
            style={{
              background: "rgba(59, 130, 246, 0.15)",
              border: "1px solid #3b82f6",
              borderRadius: 14,
              padding: 20,
            }}
          >
            <div style={{ color: "#60a5fa", fontWeight: 800, fontSize: 19 }}>
              → AŞAMA 2 (SIRADAKİ ADIM)
            </div>
            <div
              style={{
                color: "#f8fafc",
                fontSize: 22,
                fontWeight: 700,
                marginTop: 6,
              }}
            >
              Model A: Seq2Seq Transformer
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 18, marginTop: 6 }}>
              Subword/BPE tokenizasyonu ve Çoklu Kafa Öz-Dikkat (Multi-Head Self-Attention).
            </div>
          </div>

          <div
            style={{
              background: "rgba(168, 85, 247, 0.15)",
              border: "1px solid #a855f7",
              borderRadius: 14,
              padding: 20,
            }}
          >
            <div style={{ color: "#c084fc", fontWeight: 800, fontSize: 19 }}>
              → AŞAMA 3 (HEDEF MODEL)
            </div>
            <div
              style={{
                color: "#f8fafc",
                fontSize: 22,
                fontWeight: 700,
                marginTop: 6,
              }}
            >
              Model B: Pretrained Türkçe LM
            </div>
            <div style={{ color: "#cbd5e1", fontSize: 18, marginTop: 6 }}>
              Önceden eğitilmiş Türkçe dil modelinin ince ayarı (Fine-Tuning) ve Perplexity kıyaslaması.
            </div>
          </div>
        </div>
      </div>

      <BottomProgressBar
        sceneTitle="Test Seti Değerlendirme Metrikleri ve Derin Öğrenme Yol Haritası"
        stepIndex={5}
      />
    </AbsoluteFill>
  );
};

export const DemoVideo: React.FC = () => {
  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 20% 20%, #1e293b 0%, #0f172a 60%, #020617 100%)",
      }}
    >
      <Sequence from={0} durationInFrames={180}>
        <Scene1Intro />
      </Sequence>
      <Sequence from={180} durationInFrames={210}>
        <Scene2Preprocessing />
      </Sequence>
      <Sequence from={390} durationInFrames={240}>
        <Scene3Architecture />
      </Sequence>
      <Sequence from={630} durationInFrames={240}>
        <Scene4DemoAndError />
      </Sequence>
      <Sequence from={870} durationInFrames={180}>
        <Scene5MetricsAndRoadmap />
      </Sequence>
    </AbsoluteFill>
  );
};
