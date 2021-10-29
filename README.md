# Selenium (HTML/XML Formatter on python)
Facebook dan login olup  "Begeni,"Yorum","Paylaşım" gibi alanları çeken bir selenium projesidir. Çektiği dataları 
sum_post.py kodu  ile toplanbegeni,toplamyorum ve toplampaylaşım csv dosyasına basar ve ocr.py kodu aldığı ekran görüntüleri OCR(Optical Character Recognition)  de pytesseract kütüphanesi ile txt ye çevirip oradaki "Begeni","Yorum","Paylaşım" alanları alıp tekrar bir csv dosyasına basmaktadır.


# Running Browser Tests on Linux

Kodun çalışması için choromedriver.exe nin sürümü ile chorome sürümünün aynı olması gerekmektedir aksi halde hata vericektir. Dosya içerisinde yer alan choromedriver.exe 95.0.4638.54 sürümüne aittir.Eger sürümünüz aynı değilse  => https://chromedriver.chromium.org/downloads  adresinden aynı olan sürümü indiriniz ve dosyada bulunan choromedriver.exe silip indirdiğiniz exe dosyasına yerleştiriniz.

bot_facebook.py  =>> python bot_facebook --month 202110  # 202110 örnek verilmiştir istenilen ay bilgisini bu formatta yazınız

ocr.py =>> python ocr.py

sum_post.py =>> python sum_post.py --dir DOM # DOM veya OCR yazılmalıdır.

# Output
Bu projede  çıkarılan veriler şu örneğe benziyor:

bot_facebook.py
Begeni,Paylasım,Yorum
36,9 ,0
24,0,0
41,1 ,1 
49,22 ,0

sum_post.py
ToplamBegeni,ToplamYorum,ToplamPaylasim
88,0,0
