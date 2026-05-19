# 🌱 Akıllı Tarım Yönetim Sistemi

## 👥 Grup Üyeleri
- **Ahmet Enes Altun**  
- **Hayat Ay**  
- **Sami Yusuf Yıldız**  
- **Ebubekir Yılmaz**  
- **Ceren Çam** 

---

# 📌 Proje Açıklaması

Bu proje, sensör verileri ve yapay zeka kullanarak tarım süreçlerini optimize etmeyi amaçlamaktadır.

Toprak nemi, sıcaklık ve hava durumu gibi veriler analiz edilerek sulama, gübreleme ve ilaçlama işlemleri daha verimli bir şekilde yönetilecektir.

Sistem, tarım alanından toplanan verileri analiz ederek çiftçilere doğru kararlar almalarında yardımcı olur. Böylece hem verimlilik artırılır hem de su ve gübre gibi kaynakların gereksiz kullanımı azaltılır.

---

# 🛠️ Kullanılan Teknolojiler

- Python  
- TensorFlow  
- IoT Sensörleri  
- Django  
- PostgreSQL  
- MQTT  

---

# 📦 Teslim Edilecek Modüller

- Sensör veri toplama modülü  
- Yapay zeka tabanlı analiz motoru  
- Web tabanlı yönetim paneli  
- Mobil uygulama  

---

# 🏗️ Proje Mimari Tasarımı (Ahmet Enes Altun)

## 📝 Genel Mimari

Akıllı Tarım Yönetim Sistemi, tarım alanına yerleştirilen IoT sensörlerinden veri toplayan, bu verileri analiz eden ve kullanıcıya web veya mobil uygulama üzerinden sunan bir sistemdir.

### Sistem çalışma akışı

- IoT sensörleri çevresel verileri toplar  
- Toplanan veriler Django API aracılığıyla sunucuya iletilir  
- Veriler PostgreSQL veritabanında saklanır  
- TensorFlow tabanlı yapay zeka modeli verileri analiz eder  
- Analiz sonuçları web paneli ve mobil uygulama üzerinden kullanıcıya sunulur  

---

## 🔧 Sistem Modülleri

- Sensör Veri Toplama Modülü  
- Veri İşleme ve Depolama Modülü  
- Yapay Zeka Analiz Modülü  
- Web Yönetim Paneli  
- Mobil Uygulama  

---

## 🧩 Bileşenler Arasındaki İlişki

IoT Sensörleri → Django API → PostgreSQL Veritabanı → TensorFlow Analiz Motoru → Web Paneli / Mobil Uygulama

Sensörlerden gelen veriler backend tarafından alınır, veritabanında saklanır ve yapay zeka motoru ile analiz edilerek kullanıcılara öneriler sunulur.

---

## 🏛️ Kullanılan Tasarım Desenleri

### Katmanlı Mimari (Layered Architecture)

Sistem aşağıdaki katmanlardan oluşmaktadır:

- Veri Katmanı  
- İş Mantığı Katmanı  
- Sunum Katmanı  

Bu yapı sayesinde sistem daha düzenli, sürdürülebilir ve geliştirilebilir hale gelir.

### MVT (Model-View-Template)

Django frameworkü backend geliştirilmesinde **MVT mimarisini** kullanır.

- **Model:** Veritabanı yapısını temsil eder  
- **View:** İş mantığını yönetir  
- **Template:** Kullanıcıya gösterilen arayüzü oluşturur  

---

## 📊 Mimari Diyagram

![Akıllı Tarım Mimari Diyagramı](architecture.png)

---

## ✅ Sonuç

Bu mimari yapı sayesinde sistem sensörlerden gelen verileri analiz ederek tarım süreçlerini optimize eder. Modüler yapı sayesinde sistemin geliştirilmesi ve ileride genişletilmesi kolaydır.

---

# 🏗️ Teknoloji Araştırması ve Seçim Gerekçeleri (Ebubekir Yılmaz)

## 1. Programlama Dili: Python

Projenin ana geliştirme dili olarak **Python 3.10+** seçilmiştir.

**Neden?**  
IoT cihazlarından veri çekme, TensorFlow ile yapay zeka modeli eğitme ve Django ile web sunucusu geliştirme süreçlerinin tamamını tek bir dil ekosisteminde birleştirmek mümkündür.

**Gerekçe:**  
Python geniş kütüphane desteğine sahiptir. Sensör verisi işleme için **Pandas**, matematiksel hesaplamalar için **NumPy** gibi güçlü araçlar sağlar.

---

## 2. Backend Framework: Django & Django REST Framework

Sistem mimarisinin web uygulama çatısı olarak **Django** tercih edilmiştir.

**Neden?**  
Kullanıcı yönetimi, admin paneli ve güvenli veritabanı erişimi gibi özellikleri hazır olarak sunar.

**Gerekçe:**  
Django REST Framework sayesinde sensör cihazları ve mobil uygulamalar için API geliştirmek kolaylaşır.

---

## 3. Veritabanı: PostgreSQL

Veri depolama birimi olarak **PostgreSQL** seçilmiştir.

**Neden?**  
Büyük veri setlerini güvenli ve performanslı şekilde yönetebilir.

**Gerekçe:**  
Sensörlerden gelen veriler düzenli şekilde saklanabilir ve analiz süreçlerinde kolayca kullanılabilir.

---

## 4. Yapay Zeka: TensorFlow

Analiz motoru için **TensorFlow** kullanılacaktır.

**Neden?**  
Makine öğrenmesi ve veri analizi için güçlü bir altyapı sunar.

**Gerekçe:**  
Sensör verileri kullanılarak sulama veya gübreleme önerileri üretilebilir.

---

## 5. IoT İletişim Protokolü: MQTT

Sensörler ile sunucu arasındaki veri iletişimi için **MQTT protokolü** kullanılacaktır.

**Neden?**  
Düşük bant genişliği kullanır ve IoT cihazları için optimize edilmiştir.

**Gerekçe:**  
Tarım alanlarında bulunan sensörlerin düşük enerji tüketimi ile veri göndermesini sağlar.

---

## 📊 Özet Karşılaştırma Tablosu

| Bileşen | Seçilen Araç | En Büyük Avantajı |
| :--- | :--- | :--- |
| **Dil** | Python 3.10+ | Ekosistem birliği (AI + Web + Scripting) |
| **Veri Analizi** | Pandas / NumPy | Sensör verilerini temizleme ve işleme hızı |
| **Haberleşme** | MQTT / WebSockets | Gerçek zamanlı veri akışı ve düşük enerji tüketimi |
| **Deployment** | Docker | Ortam bağımsız, hızlı ve hatasız kurulum |

## 📋 Proje Kapsam Belgesi (Hayat Ay)
##  1. Proje Tanımı:
Akıllı Tarım Yönetim Sistemi, tarım alanlarından IoT sensörleri aracılığıyla toplanan verileri analiz ederek
çiftçilere daha verimli ve sürdürülebilir tarım yönetimi sunmayı amaçlayan bir yazılım sistemidir. Sistem,
çevresel verileri toplayarak analiz eder ve kullanıcıya web veya mobil arayüz üzerinden anlamlı bilgiler sağlar.
Toplanan veriler merkezi bir sistemde saklanır ve yapay zeka destekli analizler ile değerlendirilir. Böylece kullanıcılar tarım faaliyetlerini daha bilinçli ve verimli şekilde yönetebilir.

##  2. Projenin Amacı
Bu projenin amacı, tarım alanlarında kullanılan sensörlerden elde edilen verileri dijital ortamda analiz ederek çiftçilere karar destek sistemi sunmaktır.
## Projenin temel hedefleri şunlardır:
* Tarımsal verilerin otomatik olarak toplanması
* Verilerin güvenli şekilde saklanması
* Yapay zeka algoritmaları ile analiz edilmesi
* Kullanıcıların web veya mobil arayüz üzerinden verilere erişebilmesi
* Tarımsal verimliliğin artırılması

## 3. Kullanılan Teknolojiler
## Projenin geliştirilmesinde aşağıdaki teknolojiler kullanılacaktır:
* Python: Sistem geliştirme ve veri işleme süreçlerinde ana programlama dili olarak kullanılacaktır.
* TensorFlow: Sensörlerden gelen verilerin analiz edilmesi ve tahmin modellerinin oluşturulması için kullanılacaktır.
* IoT Sensörleri: Tarım alanından sıcaklık, nem ve diğer çevresel verileri toplamak için kullanılacaktır.
* Django: Web tabanlı API ve yönetim panelinin geliştirilmesi için kullanılacaktır.
* PostgreSQL: Sensör verilerinin güvenli ve düzenli şekilde saklanması için veritabanı sistemi olarak kullanılacaktır.

## 4. Proje Kapsamı
## ✅ Kapsama Dahil Olan Özellikler
* IoT sensörlerinden veri toplanması
* Sensör verilerinin API aracılığıyla sisteme gönderilmesi
* Verilerin PostgreSQL veritabanında saklanması
* Python ve TensorFlow kullanılarak veri analizi yapılması
* Django tabanlı web arayüzü üzerinden verilerin görüntülenmesi
* Kullanıcıların sisteme giriş yapabilmesi
* Sistem yöneticisinin verileri yönetebilmesi

## ❌ Kapsama Dahil Olmayan Özellikler
* Sensör donanımının fiziksel üretimi
* Ağır tarım makinelerinin doğrudan kontrol edilmesi
* Ticari ölçekli büyük tarım işletmeleri için özel modüller

## 5. Proje Paydaşları
Paydaş                          Açıklama
* Çiftçiler	        |         Sistemi kullanarak tarım verilerini takip eder
* Sistem            |         Yöneticisi	Sistemi yönetir ve kontrol eder
* Yazılım Geliştiriciler	|   Sistemin geliştirilmesini sağlar
* Proje Ekibi            |   	Projenin planlanması ve uygulanmasından sorumludur

## 6. Sonuç
Akıllı Tarım Yönetim Sistemi, IoT sensörleri ve yapay zeka teknolojilerini bir araya getirerek tarım verilerinin daha verimli şekilde analiz edilmesini sağlamayı amaçlamaktadır. Bu sistem sayesinde çiftçiler çevresel verileri daha kolay takip edebilecek ve tarım süreçlerini daha verimli şekilde yönetebilecektir.

---

## ⚙️ Geliştirme Ortamı Kurulumu (Ceren Çam)

## Geliştirme Ortamı
Akıllı Tarım Yönetim Sistemi projesinin geliştirme sürecinde kullanılacak yazılım araçları ve bağımlılıklar belirlenmiş ve geliştirme ortamı yapılandırılmıştır. Bu ortam, ekip üyelerinin aynı teknolojileri kullanarak proje üzerinde çalışabilmesini sağlar.

## Kullanılan Geliştirme Araçları

## 1. IDE (Kod Geliştirme Ortamı)
Projenin geliştirilmesi için Visual Studio Code (VS Code) kullanılacaktır.

VS Code;
- Python geliştirme desteği sunar
- Git ile entegre çalışabilir
- Django projeleri için uygun bir geliştirme ortamı sağlar

## 2. Programlama Dili
Projenin geliştirilmesinde ana programlama dili olarak Python 3.10+ kullanılacaktır.

Python;
- sensör verilerinin işlenmesi
- yapay zeka modellerinin geliştirilmesi
- backend servislerinin oluşturulması

gibi işlemler için kullanılacaktır.

## 3. Backend Framework
Web tabanlı yönetim paneli ve API geliştirme süreçleri için Django frameworkü kullanılacaktır.
API geliştirme sürecinde ayrıca Django REST Framework (DRF) kullanılacaktır.

## 4. Yapay Zeka ve Veri Analizi Kütüphaneleri
Sensörlerden elde edilen verilerin analiz edilmesi için TensorFlow kullanılacaktır.
Veri işleme ve analiz süreçlerinde aşağıdaki Python kütüphaneleri kullanılacaktır:
- NumPy
- Pandas

Bu kütüphaneler sensör verilerinin işlenmesi ve analiz edilmesi için kullanılacaktır.

## 5. Veritabanı Sistemi
Projenin veri depolama sistemi olarak PostgreSQL veritabanı kullanılacaktır.

PostgreSQL;
- sensör verilerinin saklanması
- kullanıcı bilgilerinin tutulması
- analiz sonuçlarının depolanması

için kullanılacaktır.

## 6. IoT İletişim Protokolü
Tarım alanında bulunan sensörler ile sistem arasındaki veri iletişimi için MQTT protokolü kullanılacaktır.

MQTT;
- düşük enerji tüketimi
- hızlı veri iletimi
- IoT cihazları ile uyumlu yapı

gibi avantajlar sağlar.

## 7. Versiyon Kontrol Sistemi
Projenin kaynak kodlarının yönetilmesi için Git ve GitHub kullanılmaktadır.

Git;
- ekip üyelerinin aynı proje üzerinde birlikte çalışmasını sağlar
- yapılan değişikliklerin takip edilmesini sağlar
- proje sürümlerinin kontrol edilmesine yardımcı olur

Proje deposu GitHub üzerinde oluşturulmuş ve ekip üyeleri projeye dahil edilmiştir.

## 8. AI Destekli Geliştirme Araçları
Proje geliştirme sürecinde bazı modüllerin oluşturulması ve prototip geliştirme aşamalarında Antigravity AI aracı kullanılacaktır.

Antigravity;
- proje modüllerinin hızlı şekilde oluşturulması
- prototip geliştirme süreçlerinin hızlandırılması
- yazılım geliştirme sürecinin desteklenmesi

amacıyla kullanılmaktadır.

## 9. Container / Deployment Aracı

Projenin farklı sistemlerde çalıştırılabilmesi ve taşınabilirliğinin sağlanması için Docker kullanılacaktır.

Docker;
- uygulamanın farklı işletim sistemlerinde çalışması
- proje ortamını ekip üyeleri arasında standartlaştırması
- ileride deployment süreçlerini kolaylaştırması

amacıyla kullanılacaktır.

## Sonuç
Belirlenen geliştirme ortamı sayesinde ekip üyeleri aynı araçları kullanarak proje üzerinde çalışabilir. Bu ortam, yazılım geliştirme sürecinin düzenli ilerlemesini ve ekip içi iş birliğinin sağlanmasını kolaylaştırır.

---

## 📱 Mobil Uygulama İşlevsellik Tanımı (Ceren Çam)

Bu belge, Akıllı Tarım Yönetim Sistemi'nin mobil uygulama bileşeninin temel işlevlerini, kullanıcı erişim kapsamını ve genel uygulama akışını tanımlamak amacıyla hazırlanmıştır. Mobil uygulama, çiftçilerin tarla başında olmaksızın sistemlerini anlık olarak takip edebilmelerini sağlayan kritik bir bileşendir.

---

### Mobil Uygulamanın Amacı

Mobil uygulama; IoT sensörlerinden toplanan tarım verilerini çiftçiye akıllı telefon üzerinden sunmayı, sulama ve gübreleme gibi temel tarımsal işlemlerin takibini kolaylaştırmayı ve yapay zeka destekli önerileri anlık olarak iletmeyi hedeflemektedir.

---

### Hedef Kullanıcılar

| Kullanıcı Rolü | Açıklama |
|---|---|
| **Çiftçi** | Tarlasının sensör verilerini takip eder, sistem önerilerini görüntüler |
| **Sistem Yöneticisi** | Tüm tarla ve sensör verilerini izler, gerektiğinde müdahale eder |

---

### Kullanıcıların Erişebileceği Bilgiler

Mobil uygulama üzerinden kullanıcılar aşağıdaki verilere erişebilecektir:

- **Toprak Nemi:** Anlık toprak nem yüzdesi ve tarihsel değişim grafiği
- **Hava Sıcaklığı:** Tarla konumuna özgü sıcaklık verisi
- **Hava Nemi:** Çevresel nem oranı
- **Sulama Durumu:** Aktif sulama sistemi açık/kapalı bilgisi ve geçmiş sulama kayıtları
- **Gübreleme Takibi:** Planlanan ve gerçekleşen gübreleme işlemlerinin listesi
- **Yapay Zeka Önerileri:** TensorFlow analiz motorunun ürettiği sulama ve gübreleme tavsiyeleri
- **Sensör Durumu:** Tarlaya bağlı sensörlerin aktiflik bilgisi

---

### Kullanıcıların Gerçekleştirebileceği İşlemler

#### Kimlik Doğrulama
- Kullanıcı adı ve şifre ile güvenli giriş yapma
- Oturumu kapatma

#### Tarla ve Sensör Yönetimi
- Kayıtlı tarlalarını listeleme ve seçme
- Seçili tarlaya ait aktif sensörleri görüntüleme
- Sensör verilerini anlık veya geçmişe yönelik filtreleyerek inceleme

#### Sulama Kontrolü
- Otomatik sulama eşiğinin (örn: %30 toprak nemi) mevcut durumunu görüntüleme
- Sulama sisteminin ne zaman devreye girdiğini geçmiş kayıtlardan takip etme

#### Gübreleme Takibi
- Geçmiş gübreleme işlemlerini tarihe göre listeleme
- Yapay zeka tarafından önerilen bir sonraki gübreleme zamanını görüntüleme

#### Analiz ve Raporlar
- Son 7 günlük nem ve sıcaklık ortalamalarını kart yapısında görüntüleme
- TensorFlow analiz motorundan gelen istatistiksel özeti (ortalama, medyan, standart sapma) okuma

#### Bildirimler
- Toprak nemi kritik seviyenin altına düştüğünde anlık uyarı alma
- Sistem tarafından önerilen işlem bildirimleri

---

### Genel Uygulama Akışı

Uygulama Açılışı → Giriş Ekranı (Kullanıcı adı + Şifre) → Kimlik Doğrulama (Django REST API)

- Kimlik doğrulama **başarısız** ise → Hata mesajı gösterilir, kullanıcı tekrar deneyebilir
- Kimlik doğrulama **başarılı** ise → Ana Ekran / Dashboard açılır

Dashboard üzerinden erişilebilen akışlar:

- Tarla Seç → Sensör Listesi → Sensör Detayı
- Sulama Durumu → Geçmiş Kayıtlar
- Gübreleme Takibi → Öneri Görüntüle
- Analiz Raporu → İstatistiksel Özet
- Bildirimler → Kritik Uyarı Detayı

---

### API Entegrasyonu

Mobil uygulama, Django REST Framework üzerinden geliştirilen backend ile aşağıdaki uç noktalar aracılığıyla iletişim kurar:

| Endpoint | Metot | İşlev |
|---|---|---|
| `/api/sensor-data/` | GET | Anlık sensör verilerini çeker |
| `/api/analysis/` | GET | Son 100 verinin istatistiksel analizini getirir |
| `/api/token/` | POST | Kullanıcı girişi ve token alımı (DRF `obtain_auth_token`) |

---

### Arayüz Tasarım Kararları

Mobil uygulama arayüzü aşağıdaki tasarım ilkeleri benimsenerek planlanmıştır:

- **Renk paleti:** Tarım temasıyla uyumlu yeşil ve beyaz tonları
- **Font:** Arial — okunabilirlik öncelikli
- **Kart yapısı:** Her veri türü ayrı bir kart bileşeninde gösterilir
- **Responsive:** Farklı ekran boyutlarıyla uyumlu düzen
- **Sade navigasyon:** Alt menü çubuğu ile Dashboard, Sensörler, Analiz ve Ayarlar sayfaları arasında geçiş

---

### Sonuç

Bu işlevsellik tanımı belgesi, mobil uygulama geliştirme sürecine yol göstermek amacıyla hazırlanmıştır. Belirlenen işlevler, kullanıcı hikayeleri ve sistem gereksinimleriyle uyumlu olup projenin genel mimarisine entegre biçimde tasarlanmıştır. Mobil uygulama, Django REST API üzerinden veri alarak çiftçilere her yerden erişim imkânı sunacaktır.

---

## 📋 Gereksinim Toplama ve Analizi (Sami Yusuf Yıldız)

Yazılım projelerinde gereksinim toplama ve analiz aşaması, sistemin doğru şekilde tasarlanması ve geliştirilmesi için en önemli adımlardan biridir. Bu aşamada sistemin hangi ihtiyaçlara çözüm üreteceği, kullanıcıların sistemden beklentileri ve sistemin yerine getirmesi gereken işlevler detaylı bir şekilde incelenmiştir. Projenin bu bölümünde Akıllı Tarım Yönetim Sistemi için gerekli olan fonksiyonel ve fonksiyonel olmayan gereksinimler belirlenmiş ve analiz edilmiştir.

Gereksinim toplama sürecinde tarım sektöründeki temel ihtiyaçlar araştırılmış, özellikle çiftçilerin tarımsal verileri daha verimli kullanabilmesi için gerekli olan sistem özellikleri değerlendirilmiştir. IoT sensörlerinden elde edilen verilerin analiz edilmesi, saklanması ve kullanıcıya anlamlı bilgiler halinde sunulması projenin temel gereksinimleri arasında yer almaktadır. Ayrıca sistemin hem web hem de mobil platformlar üzerinden erişilebilir olması hedeflenmiştir.

## Fonksiyonel Gereksinimler

Fonksiyonel gereksinimler, sistemin kullanıcılar için yerine getirmesi gereken temel işlevleri ifade eder. Proje kapsamında belirlenen başlıca fonksiyonel gereksinimler şunlardır:

- Tarım alanlarına yerleştirilen IoT sensörleri aracılığıyla sıcaklık, nem ve toprak verilerinin toplanması
- Sensörlerden elde edilen verilerin sistem sunucusuna gönderilmesi
- Toplanan verilerin PostgreSQL veritabanında güvenli şekilde saklanması
- Yapay zeka algoritmaları kullanılarak sensör verilerinin analiz edilmesi
- Analiz sonuçlarının kullanıcıya web paneli veya mobil uygulama aracılığıyla sunulması
- Kullanıcıların sisteme güvenli bir şekilde giriş yapabilmesi ve kendi verilerini görüntüleyebilmesi

## Fonksiyonel Olmayan Gereksinimler

Fonksiyonel olmayan gereksinimler, sistemin performans, güvenlik ve kullanılabilirlik gibi özelliklerini tanımlar. Proje kapsamında belirlenen başlıca fonksiyonel olmayan gereksinimler şunlardır:

- Sistem sensör verilerini hızlı ve güvenilir bir şekilde işleyebilmelidir
- Kullanıcı ve sensör verileri güvenli bir veritabanında saklanmalıdır
- Sistem farklı cihazlar ve platformlar üzerinden erişilebilir olmalıdır
- Sistem modüler bir yapıda tasarlanmalı ve ileride geliştirilebilir olmalıdır
- Veri aktarımı sırasında veri bütünlüğü korunmalıdır
## 📖 User Stories

### User Story 1
**Rol:** Çiftçi  
**İstek:** Tarlamdaki toprak nemi ve sıcaklık verilerini sistem üzerinden görmek istiyorum.  
**Sebep:** Böylece bitkilerimin mevcut durumunu takip edebilirim.

---

### User Story 2
**Rol:** Çiftçi  
**İstek:** Sensörlerden gelen verilerin yapay zeka tarafından analiz edilmesini istiyorum.  
**Sebep:** Böylece sulama ve gübreleme zamanlarını daha doğru planlayabilirim.

---

### User Story 3
**Rol:** Çiftçi  
**İstek:** Mobil uygulama üzerinden tarlamdaki verileri anlık olarak görüntülemek istiyorum.  
**Sebep:** Böylece bulunduğum yerden bağımsız olarak tarım alanımı kontrol edebilirim.

---

### User Story 4
**Rol:** Kullanıcı  
**İstek:** Sisteme güvenli bir şekilde giriş yapmak istiyorum.  
**Sebep:** Böylece yalnızca bana ait tarım verilerine erişebilirim.

---

### User Story 5
**Rol:** Çiftçi  
**İstek:** Sistemden analiz sonuçlarına göre öneriler almak istiyorum.  
**Sebep:** Böylece su, gübre ve ilaç kullanımını daha verimli şekilde yönetebilirim.

---

### User Story 6
**Rol:** Yönetici  
**İstek:** Sensör verilerinin veritabanında güvenli şekilde saklanmasını istiyorum.  
**Sebep:** Böylece geçmiş verileri inceleyebilir ve analiz yapabilirim.

---

### User Story 7
**Rol:** Kullanıcı  
**İstek:** Sisteme hem web hem de mobil cihazlardan erişebilmek istiyorum.  
**Sebep:** Böylece istediğim yerden sistem verilerine ulaşabilirim.
## Sonuç

Gereksinim toplama ve analiz süreci sayesinde sistemin gerçekleştirmesi gereken işlevler ve teknik ihtiyaçlar net bir şekilde belirlenmiştir. Bu aşama, projenin sonraki geliştirme süreçleri için sağlam bir temel oluşturmuş ve sistem mimarisinin daha planlı bir şekilde tasarlanmasına katkı sağlamıştır. Doğru bir gereksinim analizi yapılması, projenin hedeflerine ulaşması ve kullanıcı ihtiyaçlarının karşılanması açısından büyük önem taşımaktadır.


---


## 📄  Detaylı Gereksinim Belgesi (Hayat Ay)

 ## 👤 1. Kullanıcı Hikayeleri
 ## User Story 1

- Rol: Çiftçi
- İstek: Tarlamdaki toprak nemi ve sıcaklık verilerini sistem üzerinden görmek istiyorum.
- Sebep: Böylece bitkilerimin mevcut durumunu takip edebilirim.

## User Story 2

- Rol: Çiftçi
- İstek: Sensörlerden gelen verilerin yapay zeka tarafından analiz edilmesini istiyorum.
- Sebep: Böylece sulama ve gübreleme zamanlarını daha doğru planlayabilirim.

## User Story 3

- Rol: Çiftçi
- İstek: Mobil uygulama üzerinden tarlamdaki verileri anlık olarak görüntülemek istiyorum.
- Sebep: Böylece bulunduğum yerden bağımsız olarak tarım alanımı kontrol edebilirim.

## User Story 4

- Rol: Kullanıcı
- İstek: Sisteme güvenli bir şekilde giriş yapmak istiyorum.
- Sebep: Böylece yalnızca bana ait tarım verilerine erişebilirim.

## User Story 5

- Rol: Çiftçi
- İstek: Sistemden analiz sonuçlarına göre öneriler almak istiyorum.
- Sebep: Böylece su, gübre ve ilaç kullanımını daha verimli şekilde yönetebilirim.

## User Story 6

- Rol: Yönetici
- İstek: Sensör verilerinin veritabanında güvenli şekilde saklanmasını istiyorum.
- Sebep: Böylece geçmiş verileri inceleyebilir ve analiz yapabilirim.

## User Story 7

- Rol: Kullanıcı
- İstek: Sisteme hem web hem de mobil cihazlardan erişebilmek istiyorum.
- Sebep: Böylece istediğim yerden sistem verilerine ulaşabilirim.

## 🎬 2.Kullanım Senaryoları (Use Case)
 ## Senaryo 1 – Sensör Verilerini Görüntüleme
- Aktör: Çiftçi
-Adımlar:
-Kullanıcı sisteme giriş yapar.
-Sistem kullanıcı bilgilerini doğrular.
-IoT sensörlerinden gelen veriler veritabanından alınır.
-Veriler kullanıcı arayüzünde gösterilir.

-Sonuç:
Kullanıcı tarlasındaki güncel durumu görüntüler.

## Senaryo 2 – Yapay Zeka ile Veri Analizi
- Aktör: Sistem
- Adımlar:
- Sensörlerden veri toplanır.
- Veriler sistemde işlenir.
- Python ve TensorFlow kullanılarak analiz yapılır.
- Analiz sonuçları veritabanına kaydedilir.

- Sonuç:
Sistem tarımsal kararlar için analiz sonuçları üretir.

## Senaryo 3 – Mobil Erişim
- Aktör: Çiftçi
- Adımlar:
- Kullanıcı mobil uygulamayı açar.
- Kullanıcı sisteme giriş yapar.
- Sensör verileri görüntülenir.

- Sonuç:
Kullanıcı bulunduğu yerden bağımsız olarak sisteme erişir.

## Senaryo 4 – Güvenli Giriş
- Aktör: Kullanıcı
- Adımlar:
- Kullanıcı kullanıcı adı ve şifre girer.
- Sistem kimlik doğrulaması yapar.
- Kullanıcı sisteme giriş yapar.

- Sonuç:
Yetkili erişim sağlanır.

## Senaryo 5 – Öneri Sistemi
- Aktör: Sistem
- Adımlar:
- Sensör verileri analiz edilir.
- Sistem sulama veya gübreleme önerileri oluşturur.
- Kullanıcıya öneriler gösterilir.

- Sonuç:
Kullanıcı doğru tarım kararları alır.

## Senaryo 6 – Veri Yönetimi 
- Aktör: Yönetici
- Adımlar:
- Yönetici sisteme giriş yapar
- Sistem veritabanına erişim sağlar
- Yönetici sensör verilerini görüntüler veya kontrol eder
- Gerekirse veri düzenleme veya silme işlemi yapar

-Sonuç:
Veriler güvenli ve düzenli şekilde yönetilir


## 3. Fonksiyonel Gereksinimler

- IoT sensörlerinden veri toplamalıdır.
- Toplanan verileri PostgreSQL veritabanında saklamalıdır.
- Python ile veri işleme yapmalıdır.
- TensorFlow ile veri analizi gerçekleştirmelidir.
- Django framework kullanılarak web arayüzü sunmalıdır.
- Kullanıcı giriş ve kimlik doğrulama sistemi içermelidir.
- Mobil ve web platformlarını desteklemelidir.
- Kullanıcıya analiz sonuçlarını göstermelidir.
- Kullanıcıya öneri sistemi sunmalıdır.

## 4. Fonksiyonel Olmayan Gereksinimler
- Sistem güvenli olmalıdır.
- Sistem hızlı çalışmalıdır.
- Sistem kullanıcı dostu bir arayüze sahip olmalıdır.
- Sistem farklı cihazlarda sorunsuz çalışmalıdır.
- Sistem yüksek veri doğruluğu sağlamalıdır.
- Sistem ölçeklenebilir olmalıdır.

## 👥5. Paydaşlar
- Çiftçiler (Sistemin ana kullanıcıları)
- Sistem yöneticileri
- Yazılım geliştirme ekibi
- Proje yöneticisi

## 6. Paydaş Onayı ve Önceliklendirme

- Toplanan gereksinimler proje paydaşları ile paylaşılmış ve değerlendirilmiştir. Yapılan toplantılar ve değerlendirmeler sonucunda gereksinimler onaylanmış ve önceliklendirilmiştir.

## Yüksek Öncelik:
- Sensör verilerinin toplanması
- Sensör verilerinin görüntülenmesi
- Yapay zeka ile veri analizi
- Güvenli kullanıcı girişi
- Veri güvenliği

## Orta Öncelik:
- Mobil uygulama erişimi
- Öneri sistemi
- Kullanıcı deneyimi

## Düşük Öncelik:
- Ek raporlama özellikleri
- Gelişmiş analiz araçları

Bu önceliklendirme, sistem geliştirme sürecinin planlanmasında kullanılacaktır.

## 7. Sonuç
- Bu gereksinim belgesi, Akıllı Tarım Yönetim Sistemi için kullanıcı ihtiyaçlarını, sistem gereksinimlerini ve kullanım senaryolarını detaylı şekilde tanımlamaktadır. Bu belge proje geliştirme sürecinde referans doküman olarak kullanılacaktır.

---

## 🏗️ Detaylı Mimari Tasarım (Ceren Çam)

## Genel Bakış

Bu bölümde, Akıllı Tarım Yönetim Sistemi'nin genel mimarisi daha detaylı şekilde ele alınmış ve sistem bileşenleri arasındaki ilişkiler teknik olarak açıklanmıştır.

Bu tasarım, sistemin ölçeklenebilir, sürdürülebilir ve modüler bir yapıda geliştirilmesini hedeflemektedir.

## Katmanlı Mimari Yapı

Sistem, üç ana katmandan oluşmaktadır:

### 1. Veri Katmanı (Data Layer)
- PostgreSQL veritabanı kullanılmaktadır  
- Sensör verileri, kullanıcı bilgileri ve analiz sonuçları burada saklanır  
- Veriler düzenli ve güvenli şekilde depolanır  

### 2. İş Mantığı Katmanı (Business Logic Layer)
- Django ve Django REST Framework kullanılarak geliştirilir  
- API servisleri bu katmanda yer alır  
- Sensör verileri işlenir ve yapay zeka modeline gönderilir  
- TensorFlow ile analiz işlemleri gerçekleştirilir  

### 3. Sunum Katmanı (Presentation Layer)
- Web arayüzü ve mobil uygulama bu katmanda yer alır  
- Kullanıcılar verileri görüntüler ve sistemle etkileşime geçer  
- Kullanıcı dostu arayüzler sayesinde sistem kolay kullanılabilir  

## Veri Akışı

Sistem içerisindeki veri akışı aşağıdaki gibidir:

IoT Sensörleri → MQTT Broker → Django API → PostgreSQL → TensorFlow → Django API → Web / Mobil Arayüz

- Sensörler veriyi toplar  
- MQTT ile sunucuya iletilir  
- Django API veriyi alır ve veritabanına kaydeder  
- Yapay zeka modeli veriyi analiz eder  
- Sonuçlar kullanıcıya sunulur  

## Bileşenler Arası İletişim

Sistem bileşenleri arasında iletişim aşağıdaki şekilde sağlanmaktadır:

- IoT sensörleri, MQTT protokolü ile veri gönderir  
- MQTT Broker, veriyi backend sistemine iletir  
- Django API, gelen verileri işler ve veritabanına kaydeder  
- TensorFlow modeli, verileri analiz ederek sonuç üretir  
- Web ve mobil uygulamalar, API üzerinden bu verilere erişir  

## Sistem Bileşenleri Detayı

### Sensör Katmanı
- Tarım alanından veri toplar  
- Sıcaklık, nem ve toprak bilgilerini üretir  

### API Katmanı
- Sensörlerden gelen verileri karşılar  
- Verileri işler ve saklar  
- Mobil ve web uygulamalarına veri sağlar  

### Yapay Zeka Katmanı
- TensorFlow ile geliştirilmiştir  
- Sensör verilerini analiz eder  
- Kullanıcıya öneriler üretir  

### Kullanıcı Arayüzü
- Web paneli ve mobil uygulamadan oluşur  
- Kullanıcılar verileri görüntüler ve takip eder  

## Mimari Yaklaşım

Sistem tasarımında katmanlı mimari yapısı benimsenmiştir. Bu sayede:

- Sistem modüler hale gelir  
- Bakım ve geliştirme kolaylaşır  
- Farklı bileşenler bağımsız şekilde geliştirilebilir  

## Mimari Diyagram

![Detaylı Mimari Diyagram](architecture_detailed.png)

Diyagram, sistem bileşenleri arasındaki veri akışını görsel olarak temsil etmektedir.

## Sonuç

Detaylı mimari tasarım sayesinde sistemin tüm bileşenleri ve veri akışı net bir şekilde tanımlanmıştır. Bu yapı, sistemin sürdürülebilir ve ölçeklenebilir bir şekilde geliştirilmesine olanak sağlar.

---

# 🛠️ Teknik Uygulama ve API Tasarımı (Ebubekir Yılmaz)

Projenin backend altyapısı ve sensör veri akışını simüle eden merkezi API sistemi kurulmuştur. Bu yapı, fiziksel donanım aşamasına kadar sistemin tüm fonksiyonlarını test etmeye olanak sağlar.

## 📡 1. API Endpoint Tasarımı
Sistem bileşenleri (IoT, Web, Mobil) arasındaki iletişim RESTful standartlarına uygun olarak tasarlanmıştır.

| Metot | Endpoint | Açıklama | Yetki |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/sensor-data/` | Sensörden gelen anlık verileri (sıcaklık, nem vb.) kaydeder ve karar üretir. | IoT Device |
| **GET** | `/admin/` | Veritabanındaki tüm geçmiş sensör verilerini ve sistem kararlarını listeleyen panel. | Yönetici |

## 🚜 2. Akıllı Tarım Simülasyonu
Fiziksel sensörlerin (ESP32/Arduino) yerini alan bir `simulator.py` modülü geliştirilmiştir.

* **Çalışma Mantığı:** Gerçek bir tarladaki çevresel değişimleri simüle ederek rastgele ancak fiziksel limitler dahilinde veri üretir.
* **Karar Mekanizması:** Sistem, gelen toprak nemi verisini anlık analiz eder. Nem **%30'un** altına düştüğünde otomatik olarak "SULAMA SİSTEMİ BAŞLATILDI" komutunu üretir.

## ⚙️ 3. Kurulum ve Çalıştırma Talimatları
Projeyi yerel ortamda ayağa kaldırmak için aşağıdaki adımlar izlenmelidir:

1. **Gereksinimler:** `pip install -r requirements.txt` komutuyla gerekli kütüphaneleri kurun.
2. **Veritabanı:** `python manage.py migrate` komutuyla veritabanı tablolarını oluşturun.
3. **Sunucu:** `python manage.py runserver` ile Django sunucusunu başlatın.
4. **Simülatör:** Yeni bir terminalde `python simulator.py` komutuyla veri akışını başlatın.

---
   
## 🏗️ Proje Görevi: Akıllı Tarım Veritabanı Mimarisi ve Sensör Veri Yönetimi(Hayat Ay)
- Bu çalışma, "Akıllı Tarım Yönetim Sistemi" kapsamında, tarlalardan gelen anlık sensör verilerini güvenli bir şekilde depolamak, ilişkilendirmek ve analiz edilebilir hale getirmek amacıyla tasarlanmıştır
## 1. Veritabanı Şeması ve Tablo Tasarımı
   Sensör verilerinin sadece saklanması değil, anlamlandırılması için PostgreSQL üzerinde ilişkisel bir şema (Relational Schema) oluşturulmuştur.
-  **Tarlalar Tablosu (tarlalar):** Sistemin en üst katmanıdır. Her tarlanın adı, konumu ve o tarlaya özel "Otomatik Sulama Eşiği" (Örn: %30 nem) bu tabloda tanımlanır.
 - **Sensörler Tablosu (sensorler):** Hangi sensörün hangi tarlada bulunduğunu ve cihazın aktiflik durumunu takip eder.
-  **Ölçümler Tablosu (olcumler):** Sensörlerden gelen sıcaklık, hava nemi ve toprak nemi gibi verileri saniyelik zaman damgalarıyla (Timestamp) kaydeden ana veri deposudur.
## 2. Sensör Verilerinin Depolanması ve İşlenmesi
-Tasarlanan mimari, sensör verilerini şu kriterlere göre işlemektedir.
- **Veri Hassasiyeti:** Nem ve sıcaklık değerleri DECIMAL veri tipiyle tanımlanarak yüksek hassasiyette (virgülden sonraki değerler dahil) korunur.
- **Veri İlişkilendirme:** Ölçümler tablosu, sensör ve tarla tablolarıyla "Foreign Key" (Dış Anahtar) yapıları üzerinden bağlanmıştır. Bu sayede bir ölçümün tam olarak hangi tarladan geldiği anında sorgulanabilir.
- **Performans ve Kayıt:** BIGSERIAL anahtar yapısı kullanılarak, milyonlarca sensör verisinin performans kaybı yaşanmadan depolanması garanti altına alınmıştır.
  
---

# 🎨 Gelişmiş GUI Tasarımı(Ahmet Enes Altun)

## 📌 Amaç

Akıllı Tarım Yönetim Sistemi için kullanıcı dostu ve anlaşılır bir arayüz tasarlanmıştır.  
Bu GUI tasarımının amacı, kullanıcıların sensör verilerini kolayca görebilmesini ve sistemi rahat bir şekilde yönetebilmesini sağlamaktır.

---

# 🖥️ Arayüz Yapısı

Sistem web tabanlı bir arayüze sahiptir. Kullanıcı sisteme giriş yaptıktan sonra dashboard ekranına ulaşır.

### Sayfalar

- Dashboard
- Login
- Sensör Verileri
- Kullanıcı Paneli

---

# 🎨 Renk Paleti

Tarım temasına uygun renkler seçilmiştir.

| Renk | Anlamı |
|-----|------|
| Yeşil | Tarım ve doğa |
| Beyaz | Temiz ve sade arayüz |
| Gri | Arka plan |
| Açık Yeşil | Kart ve paneller |

Bu renkler kullanıcıyı yormayan ve sade bir görünüm oluşturur.

---

# 🔤 Font Seçimi

Font olarak **Arial** seçilmiştir.

### Neden Arial?

- Okunması kolaydır
- Sade görünür
- Web arayüzlerinde yaygın kullanılır
- Kullanıcı deneyimini artırır

---

# 🧭 Ana Menü Tasarımı

Ana menü üst kısımda yer alır.

### Menü İçeriği

- Dashboard
- Sensör Verileri
- Login
- Çıkış

Bu menü sayesinde kullanıcı sistem içinde kolayca gezinebilir.

---

# 📊 Dashboard Tasarımı

Dashboard sistemin ana ekranıdır.

### Dashboard içinde

- Toprak nemi
- Sıcaklık
- Hava durumu
- Sensör verileri

Kart yapısı kullanılmıştır.

### Kart Yapısı

- Beyaz arka plan
- Yuvarlak köşe
- Gölge efekti
- Kolay okunabilir veri

---

# 🧩 Kullanıcı Etkileşimleri

Kullanıcı sistem ile şu şekilde etkileşime girer:

- Sisteme giriş yapar
- Dashboard ekranını açar
- Sensör verilerini görüntüler
- Tarım verilerini takip eder

Bu yapı kullanıcı deneyimini kolaylaştırır.

---

# 📱 Responsive Tasarım

Arayüz mobil ve bilgisayar uyumlu olacak şekilde tasarlanmıştır.

### Özellikler

- Mobil uyumlu
- Tablet uyumlu
- Bilgisayar uyumlu
- Basit ve hızlı arayüz

---



---
# 🧠 Yapay Zeka ve Veri Analizi Modülü (Ebubekir Yılmaz)

Bu hafta projenin karar destek mekanizmasını güçlendirmek amacıyla **TensorFlow** tabanlı bir analiz motoru sisteme entegre edilmiştir. Yapılan çalışmaların teknik detayları aşağıdadır:

### 1. TensorFlow Tabanlı İstatistiksel Analiz
Sensörlerden gelen ham verilerin anlamlandırılması için geleneksel yöntemler yerine, gelecekteki derin öğrenme modellerine temel oluşturması amacıyla TensorFlow ekosistemi tercih edilmiştir.
- **İşlenen Veriler:** Toprak nemi ve hava sıcaklığı.
- **Hesaplamalar:** Aritmetik Ortalama ($\mu$), Medyan ve Standart Sapma ($\sigma$).
- **Tensor Yapısı:** Veriler `tf.float32` formatındaki tensörlere dönüştürülerek yüksek performanslı işleme (GPU uyumlu) sağlanmıştır.

### 2. API Entegrasyonu ve Veri Akışı
- `/api/analysis/` uç noktası (endpoint) üzerinden veritabanındaki son 100 verinin anlık istatistiksel raporu JSON formatında sunulmaktadır.
- Bu yapı, web arayüzünde (Dashboard) çiftçilere tarladaki verilerin tutarlılığı hakkında bilgi vermek için kullanılacaktır.

### 3. Performans ve Doğruluk Testleri
- Geliştirilen `test_analysis.py` modülü ile 10.000 veri üzerinde yapılan testlerde, analiz süresi ortalama **0.03 saniye** olarak ölçülmüştür.
- Hesaplama sonuçlarının matematiksel doğruluğu test verileriyle teyit edilmiştir.

---

# 🖥️ Django Temel Yönetim Paneli Arayüzü (Ceren Çam)

Bu hafta, sensör verilerinin görselleştirileceği ve temel yönetim işlemlerinin yapılabileceği
web arayüzü geliştirilmiştir. Arayüz, Django framework'ü kullanılarak oluşturulmuş ve
Bootstrap 5 ile stilize edilmiştir.

## Oluşturulan Dosyalar

* `dashboard/urls.py` → Dashboard URL yönlendirmeleri
* `dashboard/views.py` → Sayfa mantığı ve veri işleme
* `dashboard/templates/dashboard/dashboard.html` → Ana panel şablonu
* `dashboard/templates/dashboard/sensor_listesi.html` → Sensör listesi şablonu
* `dashboard/templates/dashboard/sensor_ekle.html` → Manuel veri ekleme şablonu

## Geliştirilen Özellikler

### Ana Dashboard Sayfası
* Toplam kayıt sayısı, son sıcaklık, toprak nemi ve hava nemi özet kartları
* Chart.js kütüphanesi ile sıcaklık ve nem grafikleri
* Son 50 sensör verisini gösteren tablo
* Toprak nemi %30'un altına düştüğünde otomatik ⚠️ sulama uyarısı

### Filtreleme Sistemi
* Başlangıç ve bitiş tarihine göre filtreleme
* Cihaz ID'sine göre arama
* Filtreleri temizleme butonu

### Sensör Yönetimi
* Kayıtlı sensörleri listeleme
* Sensöre ait tüm verileri silme (onay ekranıyla)
* Manuel sensör verisi ekleme formu

## URL Yapısı

| URL | Açıklama |
| --- | --- |
| `/` | Ana dashboard sayfası |
| `/sensorler/` | Sensör listesi |
| `/sensor-ekle/` | Manuel veri ekleme |
| `/sensor-sil/<cihaz_id>/` | Sensör verilerini silme |

## Kullanılan Teknolojiler

* **Bootstrap 5** → Responsive tasarım ve stil
* **Chart.js** → Sıcaklık ve nem grafikleri
* **Bootstrap Icons** → Arayüz ikonları
* **Django Template Engine** → Dinamik HTML üretimi

## Sonuç

Geliştirilen yönetim paneli sayesinde kullanıcılar sensör verilerini grafikler ve
tablolar halinde görüntüleyebilmekte, tarih aralığına ve cihaz ID'sine göre
filtreleyebilmekte ve sensör yönetimi işlemlerini gerçekleştirebilmektedir.


-------

## Toprak Nemi Veri Toplama Modülü(Hayat Ay )
 ## Genel Bakış
- Bu modül, tarla sensörlerinden gelen toprak nemi verilerini MQTT protokolü üzerinden sürekli dinler, gelen verileri bellekte biriktirir ve her 5 dakikada bir toplu olarak PostgreSQL veritabanına yazar. Toprak nemi %30'un altına düştüğünde otomatik sulama uyarısı üretir. Olası bağlantı hatalarında veri kaybını önlemek için hata yönetimi ve loglama mekanizmaları içerir.

 ## Sistem Mimarisi
- [Tarla Sensörleri]
     -  ↓  MQTT
 - [MQTTCollector]   → Mesajları alır ve parse eder
     -  ↓
 - [SensorBuffer]    → Thread-safe bellek tamponu
      - ↓  (her 5 dakikada bir)
  - [FlushScheduler]   → Zamanlayıcı
   -    ↓
- [DatabaseManager]   → PostgreSQL'e toplu yazar

 ## Sonuç
- Bu modül, tarımsal IoT sistemleri için ihtiyaç duyulan toprak nemi veri toplama sürecini eksiksiz olarak karşılamaktadır. MQTT protokolü ile kesintisiz veri alımı, thread-safe bellek tamponu ile güvenli veri yönetimi ve PostgreSQL entegrasyonu ile kalıcı depolama bir arada sağlanmıştır. Hata yönetimi ve loglama mekanizmaları sayesinde sistem, bağlantı kesintilerinde dahi veri kaybı yaşamadan çalışmaya devam edebilmektedir. Unit testler ve gerçek veritabanı bağlantısıyla çalışan entegrasyon testleri ile sistemin doğruluğu kapsamlı biçimde doğrulanmıştır. Modül, üretime hazır ve genişletilebilir bir yapıda tasarlanmıştır.

---

# 🔒 API Entegrasyon Sorunları: Servis Cevaplarını Doğrulama (Ceren Çam)

## Genel Bakış

Bu hafta, farklı servislerden gelen API cevaplarının doğrulanması ve hatalı cevapların ele alınması amacıyla bir mekanizma geliştirilmiştir. Ayrıca sistemin tüm API olaylarını kayıt altına alabilmesi için loglama ve hata takibi sistemi projeye entegre edilmiştir.

---

## Eklenen Modüller

### 1. Doğrulama Modülü (api/validators.py)

Farklı kaynaklardan gelen API cevaplarını doğrulayan fonksiyonlar bu modülde yer almaktadır.

**Sensör Verisi Doğrulama:**

* Zorunlu alanların varlığı kontrol edilir (device_id, temperature, humidity, soil_moisture)
* Her alanın veri tipi doğrulanır
* Değerlerin geçerli fiziksel sınırlar içinde olup olmadığı kontrol edilir
* Toprak nemi %15'in altına düştüğünde ve sıcaklık 40°C üzerine çıktığında uyarı üretilir

**Hava Durumu API Doğrulama:**

* Zorunlu alanların varlığı kontrol edilir (city, temperature, humidity, description)
* Sayısal alanlar için tip ve aralık kontrolü yapılır

**Genel HTTP Cevap Doğrulama:**

* Gelen HTTP durum koduna göre hata veya uyarı üretilir
* 400, 401, 403, 404, 429, 500 ve üzeri kodlar ayrı ayrı ele alınır

---

### 2. Hata Yönetimi Modülü (api/error_handler.py)

Tüm API hatalarının merkezi bir noktadan yönetilmesi amacıyla geliştirilmiştir.

* Tüm hata yanıtları tutarlı bir JSON formatında döndürülür
* Her yanıtta hata kodu, açıklama, detaylar ve zaman damgası bulunur
* Doğrulama hataları HTTP 422 ile yanıtlanır
* Beklenmeyen hatalar yakalanarak güvenli bir HTTP 500 yanıtı döndürülür
* Dış servislere ulaşılamama durumunda HTTP 503 yanıtı üretilir

---

### 3. Loglama Modülü (api/loglama_config.py)

Sistemin tüm API olaylarını kayıt altına alabilmesi için loglama yapılandırması oluşturulmuştur.

**Log Dosyaları:**

* api/logs/api_genel.log → INFO ve üzeri tüm API olaylarını kaydeder
* api/logs/api_hatalar.log → Yalnızca ERROR ve CRITICAL seviyesindeki olayları kaydeder

**Özellikler:**

* Dosyalar 5 MB dolduğunda otomatik olarak yenilenir, en fazla 3 yedek tutulur
* Loglar aynı anda hem terminale hem de dosyaya yazılır
* Django ayarlarına (settings.py) entegre edilmiştir

---

### 4. Test Modülü (api/test_dogrulama.py)

Geliştirilen doğrulama ve hata yönetimi sistemi 17 test senaryosu ile test edilmiştir.

* Geçerli sensör verisi
* Eksik alan kontrolü
* Aralık dışı sıcaklık ve nem değerleri
* Yanlış veri tipi kontrolü
* Boş device_id kontrolü
* Düşük toprak nemi uyarı senaryosu
* Hava durumu API doğrulama senaryoları
* HTTP durum kodu senaryoları (200, 400, 401, 404, 429, 500)

Tüm testler başarıyla geçmiştir.

---

## Sonuç

Bu hafta geliştirilen sistem sayesinde sensörlerden ve dış servislerden gelen API cevapları doğrulanmakta, hatalı veriler sisteme girmeden önce tespit edilmektedir. Merkezi hata yönetimi ve loglama altyapısı sayesinde sistem davranışları takip edilebilir ve sorunlar hızlıca tespit edilebilir hale gelmiştir.



<<<<<<< HEAD
---

=======
>>>>>>> 20a0c3a39581ee39153fef5bce63e7f204d23ab9
# 🔧 Veritabanı Bağlantı Hataları ve Çözümleri (Hayat Ay)

## Genel Bakış

Bu hafta `tarim_projesi/settings.py` ve `akilli_tarim_db.sql` dosyaları incelenerek tespit edilen veritabanı bağlantı hataları giderilmiş ve bağlantı havuzu yapılandırması iyileştirilmiştir.

---

## Tespit Edilen Hatalar ve Yapılan Düzeltmeler

### 1. Veritabanı SQLite Olarak Bırakılmıştı

Proje dokümantasyonunda PostgreSQL seçilmiş ve `requirements.txt` içinde `psycopg2-binary` kurulu olmasına rağmen `settings.py` içinde veritabanı motoru SQLite olarak tanımlıydı.

**Hatalı kod:**
```python
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
```

**Düzeltme:** Veritabanı motoru PostgreSQL olarak güncellendi ve bağlantı bilgileri ortam değişkenlerinden okunacak şekilde yapılandırıldı.

---

### 2. Bağlantı Havuzu Tanımlanmamıştı

`CONN_MAX_AGE` parametresi tanımlanmadığı için Django'nun varsayılan değeri olan `0` kullanılıyordu. Bu durum, her HTTP isteğinde PostgreSQL'e yeni bir bağlantı açılıp kapanmasına neden olmaktaydı. Birden fazla sensörün eş zamanlı veri göndermesi durumunda bağlantı tükenmesi yaşanabilirdi.

**Düzeltme:** Bağlantı havuzu aşağıdaki parametrelerle yapılandırıldı:

```python
'CONN_MAX_AGE': 60,
'CONN_HEALTH_CHECKS': True,
'OPTIONS': {
    'connect_timeout': 5,
    'keepalives': 1,
    'keepalives_idle': 30,
    'keepalives_interval': 5,
    'keepalives_count': 5,
}
```

---

### 3. SECRET_KEY Açıkta Bırakılmıştı

Gizli anahtar doğrudan `settings.py` dosyasına yazılmış ve Git deposuna yüklenmiş durumdaydı.

**Düzeltme:** Ortam değişkeninden okunacak şekilde güncellendi.

---

### 4. MIDDLEWARE'de Bozuk Satır

`SecurityMiddleware` satırı markdown linki formatında yazılmıştı. Python bu satırı tanıyamadığından uygulama başlarken hata veriyordu.

**Hatalı kod:**
```python
'[django.middleware.security](http://django.middleware.security).SecurityMiddleware',
```

**Düzeltme:** Düzgün string formatına dönüştürüldü.

---

### 5. CORS Tüm Kaynaklara Açıktı

`CORS_ALLOW_ALL_ORIGINS = True` ayarı her adresten gelen isteği kabul ediyordu.

**Düzeltme:** Yalnızca gerekli adreslere izin verilecek şekilde güncellendi.

---

### 6. ALLOWED_HOSTS Boş Bırakılmıştı

`ALLOWED_HOSTS = []` olarak bırakıldığında Django production ortamında tüm istekleri reddeder.

**Düzeltme:** `localhost` ve `127.0.0.1` adresleri eklendi.

---

### 7. api.loglama_config Import Hatası

`settings.py` dosyasının en altında `api` modülünden import yapılıyordu. Ancak `settings.py` yüklenirken `api` modülü henüz tanınmadığından `ModuleNotFoundError` hatası alınıyordu.

**Düzeltme:** Import satırı kaldırılarak loglama yapılandırması doğrudan `settings.py` içine yazıldı.

---

### 8. SQL Dosyasında FOREIGN KEY Eksikti

`toprak_nemi_olcumleri` tablosundaki `sensor_id` sütununa FOREIGN KEY tanımlanmamıştı. Bu durum, var olmayan bir sensör ID'siyle kayıt eklenmesine ve veri bütünlüğünün bozulmasına neden olabilirdi.

**Düzeltme:**
```sql
sensor_id INTEGER NOT NULL REFERENCES sensorler(id) ON DELETE CASCADE,
```

---

## Özet Tablo

| # | Hata | Dosya | Önem | Durum |
|---|------|-------|------|-------|
| 1 | SQLite kullanılıyor, PostgreSQL olmalı | settings.py | 🔴 Kritik | Düzeltildi |
| 2 | Bağlantı havuzu tanımlanmamış | settings.py | 🔴 Kritik | Düzeltildi |
| 3 | SECRET_KEY hardcode | settings.py | 🔴 Kritik | Düzeltildi |
| 4 | MIDDLEWARE'de bozuk satır | settings.py | 🔴 Kritik | Düzeltildi |
| 5 | CORS herkese açık | settings.py | 🟠 Yüksek | Düzeltildi |
| 6 | ALLOWED_HOSTS boş | settings.py | 🟠 Yüksek | Düzeltildi |
| 7 | api.loglama_config import hatası | settings.py | 🔴 Kritik | Düzeltildi |
| 8 | FOREIGN KEY eksik | akilli_tarim_db.sql | 🔴 Kritik | Düzeltildi |

---

---

# 🔒 Güvenlik Denetimi, UI/UX Yenilemesi (Ebubekir Yılmaz)

Bu hafta projenin güvenlik altyapısı baştan denetlenmiş, tespit edilen tüm açıklar kapatılmış ve yönetim panelinin UI/UX tasarımı için wireframe ve mockup'lar hazırlanmıştır. Yapılan çalışmaların teknik detayları aşağıdadır:

## 🛡️ 1. Güvenlik Açığı Taraması (XSS ve SQL Injection Testleri)

Projedeki tüm view, template ve API endpoint'leri otomatik testlerle taranmıştır. Django test framework'ü kullanılarak `api/test_guvenlik.py` dosyasında 13 ayrı güvenlik testi yazılmıştır.

- **XSS Testleri:** `device_id` alanına ve URL filtre parametrelerine HTML/JS payload'i enjekte edilerek dashboard'da escape kontrolü yapılmıştır. JavaScript context'inden çıkış denemeleri (kritik XSS) ayrıca test edilmiştir.
- **SQL Injection Testleri:** Klasik `'; DROP TABLE` payload'i, `OR 1=1` bypass denemesi, tarih filtresine injection ve API POST üzerinden injection denenmiştir. Django ORM'in parametreli sorgularıyla sistemin korumalı olduğu doğrulanmıştır.
- **Yetkilendirme Testleri:** Anonim kullanıcının API ve dashboard'a erişim denemesi simüle edilmiştir.
- **CSRF ve Information Disclosure Testleri:** Form'ların CSRF token kontrolü ve hata mesajlarının stack trace sızdırıp sızdırmadığı kontrol edilmiştir.

Çalıştırma komutu: `python manage.py test api.test_guvenlik -v 2`

## 🔧 2. Güvenlik Denetimi ve İyileştirmeler

Tarama sonucunda **10 güvenlik açığı** tespit edilmiş ve hepsi kapatılmıştır:

| Açık | Çözüm |
| :--- | :--- |
| `\|safe` filtresi ile Stored XSS | Django'nun `json_script` etiketine geçildi |
| Dashboard view'larında auth eksikti | Tüm view'lara `@login_required` eklendi |
| API endpoint'leri anonim erişime açıktı | `IsAuthenticated` permission + Token + Session auth |
| Token sistemi aktif değildi | `rest_framework.authtoken` aktive edildi, migration çalıştırıldı |
| Token alma endpoint'i yoktu | `/api/token/` endpoint'i eklendi (`obtain_auth_token`) |
| API hata mesajları stack trace sızdırıyordu | Generic mesaja çevrildi |
| `DEBUG=True` hardcoded'du | Ortam değişkeni ile kontrol edilebilir hale getirildi |
| Simulator yetki kontrolünden geçemiyordu | Token destekli yeniden yazıldı |
| Güvenlik header'ları eksikti | `X-Frame-Options`, `nosniff`, `HSTS`, secure cookie ayarları eklendi |
| Tarih filtresine bozuk girdi view'ı çökertiyordu | `try/except` ile zarif hata yönetimi |

### Kullanıcı Yetkilendirme ve Kimlik Doğrulama

- **Login/Logout sistemi:** Django'nun yerleşik `auth_views.LoginView` ve `LogoutView` ile entegre edildi.
- **Bootstrap 5 stilli giriş ekranı:** `tarim_projesi/templates/registration/login.html` olarak tasarlandı.
- **Çift katmanlı yetkilendirme:** Web arayüzü için Session, IoT cihazlar için Token authentication.
- **Şifre kalitesi:** En az 10 karakter, yaygın şifreler reddedilir.
- **Session güvenliği:** HttpOnly + SameSite cookie'ler, 2 saatlik otomatik logout.

### Eklenen ve Güncellenen Dosyalar

- `api/test_guvenlik.py` (yeni — 13 test)
- `api/views.py` (auth + permission düzenlemeleri)
- `tarim_projesi/settings.py` (güvenlik ayarları)
- `tarim_projesi/urls.py` (login/logout/token endpoint'leri)
- `tarim_projesi/templates/registration/login.html` (yeni)
- `dashboard/views.py` (her view'a `@login_required`)
- `dashboard/templates/dashboard/dashboard.html` (XSS koruması — `json_script`)
- `simulator.py` (token destekli)
- `guvenlik_acigi_raporu.md` (detaylı denetim raporu)

## 🎨 3. Web Tabanlı Yönetim Paneli UI/UX Tasarımı

Mevcut dashboard, sensör listesi ve veri ekleme sayfaları için yeni bir tasarım sistemi geliştirilmiştir.

### Bilgi Mimarisi
4 temel sayfa tanımlanmıştır: **Login → Dashboard → Sensör Listesi → Manuel Veri Girişi**. Tüm sayfalar arasında navbar üzerinden gezinme mümkündür; sağ üst köşede oturum bilgisi ve çıkış butonu yer alır.

### Tasarım Sistemi
- **Renk paleti:** Mevcut yeşil tema korundu (`#2e7d32` ana, `#1b5e20` koyu, `#e8f5e9` açık)
- **Durum göstergeleri:** Renk + ikon + metin kombinasyonu (renk körlüğü erişilebilirliği için)
  - 🌾 İdeal (yeşil) | ⚠️ Sulama Gerekli (turuncu) | 🛑 Aşırı Doygun (kırmızı)
- **Etkileşim:** Hover animasyonları, kart bazlı sensör listesi, kompakt filtre barı
- **Responsive:** Mobile (2x2 grid), tablet (2 kolon), desktop (4 kolon)

### Yenilenen Bileşenler
- **Dashboard:** Stat kartlarında trend göstergesi (▲/▼), tabloda renkli durum badge'leri
- **Sensör Listesi:** Tablo yerine kart grid yapısı, son ölçüm değerleri özet halinde
- **Sensör Ekle:** Geçerli aralık bilgi kutusu, inline hata mesajları
- **Login:** Gradient arkaplan, ikonlu input alanları

### Teslimatlar
- `docs/wireframes.html` — 4 sayfanın SVG wireframe çizimleri
- `docs/mockup.html` — Tarayıcıda açılan, sayfalar arası gezilebilir tam görsel mockup
- `docs/ui_ux_tasarim_raporu.md` — Bilgi mimarisi, kullanıcı akışları ve tasarım kararlarının dokümantasyonu

---

## 📚 API Dokümantasyonu ve Kullanıcı Kılavuzu (Ceren Çam)

Bu bölümde projenin API referans belgesi ve kullanıcılara yönelik kapsamlı kurulum-kullanım kılavuzu hazırlanmıştır. Tüm belgeler `docs/` klasörü altında düzenlenmiştir.

## Oluşturulan Belgeler

* **`docs/api-dokumantasyon.md`** → Tüm API endpoint'leri, istek/yanıt formatları, hata kodları ve örnek cURL komutları
* **`docs/kullanici-kilavuzu.md`** → Kurulum, çalıştırma, kullanım ve sorun giderme adımları

## API Dokümantasyonu İçeriği

Mevcut sistemdeki üç temel endpoint belgelenmiştir:

| Metot | Endpoint | Açıklama |
|---|---|---|
| `POST` | `/api/sensor-data/` | Sensör verisini kaydeder ve sulama kararı üretir |
| `GET` | `/api/analysis/` | Son 100 ölçümün TensorFlow istatistik raporunu döndürür |
| `GET` | `/admin/` | Yönetici paneli — tüm veriler ve kullanıcı yönetimi |

Her endpoint için istek gövdesi (request body), örnek JSON yanıtları ve olası hata kodları (`400`, `401`, `404`, `500`) açıklanmıştır. Veri akış diyagramı da belgeye eklenmiştir.

## Kullanıcı Kılavuzu İçeriği

Kılavuz üç ana başlık altında düzenlenmiştir:

### Kurulum

* Python 3.10+ ve sanal ortam (venv) kurulumu
* `pip install -r requirements.txt` ile bağımlılık yükleme
* PostgreSQL veritabanı oluşturma ve tablo migrasyonu
* Yönetici hesabı oluşturma

### Kullanım

* Django sunucusunu ve sensör simülatörünü başlatma
* `http://localhost:8000/admin/` üzerinden yönetici paneline erişim
* Sensör verilerini filtreleme ve izleme
* Analiz raporunu görüntüleme

### Sorun Giderme

Aşağıdaki yaygın sorunlar için adım adım çözümler hazırlanmıştır:

* Sunucu başlamıyor
* Veritabanına bağlanılamıyor
* Simülatör veri gönderemiyor
* Bağımlılık kurulum hataları
* Yönetici parolası sıfırlama

## Sonuç

Hazırlanan belgeler sayesinde projeyi daha önce hiç görmemiş bir kullanıcı sistemi sıfırdan kurup çalıştırabilir. API dokümantasyonu ise ileride sisteme entegre edilecek yeni cihaz veya modüller için referans kaynak niteliği taşımaktadır.



---

## 📊 — IoT Sensör Veri Toplama Modülü Gereksinim Analizi(Hayat AY )

### 1. Sensörler ve Toplanan Veriler

Sistemde `models.py` ve `validators.py` dosyaları incelenerek aktif olarak kullanılan üç sensör parametresi tespit edildi.

**Sıcaklık (`temperature`):** Django modelinde `FloatField` olarak tanımlanmış olup `-10.0 °C` ile `60.0 °C` arasındaki değerleri kabul etmektedir. `40.0 °C` üzerindeki değerlerde `"Sıcaklık aşırı yüksek"` uyarısı üretilmektedir. Fiziksel sensör olarak ±0.5 °C hassasiyetiyle DHT22, SHT31 veya DS18B20 kullanılması önerilmektedir.

**Hava Nemi (`humidity`):** `0.0%` ile `100.0%` arasında `float` tipinde veri kabul etmektedir. Mevcut kodda kritik eşik tanımlanmamış olup `30%` altı kuru, `85%` üstü yoğun olarak uyarı eşiği belirlenmesi gerektiği tespit edildi. ±2% RH hassasiyetiyle DHT22 veya SHT31 önerilmektedir.

**Toprak Nemi (`soil_moisture`):** `0.0%` ile `100.0%` arasında veri kabul etmektedir. `15.0%` altında `"Toprak nemi kritik seviyede düşük"` uyarısı üretilmektedir. `views.py` içindeki `sulama_karari_uret()` fonksiyonu üzerinden `30%` altında sulama başlatma, `30–70%` arasında ideal durum, `70%` üzerinde sulama durdurma kararı verilmektedir. Capacitive Soil Moisture v1.2 veya TEROS-12 sensörü önerilmektedir.

Gelecek dönem için öncelik sırasına göre ışık (µmol/m²/s), pH (0–14), yağmur (mm/saat), CO2 (ppm) ve rüzgar (m/s) sensörlerinin sisteme eklenmesi planlandı.

### 2. Veri Toplama Sıklığı

Mevcut kodda veri toplama sıklığı hiçbir yerde tanımlanmamış olduğu tespit edildi. Bu eksikliği gidermek amacıyla dört farklı senaryo için sıklık değerleri belirlendi ve `collector_config.json` dosyasına aktarıldı.

**Normal izleme:** Sıcaklık ve hava nemi 15 dakikada bir, toprak nemi 10 dakikada bir toplanmaktadır. Zamanlayıcı tabanlı bu senaryo verimli kaynak kullanımını hedeflemektedir.

**Kritik eşik aşımı:** `validators.py` içindeki eşik değerlerinden herhangi biri aşıldığında tüm parametreler 1 dakikaya düşmektedir. Hızlı müdahale gerektiren durumlar için otomatik olarak tetiklenmektedir.

**Sulama aktifken:** `sulama_karari_uret()` fonksiyonunun sulama başlatma kararı vermesi durumunda toprak nemi 2 dakikada bir, sıcaklık ve hava nemi 5 dakikada bir toplanmaktadır. Bu sayede sulama sürecinin etkisi anlık olarak takip edilmektedir.

**İstatistiksel analiz:** `IstatistikselAnaliz` endpoint'i ve `TarimAnalizMotoru` için saatlik ortalama değerler kullanılmaktadır. `TarimAnalizMotoru` her parametre için ortalama, medyan, standart sapma ve veri adedi hesaplamaktadır.

`SensorData` modelindeki `auto_now_add=True` alanı saniye hassasiyetinde çalışmaktadır. Yüksek frekanslı senaryolarda milisaniye hassasiyetine geçilmesi gerekebileceği not edildi. Ayrıca `IstatistikselAnaliz` endpoint'indeki `queryset[:100]` sabit limitinin zaman bazlı filtrelemeye (`?start_date=&end_date=`) dönüştürülmesi gerektiği tespit edildi.

### 3. Veri Formatları

API'ye gönderilecek verinin `device_id`, `temperature`, `humidity` ve `soil_moisture` alanlarını içeren JSON formatında olması gerekmektedir. `timestamp` alanı `auto_now_add=True` ile otomatik olarak oluşturulmaktadır.

`validators.py` üzerinden belirlenen alan kısıtlamaları şu şekildedir: `device_id` en fazla 50 karakter uzunluğunda string, `temperature` `-10.0` ile `60.0` arasında float, `humidity` `0.0` ile `100.0` arasında float, `soil_moisture` `0.0` ile `100.0` arasında float tipinde olmalıdır. Tüm alanlar zorunludur.

Başarılı veri iletiminde API `HTTP 201` durum koduyla `mesaj`, `karar`, `kayit_id` ve `uyarilar` alanlarını içeren bir yanıt döndürmektedir. Geçersiz veri gönderiminde `HTTP 400` durum koduyla `hata` ve `detaylar` alanları döndürülmektedir.

`IstatistikselAnaliz` endpoint'i her sensör parametresi için `TarimAnalizMotoru` üzerinden hesaplanan `ortalama`, `medyan`, `standart_sapma` ve `veri_adedi` değerlerini döndürmektedir. `TarimAnalizMotoru` verileri TensorFlow Tensor formatına dönüştürerek GPU hızlandırması ve ileride geliştirilecek yapay zeka modelleriyle uyumluluk sağlamaktadır.

### 4. Veri Güvenliği Gereksinimleri

`SensorDataReceiver` ve `IstatistikselAnaliz` endpoint'lerinin kimlik doğrulaması olmadan erişilebilir durumda olduğu tespit edildi. API katmanında `device_id` bazlı `X-API-Key` header kimlik doğrulaması, taşıma katmanında HTTPS/TLS ve MQTT broker'da kullanıcı adı/şifre veya TLS sertifikası zorunlu hale getirilmesi gerektiği belirlendi. Orta vadeli gereksinim olarak DRF Throttle ile sensör başına 10 istek/dakika rate limiting ve kayıtsız cihazları engelleyecek device whitelist yapısı oluşturulması planlandı.

`validators.py` incelemesinde doğrulama katmanının sağlıklı biçimde kurgulandığı görüldü. Zorunlu alan eksikliği, sayısal tip doğrulaması ve aralık dışı değer reddi uygulanmış durumdadır. Tüm doğrulama kararları `hatalar` ve `uyarilar` olmak üzere iki seviyeli geri bildirim yapısıyla `api.validators` logger'a aktarılmaktadır. Tek eksik olarak `humidity` kritik eşiğinin tanımlanmamış olduğu tespit edildi.

Loglama altyapısı incelendiğinde `INFO`, `WARNING` ve `ERROR` seviyelerinin mevcut olduğu görüldü. Güvenlik ihlallerini kapsayan `CRITICAL` seviyesi ve `sensor_sil` işlemlerini kapsayan `AUDIT` seviyesinin eksik olduğu belirlendi.

Veri saklama politikası olarak `device_id` ile konum ilişkisi kurulması durumunda KVKK kapsamına girebileceği not edildi. Ham verinin 1 yıl, agregat verinin 5 yıl saklanması, PostgreSQL bağlantısının SSL zorunlu yapılandırılması ve MQTT payload şifrelemesi için TLS kullanılması gerektiği belirlendi.

### 5. Veri Toplama Temeli

Analiz sonuçlarına dayanarak veri toplama sürecinin çalışabilir iskelet yapısı iki dosya halinde oluşturuldu.

**`collector_config.json`:** MQTT bağlantı ayarları, API adresi ve anahtarı, belirlenen dört senaryo için veri toplama sıklıkları, üç sensör parametresinin tamamı için minimum, maksimum ve kritik eşik değerleri ile buffer boyutu, yeniden deneme süresi ve maksimum deneme sayısı bu dosyada merkezi olarak yönetilmektedir.

**`sensor_collector.py`:** MQTT üzerinden gelen ham sensör verisi alınmakta, `ALAN_ADI_HARITASI` üzerinden alan adları API formatına dönüştürülmekte, `collector_config.json` içindeki eşik değerleriyle karşılaştırılarak senaryo belirlenmekte ve veri API'ye iletilmektedir. Bağlantı hatası durumunda veriler `deque` yapısındaki buffer'a alınmakta ve belirlenen aralıklarla yeniden gönderim denenmektedir. MQTT bağlantısı QoS 1 seviyesinde tutularak en az bir kez teslim garantisi sağlanmaktadır. Config dosyasında kimlik bilgileri tanımlandığında MQTT broker kimlik doğrulaması otomatik olarak devreye girmektedir.

