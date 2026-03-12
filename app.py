import streamlit as st
import pandas as pd

st.set_page_config(page_title="Makine Uygunluk Motoru", layout="wide")

st.title("Makine Uygunluk Karar Motoru")
st.write("Zemin ve iş bilgisine göre makine uygunluğunu değerlendirir.")

st.sidebar.header("İş Girdileri")

is_tipi = st.sidebar.selectbox("İş Tipi", ["Fore Kazık", "Ankraj"])
derinlik = st.sidebar.number_input("Derinlik (m)", min_value=0.0, value=15.0, step=1.0)
cap = st.sidebar.number_input("Çap (mm)", min_value=0, value=800, step=50)
zemin = st.sidebar.selectbox("Zemin Tipi", ["Kil", "Kum", "Kumtaşı", "Kaya"])
yeralti_suyu = st.sidebar.selectbox("Yeraltı Suyu", ["Yok", "Düşük", "Yüksek"])

makineler = pd.DataFrame([
    {
        "Makine": "Makine A",
        "İş Tipi": "Fore Kazık",
        "Max Derinlik": 20,
        "Max Çap": 1000,
        "Zemin Uygunluğu": ["Kil", "Kum", "Kumtaşı"]
    },
    {
        "Makine": "Makine B",
        "İş Tipi": "Fore Kazık",
        "Max Derinlik": 35,
        "Max Çap": 1500,
        "Zemin Uygunluğu": ["Kil", "Kum", "Kumtaşı", "Kaya"]
    },
    {
        "Makine": "Makine C",
        "İş Tipi": "Ankraj",
        "Max Derinlik": 45,
        "Max Çap": 300,
        "Zemin Uygunluğu": ["Kil", "Kum", "Kumtaşı"]
    },
    {
        "Makine": "Makine D",
        "İş Tipi": "Ankraj",
        "Max Derinlik": 60,
        "Max Çap": 400,
        "Zemin Uygunluğu": ["Kil", "Kum", "Kumtaşı", "Kaya"]
    }
])

def karar_ver(row):
    if row["İş Tipi"] != is_tipi:
        return "Uygun Değil"
    if derinlik > row["Max Derinlik"]:
        return "Uygun Değil"
    if cap > row["Max Çap"]:
        return "Uygun Değil"
    if zemin not in row["Zemin Uygunluğu"]:
        return "Riskli"
    if yeralti_suyu == "Yüksek" and zemin in ["Kum", "Kil"]:
        return "Şartlı Uygun"
    return "Uygun"

sonuc_df = makineler.copy()
sonuc_df["Karar"] = sonuc_df.apply(karar_ver, axis=1)

st.subheader("Girilen İş")
st.write({
    "İş Tipi": is_tipi,
    "Derinlik (m)": derinlik,
    "Çap (mm)": cap,
    "Zemin Tipi": zemin,
    "Yeraltı Suyu": yeralti_suyu
})

st.subheader("Makine Uygunluk Sonuçları")
st.dataframe(sonuc_df[["Makine", "İş Tipi", "Max Derinlik", "Max Çap", "Karar"]], use_container_width=True)

st.subheader("Özet")
uygunlar = sonuc_df[sonuc_df["Karar"] == "Uygun"]["Makine"].tolist()
sartli = sonuc_df[sonuc_df["Karar"] == "Şartlı Uygun"]["Makine"].tolist()
riskli = sonuc_df[sonuc_df["Karar"] == "Riskli"]["Makine"].tolist()

st.write("**Uygun makineler:**", uygunlar if uygunlar else "Yok")
st.write("**Şartlı uygun makineler:**", sartli if sartli else "Yok")
st.write("**Riskli makineler:**", riskli if riskli else "Yok")
