import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(page_title="Diyet ve Aktivite Asistanı", layout="wide", initial_sidebar_state="expanded")

DATA_FILE = "diyet_verileri_kalici.json"

# Kalıcı Veri Saklama ve Yükleme Mekanizması
def verileri_yukle():
    default_data = {
        "besin_veritabani": {
            "tavuk gogsu": {"kalori": 165, "protein": 31.0, "karb": 0.0, "yag": 3.6},
            "kofte": {"kalori": 220, "protein": 24.0, "karb": 2.0, "yag": 13.0},
            "ton baligi": {"kalori": 110, "protein": 25.0, "karb": 0.0, "yag": 1.0},
            "marul": {"kalori": 15, "protein": 1.4, "karb": 2.9, "yag": 0.2},
            "salatalik": {"kalori": 15, "protein": 0.7, "karb": 3.6, "yag": 0.1},
            "domates": {"kalori": 18, "protein": 0.9, "karb": 3.9, "yag": 0.2},
            "zeytinyagi": {"kalori": 884, "protein": 0.0, "karb": 0.0, "yag": 100.0},
            "dilim peynir": {"kalori": 320, "protein": 22.0, "karb": 1.5, "yag": 25.0},
            "tam bugday ekmegi": {"kalori": 247, "protein": 13.0, "karb": 41.0, "yag": 3.4},
            "labne": {"kalori": 210, "protein": 6.0, "karb": 4.0, "yag": 20.0},
            "sut": {"kalori": 50, "protein": 3.4, "karb": 4.8, "yag": 1.5},
            "kahve": {"kalori": 2, "protein": 0.1, "karb": 0.3, "yag": 0.0},
            "kefir": {"kalori": 60, "protein": 3.5, "karb": 4.5, "yag": 3.0},
            "x-lim toz": {"kalori": 20, "protein": 0.0, "karb": 5.0, "yag": 0.0},
            "badem": {"kalori": 575, "protein": 21.0, "karb": 22.0, "yag": 49.0},
            "mandalina": {"kalori": 53, "protein": 0.8, "karb": 13.3, "yag": 0.3},
            "meyveli soda": {"kalori": 45, "protein": 0.0, "karb": 11.0, "yag": 0.0}
        },
        "hazir_tarifler": {
            "Tavuklu Salata": {"tavuk gogsu": 200, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Köfteli Salata": {"kofte": 150, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Ton Balıklı Salata": {"ton baligi": 110, "marul": 30, "domates": 100, "salatalik": 100, "zeytinyagi": 10, "dilim peynir": 30, "tam bugday ekmegi": 25, "labne": 15},
            "Latte (Orta Boy)": {"sut": 250, "kahve": 30},
            "Americano (Orta Boy)": {"kahve": 20},
            "Kefir Karışımı": {"kefir": 200, "x-lim toz": 5},
            "Badem (1 Avuç)": {"badem": 30},
            "Mandalina (3 Adet)": {"mandalina": 300},
            "Meyveli Soda": {"meyveli soda": 200}
        },
        "gunluk_kayitlar": [],
        "aktivite_loglari": {},
        "profil": {
            "cinsiyet": "Kadın", "yas": 20, "boy": 165, "mevcut_kilo": 58.0, "hedef_kilo": 55.0, 
            "hedef_kalori": 1800, "hedef_protein": 90, "hedef_karb": 200, "hedef_yag": 60
        }
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "hedef_kilo" not in data.get("profil", {}):
                    data["profil"]["hedef_kilo"] = 55.0
                if "mevcut_kilo" not in data.get("profil", {}) and "kilo" in data.get("profil", {}):
                    data["profil"]["mevcut_kilo"] = data["profil"]["kilo"]
                return data
        except:
            return default_data
    return default_data

def verileri_kaydet():
    data = {
        "besin_veritabani": st.session_state.besin_veritabani,
        "hazir_tarifler": st.session_state.hazir_tarifler,
        "gunluk_kayitlar": st.session_state.gunluk_kayitlar,
        "aktivite_loglari": st.session_state.aktivite_loglari,
        "profil": st.session_state.profil
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

loaded_data = verileri_yukle()
if "besin_veritabani" not in st.session_state:
    st.session_state.besin_veritabani = loaded_data["besin_veritabani"]
if "hazir_tarifler" not in st.session_state:
    st.session_state.hazir_tarifler = loaded_data["hazir_tarifler"]
if "gunluk_kayitlar" not in st.session_state:
    st.session_state.gunluk_kayitlar = loaded_data["gunluk_kayitlar"]
if "aktivite_loglari" not in st.session_state:
    st.session_state.aktivite_loglari = loaded_data.get("aktivite_loglari", {})
if "profil" not in st.session_state:
    st.session_state.profil = loaded_data["profil"]

st.title("Diyet ve Aktivite Asistanı")

menu = st.sidebar.selectbox(
    "Menü", 
    [
        "Günlük Takip Paneli", 
        "Haftalık Program & Değerlendirme", 
        "Tarif & Malzeme Yönetimi", 
        "Hedef & Kilo Analiz Sihirbazı"
    ]
)

# ----------------------------------------------------
# 1. GÜNLÜK TAKİP PANELİ
# ----------------------------------------------------
if menu == "Günlük Takip Paneli":
    st.header("Günlük Beslenme ve Aktivite Takip Paneli")
    
    secilen_tarih = str(st.date_input("Kayıt Tarihi", datetime.date.today()))
    
    if secilen_tarih not in st.session_state.aktivite_loglari:
        st.session_state.aktivite_loglari[secilen_tarih] = {
            "adim": 10000, "su": 2.0, "pilates_tur": "Mat Pilates", "pilates_sure": 45,
            "yuruyus_tur": "Orta Tempo (5 km/s)", "yuruyus_sure": 30
        }

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Öğün Girişi")
        ogun_turu = st.selectbox("Öğün Türü", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"])
        secilen_tarif = st.selectbox("Mevcut Tarifler", list(st.session_state.hazir_tarifler.keys()))
        
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
                "Yağ": round(t_yag, 1)
            })
            verileri_kaydet()
            st.success(f"'{secilen_tarif}' öğüne eklendi.")

    with col2:
        st.subheader("Günlük Aktivite ve Hareket")
        curr_aktivite = st.session_state.aktivite_loglari[secilen_tarih]
        
        adim_sayisi = st.number_input("Günlük Adım Sayısı", min_value=0, max_value=60000, value=int(curr_aktivite["adim"]), step=500)
        su_miktari = st.slider("Su Tüketimi (Litre)", 0.0, 5.0, float(curr_aktivite["su"]), 0.5)
        
        pilates_secenekleri = ["Mat Pilates", "Reformer Pilates", "Yoğun / Klinik Pilates"]
        p_tur_idx = pilates_secenekleri.index(curr_aktivite["pilates_tur"]) if curr_aktivite["pilates_tur"] in pilates_secenekleri else 0
        p_tur = st.selectbox("Pilates Türü", pilates_secenekleri, index=p_tur_idx)
        p_sure = st.number_input("Pilates Süresi (Dakika)", min_value=0, value=int(curr_aktivite["pilates_sure"]), step=5)
        
        yuruyus_secenekleri = ["Hafif Tempo (4 km/s)", "Orta Tempo (5 km/s)", "Tempolu / Eğimli (6.5 km/s)"]
        y_tur_idx = yuruyus_secenekleri.index(curr_aktivite["yuruyus_tur"]) if curr_aktivite["yuruyus_tur"] in yuruyus_secenekleri else 0
        y_tur = st.selectbox("Yürüyüş Temposu", yuruyus_secenekleri, index=y_tur_idx)
        y_sure = st.number_input("Yürüyüş Süresi (Dakika)", min_value=0, value=int(curr_aktivite["yuruyus_sure"]), step=5)
        
        if st.button("Aktiviteleri Güncelle"):
            st.session_state.aktivite_loglari[secilen_tarih] = {
                "adim": adim_sayisi, "su": su_miktari, "pilates_tur": p_tur, 
                "pilates_sure": p_sure, "yuruyus_tur": y_tur, "yuruyus_sure": y_sure
            }
            verileri_kaydet()
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
        
    met_p = {"Mat Pilates": 3.0, "Reformer Pilates": 4.0, "Yoğun / Klinik Pilates": 5.0}
    met_y = {"Hafif Tempo (4 km/s)": 2.9, "Orta Tempo (5 km/s)": 3.5, "Tempolu / Eğimli (6.5 km/s)": 5.0}
    
    aktivite_guncel = st.session_state.aktivite_loglari[secilen_tarih]
    pilates_kalori = (met_p.get(aktivite_guncel["pilates_tur"], 3.0) * 3.5 * kilo_val / 200) * aktivite_guncel["pilates_sure"]
    yuruyus_kalori = (met_y.get(aktivite_guncel["yuruyus_tur"], 3.5) * 3.5 * kilo_val / 200) * aktivite_guncel["yuruyus_sure"]
    adim_kalorisi = (aktivite_guncel["adim"] / 1000) * 40
    
    toplam_harcanan = bmr + pilates_kalori + yuruyus_kalori + adim_kalorisi
    
    df_tum = pd.DataFrame(st.session_state.gunluk_kayitlar) if st.session_state.gunluk_kayitlar else pd.DataFrame()
    if not df_tum.empty and "Tarih" in df_tum.columns:
        df_bugun = df_tum[df_tum["Tarih"] == secilen_tarih]
        toplam_alinan = df_bugun["Kalori"].sum() if not df_bugun.empty else 0.0
        toplam_protein = df_bugun["Protein"].sum() if not df_bugun.empty else 0.0
        toplam_karb = df_bugun["Karbonhidrat"].sum() if not df_bugun.empty else 0.0
        toplam_yag = df_bugun["Yağ"].sum() if not df_bugun.empty else 0.0
        
        st.dataframe(df_bugun[["Öğün", "Tarif", "İçerik", "Kalori", "Protein", "Karbonhidrat", "Yağ"]], use_container_width=True)
    else:
        toplam_alinan, toplam_protein, toplam_karb, toplam_yag = 0.0, 0.0, 0.0, 0.0
        st.info("Bugün için henüz öğün kaydı girilmedi.")

    net_fark = toplam_alinan - toplam_harcanan
    
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Alınan Kalori", f"{toplam_alinan:.1f} kcal")
    c_m2.metric("Harcanan Kalori", f"{toplam_harcanan:.1f} kcal")
    c_m3.metric("Net Kalori Dengesi", f"{net_fark:+.1f} kcal")
    c_m4.metric("Su Tüketimi", f"{aktivite_guncel['su']} Litre")
    
    st.write(f"Makro Dağılımı -> Protein: **{toplam_protein:.1f}g** | Karbonhidrat: **{toplam_karb:.1f}g** | Yağ: **{toplam_yag:.1f}g** | Adım: **{aktivite_guncel['adim']} adım**")

# ----------------------------------------------------
# 2. HAFTALIK PROGRAM & DEĞERLENDİRME
# ----------------------------------------------------
elif menu == "Haftalık Program & Değerlendirme":
    st.header("Haftalık Program ve Kalori Değerlendirmesi")
    
    if st.session_state.gunluk_kayitlar:
        df_tum = pd.DataFrame(st.session_state.gunluk_kayitlar)
        haftalik_ozet = df_tum.groupby("Tarih")[["Kalori", "Protein", "Karbonhidrat", "Yağ"]].sum().reset_index()
        haftalik_ozet = haftalik_ozet.sort_values("Tarih", ascending=False)
        
        st.subheader("Gün Bazlı Geçmiş Dökümü")
        st.dataframe(haftalik_ozet, use_container_width=True)
        
        st.subheader("Haftalık Kalori Trendi")
        st.line_chart(haftalik_ozet.set_index("Tarih")["Kalori"])
        
        ortalama_kalori = haftalik_ozet["Kalori"].mean()
        hedef_k = st.session_state.profil["hedef_kalori"]
        
        st.markdown(f"**Haftalık Ortalama Alınan Kalori:** {ortalama_kalori:.1f} kcal (Hedef: {hedef_k} kcal)")
        if ortalama_kalori > hedef_k:
            st.warning("Haftalık ortalamanız hedef kalorinin üzerinde.")
        else:
            st.success("Haftalık ortalamanız hedef aralığında.")
    else:
        st.info("Değerlendirme yapabilmek için günlük kayıtlar eklemelisiniz.")

# ----------------------------------------------------
# 3. TARİF & MALZEME YÖNETİMİ (Kendi Kendine Ekleme Özelliği)
# ----------------------------------------------------
elif menu == "Tarif & Malzeme Yönetimi":
    st.header("Tarif ve Malzeme Yönetim Paneli")
    
    tab1, tab2 = st.tabs(["1. Yeni Malzeme Ekle", "2. Gramaj Esaslı Yeni Tarif Oluştur"])
    
    with tab1:
        st.subheader("Veritabanına Yeni Malzeme Tanımla (100g / ml Başına)")
        m_ad = st.text_input("Malzeme Adı (Örn: Lor Peyniri, Yulaf vb.)")
        m_kal = st.number_input("100 gramdaki Kalori (kcal)", min_value=0.0, value=100.0, step=5.0)
        m_pro = st.number_input("100 gramdaki Protein (g)", min_value=0.0, value=10.0, step=1.0)
        m_kar = st.number_input("100 gramdaki Karbonhidrat (g)", min_value=0.0, value=5.0, step=1.0)
        m_yag = st.number_input("100 gramdaki Yağ (g)", min_value=0.0, value=3.0, step=1.0)
        
        if st.button("Malzemeyi Veritabanına Kaydet"):
            if m_ad.strip():
                temiz_ad = m_ad.strip().lower()
                st.session_state.besin_veritabani[temiz_ad] = {
                    "kalori": m_kal, "protein": m_pro, "karb": m_kar, "yag": m_yag
                }
                verileri_kaydet()
                st.success(f"'{m_ad}' başarıyla veritabanına eklendi! Artık tariflerde kullanabilirsin.")
            else:
                st.warning("Lütfen geçerli bir malzeme adı girin.")
                
        st.markdown("---")
        st.subheader("Mevcut Malzeme Listesi")
        df_malzeme = pd.DataFrame([
            {"Malzeme Adı": k, "Kalori (100g)": v["kalori"], "Protein (g)": v["protein"], "Karb (g)": v["karb"], "Yağ (g)": v["yag"]}
            for k, v in st.session_state.besin_veritabani.items()
        ])
        st.dataframe(df_malzeme, use_container_width=True)

    with tab2:
        st.subheader("Gramaj Esaslı Yeni Tarif / Yemek Oluştur")
        t_ad = st.text_input("Tarif / Yemek Adı (Örn: Omlet, Yulaf Lapası, Özel Salata vb.)")
        
        # Kullanıcının malzemeleri tek tek seçip gramaj girmesi için dinamik alan
        secilen_malzemeler = st.multiselect("Tarifte Kullanılacak Malzemeleri Seç", list(st.session_state.besin_veritabani.keys()))
        
        tarif_gramajlari = {}
        if secilen_malzemeler:
            st.markdown("**Seçilen Malzemelerin Miktarları (Gram / ml):**")
            for m in secilen_malzemeler:
                gr = st.number_input(f"{m.title()} kaç gram/ml?", min_value=1.0, value=100.0, step=5.0, key=f"gram_{m}")
                tarif_gramajlari[m] = gr
                
        if st.button("Bu Tarifi Kütüphaneye Kaydet"):
            if t_ad.strip() and tarif_gramajlari:
                st.session_state.hazir_tarifler[t_ad.strip()] = tarif_gramajlari
                verileri_kaydet()
                st.success(f"'{t_ad}' tarifi başarıyla kaydedildi! Artık günlük öğün eklerken seçebilirsin.")
            else:
                st.warning("Lütfen tarif adı yazın ve en az bir malzeme seçip gramaj belirleyin.")
                
        st.markdown("---")
        st.subheader("Kayıtlı Tarifler ve İçerdikleri Malzemeler")
        for tarif_adi, icerik in st.session_state.hazir_tarifler.items():
            detay_str = ", ".join([f"{gr}g {malzeme}" for malzeme, gr in icerik.items()])
            st.write(f"🔹 **{tarif_adi}**: {detay_str}")

# ----------------------------------------------------
# 4. HEDEF & KİLO ANALİZ SİHİRBAZI (Mevcut vs Hedef Kilo + Kalori Açığı & Süre)
# ----------------------------------------------------
elif menu == "Hedef & Kilo Analiz Sihirbazı":
    st.header("Kişiselleştirilmiş Hedef, Kilo ve Kalori Açığı Sihirbazı")
    
    p = st.session_state.profil
    
    c1, c2, c3 = st.columns(3)
    cinsiyet = c1.selectbox("Cinsiyet", ["Kadın", "Erkek"], index=0 if p["cinsiyet"] == "Kadın" else 1)
    yas = c2.number_input("Yaş", min_value=15, max_value=80, value=int(p["yas"]))
    boy = c3.number_input("Boy (cm)", min_value=120, max_value=210, value=int(p["boy"]))
    
    c4, c5 = st.columns(2)
    mevcut_kilo = c4.number_input("Mevcut Kilon (kg)", min_value=35.0, max_value=160.0, value=float(p["mevcut_kilo"]), step=0.5)
    hedef_kilo = c5.number_input("Hedeflenen Kilon (kg)", min_value=30.0, max_value=150.0, value=float(p["hedef_kilo"]), step=0.5)
    
    aktivite = st.selectbox("Aktivite Düzeyi", ["Hareketsiz / Masa Başı", "Hafif Aktif (Haftada 1-3 gün)", "Orta Aktif (Haftada 3-5 gün)", "Çok Aktif"])

    if st.button("Hedeflerimi ve Süreyi Hesapla"):
        # BMR Hesaplama (Mifflin-St Jeor)
        if cinsiyet == "Kadın":
            bmr = (10 * mevcut_kilo) + (6.25 * boy) - (5 * yas) - 161
        else:
            bmr = (10 * mevcut_kilo) + (6.25 * boy) - (5 * yas) + 5
            
        carpanlar = {
            "Hareketsiz / Masa Başı": 1.2,
            "Hafif Aktif (Haftada 1-3 gün)": 1.375,
            "Orta Aktif (Haftada 3-5 gün)": 1.55,
            "Çok Aktif": 1.725
        }
        
        tdee = bmr * carpanlar[aktivite]
        kilo_farki = mevcut_kilo - hedef_kilo  # Pozitifse kilo verme, negatifse kilo alma hedefi
        
        st.session_state.profil["cinsiyet"] = cinsiyet
        st.session_state.profil["yas"] = yas
        st.session_state.profil["boy"] = boy
        st.session_state.profil["mevcut_kilo"] = mevcut_kilo
        st.session_state.profil["hedef_kilo"] = hedef_kilo
        
        if kilo_farki > 0:
            # Kilo verme hedefi (Sağlıklı haftalık kilo kaybı: ~0.5 kg için günlük 500 kcal açık)
            hedef_kalori = tdee - 500
            st.session_state.profil["hedef_kalori"] = round(hedef_kalori)
            
            toplam_yakilacak_ yag_kcal = kilo_farki * 7700
            tahmini_gun = toplam_yakilacak_ yag_kcal / 500
            tahmini_hafta = tahmini_gun / 7
            
            st.success("Hedefleriniz başarıyla hesaplandı ve kaydedildi!")
            st.markdown("---")
            st.subheader("📊 Analiz ve Tahmin Sonuçları")
            st.metric("Mevcut Kilo", f"{mevcut_kilo} kg")
            st.metric("Hedef Kilo", f"{hedef_kilo} kg")
            st.metric("Kilo Farkı", f"-{kilo_farki:.1f} kg (Verilmesi Gereken)")
            st.metric("Günlük Harcanan Toplam Enerji (TDEE)", f"{round(tdee)} kcal")
            st.metric("Önerilen Günlük Kalori Alımı", f"{round(hedef_kalori)} kcal")
            st.markdown(f"💡 **Kalori Açığı:** Kilo verebilmek için günlük harcamanızın altında, **{round(hedef_kalori)} kcal** beslenmeli ve günde yaklaşık **500 kcal açık** oluşturmalısınız.")
            st.markdown(f"⏱️ **Tahmini Süre:** Haftada ortalama 0.5 kg vererek bu hedefe **yaklaşık {tahmini_hafta:.1f} haftada (yaklaşık {round(tahmini_gun)} günde)** ulaşabilirsiniz.")
            
        elif kilo_farki < 0:
            # Kilo alma hedefi
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
            st.metric("Günlük Harcanan Toplam Enerji (TDEE)", f"{round(tdee)} kcal")
            st.metric("Önerilen Günlük Kalori Alımı", f"{round(hedef_kalori)} kcal")
            st.markdown(f"💡 **Kalori Fazlası:** Kilo alabilmek için günlük harcamanızın üzerinde, günde yaklaşık **300 kcal fazlalık** oluşturmalısınız.")
            st.markdown(f"⏱️ **Tahmini Süre:** Bu hedefe **yaklaşık {tahmini_hafta:.1f} haftada (yaklaşık {round(tahmini_gun)} günde)** ulaşabilirsiniz.")
        else:
            st.session_state.profil["hedef_kalori"] = round(tdee)
            st.success("Mevcut kilonuz ve hedef kilonuz aynı! Kilonuzu korumak için günlük kalori hedefiniz TDEE ile aynı ayarlandı.")
            
        st.session_state.profil["hedef_protein"] = round((st.session_state.profil["hedef_kalori"] * 0.20) / 4)
        st.session_state.profil["hedef_karb"] = round((st.session_state.profil["hedef_kalori"] * 0.50) / 4)
        st.session_state.profil["hedef_yag"] = round((st.session_state.profil["hedef_kalori"] * 0.30) / 9)
        verileri_kaydet()

    st.markdown("---")
    st.subheader("Mevcut Kayıtlı Hedef Özetiniz")
    st.write(f"Mevcut Kilo: **{st.session_state.profil['mevcut_kilo']} kg** | Hedef Kilo: **{st.session_state.profil['hedef_kilo']} kg**")
    st.write(f"Günlük Kalori Hedefi: **{st.session_state.profil['hedef_kalori']} kcal**")
    st.write(f"Önerilen Makro Dağılımı -> Protein: **{st.session_state.profil['hedef_protein']}g** | Karbonhidrat: **{st.session_state.profil['hedef_karb']}g** | Yağ: **{st.session_state.profil['hedef_yag']}g**")
