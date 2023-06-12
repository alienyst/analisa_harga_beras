import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout='wide')

st.title('Analisa Kenaikan Harga Beras')

image = Image.open('media/avatar.png')

col1, col2 = st.columns([1,12])
with col1 :
	st.image(image, width=64)
with col2 :
	st.markdown('**Ali**')
	st.markdown('_11 Juni 2023_')

st.markdown('Berita tentang kenaikan harga beras yang signifikan, \
	seperti yang diungkapkan dalam artikel [berikut](https://www.cnbcindonesia.com/news/20230425095515-4-432133/naik-terus-harga-beras-makin-gila-dan-menakutkan), \
	menunjukkan adanya kekhawatiran terhadap stabilitas harga beras di pasar. \
	Kenaikan harga beras dapat memiliki dampak yang luas terhadap masyarakat dan perekonomian secara keseluruhan. \
	Oleh karena itu, analisis kenaikan harga beras menjadi sangat penting untuk memahami faktor-faktor yang mendasarinya \
	dan implikasi ekonomi yang terkait. \
	')

st.write('')


#harga beras
hb = pd.read_csv('media/harga_beras_clean.csv')
hb.Tanggal = pd.to_datetime(hb.Tanggal)
hb = hb.iloc[:,1:9].copy()
hb['Tahun'] = hb.Tanggal.dt.year.astype('string')

st.header('Harga Beras')

freq = st.selectbox('Frekuensi', ['Harian','Bulan-Tahun','Bulanan'])
time_unit = {
	'Harian' : 'yearmonthdate',
	'Bulan-Tahun' : 'yearmonth',
	'Bulanan' : 'month'
}


col_bp1, col_bp2 = st.columns([4,1])

with col_bp1:
	rice_price_line = alt.Chart(hb).mark_line().encode(
		alt.X('Tanggal', title='Waktu', timeUnit=time_unit[freq]),
		alt.Y('Beras', title='Harga Beras',aggregate='mean')
	)

	st.altair_chart(rice_price_line, use_container_width=True)

with col_bp2:
	sales_bar = alt.Chart(hb.groupby('Tahun')['Beras'].mean().reset_index()).mark_bar().encode(
		alt.X('Tahun'),
		alt.Y('Beras', title='Rata-rata Harga Beras')
		)
	st.altair_chart(sales_bar, use_container_width=True)


st.markdown('<div style="text-align: justify;">Terlihat adanya tren kenaikan harga beras dari tahun ke tahun. Meskipun fluktuasi harga beras dapat terjadi dalam jangka pendek, analisis data tersebut menunjukkan adanya peningkatan harga beras secara keseluruhan dari tahun 2020 hingga 2023. \
	Pada tahun 2020, harga beras berkisar antara 10.805,83 Rupiah/kg hingga 13.130 Rupiah/kg untuk berbagai kualitas beras. Kemudian, harga beras mengalami penurunan pada tahun 2021, namun tetap berada dalam kisaran yang tinggi. Pada tahun 2022, harga beras kembali naik dan pada tahun 2023, terjadi peningkatan yang lebih signifikan.</div>', unsafe_allow_html=True)


#luas lahan
lp = pd.read_csv('media/luas_lahan.csv')
data = {
	(2018, 'Luas Panen (ha)'): lp.iloc[1:,1],
	(2019, 'Luas Panen (ha)'): lp.iloc[1:,2],
    (2020, 'Luas Panen (ha)'): lp.iloc[1:,3],
    (2021, 'Luas Panen (ha)'): lp.iloc[1:,4],
    (2022, 'Luas Panen (ha)'): lp.iloc[1:,5],
    (2018, 'Produktivitas (ku/ha)'): lp.iloc[1:,6],
    (2019, 'Produktivitas (ku/ha)'): lp.iloc[1:,7],
    (2020, 'Produktivitas (ku/ha)'): lp.iloc[1:,8],
    (2021, 'Produktivitas (ku/ha)'): lp.iloc[1:,9],
    (2022, 'Produktivitas (ku/ha)'): lp.iloc[1:,10],
    (2018, 'Produksi (ton)'): lp.iloc[1:,11],
    (2019, 'Produksi (ton)'): lp.iloc[1:,12],
    (2020, 'Produksi (ton)'): lp.iloc[1:,13],
    (2021, 'Produksi (ton)'): lp.iloc[1:,14],
    (2022, 'Produksi (ton)'): lp.iloc[1:,15]
}

lp = pd.DataFrame(data)

lp.columns = pd.MultiIndex.from_tuples([
	('Luas Panen (ha)', 2018),
    ('Luas Panen (ha)', 2019),
    ('Luas Panen (ha)', 2020),
    ('Luas Panen (ha)', 2021),
    ('Luas Panen (ha)', 2022),
    ('Produktivitas (ku/ha)', 2018),
    ('Produktivitas (ku/ha)', 2019),
    ('Produktivitas (ku/ha)', 2020),
    ('Produktivitas (ku/ha)', 2021),
    ('Produktivitas (ku/ha)', 2022),
    ('Produksi (ton)', 2018),
    ('Produksi (ton)', 2019),
    ('Produksi (ton)', 2020),
    ('Produksi (ton)', 2021),
    ('Produksi (ton)', 2022)
])

lp = pd.DataFrame(lp.sum(), columns=['Jumlah']).reset_index().pivot(index='level_1', columns='level_0')
lp.columns = ['Luas Panen (ha)','Produksi (ton)','Produktivitas (ku/ha)']
lp.index.name = 'Tahun'

st.header('Luas Panen, Produksi dan Produktivitas Padi')
# st.dataframe(lp, use_container_width=True)

lp_select = st.selectbox('Kategori', lp.columns)

lp_cat = {
	'Luas Panen (ha)' : 'Luas Panen (ha)',
	'Produksi (ton)' : 'Produksi (ton)',
	'Produktivitas (ku/ha)' : 'Produktivitas (ku/ha)'
}

lpx = lp.reset_index()
lpx['Tahun'] = lpx['Tahun'].astype('string')

luas_lahan = alt.Chart(lpx).mark_bar().encode(
		alt.X('Tahun'),
		alt.Y(lp_cat[lp_select], title=lp_select)
		)

st.altair_chart(luas_lahan, use_container_width=True)

st.markdown('<div style="text-align: justify;">Luas panen mencerminkan jumlah lahan yang digunakan untuk bercocok tanam padi. Produksi mengindikasikan total produksi padi dalam satuan ton. Produktivitas adalah rata-rata produksi padi per hektar lahan.</div>', unsafe_allow_html=True)
st.markdown("""<div style="text-align: justify;">
		    <ul>
		    <li>Luas panen padi mengalami sedikit penurunan dari tahun 2018 hingga 2021, tetapi meningkat sedikit pada tahun 2022. Hal ini menunjukkan bahwa ada fluktuasi dalam luas lahan yang digunakan untuk menanam padi.</li>
    		<li>Meskipun luas panen mengalami fluktuasi, produksi padi relatif stabil dari tahun 2018 hingga 2022. Hal ini menunjukkan adanya peningkatan dalam produktivitas pertanian, karena meskipun lahan yang digunakan sedikit berkurang, produksi padi tetap stabil.</li>
    		<li>Produktivitas padi (berdasarkan kilogram per hektar) juga mengalami fluktuasi kecil dari tahun 2018 hingga 2022. Namun, secara keseluruhan, produktivitas padi tetap relatif tinggi dan stabil selama periode tersebut.</li>
    		</ul>
	</div>""", unsafe_allow_html=True)


st.header('Impor Beras')

ib = pd.read_csv('media/impor_beras.csv')
col = ['Negara Asal']
col.extend([x for x in range(2015,2023)])
ib = ib.iloc[1:,1:]
ib.columns = col
ibx = pd.DataFrame(ib.drop('Negara Asal', axis=1).sum()).reset_index()
ibx.columns = ['Tahun', 'Jumlah']
ibx['Tahun'] = ibx['Tahun'].astype('string')
rice_import_line = alt.Chart(ibx).mark_line().encode(
	alt.X('Tahun'),
	alt.Y('Jumlah', title='Impor Beras (ton)')
)

st.altair_chart(rice_import_line, use_container_width=True)


st.markdown("""<div style="text-align: justify;">
		    <ul>
		    <li>Pada tahun 2018, terjadi lonjakan yang signifikan dalam impor beras, mencapai 2.253.824,4 ton. Hal ini menunjukkan peningkatan permintaan beras impor pada tahun tersebut.</li>
    		<li>Jumlah impor beras kembali menurun pada tahun 2019, menjadi 444.508,8 ton. Namun, pada tahun 2020 dan 2021, jumlah impor beras naik kembali menjadi 356.286,2 ton dan 407.741,4 ton.</li>
    		<li>Pada tahun 2022, terjadi peningkatan lagi dalam impor beras, mencapai 429.207,3 ton. Hal ini menunjukkan bahwa impor beras masih menjadi faktor yang signifikan dalam memenuhi kebutuhan beras di dalam negeri.</li>
    		</ul>
	</div>""", unsafe_allow_html=True)

st.write("Dengan menggabungkan data impor beras dengan data sebelumnya mengenai luas panen, produksi, produktivitas, dan harga beras, dapat dilihat bahwa meskipun produksi padi relatif stabil, impor beras masih dibutuhkan untuk memenuhi kebutuhan dalam negeri. Peningkatan harga beras juga dapat terkait dengan fluktuasi dalam jumlah impor beras yang terjadi selama periode yang diberikan.")

#Data Inflasi
infx = pd.read_csv('media/inflasi.csv', index_col=0)
infx['Tahun'] = infx['Tahun'].astype('string')

infx = pd.DataFrame(infx.groupby('Tahun')['Data Inflasi'].mean()).reset_index()

st.header('Data Inflasi')

infx_bar = alt.Chart(infx).mark_line().encode(
	alt.X('Tahun'),
	alt.Y('Data Inflasi', title='Rata-rata Inflasi')
	)
st.altair_chart(infx_bar, use_container_width=True)

st.markdown("""<div style="text-align: justify;">
		    <ul>
		    <li>Tingkat inflasi mengalami fluktuasi selama periode yang diberikan. Pada tahun 2018, tingkat inflasi mencapai 3.1975%. Kemudian, inflasi mengalami penurunan pada tahun 2019 menjadi 3.029167%.</li>
    		<li>Pada tahun 2020, terjadi penurunan yang signifikan dalam tingkat inflasi menjadi 2.035833%. Hal ini menunjukkan adanya perlambatan dalam laju kenaikan harga barang dan jasa.</li>
    		<li>Pada tahun 2021, tingkat inflasi terus menurun menjadi 1.56%. Ini menunjukkan adanya stabilitas harga yang lebih tinggi, di mana laju kenaikan harga relatif rendah.</li>
    		<li>Namun, pada tahun 2022, tingkat inflasi meningkat secara signifikan menjadi 4.205833%. Ini menunjukkan adanya tekanan inflasi yang lebih tinggi dan laju kenaikan harga yang lebih cepat.</li>
    		</ul>
	</div>""", unsafe_allow_html=True)

st.write("Dengan mempertimbangkan data inflasi ini, dapat dikatakan bahwa inflasi memiliki dampak pada daya beli dan harga-harga beras. Tingkat inflasi yang rendah pada tahun 2020 dan 2021 dapat membantu menjaga stabilitas harga beras, sementara inflasi yang lebih tinggi pada tahun 2022 dapat mempengaruhi harga beras dan biaya produksinya.")

st.header('Kesimpulan')

st.write('Meskipun produksi padi relatif stabil, impor beras masih dibutuhkan untuk memenuhi kebutuhan dalam negeri. Peningkatan harga beras dapat dipengaruhi oleh faktor-faktor seperti fluktuasi impor beras, inflasi, dan tekanan pada pasokan dan permintaan. Kesimpulan ini menunjukkan pentingnya menjaga stabilitas produksi padi dan pasokan beras dalam negeri untuk mengendalikan harga beras dan mengurangi ketergantungan pada impor.')

st.text('Sumber Data : bps.go.id dan hargapangan.id')