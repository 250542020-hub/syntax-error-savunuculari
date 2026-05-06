# 🔒 Güvenlik Açığı Tarama Raporu — XSS ve SQL Injection Testleri

**Proje:** Akıllı Tarım Yönetim Sistemi
**Ekip:** Syntax Error Savunucuları
**Tarih:** 03.05.2026
**İncelenen dosyalar:** `api/views.py`, `tarim_projesi/settings.py`, `dashboard/views.py`, `dashboard/templates/dashboard/*.html`, `api/validators.py`

---

## 1. Özet

Sistem üzerinde XSS, SQL Injection, yetkilendirme bypass ve information disclosure kategorilerinde testler yapılmıştır. Test scripti `api/test_guvenlik.py` dosyası olarak ekibe sunulmuş ve Django test framework'ü kullanılarak otomatize edilmiştir. Aşağıdaki bulgular tespit edilmiş, her biri için kanıt, önem derecesi ve önerilen düzeltme verilmiştir.

---

## 2. Bulgular Özeti

| # | Açık | Kategori | Konum | Önem | Durum |
|---|------|----------|-------|------|-------|
| 1 | `\|safe` filtresi ile JS context'inde XSS | XSS — Stored | `dashboard/templates/dashboard/dashboard.html:172` | 🔴 Kritik | Açık |
| 2 | Dashboard view'larında authentication yok | Auth Bypass | `dashboard/views.py` | 🔴 Kritik | Açık |
| 3 | `authtoken` `INSTALLED_APPS`'e eklenmemiş | Yapılandırma | `tarim_projesi/settings.py` | 🔴 Kritik | Açık |
| 4 | Token endpoint URL'leri tanımlanmamış | Yapılandırma | `tarim_projesi/urls.py` | 🟠 Yüksek | Açık |
| 5 | Simulator artık çalışmaz hale geldi | Operasyonel | `simulator.py` | 🟠 Yüksek | Açık |
| 6 | DEBUG=True hardcoded | Information Disclosure | `tarim_projesi/settings.py` | 🟠 Yüksek | Açık |
| 7 | API exception generic mesaja çevrildi | Info Disclosure | `api/views.py` | ✅ Çözüldü | Kapatıldı |
| 8 | API IsAuthenticated permission eklendi | Auth | `api/views.py` | ✅ Çözüldü | Kapatıldı |
| 9 | X-Frame-Options, nosniff header'ları | Header Güvenliği | `tarim_projesi/settings.py` | ✅ Çözüldü | Kapatıldı |

---

## 3. Detaylı Bulgular

### 🔴 Bulgu 1 — Stored XSS: `|safe` filtresi (KRİTİK)

**Konum:** `dashboard/templates/dashboard/dashboard.html`, 172. satır civarı:

```django
const grafik_verisi = {{ grafik_verisi|safe }};
```

**Saldırı senaryosu:**
1. Yetkili bir kullanıcı `/sensor-ekle/` formuna gider.
2. `device_id` alanına şu payload girer:
   ```
   </script><script>alert('XSS')</script>
   ```
3. Veri kaydedilir.
4. Bu veriden sonra dashboard'a giren her kullanıcının tarayıcısında JavaScript çalışır. Saldırgan oturum çerezini çalabilir, kullanıcı adına işlem yapabilir.

**Test:** `XSSTestleri.test_03_javascript_context_xss`

**Sebep:** `|safe` filtresi Django'nun otomatik HTML escape mekanizmasını devre dışı bırakır. Bu kullanıcı tarafından girilebilen veride **asla** kullanılmamalıdır. JavaScript context'ine veri basmanın doğru yolu `json_script` etiketidir.

**Çözüm:** Görev 2'de kod ile birlikte verilecek.

---

### 🔴 Bulgu 2 — Yetkilendirme Bypass: Dashboard public (KRİTİK)

**Konum:** `dashboard/views.py` — `dashboard`, `sensor_listesi`, `sensor_ekle`, `sensor_sil` fonksiyonlarının hiçbirinde `@login_required` dekoratörü yok.

**Saldırı senaryosu:**
- Anonim biri `http://siteadresi/` adresine girerek tüm sensör verilerini görebilir.
- `http://siteadresi/sensor-ekle/` adresine POST atarak rastgele veri ekleyebilir (CSRF token aldıktan sonra).
- `http://siteadresi/sensor-sil/<device_id>/` adresine POST atarak veri silebilir.

API tarafına `IsAuthenticated` eklemek API'yi koruyor ama web arayüzü hâlâ tamamen açık. Ekip API'yi kapattı, web tarafını unuttu.

**Test:** `YetkilendirmeTestleri.test_03_dashboard_anonim_erisim`, `test_04_sensor_silme_anonim`

---

### 🔴 Bulgu 3 — Token Authentication aslında çalışmıyor (KRİTİK)

**Konum:** `tarim_projesi/settings.py`

`api/views.py` içinde `TokenAuthentication` kullanılıyor ve global REST_FRAMEWORK config'inde de yer alıyor. **AMA** `'rest_framework.authtoken'` `INSTALLED_APPS` listesine eklenmemiş — yorum satırı olarak bırakılmış. Bu olmadan:
- `Token` modeli veritabanında oluşturulmaz
- `migrate` çalıştırınca authtoken tabloları oluşmaz
- Token tabanlı erişim hata verir

Şu anda sadece `SessionAuthentication` aktif olarak çalışıyor. Yani sensörler/IoT cihazları ve simulator API'ye giriş yapamaz.

---

### 🟠 Bulgu 4 — Token alma endpoint'i yok

`obtain_auth_token` view'ı `urls.py`'a eklenmediği için kullanıcı/cihaz token'i nasıl alacak belirsiz. Token sistemi kurulmuş ama "kapı kilidi var, anahtar dağıtım mekanizması yok".

---

### 🟠 Bulgu 5 — `simulator.py` çalışmaz hale geldi

API endpoint'lerine `IsAuthenticated` eklendiği için simulator artık 401 alır. POST gönderirken Authorization header eklemiyor. Görev 2'de bu da düzeltilecek.

---

### 🟢 SQL Injection — Risk yok (Django ORM koruması yeterli)

**Test sonuçları:** `SQLInjectionTestleri` paketindeki dört test de geçer.

`dashboard/views.py` içindeki tüm filtreler Django ORM üzerinden parametreli sorgu ile çalışıyor:
```python
veriler = veriler.filter(device_id__icontains=cihaz)
veriler = veriler.filter(timestamp__date__gte=baslangic)
```

Ham SQL (`raw()`, `extra()`, `cursor.execute()`) kullanılmadığı için klasik SQL injection saldırıları (`'; DROP TABLE`, `' OR 1=1`) ORM tarafından otomatik escape ediliyor. `api/validators.py` da ek bir tip ve aralık kontrolü yapıyor.

**Tavsiye:** İleride raw SQL kullanılması durumunda **mutlaka** `cursor.execute(sql, [params])` formatında parametreli sorgu kullanılmalı, string formatlamayla SQL inşa edilmemeli.

---

### 🟢 CSRF — Form'larda token mevcut

`sensor_ekle.html` ve `sensor_listesi.html`'de `{% csrf_token %}` etiketi var, Django middleware aktif. CSRF koruması çalışıyor.

---

### 🟢 Information Disclosure — Düzeltildi

`api/views.py` içinde exception handler `str(e)` yerine generic mesaj döndürmeye çevrildi. Bu, Django'nun stack trace'i ya da veritabanı hata detaylarını saldırgana sızdırmasını engelliyor.

```python
# ÖNCE (kötü):
return Response({"hata": str(e)}, status=400)

# SONRA (iyi):
return Response({"hata": "Veri formatı hatalı veya eksik."}, status=400)
```

---

## 4. Önem Derecelendirme Açıklaması

- 🔴 **Kritik:** Anonim saldırgan tarafından doğrudan istismar edilebilir, veri sızıntısı/değişimi/sistem ele geçirme riski.
- 🟠 **Yüksek:** Sistemin çalışmasını etkiler veya saldırı yüzeyini genişletir.
- 🟡 **Orta:** Best practice ihlali, doğrudan istismar zor.

---

## 5. Test Çalıştırma Talimatı

```bash
# Önce test_guvenlik.py'yi api/ klasörüne kaydet, sonra:
python manage.py test api.test_guvenlik

# Sadece XSS testlerini çalıştırmak için:
python manage.py test api.test_guvenlik.XSSTestleri

# Detaylı çıktı ile:
python manage.py test api.test_guvenlik -v 2
```

Şu an test paketi çalıştırılırsa **6 test başarısız olacak** — bunlar Bulgu 1, 2, 3 ve ilişkili maddeleri ortaya çıkarır. Görev 2'deki düzeltmeler uygulandıktan sonra tüm testler geçmelidir.

---

## 6. Sonuç

Ebubekir'in API tarafında yaptığı `IsAuthenticated` ve generic exception düzenlemeleri doğru yöndeydi ancak sistem hâlâ **3 kritik açık** ile çalışıyor. Görev 2 kapsamında bu açıklar kapatılacaktır.
