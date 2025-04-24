# Maç Sonucu Tahmin Modeli İçin Veri Seti Hazırlığı </br> </br>
*Veri seti için Maçkolik sitesinden verileri web scraping yöntemiyle çektim. Bunun için Python Selenium kütüphanesini kullandım. Veri setimizde 6 takım bulunmaktadır. Bunlar: Liverpool, Manchester City, Manchester United, Arsenal, Chelsea, Tottenham. Her takım için 700 maçın verileri toplanmıştır. Feature Space ise aşağıdaki gibidir;* </br> </br>
*Tarih, 	
Rakip Takım,	
Takım ID,	
Is_Home,	
Sonuç,	
Gol,
Rakip Gol,
Topla Oynama(%),	
Şut,	
İsabetli, 
Şut,	
Başarılı Pas,	
Pas Başarısı(%),	
Korner,	
Faul,	
Ofsayt,	
Rakip Topla Oynama(%),	
Rakip Şut,	
Rakip İsabetli Şut,	
Rakip Başarılı Pas,	
Rakip Pas Başarısı(%),	
Rakip Korner,	
Rakip Faul,	
Rakip Ofsayt,	
Şut Verimliliği(İsabetli Şut/Şut),
Gol Farkı,
Sezon,
Ay,
Haftanın Günü,
Son 5 Maç Gol Ort,
Son 5 Maç Galibiyet Oranı* 
</br> </br>
*Şut Verimliliği(İsabetli Şut/Şut),
Gol Farkı,
Sezon,
Ay,
Haftanın Günü,
Son 5 Maç Gol Ort ve Son 5 Maç Galibiyet Oranı özellikleri **feature engineering** yapılarak oluşturulmuştur.* </br> </br>
*Daha sonrasında elimizdeki veriler üzerinden **veri görselleştirme ve korelasyon analizi** gerçekleştirildi. Bunlara da aşağıda yer verilmiştir.*

</br> </br>
### Veri Görselleştirme </br> 
<img width="1046" alt="3" src="https://github.com/user-attachments/assets/79220f47-980c-48e0-8f01-9169e88e1d1f" />
<img width="1046" alt="2" src="https://github.com/user-attachments/assets/b532a86f-f48d-4e5f-a9de-f616d02cf06b" />
<img width="1046" alt="1" src="https://github.com/user-attachments/assets/02c111bd-46aa-452e-b59f-63dbd7f5298a" />
<img width="1046" alt="4" src="https://github.com/user-attachments/assets/b6a6cf9b-24c4-4eec-88e9-d709f40b9c72" />

</br> </br> 
### Korelasyon Analizi  </br>
<img width="1257" alt="1" src="https://github.com/user-attachments/assets/cf82a10d-75d2-4b0c-bc08-7a5342a490ef" />
<img width="1182" alt="2" src="https://github.com/user-attachments/assets/793b4c50-f9d0-4fc4-bc82-73d5ab4516fd" />
