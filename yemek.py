"""
=============================================================
  YEMEK TARİF PLATFORMU - Proje 6
  Python OOP + Tkinter Grafik Arayüzü
=============================================================
  Sınıflar:
    - Malzeme    : Bir tarifteki malzeme bilgisi
    - Tarif      : Yemek tarifi
    - Kullanici  : Platforma kayıtlı kullanıcı
    - Degerlendirme : Kullanıcı puanı + yorum
    - TarifPlatformu : Tüm sistemi yöneten ana sınıf
  Ek Özellikler:
    - Tarif arama (isim, kategori, malzeme)
    - Puanlama & yorum sistemi
    - Favorilere ekleme
    - Hazırlık süresine göre filtreleme
    - Alışveriş listesi oluşturma
    - Kullanıcı giriş/kayıt
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import uuid  # Benzersiz ID üretimi için


# ─────────────────────────────────────────────
#  SINIF 1: Malzeme
# ─────────────────────────────────────────────
class Malzeme:
    """
    Bir tarifteki tek bir malzemeyi temsil eder.
    Attributes:
        malzeme_adi (str) : Malzemenin adı (örn. 'Un')
        miktar      (str) : Kullanılacak miktar (örn. '2')
        birim       (str) : Ölçü birimi (örn. 'su bardağı')
    """

    def __init__(self, malzeme_adi: str, miktar: str, birim: str = ""):
        self.malzeme_adi = malzeme_adi
        self.miktar = miktar
        self.birim = birim

    def bilgi(self) -> str:
        """Malzemeyi okunabilir biçimde döndürür."""
        if self.birim:
            return f"{self.miktar} {self.birim} {self.malzeme_adi}"
        return f"{self.miktar} {self.malzeme_adi}"

    def __repr__(self):
        return f"Malzeme({self.malzeme_adi}, {self.miktar} {self.birim})"


# ─────────────────────────────────────────────
#  SINIF 2: Degerlendirme (Ek Özellik)
# ─────────────────────────────────────────────
class Degerlendirme:
    """
    Kullanıcının bir tarife verdiği puan ve yorumu tutar.
    Attributes:
        kullanici_id (str)  : Değerlendiren kullanıcının ID'si
        puan         (int)  : 1-5 arası puan
        yorum        (str)  : İsteğe bağlı yorum metni
        tarih        (str)  : Değerlendirme tarihi
    """

    def __init__(self, kullanici_id: str, puan: int, yorum: str = ""):
        if not 1 <= puan <= 5:
            raise ValueError("Puan 1 ile 5 arasında olmalıdır.")
        self.kullanici_id = kullanici_id
        self.puan = puan
        self.yorum = yorum
        self.tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

    def bilgi(self) -> str:
        """Değerlendirmeyi okunabilir biçimde döndürür."""
        yildiz = "★" * self.puan + "☆" * (5 - self.puan)
        return f"[{self.tarih}] {yildiz}  {self.yorum}"


# ─────────────────────────────────────────────
#  SINIF 3: Tarif
# ─────────────────────────────────────────────
class Tarif:
    """
    Bir yemek tarifini temsil eder.
    Attributes:
        tarif_id         (str)           : Benzersiz tarif kimliği
        tarif_adi        (str)           : Tarifin adı
        kategori         (str)           : Çorba, Ana Yemek, Tatlı vb.
        hazirlama_suresi (int)           : Dakika cinsinden hazırlık süresi
        zorluk           (str)           : Kolay / Orta / Zor
        malzemeler       (list[Malzeme]) : Malzeme listesi
        yapilis_adim     (list[str])     : Yapılış adımları
        degerlendirmeler (list[Degerlendirme]): Kullanıcı değerlendirmeleri
        ekleyen_id       (str)           : Tarifi ekleyen kullanıcının ID'si
        ekleme_tarihi    (str)           : Eklenme tarihi
    """

    ZORLUK_SEVIYELERI = ["Kolay", "Orta", "Zor"]

    def __init__(self, tarif_adi: str, kategori: str, hazirlama_suresi: int,
                 zorluk: str, ekleyen_id: str):
        self.tarif_id = str(uuid.uuid4())[:8]      # Kısa benzersiz ID
        self.tarif_adi = tarif_adi
        self.kategori = kategori
        self.hazirlama_suresi = hazirlama_suresi   # dakika
        self.zorluk = zorluk if zorluk in self.ZORLUK_SEVIYELERI else "Orta"
        self.ekleyen_id = ekleyen_id
        self.ekleme_tarihi = datetime.now().strftime("%d.%m.%Y")
        self.malzemeler: list[Malzeme] = []
        self.yapilis_adim: list[str] = []
        self.degerlendirmeler: list[Degerlendirme] = []

    # ── Tarif güncelleme metodları ──────────────
    def tarif_ekle(self):
        """Tarifin sisteme eklenmesini temsil eder (platform tarafından çağrılır)."""
        print(f"[Tarif] '{self.tarif_adi}' tarifi sisteme eklendi.")

    def tarif_guncelle(self, tarif_adi: str = None, kategori: str = None,
                       hazirlama_suresi: int = None, zorluk: str = None):
        """Tarif bilgilerini kısmen veya tamamen günceller."""
        if tarif_adi:
            self.tarif_adi = tarif_adi
        if kategori:
            self.kategori = kategori
        if hazirlama_suresi is not None:
            self.hazirlama_suresi = hazirlama_suresi
        if zorluk and zorluk in self.ZORLUK_SEVIYELERI:
            self.zorluk = zorluk

    def malzeme_ekle(self, malzeme: Malzeme):
        """Tarife yeni malzeme ekler."""
        self.malzemeler.append(malzeme)

    def adim_ekle(self, adim: str):
        """Tarifte yapılış adımı ekler."""
        self.yapilis_adim.append(adim)

    # ── Değerlendirme metodu ─────────────────────
    def tarif_degerlendir(self, kullanici_id: str, puan: int, yorum: str = "") -> bool:
        """
        Kullanıcının tarifi değerlendirmesini kaydeder.
        Aynı kullanıcı bir tarifi yalnızca bir kez değerlendirebilir.
        Returns: Başarılıysa True, kullanıcı zaten değerlendirdiyse False
        """
        # Daha önce değerlendirmiş mi kontrol et
        for d in self.degerlendirmeler:
            if d.kullanici_id == kullanici_id:
                return False  # Zaten değerlendirmiş
        try:
            yeni_degerlendirme = Degerlendirme(kullanici_id, puan, yorum)
            self.degerlendirmeler.append(yeni_degerlendirme)
            return True
        except ValueError:
            return False

    # ── Hesaplama metodları ──────────────────────
    def ortalama_puan(self) -> float:
        """Tüm değerlendirmelerin ortalamasını döndürür."""
        if not self.degerlendirmeler:
            return 0.0
        toplam = sum(d.puan for d in self.degerlendirmeler)
        return round(toplam / len(self.degerlendirmeler), 1)

    def puan_yildiz(self) -> str:
        """Ortalama puanı yıldız olarak döndürür."""
        ort = self.ortalama_puan()
        dolu = int(ort)
        return "★" * dolu + "☆" * (5 - dolu) + f" ({ort})"

    def malzeme_isimleri(self) -> list[str]:
        """Tarifteki malzeme isimlerini küçük harfle döndürür."""
        return [m.malzeme_adi.lower() for m in self.malzemeler]

    def ozet(self) -> str:
        """Tarif özetini tek satırda döndürür."""
        return (f"[{self.tarif_id}] {self.tarif_adi} | "
                f"{self.kategori} | {self.hazirlama_suresi} dk | "
                f"{self.zorluk} | ⭐{self.ortalama_puan()}")

    def __repr__(self):
        return f"Tarif({self.tarif_adi}, {self.kategori})"


# ─────────────────────────────────────────────
#  SINIF 4: Kullanici
# ─────────────────────────────────────────────
class Kullanici:
    """
    Platforma kayıtlı bir kullanıcıyı temsil eder.
    Attributes:
        kullanici_id  (str)       : Benzersiz kullanıcı kimliği
        ad            (str)       : Kullanıcı adı
        email         (str)       : E-posta adresi
        sifre         (str)       : Şifre (gerçek projede hash'lenmeli)
        favoriler     (list[str]) : Favori tarif ID listesi
        eklenen_tarifler (list[str]) : Bu kullanıcının eklediği tarif ID'leri
        kayit_tarihi  (str)       : Kayıt tarihi
    """

    def __init__(self, ad: str, email: str, sifre: str):
        self.kullanici_id = str(uuid.uuid4())[:8]
        self.ad = ad
        self.email = email
        self.sifre = sifre
        self.favoriler: list[str] = []             # Tarif ID'leri
        self.eklenen_tarifler: list[str] = []      # Tarif ID'leri
        self.kayit_tarihi = datetime.now().strftime("%d.%m.%Y")

    def favoriye_ekle(self, tarif_id: str) -> bool:
        """Tarifi favorilere ekler; zaten ekliyse False döndürür."""
        if tarif_id in self.favoriler:
            return False
        self.favoriler.append(tarif_id)
        return True

    def favoriden_cikar(self, tarif_id: str) -> bool:
        """Tarifi favorilerden çıkarır; bulunamazsa False döndürür."""
        if tarif_id in self.favoriler:
            self.favoriler.remove(tarif_id)
            return True
        return False

    def tarif_ekle_listesi(self, tarif_id: str):
        """Kullanıcının eklediği tarif listesine kayıt ekler."""
        self.eklenen_tarifler.append(tarif_id)

    def kurs_listesi(self) -> list[str]:
        """Kullanıcının eklediği tariflerin ID listesini döndürür."""
        return self.eklenen_tarifler

    def sifre_dogru_mu(self, sifre: str) -> bool:
        """Girilen şifrenin doğru olup olmadığını kontrol eder."""
        return self.sifre == sifre

    def __repr__(self):
        return f"Kullanici({self.ad}, {self.email})"


# ─────────────────────────────────────────────
#  SINIF 5: TarifPlatformu (Ana Sistem)
# ─────────────────────────────────────────────
class TarifPlatformu:
    """
    Tüm sistemi yöneten ana platform sınıfı.
    Attributes:
        tarifler     (dict) : tarif_id -> Tarif eşlemesi
        kullanicilar (dict) : kullanici_id -> Kullanici eşlemesi
        aktif_kullanici (Kullanici | None): Oturum açmış kullanıcı
    """

    KATEGORILER = ["Çorba", "Ana Yemek", "Salata", "Tatlı",
                   "Aperatif", "İçecek", "Kahvaltı", "Diğer"]

    def __init__(self):
        self.tarifler: dict[str, Tarif] = {}
        self.kullanicilar: dict[str, Kullanici] = {}
        self.aktif_kullanici: Kullanici | None = None
        self._ornek_veriler_yukle()  # Başlangıç verileri

    # ── Kullanıcı yönetimi ──────────────────────
    def kullanici_kayit(self, ad: str, email: str, sifre: str) -> tuple[bool, str]:
        """
        Yeni kullanıcı kaydeder.
        Returns: (başarı_durumu, mesaj)
        """
        # E-posta zaten kayıtlı mı?
        for k in self.kullanicilar.values():
            if k.email == email:
                return False, "Bu e-posta zaten kullanılıyor."
        yeni_kullanici = Kullanici(ad, email, sifre)
        self.kullanicilar[yeni_kullanici.kullanici_id] = yeni_kullanici
        return True, f"Hoş geldiniz, {ad}! Kayıt başarılı."

    def giris_yap(self, email: str, sifre: str) -> tuple[bool, str]:
        """
        Kullanıcı girişi yapar.
        Returns: (başarı_durumu, mesaj)
        """
        for k in self.kullanicilar.values():
            if k.email == email and k.sifre_dogru_mu(sifre):
                self.aktif_kullanici = k
                return True, f"Hoş geldiniz, {k.ad}!"
        return False, "E-posta veya şifre hatalı."

    def cikis_yap(self):
        """Aktif kullanıcının oturumunu kapatır."""
        self.aktif_kullanici = None

    # ── Tarif yönetimi ──────────────────────────
    def tarif_ekle(self, tarif: Tarif) -> bool:
        """Platforma yeni tarif ekler; giriş yapılmış olması gerekir."""
        if not self.aktif_kullanici:
            return False
        self.tarifler[tarif.tarif_id] = tarif
        self.aktif_kullanici.tarif_ekle_listesi(tarif.tarif_id)
        return True

    def tarif_sil(self, tarif_id: str) -> tuple[bool, str]:
        """Tarifi siler; yalnızca ekleyen kişi silebilir."""
        if tarif_id not in self.tarifler:
            return False, "Tarif bulunamadı."
        tarif = self.tarifler[tarif_id]
        if tarif.ekleyen_id != self.aktif_kullanici.kullanici_id:
            return False, "Bu tarifi yalnızca ekleyen kişi silebilir."
        del self.tarifler[tarif_id]
        return True, "Tarif silindi."

    # ── Arama ve filtreleme (Ek Özellik) ────────
    def tarif_ara(self, arama_metni: str) -> list[Tarif]:
        """
        İsim, kategori veya malzeme içinde arama yapar.
        Büyük/küçük harf duyarsızdır.
        """
        arama = arama_metni.lower().strip()
        sonuclar = []
        for tarif in self.tarifler.values():
            if (arama in tarif.tarif_adi.lower() or
                    arama in tarif.kategori.lower() or
                    any(arama in m for m in tarif.malzeme_isimleri())):
                sonuclar.append(tarif)
        return sonuclar

    def kategoriye_gore_filtrele(self, kategori: str) -> list[Tarif]:
        """Belirtilen kategorideki tarifleri döndürür."""
        return [t for t in self.tarifler.values()
                if t.kategori == kategori]

    def sureye_gore_filtrele(self, maks_dakika: int) -> list[Tarif]:
        """Hazırlık süresi verilen dakikanın altındaki tarifleri döndürür."""
        return [t for t in self.tarifler.values()
                if t.hazirlama_suresi <= maks_dakika]

    def en_cok_puan_alan(self, n: int = 5) -> list[Tarif]:
        """En yüksek ortalama puanlı n tarifi döndürür."""
        siralı = sorted(self.tarifler.values(),
                        key=lambda t: t.ortalama_puan(), reverse=True)
        return siralı[:n]

    # ── Favori & Alışveriş listesi (Ek Özellik) ─
    def favorileri_getir(self) -> list[Tarif]:
        """Aktif kullanıcının favori tariflerini döndürür."""
        if not self.aktif_kullanici:
            return []
        return [self.tarifler[tid] for tid in self.aktif_kullanici.favoriler
                if tid in self.tarifler]

    def alisveris_listesi_olustur(self, tarif_idleri: list[str]) -> dict[str, str]:
        """
        Seçili tarifler için birleşik alışveriş listesi oluşturur.
        Returns: {'malzeme_adi': 'miktar birim'} sözlüğü
        """
        alisveris: dict[str, str] = {}
        for tid in tarif_idleri:
            if tid in self.tarifler:
                for m in self.tarifler[tid].malzemeler:
                    anahtar = m.malzeme_adi
                    # Basit birleştirme: aynı malzeme birden fazla tarifteyse listele
                    if anahtar in alisveris:
                        alisveris[anahtar] += f" + {m.miktar} {m.birim}".strip()
                    else:
                        alisveris[anahtar] = f"{m.miktar} {m.birim}".strip()
        return alisveris

    # ── Örnek veriler ───────────────────────────
    def _ornek_veriler_yukle(self):
        """Sisteme başlangıç için örnek kullanıcı ve tarifler yükler."""

        # Örnek kullanıcılar
        self.kullanici_kayit("Admin", "admin@tarif.com", "1234")
        self.kullanici_kayit("Ayşe Yılmaz", "ayse@mail.com", "ayse123")

        # Admin ile giriş yap ve tarifleri ekle
        self.giris_yap("admin@tarif.com", "1234")

        # ── Tarif 1: Mercimek Çorbası
        t1 = Tarif("Mercimek Çorbası", "Çorba", 30, "Kolay",
                   self.aktif_kullanici.kullanici_id)
        for malzeme_bilgi in [
            ("Kırmızı Mercimek", "1", "su bardağı"),
            ("Soğan", "1", "adet"),
            ("Havuç", "1", "adet"),
            ("Tereyağı", "2", "yemek kaşığı"),
            ("Tuz", "1", "çay kaşığı"),
            ("Kırmızı Pul Biber", "1", "çay kaşığı"),
        ]:
            t1.malzeme_ekle(Malzeme(*malzeme_bilgi))
        for adim in [
            "Soğan ve havucu doğrayıp tereyağında kavurun.",
            "Yıkanmış mercimeği ekleyip 5 dakika daha kavurun.",
            "Üzerine 1 litre su ekleyin ve kısık ateşte 20 dakika pişirin.",
            "Blender ile pürüzsüz hale getirin.",
            "Servis etmeden önce üzerine kızdırılmış tereyağı ve pul biber ekleyin.",
        ]:
            t1.adim_ekle(adim)
        self.tarif_ekle(t1)

        # ── Tarif 2: Kek
        t2 = Tarif("Çikolatalı Kek", "Tatlı", 50, "Orta",
                   self.aktif_kullanici.kullanici_id)
        for malzeme_bilgi in [
            ("Un", "2", "su bardağı"),
            ("Şeker", "1.5", "su bardağı"),
            ("Yumurta", "3", "adet"),
            ("Kakao", "4", "yemek kaşığı"),
            ("Süt", "1", "su bardağı"),
            ("Sıvı Yağ", "0.5", "su bardağı"),
            ("Kabartma Tozu", "1", "paket"),
        ]:
            t2.malzeme_ekle(Malzeme(*malzeme_bilgi))
        for adim in [
            "Fırını 180°C'ye ısıtın.",
            "Yumurta ve şekeri iyice çırpın.",
            "Yağ ve sütü ekleyip karıştırın.",
            "Un, kakao ve kabartma tozunu eleyerek ekleyin.",
            "Yağlanmış kalıba dökün ve 35 dakika pişirin.",
        ]:
            t2.adim_ekle(adim)
        self.tarif_ekle(t2)

        # ── Tarif 3: Salata
        t3 = Tarif("Akdeniz Salatası", "Salata", 15, "Kolay",
                   self.aktif_kullanici.kullanici_id)
        for malzeme_bilgi in [
            ("Domates", "3", "adet"),
            ("Salatalık", "2", "adet"),
            ("Zeytin", "100", "gram"),
            ("Beyaz Peynir", "150", "gram"),
            ("Zeytinyağı", "3", "yemek kaşığı"),
            ("Limon", "1", "adet"),
        ]:
            t3.malzeme_ekle(Malzeme(*malzeme_bilgi))
        for adim in [
            "Sebzeleri yıkayıp doğrayın.",
            "Peyniri küp küp kesin.",
            "Tüm malzemeleri karıştırın.",
            "Zeytinyağı ve limon suyu ile tatlandırın.",
        ]:
            t3.adim_ekle(adim)
        self.tarif_ekle(t3)

        # ── Tarif 4: Ana Yemek
        t4 = Tarif("Fırın Tavuk But", "Ana Yemek", 75, "Orta",
                   self.aktif_kullanici.kullanici_id)
        for malzeme_bilgi in [
            ("Tavuk But", "4", "adet"),
            ("Patates", "4", "adet"),
            ("Zeytinyağı", "3", "yemek kaşığı"),
            ("Sarımsak", "4", "diş"),
            ("Tuz", "1", "çay kaşığı"),
            ("Kekik", "1", "çay kaşığı"),
            ("Kırmızı Biber", "1", "çay kaşığı"),
        ]:
            t4.malzeme_ekle(Malzeme(*malzeme_bilgi))
        for adim in [
            "Tavukları zeytinyağı ve baharatlarla marine edin, 30 dakika bekletin.",
            "Patatesleri doğrayıp tavuk ile tepsiye yerleştirin.",
            "200°C fırında 45 dakika pişirin.",
            "Altın rengi alınca fırından çıkarın.",
        ]:
            t4.adim_ekle(adim)
        self.tarif_ekle(t4)

        # Örnek değerlendirmeler ekle
        t1.tarif_degerlendir("ornek1", 5, "Harika bir çorba!")
        t1.tarif_degerlendir("ornek2", 4, "Çok lezzetli.")
        t2.tarif_degerlendir("ornek1", 5, "Mükemmel kek!")
        t3.tarif_degerlendir("ornek2", 4, "Ferah ve lezzetli.")
        t4.tarif_degerlendir("ornek1", 4, "Çok güzel oldu.")

        # Oturumu kapat (kullanıcı henüz giriş yapmadı)
        self.cikis_yap()


# ══════════════════════════════════════════════
#  TKINTER GRAFİK ARAYÜZÜ
# ══════════════════════════════════════════════

# Renk paleti – koyu mutfak teması
RENKLER = {
    "bg_koyu":    "#1A1A2E",   # Arka plan
    "bg_orta":    "#16213E",   # Panel arka planı
    "bg_kart":    "#0F3460",   # Kart arka planı
    "vurgu":      "#E94560",   # Vurgu rengi (kırmızı/pembe)
    "vurgu2":     "#F5A623",   # İkincil vurgu (turuncu)
    "metin":      "#EAEAEA",   # Ana metin
    "metin_soluk":"#9E9E9E",   # İkincil metin
    "basari":     "#4CAF50",   # Başarı yeşili
    "hata":       "#F44336",   # Hata kırmızısı
}

YAZI = {
    "baslik":  ("Segoe UI", 20, "bold"),
    "alt_bas": ("Segoe UI", 13, "bold"),
    "normal":  ("Segoe UI", 10),
    "kucuk":   ("Segoe UI", 9),
    "dugme":   ("Segoe UI", 10, "bold"),
}


class TarifUygulama:
    """
    Tkinter tabanlı grafik arayüz sınıfı.
    TarifPlatformu ile haberleşerek tüm GUI işlemlerini yönetir.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.platform = TarifPlatformu()  # İş mantığı katmanı
        self._arayuz_ayarla()
        self._giris_ekrani_goster()      # Uygulama giriş ekranıyla başlar

    # ── Temel arayüz ayarları ───────────────────
    def _arayuz_ayarla(self):
        """Ana pencere boyut, renk ve başlık ayarları."""
        self.root.title("🍽️ Yemek Tarif Platformu")
        self.root.geometry("1100x700")
        self.root.configure(bg=RENKLER["bg_koyu"])
        self.root.resizable(True, True)
        # ttk stil ayarları
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("TNotebook", background=RENKLER["bg_koyu"],
                        borderwidth=0)
        stil.configure("TNotebook.Tab", background=RENKLER["bg_orta"],
                        foreground=RENKLER["metin"], padding=[12, 6],
                        font=YAZI["dugme"])
        stil.map("TNotebook.Tab",
                 background=[("selected", RENKLER["bg_kart"])],
                 foreground=[("selected", RENKLER["vurgu"])])
        stil.configure("Treeview", background=RENKLER["bg_orta"],
                        foreground=RENKLER["metin"],
                        fieldbackground=RENKLER["bg_orta"],
                        rowheight=28, font=YAZI["normal"])
        stil.configure("Treeview.Heading", background=RENKLER["bg_kart"],
                        foreground=RENKLER["vurgu2"], font=YAZI["dugme"])
        stil.map("Treeview", background=[("selected", RENKLER["vurgu"])])
        stil.configure("TCombobox", background=RENKLER["bg_orta"],
                        foreground=RENKLER["metin"],
                        fieldbackground=RENKLER["bg_orta"])
        stil.configure("Vertical.TScrollbar",
                        background=RENKLER["bg_kart"],
                        troughcolor=RENKLER["bg_koyu"])

    # ── Yardımcı widget fabrikaları ─────────────
    def _dugme(self, ebeveyn, metin, komut, renk=None, en=None):
        """Tutarlı stil için ortak düğme oluşturucu."""
        r = renk or RENKLER["vurgu"]
        kw = dict(text=metin, command=komut,
                  bg=r, fg="white", font=YAZI["dugme"],
                  relief="flat", cursor="hand2",
                  activebackground=RENKLER["bg_kart"],
                  activeforeground=RENKLER["vurgu2"],
                  padx=12, pady=6)
        if en:
            kw["width"] = en
        return tk.Button(ebeveyn, **kw)

    def _etiket(self, ebeveyn, metin, stil_key="normal", renk=None):
        """Tutarlı stil için ortak etiket oluşturucu."""
        return tk.Label(ebeveyn, text=metin,
                        bg=RENKLER["bg_koyu"],
                        fg=renk or RENKLER["metin"],
                        font=YAZI[stil_key])

    def _giris_alani(self, ebeveyn, sifreyi_gizle=False):
        """Koyu tema giriş alanı."""
        e = tk.Entry(ebeveyn,
                     bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                     insertbackground=RENKLER["metin"],
                     font=YAZI["normal"], relief="flat",
                     show="●" if sifreyi_gizle else "")
        return e

    def _cerceve_temizle(self, cerceve):
        """Verilen çerçevedeki tüm widget'ları temizler."""
        for w in cerceve.winfo_children():
            w.destroy()

    # ─────────────────────────────────────────────
    #  GİRİŞ / KAYIT EKRANI
    # ─────────────────────────────────────────────
    def _giris_ekrani_goster(self):
        """Uygulama açıldığında görünen giriş sayfası."""
        self._cerceve_temizle(self.root)

        # Arka plan çerçevesi
        cerceve = tk.Frame(self.root, bg=RENKLER["bg_koyu"])
        cerceve.pack(expand=True)

        # Logo / başlık
        tk.Label(cerceve, text="🍽️", font=("Segoe UI", 48),
                 bg=RENKLER["bg_koyu"]).pack(pady=(0, 5))
        tk.Label(cerceve, text="Yemek Tarif Platformu",
                 font=("Segoe UI", 22, "bold"),
                 bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack()
        tk.Label(cerceve, text="Lezzetleri keşfet, tariflerini paylaş",
                 font=YAZI["kucuk"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin_soluk"]).pack(pady=(2, 20))

        # Giriş formu kartı
        kart = tk.Frame(cerceve, bg=RENKLER["bg_kart"],
                        padx=40, pady=30)
        kart.pack(ipadx=10, ipady=10)

        # Sekmeler: Giriş | Kayıt Ol
        sekme_cerceve = tk.Frame(kart, bg=RENKLER["bg_kart"])
        sekme_cerceve.pack(fill="x", pady=(0, 20))

        self.aktif_sekme = tk.StringVar(value="giris")

        def sekme_sec(sekme):
            self.aktif_sekme.set(sekme)
            giris_btn.config(
                fg=RENKLER["vurgu"] if sekme == "giris" else RENKLER["metin"],
                font=("Segoe UI", 11, "bold") if sekme == "giris" else YAZI["normal"])
            kayit_btn.config(
                fg=RENKLER["vurgu"] if sekme == "kayit" else RENKLER["metin"],
                font=("Segoe UI", 11, "bold") if sekme == "kayit" else YAZI["normal"])
            form_goster()

        giris_btn = tk.Button(sekme_cerceve, text="Giriş Yap",
                              bg=RENKLER["bg_kart"], fg=RENKLER["vurgu"],
                              font=("Segoe UI", 11, "bold"), relief="flat",
                              cursor="hand2",
                              command=lambda: sekme_sec("giris"))
        giris_btn.pack(side="left", padx=10)

        kayit_btn = tk.Button(sekme_cerceve, text="Kayıt Ol",
                              bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                              font=YAZI["normal"], relief="flat",
                              cursor="hand2",
                              command=lambda: sekme_sec("kayit"))
        kayit_btn.pack(side="left", padx=10)

        # Form alanı
        self.form_cerceve = tk.Frame(kart, bg=RENKLER["bg_kart"])
        self.form_cerceve.pack()

        # Giriş alanları
        self.email_giris = tk.StringVar()
        self.sifre_giris = tk.StringVar()
        self.ad_kayit = tk.StringVar()
        self.email_kayit = tk.StringVar()
        self.sifre_kayit = tk.StringVar()

        def form_goster():
            self._cerceve_temizle(self.form_cerceve)
            if self.aktif_sekme.get() == "giris":
                _giris_form()
            else:
                _kayit_form()

        def _giris_form():
            """Giriş formu alanlarını oluşturur."""
            alanlar = [
                ("E-posta", self.email_giris, False),
                ("Şifre", self.sifre_giris, True),
            ]
            for etiket, degisken, gizle in alanlar:
                tk.Label(self.form_cerceve, text=etiket,
                         bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                         font=YAZI["kucuk"]).pack(anchor="w")
                e = tk.Entry(self.form_cerceve, textvariable=degisken,
                             bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
                             insertbackground=RENKLER["metin"],
                             font=YAZI["normal"], relief="flat", width=30,
                             show="●" if gizle else "")
                e.pack(pady=(2, 10), ipady=5)

            self._dugme(self.form_cerceve, "Giriş Yap",
                        self._giris_islemi).pack(pady=10, fill="x")

            # Hızlı demo girişi
            tk.Label(self.form_cerceve,
                     text="Demo: admin@tarif.com / 1234",
                     bg=RENKLER["bg_kart"],
                     fg=RENKLER["metin_soluk"],
                     font=YAZI["kucuk"]).pack()

        def _kayit_form():
            """Kayıt formu alanlarını oluşturur."""
            alanlar = [
                ("Adınız", self.ad_kayit, False),
                ("E-posta", self.email_kayit, False),
                ("Şifre", self.sifre_kayit, True),
            ]
            for etiket, degisken, gizle in alanlar:
                tk.Label(self.form_cerceve, text=etiket,
                         bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                         font=YAZI["kucuk"]).pack(anchor="w")
                e = tk.Entry(self.form_cerceve, textvariable=degisken,
                             bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
                             insertbackground=RENKLER["metin"],
                             font=YAZI["normal"], relief="flat", width=30,
                             show="●" if gizle else "")
                e.pack(pady=(2, 10), ipady=5)

            self._dugme(self.form_cerceve, "Kayıt Ol",
                        self._kayit_islemi,
                        renk=RENKLER["basari"]).pack(pady=10, fill="x")

        form_goster()

    def _giris_islemi(self):
        """Giriş butonu tıklandığında çalışır."""
        basari, mesaj = self.platform.giris_yap(
            self.email_giris.get(), self.sifre_giris.get())
        if basari:
            messagebox.showinfo("Hoş Geldiniz", mesaj)
            self._ana_ekran_goster()   # Ana ekrana geç
        else:
            messagebox.showerror("Hata", mesaj)

    def _kayit_islemi(self):
        """Kayıt ol butonu tıklandığında çalışır."""
        basari, mesaj = self.platform.kullanici_kayit(
            self.ad_kayit.get(),
            self.email_kayit.get(),
            self.sifre_kayit.get())
        if basari:
            messagebox.showinfo("Kayıt Başarılı", mesaj)
            # Kayıt sonrası otomatik giriş
            self.platform.giris_yap(self.email_kayit.get(),
                                    self.sifre_kayit.get())
            self._ana_ekran_goster()
        else:
            messagebox.showerror("Hata", mesaj)

    # ─────────────────────────────────────────────
    #  ANA EKRAN
    # ─────────────────────────────────────────────
    def _ana_ekran_goster(self):
        """Giriş sonrası ana uygulama ekranı."""
        self._cerceve_temizle(self.root)

        # ── Üst çubuk ──────────────────────────
        ust_cubuk = tk.Frame(self.root, bg=RENKLER["bg_kart"], pady=8)
        ust_cubuk.pack(fill="x")

        tk.Label(ust_cubuk, text="🍽️ Yemek Tarif Platformu",
                 font=YAZI["baslik"], bg=RENKLER["bg_kart"],
                 fg=RENKLER["vurgu"]).pack(side="left", padx=20)

        # Kullanıcı bilgisi ve çıkış düğmesi
        kullanici_adi = self.platform.aktif_kullanici.ad
        tk.Label(ust_cubuk, text=f"👤 {kullanici_adi}",
                 font=YAZI["normal"], bg=RENKLER["bg_kart"],
                 fg=RENKLER["metin"]).pack(side="right", padx=10)
        self._dugme(ust_cubuk, "Çıkış", self._cikis_islemi,
                    renk=RENKLER["hata"]).pack(side="right", padx=5)

        # ── Sekmeli içerik alanı ──────────────
        self.notebook = ttk.Notebook(self.root)  # self'e kaydedildi → tab olayları erişilebilir
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        notebook = self.notebook

        # Sekme 1: Tüm Tarifler
        self.tarifler_sekmesi = tk.Frame(notebook, bg=RENKLER["bg_koyu"])
        notebook.add(self.tarifler_sekmesi, text="📋 Tarifler")

        # Sekme 2: Tarif Ekle
        self.ekle_sekmesi = tk.Frame(notebook, bg=RENKLER["bg_koyu"])
        notebook.add(self.ekle_sekmesi, text="➕ Tarif Ekle")

        # Sekme 3: Favoriler
        self.favoriler_sekmesi = tk.Frame(notebook, bg=RENKLER["bg_koyu"])
        notebook.add(self.favoriler_sekmesi, text="❤️ Favoriler")

        # Sekme 4: Alışveriş Listesi
        self.alisveris_sekmesi = tk.Frame(notebook, bg=RENKLER["bg_koyu"])
        notebook.add(self.alisveris_sekmesi, text="🛒 Alışveriş Listesi")

        # Sekme 5: İstatistikler
        self.istatistik_sekmesi = tk.Frame(notebook, bg=RENKLER["bg_koyu"])
        notebook.add(self.istatistik_sekmesi, text="📊 İstatistikler")

        # Her sekmeyi doldur
        self._tarifler_sekmesini_doldur()
        self._ekle_sekmesini_doldur()
        self._favoriler_sekmesini_doldur()
        self._alisveris_sekmesini_doldur()
        self._istatistik_sekmesini_doldur()

        # ── Sekme değişim olayı: canlı güncelleme ──
        # Favoriler, Alışveriş ve İstatistik sekmeleri
        # açıldığında otomatik yenilenir
        def _sekme_degisti(event):
            secili = self.notebook.index(self.notebook.select())
            if secili == 2:    # Favoriler sekmesi (index 2)
                self._favorileri_goster()
            elif secili == 3:  # Alışveriş sekmesi (index 3)
                self._alisveris_listesi_yenile()
            elif secili == 4:  # İstatistikler sekmesi (index 4)
                self._istatistik_yenile()

        self.notebook.bind("<<NotebookTabChanged>>", _sekme_degisti)

    def _cikis_islemi(self):
        """Çıkış yapıp giriş ekranına döner."""
        self.platform.cikis_yap()
        self._giris_ekrani_goster()

    # ─────────────────────────────────────────────
    #  SEKME 1: TARİFLER
    # ─────────────────────────────────────────────
    def _tarifler_sekmesini_doldur(self):
        """Tarif listesi, arama ve filtre arayüzünü oluşturur."""
        # Üst araç çubuğu
        arac_cubugu = tk.Frame(self.tarifler_sekmesi, bg=RENKLER["bg_koyu"])
        arac_cubugu.pack(fill="x", padx=10, pady=10)

        # Arama kutusu
        tk.Label(arac_cubugu, text="🔍", font=("Segoe UI", 12),
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"]).pack(side="left")
        self.arama_degisken = tk.StringVar()
        arama_kutusu = tk.Entry(arac_cubugu,
                                textvariable=self.arama_degisken,
                                bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                                insertbackground=RENKLER["metin"],
                                font=YAZI["normal"], relief="flat", width=25)
        arama_kutusu.pack(side="left", padx=5, ipady=5)
        arama_kutusu.bind("<KeyRelease>",
                          lambda e: self._tarifleri_listele())

        # Kategori filtresi
        tk.Label(arac_cubugu, text="Kategori:",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=YAZI["normal"]).pack(side="left", padx=(15, 5))
        self.kategori_filtre = ttk.Combobox(
            arac_cubugu, width=15, font=YAZI["normal"],
            values=["Tümü"] + TarifPlatformu.KATEGORILER,
            state="readonly")
        self.kategori_filtre.set("Tümü")
        self.kategori_filtre.pack(side="left")
        self.kategori_filtre.bind("<<ComboboxSelected>>",
                                  lambda e: self._tarifleri_listele())

        # Süre filtresi
        tk.Label(arac_cubugu, text="Maks. Süre (dk):",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=YAZI["normal"]).pack(side="left", padx=(15, 5))
        self.sure_filtre = ttk.Combobox(
            arac_cubugu, width=8, font=YAZI["normal"],
            values=["Tümü", "15", "30", "45", "60", "90", "120"],
            state="readonly")
        self.sure_filtre.set("Tümü")
        self.sure_filtre.pack(side="left")
        self.sure_filtre.bind("<<ComboboxSelected>>",
                              lambda e: self._tarifleri_listele())

        # İçerik: Sol liste + Sağ detay
        icerik = tk.Frame(self.tarifler_sekmesi, bg=RENKLER["bg_koyu"])
        icerik.pack(fill="both", expand=True, padx=10)

        # ── Sol: Tarif Listesi ──────────────────
        sol = tk.Frame(icerik, bg=RENKLER["bg_koyu"])
        sol.pack(side="left", fill="both", expand=True)

        sutunlar = ("Tarif Adı", "Kategori", "Süre", "Zorluk", "Puan")
        self.tarif_agaci = ttk.Treeview(sol, columns=sutunlar,
                                        show="headings", height=20)
        genislikler = [200, 100, 70, 80, 80]
        for s, g in zip(sutunlar, genislikler):
            self.tarif_agaci.heading(s, text=s)
            self.tarif_agaci.column(s, width=g, anchor="center")
        self.tarif_agaci.pack(side="left", fill="both", expand=True)
        self.tarif_agaci.bind("<<TreeviewSelect>>",
                              self._tarif_sec_detay)

        kaydirici = ttk.Scrollbar(sol, orient="vertical",
                                  command=self.tarif_agaci.yview)
        kaydirici.pack(side="right", fill="y")
        self.tarif_agaci.configure(yscrollcommand=kaydirici.set)

        # ── Sağ: Tarif Detay Paneli ────────────
        self.detay_panel = tk.Frame(icerik, bg=RENKLER["bg_kart"],
                                    width=340, padx=15, pady=15)
        self.detay_panel.pack(side="right", fill="y", padx=(10, 0))
        self.detay_panel.pack_propagate(False)

        tk.Label(self.detay_panel, text="Tarif seçin",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin_soluk"],
                 font=YAZI["alt_bas"]).pack(expand=True)

        # İlk listeyi göster
        self._tarifleri_listele()

    def _tarifleri_listele(self):
        """Filtre ve aramaya göre tarifleri listeler."""
        # Mevcut satırları temizle
        for satir in self.tarif_agaci.get_children():
            self.tarif_agaci.delete(satir)

        # Arama & filtreleme
        arama = self.arama_degisken.get().strip()
        kategori = self.kategori_filtre.get()
        sure_str = self.sure_filtre.get()

        tarifler = list(self.platform.tarifler.values())

        # Arama filtresi
        if arama:
            tarifler = self.platform.tarif_ara(arama)

        # Kategori filtresi
        if kategori != "Tümü":
            tarifler = [t for t in tarifler if t.kategori == kategori]

        # Süre filtresi
        if sure_str != "Tümü":
            tarifler = [t for t in tarifler
                        if t.hazirlama_suresi <= int(sure_str)]

        # Tarifleri sırala (puana göre)
        tarifler.sort(key=lambda t: t.ortalama_puan(), reverse=True)

        for tarif in tarifler:
            puan_goster = (f"⭐{tarif.ortalama_puan()}"
                           if tarif.degerlendirmeler else "—")
            self.tarif_agaci.insert("", "end",
                                    iid=tarif.tarif_id,
                                    values=(tarif.tarif_adi,
                                            tarif.kategori,
                                            f"{tarif.hazirlama_suresi} dk",
                                            tarif.zorluk,
                                            puan_goster))

    def _tarif_sec_detay(self, event=None):
        """Listeden tarif seçildiğinde sağ panelde detayları gösterir."""
        secim = self.tarif_agaci.selection()
        if not secim:
            return
        tarif_id = secim[0]
        tarif = self.platform.tarifler.get(tarif_id)
        if not tarif:
            return
        self._detay_paneli_guncelle(tarif)

    def _detay_paneli_guncelle(self, tarif: Tarif):
        """Sağ detay panelini seçilen tarifte gösterir."""
        self._cerceve_temizle(self.detay_panel)

        # Başlık
        tk.Label(self.detay_panel, text=tarif.tarif_adi,
                 bg=RENKLER["bg_kart"], fg=RENKLER["vurgu"],
                 font=YAZI["alt_bas"], wraplength=300).pack(anchor="w")

        # Meta bilgiler
        meta = (f"📁 {tarif.kategori}   ⏱ {tarif.hazirlama_suresi} dk"
                f"   💪 {tarif.zorluk}")
        tk.Label(self.detay_panel, text=meta,
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin_soluk"],
                 font=YAZI["kucuk"]).pack(anchor="w", pady=(2, 8))

        # Puan
        tk.Label(self.detay_panel,
                 text=f"Puan: {tarif.puan_yildiz()}",
                 bg=RENKLER["bg_kart"], fg=RENKLER["vurgu2"],
                 font=YAZI["normal"]).pack(anchor="w", pady=(0, 8))

        # Malzemeler
        tk.Label(self.detay_panel, text="🧂 Malzemeler",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        malzeme_metin = "\n".join(
            f"  • {m.bilgi()}" for m in tarif.malzemeler) or "  (boş)"
        tk.Label(self.detay_panel, text=malzeme_metin,
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=YAZI["kucuk"], justify="left").pack(anchor="w")

        # Yapılış adımları (kaydırılabilir)
        tk.Label(self.detay_panel, text="📝 Yapılış",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 2))
        adim_cerceve = tk.Frame(self.detay_panel, bg=RENKLER["bg_kart"])
        adim_cerceve.pack(fill="both", expand=True)
        adim_metin_widget = tk.Text(
            adim_cerceve, height=6, wrap="word",
            bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
            font=YAZI["kucuk"], relief="flat",
            state="normal")
        adim_metin_widget.pack(fill="both", expand=True)
        for i, adim in enumerate(tarif.yapilis_adim, 1):
            adim_metin_widget.insert("end", f"{i}. {adim}\n")
        adim_metin_widget.config(state="disabled")

        # Değerlendirmeler
        tk.Label(self.detay_panel, text="💬 Yorumlar",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 2))
        if tarif.degerlendirmeler:
            for d in tarif.degerlendirmeler[-3:]:   # Son 3 yorum
                tk.Label(self.detay_panel,
                         text=d.bilgi(), bg=RENKLER["bg_kart"],
                         fg=RENKLER["metin_soluk"],
                         font=YAZI["kucuk"],
                         wraplength=290, justify="left").pack(anchor="w")
        else:
            tk.Label(self.detay_panel, text="  Henüz yorum yok.",
                     bg=RENKLER["bg_kart"], fg=RENKLER["metin_soluk"],
                     font=YAZI["kucuk"]).pack(anchor="w")

        # Eylem düğmeleri
        btn_cerceve = tk.Frame(self.detay_panel, bg=RENKLER["bg_kart"])
        btn_cerceve.pack(pady=8, fill="x")

        # Default arg ile lambda geç bağlama (late binding) hatası önlendi
        self._dugme(btn_cerceve, "❤️ Favori",
                    lambda tid=tarif.tarif_id: self._favoriye_ekle(tid),
                    renk=RENKLER["vurgu"]).pack(side="left", padx=2)
        self._dugme(btn_cerceve, "⭐ Değerlendir",
                    lambda t=tarif: self._degerlendirme_penceresi(t),
                    renk=RENKLER["vurgu2"]).pack(side="left", padx=2)

        # Eğer tarifi ekleyen kullanıcıysa sil butonu
        aktif = self.platform.aktif_kullanici
        if tarif.ekleyen_id == aktif.kullanici_id:
            self._dugme(btn_cerceve, "🗑️ Sil",
                        lambda tid=tarif.tarif_id: self._tarif_sil(tid),
                        renk=RENKLER["hata"]).pack(side="left", padx=2)

    # ─────────────────────────────────────────────
    #  SEKME 2: TARİF EKLE
    # ─────────────────────────────────────────────
    def _ekle_sekmesini_doldur(self):
        """Yeni tarif ekleme formunu oluşturur."""
        # Başlık
        tk.Label(self.ekle_sekmesi, text="Yeni Tarif Ekle",
                 font=YAZI["baslik"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack(pady=15)

        # İki sütunlu form
        form = tk.Frame(self.ekle_sekmesi, bg=RENKLER["bg_koyu"])
        form.pack(fill="both", expand=True, padx=30)

        sol = tk.Frame(form, bg=RENKLER["bg_koyu"])
        sol.pack(side="left", fill="both", expand=True, padx=(0, 10))
        sag = tk.Frame(form, bg=RENKLER["bg_koyu"])
        sag.pack(side="right", fill="both", expand=True)

        # ── Sol sütun: Temel bilgiler ──────────
        alanlar = {}

        def alan_ekle(ebeveyn, etiket, degisken_adi):
            tk.Label(ebeveyn, text=etiket, bg=RENKLER["bg_koyu"],
                     fg=RENKLER["metin"], font=YAZI["normal"]).pack(anchor="w")
            var = tk.StringVar()
            e = tk.Entry(ebeveyn, textvariable=var,
                         bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                         insertbackground=RENKLER["metin"],
                         font=YAZI["normal"], relief="flat")
            e.pack(fill="x", pady=(2, 10), ipady=5)
            alanlar[degisken_adi] = var

        alan_ekle(sol, "Tarif Adı *", "tarif_adi")
        alan_ekle(sol, "Hazırlama Süresi (dk) *", "sure")

        # Kategori seçimi
        tk.Label(sol, text="Kategori *", bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin"], font=YAZI["normal"]).pack(anchor="w")
        kategori_var = tk.StringVar(value="Ana Yemek")
        ttk.Combobox(sol, textvariable=kategori_var,
                     values=TarifPlatformu.KATEGORILER,
                     state="readonly", font=YAZI["normal"]).pack(
            fill="x", pady=(2, 10))
        alanlar["kategori"] = kategori_var

        # Zorluk seçimi
        tk.Label(sol, text="Zorluk *", bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin"], font=YAZI["normal"]).pack(anchor="w")
        zorluk_var = tk.StringVar(value="Orta")
        ttk.Combobox(sol, textvariable=zorluk_var,
                     values=Tarif.ZORLUK_SEVIYELERI,
                     state="readonly", font=YAZI["normal"]).pack(
            fill="x", pady=(2, 10))
        alanlar["zorluk"] = zorluk_var

        # Malzeme ekleme
        tk.Label(sol, text="Malzeme Ekle", bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin"], font=("Segoe UI", 10, "bold")).pack(
            anchor="w", pady=(10, 0))
        malzeme_cerceve = tk.Frame(sol, bg=RENKLER["bg_koyu"])
        malzeme_cerceve.pack(fill="x")

        malzeme_adi_var = tk.StringVar()
        miktar_var = tk.StringVar()
        birim_var = tk.StringVar()

        for etiket, var, gen in [("Adı", malzeme_adi_var, 15),
                                  ("Miktar", miktar_var, 6),
                                  ("Birim", birim_var, 8)]:
            kol = tk.Frame(malzeme_cerceve, bg=RENKLER["bg_koyu"])
            kol.pack(side="left", padx=2)
            tk.Label(kol, text=etiket, bg=RENKLER["bg_koyu"],
                     fg=RENKLER["metin"], font=YAZI["kucuk"]).pack(anchor="w")
            tk.Entry(kol, textvariable=var,
                     bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                     insertbackground=RENKLER["metin"],
                     font=YAZI["normal"], relief="flat",
                     width=gen).pack(ipady=4)

        self.malzeme_listesi_widget = tk.Listbox(
            sol, bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
            font=YAZI["kucuk"], height=6, relief="flat",
            selectbackground=RENKLER["vurgu"])
        self.gecici_malzemeler: list[Malzeme] = []

        def malzeme_ekle_btn():
            ad = malzeme_adi_var.get().strip()
            mkt = miktar_var.get().strip()
            brm = birim_var.get().strip()
            if not ad or not mkt:
                messagebox.showwarning("Uyarı", "Malzeme adı ve miktar zorunlu!")
                return
            m = Malzeme(ad, mkt, brm)
            self.gecici_malzemeler.append(m)
            self.malzeme_listesi_widget.insert("end", m.bilgi())
            malzeme_adi_var.set("")
            miktar_var.set("")
            birim_var.set("")

        self._dugme(sol, "➕ Malzeme Ekle", malzeme_ekle_btn,
                    renk=RENKLER["bg_kart"]).pack(pady=4)
        self.malzeme_listesi_widget.pack(fill="x")

        # ── Sağ sütun: Yapılış adımları ────────
        tk.Label(sag, text="Yapılış Adımları",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")

        adim_var = tk.StringVar()
        tk.Entry(sag, textvariable=adim_var,
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 insertbackground=RENKLER["metin"],
                 font=YAZI["normal"], relief="flat").pack(fill="x", ipady=5)

        self.adim_listesi_widget = tk.Listbox(
            sag, bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
            font=YAZI["kucuk"], height=10, relief="flat",
            selectbackground=RENKLER["vurgu"])
        self.gecici_adimlar: list[str] = []

        def adim_ekle_btn():
            adim = adim_var.get().strip()
            if not adim:
                return
            self.gecici_adimlar.append(adim)
            idx = len(self.gecici_adimlar)
            self.adim_listesi_widget.insert("end", f"{idx}. {adim}")
            adim_var.set("")

        self._dugme(sag, "➕ Adım Ekle", adim_ekle_btn,
                    renk=RENKLER["bg_kart"]).pack(pady=4)
        self.adim_listesi_widget.pack(fill="both", expand=True)

        # Kaydet düğmesi
        def tarif_kaydet():
            """Form verilerini doğrulayıp tarif kaydeder."""
            # Zorunlu alan kontrolü
            if not alanlar["tarif_adi"].get().strip():
                messagebox.showwarning("Uyarı", "Tarif adı zorunlu!")
                return
            try:
                sure = int(alanlar["sure"].get())
            except ValueError:
                messagebox.showwarning("Uyarı", "Süre sayı olmalıdır!")
                return

            # Tarif nesnesi oluştur
            yeni_tarif = Tarif(
                tarif_adi=alanlar["tarif_adi"].get().strip(),
                kategori=alanlar["kategori"].get(),
                hazirlama_suresi=sure,
                zorluk=alanlar["zorluk"].get(),
                ekleyen_id=self.platform.aktif_kullanici.kullanici_id
            )
            # Malzemeleri ekle
            for m in self.gecici_malzemeler:
                yeni_tarif.malzeme_ekle(m)
            # Adımları ekle
            for a in self.gecici_adimlar:
                yeni_tarif.adim_ekle(a)

            self.platform.tarif_ekle(yeni_tarif)
            messagebox.showinfo("Başarılı",
                                f"'{yeni_tarif.tarif_adi}' eklendi!")

            # Formu sıfırla
            for var in alanlar.values():
                var.set("")
            self.gecici_malzemeler.clear()
            self.gecici_adimlar.clear()
            self.malzeme_listesi_widget.delete(0, "end")
            self.adim_listesi_widget.delete(0, "end")

            # Tarif listesini yenile
            self._tarifleri_listele()
            # Alışveriş sekmesini yenile (yeni tarif orada görünmeli)
            self._alisveris_listesi_yenile()
            # İstatistik sekmesini yenile
            self._istatistik_yenile()

        self._dugme(self.ekle_sekmesi, "💾 Tarifi Kaydet",
                    tarif_kaydet, renk=RENKLER["basari"]).pack(pady=15)

    # ─────────────────────────────────────────────
    #  SEKME 3: FAVORİLER
    # ─────────────────────────────────────────────
    def _favoriler_sekmesini_doldur(self):
        """Favori tarif listesini gösterir."""
        tk.Label(self.favoriler_sekmesi, text="❤️ Favori Tariflerim",
                 font=YAZI["baslik"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack(pady=15)

        self._dugme(self.favoriler_sekmesi, "🔄 Yenile",
                    self._favorileri_goster,
                    renk=RENKLER["bg_kart"]).pack()

        self.favori_cerceve = tk.Frame(self.favoriler_sekmesi,
                                       bg=RENKLER["bg_koyu"])
        self.favori_cerceve.pack(fill="both", expand=True, padx=20, pady=10)
        self._favorileri_goster()

    def _favorileri_goster(self):
        """Favori tarifleri kart olarak gösterir."""
        self._cerceve_temizle(self.favori_cerceve)
        favoriler = self.platform.favorileri_getir()

        if not favoriler:
            tk.Label(self.favori_cerceve,
                     text="Henüz favori tarif eklemediniz.\n"
                          "Tarif detayından ❤️ butonuna tıklayın.",
                     bg=RENKLER["bg_koyu"], fg=RENKLER["metin_soluk"],
                     font=YAZI["normal"]).pack(expand=True, pady=50)
            return

        # Kartları ızgara düzeninde göster
        satir = tk.Frame(self.favori_cerceve, bg=RENKLER["bg_koyu"])
        satir.pack(fill="x")
        for i, tarif in enumerate(favoriler):
            if i % 3 == 0 and i != 0:
                satir = tk.Frame(self.favori_cerceve, bg=RENKLER["bg_koyu"])
                satir.pack(fill="x", pady=5)
            self._tarif_karti_olustur(satir, tarif)

    def _tarif_karti_olustur(self, ebeveyn, tarif: Tarif):
        """Tek bir tarif için görsel kart oluşturur."""
        kart = tk.Frame(ebeveyn, bg=RENKLER["bg_kart"],
                        padx=15, pady=12, width=220)
        kart.pack(side="left", padx=8, pady=5, fill="y")
        kart.pack_propagate(False)

        tk.Label(kart, text=tarif.tarif_adi,
                 bg=RENKLER["bg_kart"], fg=RENKLER["vurgu"],
                 font=("Segoe UI", 11, "bold"),
                 wraplength=180).pack(anchor="w")
        tk.Label(kart, text=f"📁 {tarif.kategori}",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=YAZI["kucuk"]).pack(anchor="w")
        tk.Label(kart, text=f"⏱ {tarif.hazirlama_suresi} dk  💪 {tarif.zorluk}",
                 bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                 font=YAZI["kucuk"]).pack(anchor="w")
        tk.Label(kart, text=tarif.puan_yildiz(),
                 bg=RENKLER["bg_kart"], fg=RENKLER["vurgu2"],
                 font=YAZI["kucuk"]).pack(anchor="w", pady=(4, 0))

        self._dugme(kart, "💔 Kaldır",
                    lambda tid=tarif.tarif_id: self._favoriden_cikar(tid),
                    renk=RENKLER["hata"]).pack(pady=(8, 0), fill="x")

    def _favoriye_ekle(self, tarif_id: str):
        """Tarifi favorilere ekler."""
        basari = self.platform.aktif_kullanici.favoriye_ekle(tarif_id)
        if basari:
            messagebox.showinfo("Favoriler", "Tarif favorilere eklendi! ❤️")
            self._favorileri_goster()
        else:
            messagebox.showinfo("Favoriler", "Bu tarif zaten favorilerinizde.")

    def _favoriden_cikar(self, tarif_id: str):
        """Tarifi favorilerden çıkarır."""
        self.platform.aktif_kullanici.favoriden_cikar(tarif_id)
        messagebox.showinfo("Favoriler", "Tarif favorilerden kaldırıldı.")
        self._favorileri_goster()

    # ─────────────────────────────────────────────
    #  SEKME 4: ALIŞVERİŞ LİSTESİ
    # ─────────────────────────────────────────────
    def _alisveris_sekmesini_doldur(self):
        """Alışveriş listesi oluşturma arayüzü."""
        tk.Label(self.alisveris_sekmesi, text="🛒 Alışveriş Listesi",
                 font=YAZI["baslik"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack(pady=15)
        tk.Label(self.alisveris_sekmesi,
                 text="Tarifleri seçin → Malzemeleri birleştir",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin_soluk"],
                 font=YAZI["normal"]).pack()

        icerik = tk.Frame(self.alisveris_sekmesi, bg=RENKLER["bg_koyu"])
        icerik.pack(fill="both", expand=True, padx=20, pady=10)

        # Sol: Çoklu seçim listesi
        sol = tk.Frame(icerik, bg=RENKLER["bg_koyu"])
        sol.pack(side="left", fill="both", expand=True)
        tk.Label(sol, text="Tarif Seç (Ctrl+Click ile çoklu seçim):",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=YAZI["normal"]).pack(anchor="w")

        self.alisveris_liste = tk.Listbox(
            sol, bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
            font=YAZI["normal"], selectmode="multiple",
            selectbackground=RENKLER["vurgu"],
            relief="flat", height=20)
        self.alisveris_liste.pack(fill="both", expand=True)

        # Listeyi doldur
        self.alisveris_tarif_idleri = []
        for tarif in self.platform.tarifler.values():
            self.alisveris_tarif_idleri.append(tarif.tarif_id)
            self.alisveris_liste.insert(
                "end",
                f"{tarif.tarif_adi} ({tarif.hazirlama_suresi} dk)")

        self._dugme(sol, "🛒 Alışveriş Listesi Oluştur",
                    self._alisveris_listesi_goster,
                    renk=RENKLER["basari"]).pack(pady=10, fill="x")

        # Sağ: Sonuç
        sag = tk.Frame(icerik, bg=RENKLER["bg_kart"],
                       padx=20, pady=15, width=300)
        sag.pack(side="right", fill="y", padx=(10, 0))
        sag.pack_propagate(False)
        tk.Label(sag, text="Malzemeler", font=YAZI["alt_bas"],
                 bg=RENKLER["bg_kart"], fg=RENKLER["vurgu"]).pack(anchor="w")

        self.alisveris_sonuc = tk.Text(
            sag, bg=RENKLER["bg_orta"], fg=RENKLER["metin"],
            font=YAZI["normal"], relief="flat", state="disabled")
        self.alisveris_sonuc.pack(fill="both", expand=True, pady=10)

    def _alisveris_listesi_goster(self):
        """Seçili tarifler için alışveriş listesini hesaplar ve gösterir."""
        secimler = self.alisveris_liste.curselection()
        if not secimler:
            messagebox.showwarning("Uyarı", "Lütfen en az bir tarif seçin!")
            return
        secili_idler = [self.alisveris_tarif_idleri[i] for i in secimler]
        alisveris = self.platform.alisveris_listesi_olustur(secili_idler)

        self.alisveris_sonuc.config(state="normal")
        self.alisveris_sonuc.delete("1.0", "end")
        self.alisveris_sonuc.insert("end", "─── ALIŞVERİŞ LİSTESİ ───\n\n")
        for malzeme, miktar in sorted(alisveris.items()):
            self.alisveris_sonuc.insert("end", f"☐  {malzeme}: {miktar}\n")
        self.alisveris_sonuc.config(state="disabled")

    def _alisveris_listesi_yenile(self):
        """
        Yeni tarif eklendiğinde alışveriş listesi kutusu güncellenir.
        Mevcut seçimleri koruyarak yeni eklenen tarifleri listeye dahil eder.
        """
        self.alisveris_liste.delete(0, "end")
        self.alisveris_tarif_idleri.clear()
        for tarif in self.platform.tarifler.values():
            self.alisveris_tarif_idleri.append(tarif.tarif_id)
            self.alisveris_liste.insert(
                "end",
                f"{tarif.tarif_adi} ({tarif.hazirlama_suresi} dk)")

    def _istatistik_yenile(self):
        """
        İstatistik sekmesinin içeriğini sıfırlayıp güncel verilerle yeniden çizer.
        Tarif ekleme/silme veya yeni yorum sonrasında çağrılır.
        """
        self._cerceve_temizle(self.istatistik_sekmesi)
        self._istatistik_sekmesini_doldur()

    # ─────────────────────────────────────────────
    #  SEKME 5: İSTATİSTİKLER
    # ─────────────────────────────────────────────
    def _istatistik_sekmesini_doldur(self):
        """Özet istatistikler paneli. _istatistik_yenile() tarafından tekrar çağrılabilir."""
        # İçerik çerçevesi — yenileme sırasında temizlenmesi için
        cerceve = tk.Frame(self.istatistik_sekmesi, bg=RENKLER["bg_koyu"])
        cerceve.pack(fill="both", expand=True)

        tk.Label(cerceve, text="📊 Platform İstatistikleri",
                 font=YAZI["baslik"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack(pady=15)

        icerik = tk.Frame(cerceve, bg=RENKLER["bg_koyu"])
        icerik.pack(fill="both", expand=True, padx=30)

        # Genel rakamlar
        platform = self.platform
        toplam_tarif = len(platform.tarifler)
        toplam_kullanici = len(platform.kullanicilar)
        toplam_yorum = sum(len(t.degerlendirmeler)
                          for t in platform.tarifler.values())

        istatler = [
            ("📋 Toplam Tarif", toplam_tarif),
            ("👤 Toplam Kullanıcı", toplam_kullanici),
            ("💬 Toplam Yorum", toplam_yorum),
        ]

        kart_satiri = tk.Frame(icerik, bg=RENKLER["bg_koyu"])
        kart_satiri.pack(fill="x", pady=10)
        for baslik, deger in istatler:
            kart = tk.Frame(kart_satiri, bg=RENKLER["bg_kart"],
                            padx=30, pady=20)
            kart.pack(side="left", expand=True, fill="both", padx=10)
            tk.Label(kart, text=str(deger), font=("Segoe UI", 28, "bold"),
                     bg=RENKLER["bg_kart"], fg=RENKLER["vurgu2"]).pack()
            tk.Label(kart, text=baslik, font=YAZI["normal"],
                     bg=RENKLER["bg_kart"], fg=RENKLER["metin"]).pack()

        # En çok puan alan tarifler
        tk.Label(icerik, text="🏆 En Yüksek Puanlı Tarifler",
                 font=YAZI["alt_bas"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin"]).pack(anchor="w", pady=(20, 5))

        en_iyi = platform.en_cok_puan_alan(5)
        for i, tarif in enumerate(en_iyi, 1):
            satir_cerceve = tk.Frame(icerik, bg=RENKLER["bg_kart"],
                                     padx=10, pady=6)
            satir_cerceve.pack(fill="x", pady=2)
            tk.Label(satir_cerceve,
                     text=f"{i}. {tarif.tarif_adi}",
                     bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                     font=YAZI["normal"]).pack(side="left")
            tk.Label(satir_cerceve,
                     text=tarif.puan_yildiz(),
                     bg=RENKLER["bg_kart"], fg=RENKLER["vurgu2"],
                     font=YAZI["normal"]).pack(side="right")

        # Kategori dağılımı
        tk.Label(icerik, text="📁 Kategorilere Göre Dağılım",
                 font=YAZI["alt_bas"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["metin"]).pack(anchor="w", pady=(20, 5))

        # Kategorileri say
        kategori_sayac: dict[str, int] = {}
        for tarif in platform.tarifler.values():
            kategori_sayac[tarif.kategori] = (
                kategori_sayac.get(tarif.kategori, 0) + 1)

        for kat, sayi in sorted(kategori_sayac.items(),
                                 key=lambda x: x[1], reverse=True):
            satir_cerceve = tk.Frame(icerik, bg=RENKLER["bg_koyu"])
            satir_cerceve.pack(fill="x", pady=1)
            tk.Label(satir_cerceve, text=f"  {kat}",
                     bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                     font=YAZI["normal"], width=20, anchor="w").pack(
                side="left")
            # İlerleme çubuğu (basit)
            max_sayi = max(kategori_sayac.values())
            bar_genislik = int((sayi / max_sayi) * 200)
            bar = tk.Frame(satir_cerceve, bg=RENKLER["vurgu"],
                           width=bar_genislik, height=20)
            bar.pack(side="left")
            tk.Label(satir_cerceve, text=f" {sayi}",
                     bg=RENKLER["bg_koyu"], fg=RENKLER["metin_soluk"],
                     font=YAZI["kucuk"]).pack(side="left")

    # ─────────────────────────────────────────────
    #  DEĞERLENDIRME PENCERESİ
    # ─────────────────────────────────────────────
    def _degerlendirme_penceresi(self, tarif: Tarif):
        """Değerlendirme yapmak için açılan modal pencere."""
        pencere = tk.Toplevel(self.root)
        pencere.title(f"Değerlendir: {tarif.tarif_adi}")
        pencere.geometry("400x300")
        pencere.configure(bg=RENKLER["bg_koyu"])
        pencere.grab_set()   # Modal davranış

        tk.Label(pencere, text=f"'{tarif.tarif_adi}'",
                 font=YAZI["alt_bas"], bg=RENKLER["bg_koyu"],
                 fg=RENKLER["vurgu"]).pack(pady=15)
        tk.Label(pencere, text="Puan (1-5):",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=YAZI["normal"]).pack()

        puan_var = tk.IntVar(value=5)
        puan_cerceve = tk.Frame(pencere, bg=RENKLER["bg_koyu"])
        puan_cerceve.pack()
        for i in range(1, 6):
            tk.Radiobutton(puan_cerceve, text=f"{'★'*i}",
                           variable=puan_var, value=i,
                           bg=RENKLER["bg_koyu"],
                           fg=RENKLER["vurgu2"],
                           activebackground=RENKLER["bg_koyu"],
                           font=("Segoe UI", 12),
                           selectcolor=RENKLER["bg_koyu"]).pack(side="left")

        tk.Label(pencere, text="Yorum (isteğe bağlı):",
                 bg=RENKLER["bg_koyu"], fg=RENKLER["metin"],
                 font=YAZI["normal"]).pack(pady=(15, 5))
        yorum_entry = tk.Entry(pencere,
                               bg=RENKLER["bg_kart"], fg=RENKLER["metin"],
                               insertbackground=RENKLER["metin"],
                               font=YAZI["normal"], relief="flat", width=35)
        yorum_entry.pack(ipady=5)

        def gonder():
            basari = tarif.tarif_degerlendir(
                self.platform.aktif_kullanici.kullanici_id,
                puan_var.get(),
                yorum_entry.get().strip())
            pencere.destroy()
            if basari:
                messagebox.showinfo("Teşekkürler",
                                    "Değerlendirmeniz kaydedildi! ⭐")
                self._tarifleri_listele()
                self._detay_paneli_guncelle(tarif)
            else:
                messagebox.showinfo("Bilgi",
                                    "Bu tarifi daha önce değerlendirdiniz.")

        self._dugme(pencere, "⭐ Değerlendirmeyi Gönder",
                    gonder, renk=RENKLER["vurgu2"]).pack(pady=20)

    # ─────────────────────────────────────────────
    #  TARIF SİLME
    # ─────────────────────────────────────────────
    def _tarif_sil(self, tarif_id: str):
        """Onay alıp tarifi siler."""
        cevap = messagebox.askyesno("Tarif Sil",
                                    "Bu tarifi silmek istediğinizden emin misiniz?")
        if cevap:
            basari, mesaj = self.platform.tarif_sil(tarif_id)
            if basari:
                messagebox.showinfo("Silindi", mesaj)
                self._cerceve_temizle(self.detay_panel)
                tk.Label(self.detay_panel, text="Tarif seçin",
                         bg=RENKLER["bg_kart"], fg=RENKLER["metin_soluk"],
                         font=YAZI["alt_bas"]).pack(expand=True)
                self._tarifleri_listele()
            else:
                messagebox.showerror("Hata", mesaj)


# ══════════════════════════════════════════════
#  PROGRAMIN GİRİŞ NOKTASI
# ══════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    uygulama = TarifUygulama(root)
    root.mainloop()