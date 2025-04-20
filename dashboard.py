import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


day_df = pd.read_csv('day.csv', sep=';')  
hour_df = pd.read_csv('hour.csv', sep=';')  

day_df.columns = day_df.columns.str.strip()
hour_df.columns = hour_df.columns.str.strip()


day_df['dteday'] = pd.to_datetime(day_df['dteday'], format='%d/%m/%Y')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'], format='%d/%m/%Y')


st.title("Analisis Faktor yang Mempengaruhi Penyewaan Sepeda dan Pola Penyewaan")


st.sidebar.header("Filter Data Berdasarkan Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", day_df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Selesai", day_df['dteday'].max())


start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)


filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
filtered_hour_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]


st.sidebar.write(f"Menampilkan data dari {start_date.strftime('%Y-%m-%d')} hingga {end_date.strftime('%Y-%m-%d')}")

st.sidebar.header("Filter Data Berdasarkan Jam")
hour_range = st.sidebar.slider(
    "Pilih Rentang Jam",
    min_value=0,
    max_value=23,
    value=(7, 18)  
)


filtered_hour_df = filtered_hour_df[(filtered_hour_df['hr'] >= hour_range[0]) & (filtered_hour_df['hr'] <= hour_range[1])]


st.header("Pertanyaan 1: Faktor yang Mempengaruhi Penyewaan Sepeda Setiap Bulan")

monthly_avg = filtered_day_df.groupby('mnth').agg({
    'cnt': 'mean',
    'temp': 'mean',
    'atemp': 'mean',
    'hum': 'mean',
    'windspeed': 'mean'
}).reset_index()

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
sns.lineplot(x='mnth', y='cnt', data=monthly_avg, marker='o')
plt.title('Rata-rata Penyewaan Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Penyewaan (cnt)')

plt.subplot(2, 2, 2)
sns.lineplot(x='mnth', y='temp', data=monthly_avg, marker='o')
plt.title('Rata-rata Suhu (temp) per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Suhu (temp)')

plt.subplot(2, 2, 3)
sns.lineplot(x='mnth', y='atemp', data=monthly_avg, marker='o')
plt.title('Rata-rata Suhu yang Dirasakan (atemp) per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Suhu yang Dirasakan (atemp)')

plt.subplot(2, 2, 4)
sns.lineplot(x='mnth', y='windspeed', data=monthly_avg, marker='o')
plt.title('Rata-rata Kecepatan Angin (windspeed) per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Kecepatan Angin (windspeed)')

plt.tight_layout()
st.pyplot(plt.gcf())

st.markdown("""
<div style="
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
">
    <p style="color: black;">
        <b>Analisis:</b><br>
        - <b>Penyewaan Sepeda:</b> Jumlah penyewaan sepeda cenderung meningkat pada bulan-bulan dengan suhu yang lebih hangat (misalnya, musim panas).<br>
        - <b>Suhu (temp):</b> Suhu rata-rata meningkat pada bulan-bulan pertengahan tahun (musim panas).<br>
        - <b>Suhu yang Dirasakan (atemp):</b> Pola serupa dengan suhu aktual, tetapi mungkin lebih tinggi karena faktor kelembaban.<br>
        - <b>Kecepatan Angin (windspeed):</b> Kecepatan angin cenderung stabil sepanjang tahun, dengan sedikit variasi.
    </p>
</div>
""", unsafe_allow_html=True)

st.header("Pertanyaan 2: Pola Penyewaan Sepeda Berdasarkan Hari dan Jam")

st.subheader("1. Pola Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")

weekday_avg = filtered_day_df.groupby('weekday')['cnt'].mean().reset_index()


plt.figure(figsize=(10, 5))
sns.lineplot(x='weekday', y='cnt', data=weekday_avg, marker='o')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
plt.xlabel('Hari (0=Senin, 6=Minggu)')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(ticks=[0, 1, 2, 3, 4, 5, 6], labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
st.pyplot(plt.gcf())


st.markdown("""
<div style="
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
">
    <p style="color: black;">
        <b>Analisis:</b><br>
        - Penyewaan sepeda cenderung lebih tinggi pada akhir pekan (Sabtu dan Minggu) dibandingkan hari kerja.<br>
        - Hari kerja (Senin-Jumat) menunjukkan pola penyewaan yang stabil, dengan sedikit peningkatan pada hari Jumat.
    </p>
</div>
""", unsafe_allow_html=True)


st.subheader("2. Pola Penyewaan Sepeda Berdasarkan Jam dalam Sehari")


hour_avg = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()


plt.figure(figsize=(12, 5))
sns.lineplot(x='hr', y='cnt', data=hour_avg, marker='o')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Jam dalam Sehari')
plt.xlabel('Jam')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(ticks=range(24), labels=[f'{i}:00' for i in range(24)], rotation=45)
plt.grid(True)
st.pyplot(plt.gcf())


st.markdown("""
<div style="
    background-color: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
">
    <p style="color: black;">
        <b>Analisis:</b><br>
        - Terdapat dua puncak penyewaan sepeda:<br>
          &nbsp;&nbsp;&nbsp;&nbsp;1. Pagi hari (sekitar jam 7-9), kemungkinan terkait dengan aktivitas pergi kerja atau sekolah.<br>
          &nbsp;&nbsp;&nbsp;&nbsp;2. Sore hari (sekitar jam 16-18), kemungkinan terkait dengan aktivitas pulang kerja atau sekolah.<br>
        - Penyewaan cenderung rendah pada tengah malam hingga dini hari (jam 0-5).
    </p>
</div>
""", unsafe_allow_html=True)


st.caption("Taufik Alwan MC541D5Y0573")