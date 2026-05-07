# 🍽️ Yemek Tarif Platformu

Modern ve kullanıcı dostu arayüze sahip, Python OOP (Nesne Yönelimli Programlama) ve Tkinter kullanılarak geliştirilmiş kapsamlı bir yemek tarif yönetim sistemi.

---

# 📌 Proje Hakkında

Bu proje, kullanıcıların yemek tariflerini görüntüleyebildiği, yeni tarif ekleyebildiği, favorilere kaydedebildiği ve tarifleri puanlayabildiği masaüstü tabanlı bir yemek tarif platformudur.

Proje tamamen Python dili ile geliştirilmiş olup:

- Nesne yönelimli programlama (OOP)
- Tkinter grafik arayüzü
- Kullanıcı yönetimi
- Veri filtreleme ve arama algoritmaları
- Listeleme ve değerlendirme sistemleri

gibi temel yazılım geliştirme prensiplerini içermektedir.

---

# 🚀 Özellikler

## 👤 Kullanıcı Sistemi

- Kullanıcı kayıt sistemi
- Kullanıcı giriş sistemi
- Oturum yönetimi
- Favori tarif yönetimi

---

## 🍲 Tarif Yönetimi

- Yeni tarif ekleme
- Tarif silme
- Tarif güncelleme
- Tarif görüntüleme
- Tarif detay ekranı

---

## 🔍 Arama ve Filtreleme

- Tarif adına göre arama
- Kategoriye göre filtreleme
- Hazırlık süresine göre filtreleme
- Malzemeye göre arama

---

## ⭐ Değerlendirme Sistemi

- Tarif puanlama (1-5)
- Yorum ekleme
- Ortalama puan hesaplama
- Yıldızlı değerlendirme sistemi

---

## ❤️ Favori Sistemi

- Favorilere tarif ekleme
- Favorilerden kaldırma
- Favori tarifleri görüntüleme

---

## 🛒 Alışveriş Listesi

- Birden fazla tarif seçebilme
- Ortak malzemeleri birleştirme
- Otomatik alışveriş listesi oluşturma

---

# 🏗️ Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|---|---|
| Python | Ana programlama dili |
| Tkinter | Grafik kullanıcı arayüzü |
| OOP | Nesne yönelimli mimari |
| UUID | Benzersiz ID üretimi |
| ttk | Gelişmiş Tkinter bileşenleri |

---

# 📂 Proje Yapısı

```text
yemek.py
```

Tüm proje tek Python dosyası içerisinde geliştirilmiştir.

---

# 🧠 Kullanılan Sınıflar

## 1. Malzeme

Bir tarif içerisindeki malzeme bilgisini temsil eder.

### Özellikleri

- Malzeme adı
- Miktar
- Birim

### Metotlar

```python
bilgi()
```

Malzemeyi okunabilir formatta döndürür.

---

## 2. Degerlendirme

Kullanıcının tarif için yaptığı puanlama ve yorumu temsil eder.

### Özellikleri

- Kullanıcı ID
- Puan
- Yorum
- Tarih

### Özellikleri

- 1-5 arası puan kontrolü
- Yıldızlı değerlendirme sistemi

---

## 3. Tarif

Sistemdeki yemek tariflerini temsil eder.

### İçerdiği Bilgiler

- Tarif adı
- Kategori
- Hazırlama süresi
- Zorluk seviyesi
- Malzemeler
- Yapılış adımları
- Değerlendirmeler

### Temel Metotlar

```python
tarif_ekle()
tarif_guncelle()
malzeme_ekle()
adim_ekle()
tarif_degerlendir()
ortalama_puan()
puan_yildiz()
```

---

## 4. Kullanici

Platform kullanıcılarını temsil eder.

### Özellikleri

- Kullanıcı adı
- E-posta
- Şifre
- Favoriler
- Eklenen tarifler

### Temel Metotlar

```python
favoriye_ekle()
favoriden_cikar()
sifre_dogru_mu()
```

---

## 5. TarifPlatformu

Sistemin ana yönetici sınıfıdır.

### Görevleri

- Kullanıcı yönetimi
- Tarif yönetimi
- Arama işlemleri
- Filtreleme
- Favori sistemi
- Alışveriş listesi oluşturma

### Temel Metotlar

```python
kullanici_kayit()
giris_yap()
tarif_ekle()
tarif_sil()
tarif_ara()
kategoriye_gore_filtrele()
sureye_gore_filtrele()
favorileri_getir()
alisveris_listesi_olustur()
```

---

# 🎨 Grafik Arayüz

Projede Tkinter kullanılarak modern koyu tema tasarlanmıştır.

## Arayüz Bölümleri

### 🔐 Giriş / Kayıt Ekranı

- Kullanıcı giriş sistemi
- Yeni kullanıcı kaydı

---

### 📋 Tarifler Sekmesi

- Tarif listeleme
- Arama
- Filtreleme
- Tarif detayları

---

### ➕ Tarif Ekle Sekmesi

- Yeni tarif oluşturma
- Malzeme ekleme
- Yapılış adımı ekleme

---

### ❤️ Favoriler Sekmesi

- Favori tarif görüntüleme
- Favoriden kaldırma

---

### 🛒 Alışveriş Listesi Sekmesi

- Tarif seçimi
- Otomatik alışveriş listesi

---

### 📊 İstatistikler Sekmesi

- Sistem istatistikleri
- En yüksek puanlı tarifler

---

# ⚙️ Kurulum

## 1. Python Kurulumu

Bilgisayarınızda Python 3.10 veya üzeri sürüm kurulu olmalıdır.

Python sürümünü kontrol etmek için:

```bash
python --version
```

---

## 2. Projeyi İndirin

```bash
git clone https://github.com/kullaniciadi/yemek-tarif-platformu.git
```

---

## 3. Proje Klasörüne Girin

```bash
cd yemek-tarif-platformu
```

---

## 4. Programı Çalıştırın

```bash
python yemek.py
```

---

# 🔑 Demo Kullanıcı

Projede örnek giriş hesabı bulunmaktadır.

```text
E-posta: admin@tarif.com
Şifre: 1234
```

---

# 📖 Örnek Kullanım

## Tarif Arama

Kullanıcı arama kutusuna:

```text
mercimek
```

yazarak mercimek içeren tarifleri bulabilir.

---

## Tarif Puanlama

Kullanıcı tarif detay ekranından:

- Yıldız verebilir
- Yorum yapabilir

---

## Alışveriş Listesi Oluşturma

Birden fazla tarif seçildiğinde sistem:

- Ortak malzemeleri birleştirir
- Tek alışveriş listesi oluşturur

---

# 🧩 Yazılım Mimarisi

Proje katmanlı OOP mantığıyla geliştirilmiştir.

## Kullanılan OOP Kavramları

| Kavram | Kullanım |
|---|---|
| Encapsulation | Sınıf yapıları |
| Composition | Tarif → Malzeme ilişkisi |
| Abstraction | Metot organizasyonu |
| Object Management | Nesne yönetimi |

---

# 📌 Veri Yapıları

Projede aşağıdaki veri yapıları kullanılmıştır:

| Veri Yapısı | Kullanım Alanı |
|---|---|
| List | Malzeme ve tarif listeleri |
| Dictionary | Kullanıcı ve tarif saklama |
| String | Kullanıcı verileri |
| UUID | Benzersiz kimlik üretimi |

---

# 🛡️ Hata Kontrolleri

Projede aşağıdaki doğrulamalar bulunmaktadır:

- Boş alan kontrolü
- Sayısal veri kontrolü
- Aynı e-posta kontrolü
- Tekrar favori ekleme kontrolü
- Aynı kullanıcının tekrar puan vermesi kontrolü

---

# 📈 Gelecekte Geliştirilebilecek Özellikler

- Veritabanı desteği (SQLite / MySQL)
- Tarif görseli ekleme
- Şifre hashleme sistemi
- Admin paneli
- API entegrasyonu
- Mobil uygulama desteği
- Yapay zekâ destekli tarif önerisi

---

# 👨‍💻 Geliştirici

Bu proje Python OOP ve Tkinter konularını uygulamalı olarak geliştirmek amacıyla hazırlanmıştır.

---

# 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
