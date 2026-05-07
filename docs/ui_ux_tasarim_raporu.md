# 🎨 Web Tabanlı Yönetim Paneli — UI/UX Tasarım Raporu

**Proje:** Akıllı Tarım Yönetim Sistemi
**Ekip:** Syntax Error Savunucuları
**Tarih:** 03.05.2026
**İlgili dosyalar:** `wireframes.html`, `mockup.html`

---

## 1. Genel Bakış

Akıllı Tarım Yönetim Paneli, ziraatçı ve sistem yöneticilerinin tarladaki IoT sensörlerden gelen sıcaklık, hava nemi ve toprak nemi verilerini gerçek zamanlı izleyebilmesi için tasarlanmış bir web arayüzüdür. Bu rapor, panelin bilgi mimarisini, kullanıcı akışlarını, ekran tasarımlarını ve tasarım kararlarını dokümante eder.

## 2. Hedef Kullanıcı

- **Birincil:** Ziraatçı / tarla yöneticisi — sahaya çıkmadan tarladaki nem ve sıcaklık durumunu masa başından izlemek ister.
- **İkincil:** Sistem yöneticisi (admin) — sensör cihazlarını yönetir, manuel veri girişi yapar, gerekirse cihaz siler.

Kullanıcının teknik bilgisi sınırlıdır; arayüz **görsel ağırlıklı**, az metin içeren ve **tek bakışta durumu özetleyen** olmalıdır.

## 3. Bilgi Mimarisi

Sistemde dört temel sayfa bulunur:

1. **Giriş (Login)** — Kimlik doğrulama
2. **Dashboard (Ana Sayfa)** — Anlık durum özeti, grafikler ve son veri tablosu
3. **Sensör Listesi** — Tüm cihazların kart bazlı listesi
4. **Manuel Veri Girişi** — Test/manuel ölçüm formu

### Sayfa hiyerarşisi

```
[Login]
   ↓ (giriş başarılı)
[Dashboard] ←──→ [Sensör Listesi] ←──→ [Manuel Veri Girişi]
   ↑                                          ↓
   └──────────── (kayıt başarılı) ────────────┘
```

Tüm sayfalar arasında navbar üzerinden gezinme mümkün; "Ana Sayfa", "Sensörler", "Veri Ekle" butonları her sayfada bulunur. Sağ üst köşede çıkış (logout) butonu vardır.

## 4. Kullanıcı Akışları

### Akış A: İlk Giriş ve Durum İncelemesi
1. Kullanıcı `/giris/` adresine gelir → Login formunu görür.
2. Kullanıcı adı + şifre girer → Dashboard'a yönlendirilir.
3. Dashboard'da 4 stat kartı (Sıcaklık, Hava Nemi, Toprak Nemi, Toplam Veri) anlık değerleri gösterir.
4. Aşağıda iki grafik (sıcaklık trendi + nem trendi) ve son sensör verileri tablosu vardır.
5. Kullanıcı tarih/cihaz filtresiyle veriyi daraltabilir.

### Akış B: Sensör Yönetimi
1. Dashboard navbar'ından **Sensörler**'e tıklar → Sensör Listesi sayfası açılır.
2. Kart bazlı liste görür; her kartta cihaz ID, durum (badge), son ölçüm değerleri özet, "Detay" ve "Sil" butonları bulunur.
3. Arama kutusu ile cihaz ID'ye göre filtreler.
4. Bir cihazı silmek için **Sil** butonuna basar — onay ister, onaylanınca silinir.

### Akış C: Manuel Veri Ekleme
1. Navbar'daki **Veri Ekle** butonuyla forma gelir.
2. Cihaz ID + 3 sayısal değer girer.
3. Geçersiz değer girerse form üstünde uyarı görür (kırmızı alert).
4. Doğru veri ise **Kaydet** ile dashboard'a yönlendirilir, en üstte yeni kayıt görünür.

## 5. Tasarım Kararları

### Renk Sistemi

| Token | Hex | Kullanım |
|-------|-----|----------|
| `--primary` | `#2e7d32` | Navbar, butonlar, vurgu |
| `--primary-dark` | `#1b5e20` | Hover, koyu vurgu |
| `--primary-light` | `#e8f5e9` | İkon arkaplanları, hafif vurgu |
| `--success-bg` | `#c8e6c9` | "İdeal" durum badge'i |
| `--warning-bg` | `#ffe0b2` | "Sulama Gerekli" badge'i |
| `--danger-bg` | `#ffcdd2` | "Aşırı Doygun" badge'i |
| Body | `#f0f7f0` | Sayfa arkaplanı (hafif yeşil tint) |

Yeşil ana renk seçildi çünkü:
- Tarım/doğa ile semantik uyum
- Bootstrap'in default mavisinden ayrışarak markaya kimlik kazandırır
- Yeşilin koyu tonu yüksek kontrast ile erişilebilirlik (WCAG AA) sağlar

### Tipografi
- **Başlıklar:** Bootstrap default sistem fontları (`-apple-system`, `Segoe UI`, `Roboto`), `font-weight: 700`
- **Body:** Aynı font ailesi, `font-weight: 400`
- **Sayısal değerler (sensör verileri):** `fs-3 fw-bold` ile büyük ve kalın gösterilir, hızlı taranabilirlik için.

### Spacing ve Grid
- Bootstrap 5 grid sistemi (`container-fluid`, `row g-3`)
- Kartlar arası gap: `1rem`
- Kart içi padding: `1.5rem` (`p-4`)
- Stat kartları desktop'ta 4 kolon, tablette 2 kolon, mobilde 2x2

### İkonografi
- **Bootstrap Icons** kütüphanesi (zaten projede yüklü)
- Sıcaklık → `bi-thermometer-half`
- Hava nemi → `bi-droplet-half`
- Toprak nemi → `bi-moisture`
- Sensör → `bi-broadcast` veya `bi-cpu`
- Logo → `bi-flower1`

### Etkileşim ve Hareket
- **Stat kartları:** Hover'da hafif kalkma animasyonu (`translateY(-2px)`) ve gölge derinleşmesi.
- **Sensör kartları:** Hover'da daha belirgin yükselme (`translateY(-3px)`) — tıklanabilirliği işaret eder.
- **Butonlar:** Bootstrap default transition'ları kullanılır (200ms).
- **Geçişler:** Sayfalar arası SPA değil, klasik Django render — performans yeterli.

### Durum Göstergeleri (Status Badges)
Sistem 3 durum tanımlar — anında anlaşılır olması için renk + ikon kombinasyonu kullanılır:

| Durum | Koşul | Görünüm |
|-------|-------|---------|
| 🌾 İdeal | Toprak nemi 30-70% arası | Yeşil pill badge |
| ⚠️ Sulama Gerekli | Toprak nemi < 30% | Turuncu pill badge |
| 🛑 Aşırı Doygun | Toprak nemi > 70% | Kırmızı pill badge |

Sadece renk değil, emoji ve metin de kullanılır — renk körlüğü olan kullanıcılar için erişilebilirlik artar.

## 6. Responsive Tasarım

Üç kırılma noktası tasarım baz alınmıştır:

- **Mobil (< 768px):** Stat kartları 2x2 grid; grafikler tam genişlik üst üste; tablo yatay kaydırma; navbar butonları sadece ikon.
- **Tablet (768px–992px):** Stat kartları 2x2 grid; grafikler tam genişlik; sensör kartları 2 kolon.
- **Desktop (≥ 992px):** Stat kartları 4 kolon; grafikler yan yana 2 kolon; sensör kartları 3 kolon.

## 7. Mevcut Durumdan Farklar (Yenileme Özeti)

Mevcut `dashboard.html` çalışır halde ama bazı iyileştirmeler getiriyoruz:

| Eksik | Yeni |
|-------|------|
| Stat kartlarında sadece sayı | Sayı + ikon + trend göstergesi (▲/▼) |
| "Hoş geldin" ya da kullanıcı adı yok | Sağ üstte oturum bilgisi + çıkış butonu |
| Filtre butonları text-only | İkonlu, daha küçük, kompakt |
| Tablo durum sütunu sade metin | Renkli pill badge'ler ile durum |
| Sensör listesi düz tablo (alfabetik) | Kart bazlı grid, son ölçüm değerleri özetli |
| Form'da hata yeri belirsiz | Üstte alert + alanların altında inline hata |
| Form'da aralık bilgisi yok | Mavi info kutusu ile geçerli aralıklar gösterilir |
| Logout butonu yok | Navbar sağda var |

## 8. Erişilebilirlik (a11y) Notları

- Tüm form input'larında label var (`<label>` etiketi `<input>` ile bağlı)
- Renk + ikon + metin: durumu sadece renkle ifade etmedik
- Kontrast oranları WCAG AA (en az 4.5:1) standartlarında
- Klavye navigasyonu: tab sırası mantıklı, focus ring görünür
- Buton + linklerde aria-label önerileri (icon-only butonlarda)

## 9. Teslim Edilen Dosyalar

1. **`wireframes.html`** — 4 sayfanın düşük detaylı SVG wireframe'leri tek dosyada (rapor + sunum için)
2. **`mockup.html`** — Tarayıcıda açılabilen, sayfalar arası gezinilebilir tam görsel mockup
3. **`ui_ux_tasarim_raporu.md`** — Bu doküman

## 10. Sonraki Adımlar

1. Mockup'taki tasarımı mevcut `dashboard/templates/` altındaki Django template'lerine entegre et:
   - `dashboard.html` → Yeni stat kartlar, navbar, badge'ler
   - `sensor_listesi.html` → Tablo yerine kart grid
   - `sensor_ekle.html` → Bilgi kutusu ve daha temiz form
2. Mockup'ta gösterilen "trend göstergeleri" (▲ 0.8°C) için view'da önceki/sonraki ölçüm farkı hesaplanmalı
3. Sensör listesi için her kartın "Detay" butonu yeni bir endpoint gerektirir (`/sensorler/<device_id>/`) — bu opsiyonel, ileri görev olarak planlanabilir.
