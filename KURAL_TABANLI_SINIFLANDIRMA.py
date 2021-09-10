# KURAL TABANLI SINIFLANDIRMA İLE POTANSİYEL MÜŞTERİ SEGMENTASYONU ve GETİRİSİ HESAPLAMA #

import pandas as pd
import time
df = pd.read_csv('persona.csv')

# Veriyi anlamak için gerekenleri yazdırır.
def dataframe_info(df):

    print("-----Head-----","\n",df.head())
    time.sleep(1)
    print("\n-----Tail-----","\n",df.tail())
    time.sleep(1)
    print("\n-----Shape-----","\n",df.shape)
    time.sleep(1)
    print("\n-----Info-----","\n",df.info)
    time.sleep(1)
    print("\n-----Columns-----","\n",df.columns)
    time.sleep(1)
    print("\n-----Index-----","\n",df.index)
    time.sleep(1)
    print("\n-----Statistical Values-----","\n",df.describe().T)
    time.sleep(1)
    print("\n-----Total Empty Values-----","\n",df.isnull().sum())
    time.sleep(1)

dataframe_info(df)

print("\n")

# Unique SOURCE'lar
print("Unique SOURCE : ",df['SOURCE'].unique())

# Unique SOURCE Sayısı
print("Unique SOURCE Amount :",df['SOURCE'].nunique())

# Unique SOURCE'ların Frekansları
print("-----Unique SOURCE Frequency-----",df['SOURCE'].value_counts(),sep = "\n")

# Unique PRICE Sayısı
print("\n")
print("Unique PRICE Amount : ",df["PRICE"].nunique())

# PRICE'lara göre satış sayısı
print("\n")
print("PRICE  Sale_Amount","\n-----  -----------")
print(df["PRICE"].value_counts(),sep="\n")

# Ülkelere göre satış sayıları
print("\n")
print("CNTRY Sale_Amount","\n-----  -----------")
print(df['COUNTRY'].value_counts(),sep ="\n")

# Ülkelere göre satışlardan yapılan toplam kazanç
print("\n")
print(df.groupby("COUNTRY").agg({"PRICE":"sum"}))

# SOURCE türlerine göre satış sayıları
print("\n")
print("SOURCE    Sale_Amount","\n--------  ----------")
print(df["SOURCE"].value_counts())

# Ülkelere göre PRICE ortalamaları
print("\n")
print(df.groupby("COUNTRY").agg({"PRICE":"mean"}))

# SOURCE'lara göre PRICE ortalamaları
print("\n")
print(df.groupby("SOURCE").agg({"PRICE":"mean"}))

# COUNTRY-SOURCE Kırılımında PRICE ortalaması
print("\n")
print(df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE":"mean"}))


# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazanç
print(df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}))



# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançların azalacak şekilde sıralanması
agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values(by ="PRICE",ascending = False)

print(agg_df.head(),"\n")


# Index'lerin değişkene çevirme

agg_df = agg_df.reset_index()

print(agg_df.head(),"\n")

# age değişkenini kategorik değişkene çevirme ve agg_df'ye ekleme

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],[0,18,23,30,40,66])

print(agg_df.head(),"\n")

# Seviye tabanlı müşteriler(persona) tanımlama

agg_df["AGE_CAT"] = agg_df["AGE_CAT"].astype("string")
[row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

# Veri setine ekleme
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

# Gereksiz değişkenler çıkarma
agg_df = agg_df[["customers_level_based", "PRICE"]]
agg_df.head()


agg_df["customers_level_based"].value_counts()

# customers_level_based'e göre groupby işlemi uygulama ve price ortalamaları alma

agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head()

# customers_level_based index'ten değişkene çevirme
agg_df = agg_df.reset_index()
agg_df.head()

# Her bir persona'nın 1 tane olması gerekir
agg_df["customers_level_based"].value_counts()
agg_df.head()

# yeni müşterileri (personaları) segmente ayırma
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
print(agg_df.head(30))
agg_df.groupby("SEGMENT").agg({"PRICE": "mean"})
print(agg_df[agg_df["SEGMENT"] == "C"])

#Yeni gelen müşterilere segmentlerine göre sınıflandırma ve getirebileceği geliri tahmin etme

# 33 yaşında ANDROID kullanan bir Türk kadınının ait olduğu segmenti bulma
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadınının ait olduğu segmenti bulma
new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]
