import datetime
import hashlib
import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Nova — Diyet ve Aktivite Asistanı",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------
# ESTETİK ÖZEL CSS (Lüks Serif Tipografi, Card & Swarovski Nova Teması)
# ----------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

    /* Ana Arkaplan ve Metin Renkleri */
    .stApp {
        background-color: #0b132b;
        color: #e0e1dd;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Tüm Başlıklar için Lüks Serif Tipografi */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', Georgia, serif !important;
        letter-spacing: 0.5px;
        color: #ffffff !important;
    }

    /* Sidebar (Yan Menü) Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #1c2541;
        color: #e0e1dd;
    }

    /* Tab'lar ve Form Başlıkları */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-size: 16px;
        color: #a0aab8;
        background-color: transparent;
        border-radius: 6px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #48cae4 !important;
    }

    /* Lüks Metric Kartları (Rakamların Kesilmesini Engelleyen Özel Tasarım) */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(28, 37, 65, 0.9) 0%, rgba(11, 19, 43, 0.95) 100%);
        border: 1px solid rgba(72, 202, 228, 0.25);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(72, 202, 228, 0.6);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Playfair Display', Georgia, serif !important;
        font-style: italic !important;
        font-size: 15px !important;
        color: #a0aab8 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 26px !important;
        color: #ffffff !important;
    }

    /* Estetik Tablo Özelleştirmeleri */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(58, 80, 107, 0.5);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }

    /* Özel Bilgi ve Makro Kartı */
    .nova-summary-card {
        background: linear-gradient(135deg, #1c2541 0%, #0b132b 100%);
        border: 1px solid #3a506b;
        border-left: 4px solid #48cae4;
        padding: 18px 24px;
        border-radius: 10px;
        margin-top: 15px;
        font-size: 15px;
        color: #e0e1dd;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }
    .nova-summary-card span {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .nova-summary-card strong {
        color: #ffffff;
        font-weight: 600;
    }

    /* Butonlar */
    .stButton > button {
        background-color: #3a506b;
        color: #ffffff;
        border: 1px solid #48cae4;
        border-radius: 8px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 500;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #48cae4;
        color: #0b132b;
        border-color: #48cae4;
    }

    /* Metin Girişleri ve Seçim Kutuları */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
        background-color: #1c2541;
        color: #ffffff;
        border-radius: 6px;
        border: 1px solid #3a506b;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sidebar İçi Ortalanmış Profil Kutusu */
    .sidebar-user-card {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .sidebar-user-name {
        font-family: 'Playfair Display', Georgia, serif;
        font-style: italic;
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 8px;
        margin-bottom: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

USERS_FILE = "kullanicilar.json"
AMBLEM_PATH = "watermarked_img_10875607693201107735.jpg"


# ----------------------------------------------------
# KULLANICI YÖNETİMİ & ŞİFRELEME FONKSİYONLARI
# ----------------------------------------------------
def sifre_hashle(sifre):
  return hashlib.sha256(sifre.encode("utf-8")).hexdigest()


def kullanicilari_yukle():
  if os.path.exists(USERS_FILE):
    try:
      with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return {}
  return {}


def kullanicilari_kaydet(users):
  with open(USERS_FILE, "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=4)


def kullanici_veri_dosyasi(username):
  return f"veriler_{username.lower().strip()}.json"


def verileri_yukle(username):
  user_file = kullanici_veri_dosyasi(username)
  default_data = {
      "besin_veritabani": {
          "tavuk gogsu": {
              "kalori": 165,
              "protein": 31.0,
              "karb": 0.0,
              "yag": 3.6,
          },
          "kofte": {"kalori": 220, "protein": 24.0, "karb": 2.0, "yag": 13.0},
          "ton baligi": {
              "kalori": 110,
              "protein": 25.0,
              "karb": 0.0,
              "yag": 1.0,
          },
          "marul": {"kalori": 15, "protein": 1.4, "karb": 2.9, "yag": 0.2},
          "salatalik": {"kalori": 15, "protein": 0.7, "karb": 3.6, "yag": 0.1},
          "domates": {"kalori": 18, "protein": 0.9, "karb": 3.9, "yag": 0.2},
          "zeytinyagi": {
              "kalori": 884,
              "protein": 0.0,
              "karb": 0.0,
              "yag": 100.0,
          },
          "dilim peynir": {
              "kalori": 320,
              "protein": 22.0,
              "karb": 1.5,
              "yag": 25.0,
          },
          "tam bugday ekmegi": {
              "kalori": 247,
              "protein": 13.0,
              "karb": 41.0,
              "yag": 3.4,
          },
          "labne": {"kalori": 210, "protein": 6.0, "karb": 4.0, "yag": 20.0},
          "sut": {"kalori": 50, "protein": 3.4, "karb": 4.8, "yag": 1.5},
          "kahve": {"kalori": 2, "protein": 0.1, "karb": 0.3, "yag": 0.0},
          "kefir": {"kalori": 60, "protein": 3.5, "karb": 4.5, "yag": 3.0},
          "x-lim toz": {"kalori": 20, "protein": 0.0, "karb": 5.0, "yag": 0.0},
          "badem": {"kalori": 575, "protein": 21.0, "karb": 22.0, "yag": 49.0},
          "mandalina": {"kalori": 53, "protein": 0.8, "karb": 13.3, "yag": 0.3},
          "meyveli soda": {
              "kalori": 45,
              "protein": 0.0,
              "karb": 11.0,
              "yag": 0.0,
          },
      },
      "hazir_tarifler": {
          "Tavuklu Salata": {
              "tavuk gogsu": 200,
              "marul": 30,
              "domates": 100,
              "salatalik": 100,
              "zeytinyagi": 10,
              "dilim peynir": 30,
              "tam bugday ekmegi": 25,
              "labne": 15,
          },
          "Köfteli Salata": {
              "kofte": 150,
              "marul": 30,
              "domates": 100,
              "salatalik": 100,
              "zeytinyagi": 10,
              "dilim peynir": 30,
              "tam bugday ekmegi": 25,
              "labne": 15,
          },
          "Ton Balıklı Salata": {
              "ton baligi": 110,
              "marul": 30,
              "domates": 100,
              "salatalik": 100,
              "zeytinyagi": 10,
              "dilim peynir": 30,
              "tam bugday ekmegi": 25,
              "labne": 15,
          },
          "Latte (Orta Boy)": {"sut": 250, "kahve": 30},
          "Americano (Orta Boy)": {"kahve": 20},
          "Kefir Karışımı": {"kefir": 200, "x-lim toz": 5},
          "Badem (1 Avuç)": {"badem": 30},
          "Mandalina (3 Adet)": {"mandalina": 300},
          "Meyveli Soda": {"meyveli soda": 200},
      },
      "gunluk_kayitlar": [],
      "aktivite_loglari": {},
      "profil": {
          "cinsiyet": "Kadın",
          "yas": 20,
          "boy": 165,
          "mevcut_kilo": 58.0,
          "hedef_kilo": 55.0,
          "hedef_kalori": 1800,
          "hedef_protein": 90,
          "hedef_karb": 200,
          "hedef_yag": 60,
      },
  }

  if os.path.exists(user_file):
    try:
      with open(user_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        profil = data.get("profil", {})
        if "mevcut_kilo" not in profil:
          profil["mevcut_kilo"] = profil.get("kilo", 58.0)
        if "hedef_kilo" not in profil:
          profil["hedef_kilo"] = 55.0
        data["profil"] = profil
        return data
    except:
      return default_data
  return default_data


def verileri_kaydet(username):
  user_file = kullanici_veri_dosyasi(username)
  data = {
      "besin_veritabani": st.session_state.besin_veritabani,
      "hazir_tarifler": st.session_state.hazir_tarifler,
      "gunluk_kayitlar": st.session_state.gunluk_kayitlar,
      "aktivite_loglari": st.session_state.aktivite_loglari,
      "profil": st.session_state.profil,
  }
  with open(user_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# ----------------------------------------------------
# 1. OTURUM KONTROLÜ VE GİRİŞ / KAYIT EKRANI (LANDING PAGE)
# ----------------------------------------------------
if "giris_yapildi" not in st.session_state:
  st.session_state.giris_yapildi = False
if "aktif_kullanici" not in st.session_state:
  st.session_state.aktif_kullanici = ""

if not st.session_state.giris_yapildi:
  col_img1, col_img2, col_img3 = st.columns([3.2, 0.9, 3.2])
  with col_img2:
    if os.path.exists(AMBLEM_PATH):
      st.image(AMBLEM_PATH, use_container_width=True)

  st.markdown(
      """
        <div style="max-width: 740px; margin: 0 auto; padding: 0px 15px; margin-bottom: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 42px; font-weight: 700; color: #ffffff; margin-bottom: 10px; padding: 0 4px;">
                <span>N</span>
                <span>O</span>
                <span>V</span>
                <span>A</span>
            </div>
            <p style="font-size: 13px; line-height: 1.7; color: #9da8b5; font-family: 'Playfair Display', Georgia, serif; font-style: italic; text-align: justify; font-weight: 400; margin: 0;">
                Gökyüzünün derinliklerinde aniden parlayan bir yıldız gibidir dönüşüm... Karanlık suları aşan bir kuğunun asil zarafeti, pırlanta gibi parlayan yeni bir yaşam iradesiyle buluşur. Nova; kendi potansiyeline uyanmak, bedenine hak ettiği değeri vermek ve her gün biraz daha parlayarak kendi en büyüleyici versiyonunu baştan yaratmak isteyenlerin sığınağıdır. Işıltınla parlamaya hazır mısın?
            </p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  tab_giris, tab_kayit = st.tabs(["Giriş Yap", "Yeni Hesap Oluştur"])
  users = kullanicilari_yukle()

  with tab_giris:
    st.subheader("Hesabınıza Giriş Yapın")
    g_user = st.text_input("Kullanıcı Adı", key="g_user").strip().lower()
    g_pass = st.text_input("Şifre", type="password", key="g_pass")

    if st.button("Giriş Yap", key="btn_giris"):
      if g_user in users and users[g_user] == sifre_hashle(g_pass):
        st.session_state.giris_yapildi = True
        st.session_state.aktif_kullanici = g_user

        u_data = verileri_yukle(g_user)
        st.session_state.besin_veritabani = u_data["besin_veritabani"]
        st.session_state.hazir_tarifler = u_data["hazir_tarifler"]
        st.session_state.gunluk_kayitlar = u_data["gunluk_kayitlar"]
        st.session_state.aktivite_loglari = u_data["aktivite_loglari"]
        st.session_state.profil = u_data["profil"]

        st.success(f"Hoş geldin, {g_user.title()}!")
        st.rerun()
      else:
        st.error("Kullanıcı adı veya şifre hatalı!")

  with tab_kayit:
    st.subheader("Yeni Nova Hesabı Oluştur")
    k_user = st.text_input("Yeni Kullanıcı Adı", key="k_user").strip().lower()
    k_pass = st.text_input("Şifre Oluştur", type="password", key="k_pass")
    k_pass_repeat = st.text_input(
        "Şifreyi Tekrar Girin", type="password", key="k_pass_rep"
    )

    if st.button("Kayıt Ol", key="btn_kayit"):
      if not k_user or not k_pass:
        st.warning("Lütfen kullanıcı adı ve şifre belirleyin.")
      elif k_pass != k_pass_repeat:
        st.error("Şifreler birbiriyle eşleşmiyor.")
      elif k_user in users:
        st.error(
            "Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı"
            " seçin."
        )
      else:
        users[k_user] = sifre_hashle(k_pass)
        kullanicilari_kaydet(users)
        st.success(
            "Hesabınız başarıyla oluşturuldu! Şimdi 'Giriş Yap' sekmesinden"
            " giriş yapabilirsiniz."
        )

else:
  # ----------------------------------------------------
  # 2. ANA UYGULAMA PANELİ (Giriş Yapılmış Halde)
  # ----------------------------------------------------
  aktif_user = st.session_state.aktif_kullanici

  # Büyütülmüş ve Yaygın (Letter-Spacing Yüksek) Sol Menü N O V A Başlığı
  st.sidebar.markdown(
      """
      <h1 style="font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 38px; font-weight: 700; letter-spacing: 14px; text-align: center; color: #ffffff; margin-top: 10px; margin-bottom: 20px;">
          N O V A
      </h1>
  """,
      unsafe_allow_html=True,
  )

  # Ortalanmış Kuğu Amblemi ve Kullanıcı Adı
  c_mid1, c_mid2, c_mid3 = st.sidebar.columns([1, 1.2, 1])
  with c_mid2:
    if os.path.exists(AMBLEM_PATH):
      st.image(AMBLEM_PATH, use_container_width=True)

  st.sidebar.markdown(
      f"""
      <div class="sidebar-user-card">
          <div class="sidebar-user-name">{aktif_user.title()}</div>
      </div>
  """,
      unsafe_allow_html=True,
  )

  if st.sidebar.button("Çıkış Yap", use_container_width=True):
    st.session_state.giris_yapildi = False
    st.session_state.aktif_kullanici = ""
    st.rerun()

  st.sidebar.divider()

  menu = st.sidebar.selectbox(
      "Navigasyon Menüsü",
      [
          "Günlük Takip Paneli",
          "Haftalık Program & Değerlendirme",
          "Tarif & Malzeme Yönetimi",
          "Hedef & Kilo Analiz Sihirbazı",
      ],
  )

  # ----------------------------------------------------
  # GÜNLÜK TAKİP PANELİ
  # ----------------------------------------------------
  if menu == "Günlük Takip Paneli":
    c_title1, c_title2 = st.columns([1, 15])
    with c_title1:
      if os.path.exists(AMBLEM_PATH):
        st.image(AMBLEM_PATH, width=50)
    with c_title2:
      st.header(f"Günlük Beslenme ve Aktivite — {aktif_user.title()}")

    secilen_tarih = str(st.date_input("Kayıt Tarihi", datetime.date.today()))

    if secilen_tarih not in st.session_state.aktivite_loglari:
      st.session_state.aktivite_loglari[secilen_tarih] = {
          "adim": 10000,
          "su": 2.0,
          "pilates_tur": "Mat Pilates",
          "pilates_sure": 45,
          "yuruyus_tur": "Orta Tempo (5 km/s)",
          "yuruyus_sure": 30,
      }

    col1, col2 = st.columns(2)

    with col1:
      st.subheader("Öğün Girişi")
      ogun_turu = st.selectbox(
          "Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"]
      )
      secilen_tarif = st.selectbox(
          "Mevcut Tarifler", list(st.session_state.hazir_tarifler.keys())
      )

      if st.button("Öğüne Ekle"):
        malzemeler = st.session_state.hazir_tarifler[secilen_tarif]
        t_kalori, t_protein, t_karb, t_yag = 0, 0, 0, 0
        detaylar = []

        for m, gram in malzemeler.items():
          if m in st.session_state.besin_veritabani:
            b = st.session_state.besin_veritabani[m]
            oran = gram / 100.0
            t_kalori += b["kalori"] * oran
            t_protein += b["protein"] * oran
            t_karb += b["karb"] * oran
            t_yag += b["yag"] * oran
            detaylar.append(f"{gram}g {m}")

        st.session_state.gunluk_kayitlar.append({
            "Tarih": secilen_tarih,
            "Öğün": ogun_turu,
            "Tarif": secilen_tarif,
            "İçerik": ", ".join(detaylar),
            "Kalori": round(t_kalori, 1),
            "Protein": round(t_protein, 1),
            "Karbonhidrat": round(t_karb, 1),
            "Yağ": round(t_yag, 1),
        })
        verileri_kaydet(aktif_user)
        st.success(f"'{secilen_tarif}' öğüne eklendi.")

    with col2:
      st.subheader("Günlük Aktivite ve Hareket")
      curr_aktivite = st.session_state.aktivite_loglari[secilen_tarih]

      adim_sayisi = st.number_input(
          "Günlük Adım Sayısı",
          min_value=0,
          max_value=60000,
          value=int(curr_aktivite["adim"]),
          step=500,
      )
      su_miktari = st.slider(
          "Su Tüketimi (Litre)", 0.0, 5.0, float(curr_aktivite["su"]), 0.5
      )

      pilates_secenekleri = [
          "Mat Pilates",
          "Reformer Pilates",
          "Yoğun / Klinik Pilates",
      ]
      p_tur_idx = (
          pilates_secenekleri.index(curr_aktivite["pilates_tur"])
          if curr_aktivite["pilates_tur"] in pilates_secenekleri
          else 0
      )
      p_tur = st.selectbox(
          "Pilates Türü", pilates_secenekleri, index=p_tur_idx
      )
      p_sure = st.number_input(
          "Pilates Süresi (Dakika)",
          min_value=0,
          value=int(curr_aktivite["pilates_sure"]),
          step=5,
      )

      yuruyus_secenekleri = [
          "Hafif Tempo (4 km/s)",
          "Orta Tempo (5 km/s)",
          "Tempolu / Eğimli (6.5 km/s)",
      ]
      y_tur_idx = (
          yuruyus_secenekleri.index(curr_aktivite["yuruyus_tur"])
          if curr_aktivite["yuruyus_tur"] in yuruyus_secenekleri
          else 0
      )
      y_tur = st.selectbox(
          "Yürüyüş Temposu", yuruyus_secenekleri, index=y_tur_idx
      )
      y_sure = st.number_input(
          "Yürüyüş Süresi (Dakika)",
          min_value=0,
          value=int(curr_aktivite["yuruyus_sure"]),
          step=5,
      )

      if st.button("Aktiviteleri Güncelle"):
        st.session_state.aktivite_loglari[secilen_tarih] = {
            "adim": adim_sayisi,
            "su": su_miktari,
            "pilates_tur": p_tur,
            "pilates_sure": p_sure,
            "yuruyus_tur": y_tur,
            "yuruyus_sure": y_sure,
        }
        verileri_kaydet(aktif_user)
        st.success("Aktivite bilgileri kaydedildi.")

    st.markdown("---")
    st.subheader("Günlük Genel Denge ve Özet")

    kilo_val = st.session_state.profil["mevcut_kilo"]
    boy_val = st.session_state.profil["boy"]
    yas_val = st.session_state.profil["yas"]
    cins_val = st.session_state.profil["cinsiyet"]

    if cins_val == "Kadın":
      bmr = (10 * kilo_val) + (6.25 * boy_val) - (5 * yas_val) - 161
    else:
      bmr = (10 * kilo_val) + (6.25 * boy_val) - (5 * yas_val) + 5

    met_p = {
        "Mat Pilates": 3.0,
        "Reformer Pilates": 4.0,
        "Yoğun / Klinik Pilates": 5.0,
    }
    met_y = {
        "Hafif Tempo (4 km/s)": 2.9,
        "Orta Tempo (5 km/s)": 3.5,
        "Tempolu / Eğimli (6.5 km/s)": 5.0,
    }

    aktivite_guncel = st.session_state.aktivite_loglari[secilen_tarih]
    pilates_kalori = (
        met_p.get(aktivite_guncel["pilates_tur"], 3.0) * 3.5 * kilo_val / 200
    ) * aktivite_guncel["pilates_sure"]
    yuruyus_kalori = (
        met_y.get(aktivite_guncel["yuruyus_tur"], 3.5) * 3.5 * kilo_val / 200
    ) * aktivite_guncel["yuruyus_sure"]
    adim_kalorisi = (aktivite_guncel["adim"] / 1000) * 40

    toplam_harcanan = bmr + pilates_kalori + yuruyus_kalori + adim_kalorisi

    df_tum = (
        pd.DataFrame(st.session_state.gunluk_kayitlar)
        if st.session_state.gunluk_kayitlar
        else pd.DataFrame()
    )
    if not df_tum.empty and "Tarih" in df_tum.columns:
      df_bugun = df_tum[df_tum["Tarih"] == secilen_tarih]
      toplam_alinan = df_bugun["Kalori"].sum() if not df_bugun.empty else 0.0
      toplam_protein = df_bugun["Protein"].sum() if not df_bugun.empty else 0.0
      toplam_karb = (
          df_bugun["Karbonhidrat"].sum() if not df_bugun.empty else 0.0
      )
      toplam_yag = df_bugun["Yağ"].sum() if not df_bugun.empty else 0.0

      st.dataframe(
          df_bugun[[
              "Öğün",
              "Tarif",
              "İçerik",
              "Kalori",
              "Protein",
              "Karbonhidrat",
              "Yağ",
          ]],
          use_container_width=True,
      )
    else:
      toplam_alinan, toplam_protein, toplam_karb, toplam_yag = 0.0, 0.0, 0.0, 0.0
      st.info("Bugün için henüz öğün kaydı girilmedi.")

    net_fark = toplam_alinan - toplam_harcanan

    # Lüks Cam Efektli Metrik Kartlar
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Alınan Kalori", f"{toplam_alinan:.1f} kcal")
    c_m2.metric("Harcanan Kalori", f"{toplam_harcanan:.1f} kcal")
    c_m3.metric("Net Kalori Dengesi", f"{net_fark:+.1f} kcal")
    c_m4.metric("Su Tüketimi", f"{aktivite_guncel['su']} Liter")

    # Alt Kısım Şık Makro ve Adım Özet Çubuğu
    st.markdown(
        f"""
        <div class="nova-summary-card">
            <span>✨ <strong>Makro Dağılımı:</strong> Protein: <strong>{toplam_protein:.1f}g</strong> | Karbonhidrat: <strong>{toplam_karb:.1f}g</strong> | Yağ: <strong>{toplam_yag:.1f}g</strong></span>
            <span>👟 <strong>Adım Hedefi:</strong> <strong>{aktivite_guncel['adim']} adım</strong></span>
        </div>
    """,
        unsafe_allow_html=True,
    )

  # ----------------------------------------------------
  # HAFTALIK PROGRAM & DEĞERLENDİRME
  # ----------------------------------------------------
  elif menu == "Haftalık Program & Değerlendirme":
    st.header("Haftalık Program ve Kalori Değerlendirmesi")

    if st.session_state.gunluk_kayitlar:
      df_tum = pd.DataFrame(st.session_state.gunluk_kayitlar)
      haftalik_ozet = (
          df_tum.groupby("Tarih")[["Kalori", "Protein", "Karbonhidrat", "Yağ"]]
          .sum()
          .reset_index()
      )
      haftalik_ozet = haftalik_ozet.sort_values("Tarih", ascending=False)

      st.subheader("Gün Bazlı Geçmiş Dökümü")
      st.dataframe(haftalik_ozet, use_container_width=True)

      st.subheader("Haftalık Kalori Trendi")
      st.line_chart(haftalik_ozet.set_index("Tarih")["Kalori"])

      ortalama_kalori = haftalik_ozet["Kalori"].mean()
      hedef_k = st.session_state.profil["hedef_kalori"]

      st.markdown(
          f"**Haftalık Ortalama Alınan Kalori:** {ortalama_kalori:.1f} kcal"
          f" (Hedef: {hedef_k} kcal)"
      )
      if ortalama_kalori > hedef_k:
        st.warning("Haftalık ortalamanız hedef kalorinin üzerinde.")
      else:
        st.success("Haftalık ortalamanız hedef aralığında.")
    else:
      st.info("Değerlendirme yapabilmek için günlük kayıtlar eklemelisiniz.")

  # ----------------------------------------------------
  # TARİF & MALZEME YÖNETİMİ
  # ----------------------------------------------------
  elif menu == "Tarif & Malzeme Yönetimi":
    st.header("Tarif ve Malzeme Yönetim Paneli")

    tab1, tab2 = st.tabs(
        ["1. Yeni Malzeme Ekle", "2. Gramaj Esaslı Yeni Tarif Oluştur"]
    )

    with tab1:
      st.subheader("Veritabanına Yeni Malzeme Tanımla (100g / ml Başına)")
      m_ad = st.text_input("Malzeme Adı (Örn: Lor Peyniri, Yulaf vb.)")
      m_kal = st.number_input(
          "100 gramdaki Kalori (kcal)", min_value=0.0, value=100.0, step=5.0
      )
      m_pro = st.number_input(
          "100 gramdaki Protein (g)", min_value=0.0, value=10.0, step=1.0
      )
      m_kar = st.number_input(
          "100 gramdaki Karbonhidrat (g)", min_value=0.0, value=5.0, step=1.0
      )
      m_yag = st.number_input(
          "100 gramdaki Yağ (g)", min_value=0.0, value=3.0, step=1.0
      )

      if st.button("Malzemeyi Veritabanına Kaydet"):
        if m_ad.strip():
          temiz_ad = m_ad.strip().lower()
          st.session_state.besin_veritabani[temiz_ad] = {
              "kalori": m_kal,
              "protein": m_pro,
              "karb": m_kar,
              "yag": m_yag,
          }
          verileri_kaydet(aktif_user)
          st.success(f"'{m_ad}' başarıyla veritabanınıza eklendi!")
        else:
          st.warning("Lütfen geçerli bir malzeme adı girin.")

      st.markdown("---")
      st.subheader("Mevcut Malzeme Listesi")
      df_malzeme = pd.DataFrame([
          {
              "Malzeme Adı": k,
              "Kalori (100g)": v["kalori"],
              "Protein (g)": v["protein"],
              "Karb (g)": v["karb"],
              "Yağ (g)": v["yag"],
          }
          for k, v in st.session_state.besin_veritabani.items()
      ])
      st.dataframe(df_malzeme, use_container_width=True)

    with tab2:
      st.subheader("Gramaj Esaslı Yeni Tarif / Yemek Oluştur")
      t_ad = st.text_input("Tarif / Yemek Adı (Örn: Omlet, Yulaf Lapası vb.)")

      secilen_malzemeler = st.multiselect(
          "Tarifte Kullanılacak Malzemeleri Seç",
          list(st.session_state.besin_veritabani.keys()),
      )

      tarif_gramajlari = {}
      if secilen_malzemeler:
        st.markdown("**Seçilen Malzemelerin Miktarları (Gram / ml):**")
        for m in secilen_malzemeler:
          gr = st.number_input(
              f"{m.title()} kaç gram/ml?",
              min_value=1.0,
              value=100.0,
              step=5.0,
              key=f"gram_{m}",
          )
          tarif_gramajlari[m] = gr

      if st.button("Bu Tarifi Kütüphaneye Kaydet"):
        if t_ad.strip() and tarif_gramajlari:
          st.session_state.hazir_tarifler[t_ad.strip()] = tarif_gramajlari
          verileri_kaydet(aktif_user)
          st.success(f"'{t_ad}' tarifi kütüphanenize kaydedildi!")
        else:
          st.warning("Lütfen tarif adı yazın ve en az bir malzeme seçin.")

      st.markdown("---")
      st.subheader("Kayıtlı Tarifleriniz")
      for tarif_adi, icerik in st.session_state.hazir_tarifler.items():
        detay_str = ", ".join(
            [f"{gr}g {malzeme}" for malzeme, gr in icerik.items()]
        )
        st.write(f"🔹 **{tarif_adi}**: {detay_str}")

  # ----------------------------------------------------
  # HEDEF & KİLO ANALİZ SİHİRBAZI
  # ----------------------------------------------------
  elif menu == "Hedef & Kilo Analiz Sihirbazı":
    st.header("Kişiselleştirilmiş Hedef, Kilo ve Kalori Açığı Sihirbazı")

    p = st.session_state.profil

    c1, c2, c3 = st.columns(3)
    cinsiyet = c1.selectbox(
        "Cinsiyet",
        ["Kadın", "Erkek"],
        index=0 if p["cinsiyet"] == "Kadın" else 1,
    )
    yas = c2.number_input(
        "Yaş", min_value=15, max_value=80, value=int(p["yas"])
    )
    boy = c3.number_input(
        "Boy (cm)", min_value=120, max_value=210, value=int(p["boy"])
    )

    c4, c5 = st.columns(2)
    mevcut_kilo = c4.number_input(
        "Mevcut Kilon (kg)",
        min_value=35.0,
        max_value=160.0,
        value=float(p["mevcut_kilo"]),
        step=0.5,
    )
    hedef_kilo = c5.number_input(
        "Hedeflenen Kilon (kg)",
        min_value=30.0,
        max_value=150.0,
        value=float(p["hedef_kilo"]),
        step=0.5,
    )

    aktivite = st.selectbox(
        "Aktivite Düzeyi",
        [
            "Hareketsiz / Masa Başı",
            "Hafif Aktif (Haftada 1-3 gün)",
            "Orta Aktif (Haftada 3-5 gün)",
            "Çok Aktif",
        ],
    )

    if st.button("Hedeflerimi ve Süreyi Hesapla"):
      if cinsiyet == "Kadın":
        bmr = (10 * mevcut_kilo) + (6.25 * boy) - (5 * yas) - 161
      else:
        bmr = (10 * mevcut_kilo) + (6.25 * boy) - (5 * yas) + 5

      carpanlar = {
          "Hareketsiz / Masa Başı": 1.2,
          "Hafif Aktif (Haftada 1-3 gün)": 1.375,
          "Orta Aktif (Haftada 3-5 gün)": 1.55,
          "Çok Aktif": 1.725,
      }

      tdee = bmr * carpanlar[aktivite]
      kilo_farki = mevcut_kilo - hedef_kilo

      st.session_state.profil["cinsiyet"] = cinsiyet
      st.session_state.profil["yas"] = yas
      st.session_state.profil["boy"] = boy
      st.session_state.profil["mevcut_kilo"] = mevcut_kilo
      st.session_state.profil["hedef_kilo"] = hedef_kilo

      if kilo_farki > 0:
        hedef_kalori = tdee - 500
        st.session_state.profil["hedef_kalori"] = round(hedef_kalori)

        toplam_yakilacak_yag_kcal = kilo_farki * 7700
        tahmini_gun = toplam_yakilacak_yag_kcal / 500
        tahmini_hafta = tahmini_gun / 7

        st.success("Hedefleriniz başarıyla hesaplandı ve kaydedildi!")
        st.markdown("---")
        st.subheader("📊 Analiz ve Tahmin Sonuçları")
        st.metric("Mevcut Kilo", f"{mevcut_kilo} kg")
        st.metric("Hedef Kilo", f"{hedef_kilo} kg")
        st.metric("Kilo Farkı", f"-{kilo_farki:.1f} kg (Verilmesi Gereken)")
        st.metric(
            "Günlük Harcanan Toplam Enerji (TDEE)", f"{round(tdee)} kcal"
        )
        st.metric("Önerilen Günlük Kalori Alımı", f"{round(hedef_kalori)} kcal")
        st.markdown(
            "💡 **Kalori Açığı:** Kilo verebilmek için günlük harcamanızın"
            f" altında, **{round(hedef_kalori)} kcal** beslenmeli ve günde"
            " yaklaşık **500 kcal açık** oluşturmalısınız."
        )
        st.markdown(
            "⏱️ **Tahmini Süre:** Haftada ortalama 0.5 kg vererek bu hedefe"
            f" **yaklaşık {tahmini_hafta:.1f} haftada (yaklaşık"
            f" {round(tahmini_gun)} günde)** ulaşabilirsiniz."
        )

      elif kilo_farki < 0:
        hedef_kalori = tdee + 300
        st.session_state.profil["hedef_kalori"] = round(hedef_kalori)

        tahmini_gun = abs(kilo_farki * 7700) / 300
        tahmini_hafta = tahmini_gun / 7

        st.success("Hedefleriniz başarıyla hesaplandı ve kaydedildi!")
        st.markdown("---")
        st.subheader("📊 Analiz ve Tahmin Sonuçları")
        st.metric("Mevcut Kilo", f"{mevcut_kilo} kg")
        st.metric("Hedef Kilo", f"{hedef_kilo} kg")
        st.metric("Kilo Farkı", f"+{abs(kilo_farki):.1f} kg (Alınması Gereken)")
        st.metric(
            "Günlük Harcanan Toplam Enerji (TDEE)", f"{round(tdee)} kcal"
        )
        st.metric("Önerilen Günlük Kalori Alımı", f"{round(hedef_kalori)} kcal")
        st.markdown(
            "💡 **Kalori Fazlası:** Kilo alabilmek için günlük harcamanızın"
            " üzerinde, günde yaklaşık **300 kcal fazlalık** oluşturmalısınız."
        )
        st.markdown(
            f"⏱️ **Tahmini Süre:** Bu hedefe **yaklaşık {tahmini_hafta:.1f}"
            f" haftada (yaklaşık {round(tahmini_gun)} günde)** ulaşabilirsiniz."
        )
      else:
        st.session_state.profil["hedef_kalori"] = round(tdee)
        st.success(
            "Mevcut kilonuz ve hedef kilonuz aynı! Kilonuzu korumak için"
            " günlük kalori hedefiniz TDEE ile aynı ayarlandı."
        )

      st.session_state.profil["hedef_protein"] = round(
          (st.session_state.profil["hedef_kalori"] * 0.20) / 4
      )
      st.session_state.profil["hedef_karb"] = round(
          (st.session_state.profil["hedef_kalori"] * 0.50) / 4
      )
      st.session_state.profil["hedef_yag"] = round(
          (st.session_state.profil["hedef_kalori"] * 0.30) / 9
      )
      verileri_kaydet(aktif_user)
