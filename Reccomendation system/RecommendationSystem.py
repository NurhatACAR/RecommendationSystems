import numpy as np
import pandas as pd

#stun adlarını veriyoruz(csv dosyası değil.)
column_names = ['user_id','item_id','rating','timestamp']
df = pd.read_csv('users.data', sep='\t', names=column_names)

df.head()

#Kaç Kayıt olduğunu gösterelim
len(df)

#csv uzantılı dosyamızı da ekleyelim.
movie_titles = pd.read_csv("movie_id_titles.csv")
movie_titles.head()

#son eklediğimiz dosyanın ekli olduğu kayıtalara bakalım 
len(movie_titles)

#iki tabloyu birleştirelim.

df = pd.merge(df, movie_titles, on='item_id')
df.head()

#Recommendation sistemi kuruyoruz
#her satırda bir kullanıcı datası olacak şekilde düzenliyoruz.

moviemat = df.pivot_table(index='user_id',columns='title',values='rating')
moviemat.head()

#Contact (1997) filmine benzer filmleri kullanıcıya gösterelim.
#Contact (1997) filmin değerlerine bakalım.

Contact_user_ratings = moviemat['Contact (1997)']
Contact_user_ratings.head()#3. kullanıcı 3.0 değer vermiş diğerleri vermemiş(NaN)

#korelasyonları hesaplayalım.
similar_to_Contact = moviemat.corrwith(Contact_user_ratings)
similar_to_Contact

#NaN Kayıtları silelim
corr_Contact = pd.DataFrame(similar_to_Contact, columns=['Correlation'])
corr_Contact.dropna(inplace=True)
corr_Contact.head()

#Sıralama yapıp film önerisinebakalım
corr_Contact.sort_values('Correlation',ascending=False).head(10)

#alaksız sonuçlar üretebilir nedeni ise oy veren sayısının az olması
#sağlıklı sonuçlar için 100'den az oy alan sonuçları silelim

df.head()
df.drop(['timestamp'], axis=1)

#her filmin ortalama rating değeri için
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())

#sıralama yapalım
ratings.sort_values('rating', ascending=False).head()

#her filmin aldığı oy sayısını hesaplayalım.
ratings['rating_oy_sayisi'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()

#şimdi sıralama yapalım
ratings.sort_values('rating_oy_sayisi',ascending = False).head()

corr_Contact.sort_values('Correlation', ascending=False).head(10)
corr_Contact = corr_Contact.join(ratings['rating_oy_sayisi'])
corr_Contact.head()

#filtreleme yapıyoruz
corr_Contact[corr_Contact['rating_oy_sayisi'] > 100].sort_values('Correlation',ascending=False).head()