# 🌱 Akıllı Tarım Yönetim Sistemi

## 👥 Grup Üyeleri ve Görev Dağılımı
- **Ahmet Enes Altun** → Proje Mimari Tasarımı  
- **Hayat Ay** → Proje Analizi ve Kapsam Belirleme  
- **Sami Yusuf Yıldız** → Gereksinim Toplama ve Analizi  
- **Ebubekir Yılmaz** → Teknoloji Araştırması ve Seçimi  
- **Ceren Çam** → Geliştirme Ortamı Kurulumu  

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

# 📋 Proje Kapsam Belgesi (Hayat Ay)

## 1. Proje Tanımı

Akıllı Tarım Yönetim Sistemi, tarım alanlarından IoT sensörleri aracılığıyla toplanan verileri analiz ederek çiftçilere daha verimli ve sürdürülebilir tarım yönetimi sunmayı amaçlayan bir yazılım sistemidir.

Sistem çevresel verileri toplar, analiz eder ve kullanıcıya web veya mobil arayüz üzerinden anlamlı bilgiler sunar.

---

## 2. Projenin Amacı

Bu projenin amacı tarım alanlarında kullanılan sensörlerden elde edilen verileri dijital ortamda analiz ederek çiftçilere bir **karar destek sistemi** sunmaktır.

### Temel hedefler

- Tarımsal verilerin otomatik olarak toplanması  
- Verilerin güvenli şekilde saklanması  
- Yapay zeka algoritmaları ile analiz edilmesi  
- Kullanıcıların web veya mobil arayüz üzerinden verilere erişebilmesi  
- Tarımsal verimliliğin artırılması  

---

## 3. Kullanılan Teknolojiler

- Python  
- TensorFlow  
- IoT Sensörleri  
- Django  
- PostgreSQL  

---

## 4. Proje Kapsamı

### ✅ Kapsama Dahil Olan Özellikler

- IoT sensörlerinden veri toplanması  
- Sensör verilerinin API aracılığıyla sisteme gönderilmesi  
- Verilerin PostgreSQL veritabanında saklanması  
- Python ve TensorFlow kullanılarak veri analizi yapılması  
- Django tabanlı web arayüzü üzerinden verilerin görüntülenmesi  
- Kullanıcıların sisteme giriş yapabilmesi  
- Sistem yöneticisinin verileri yönetebilmesi  

### ❌ Kapsama Dahil Olmayan Özellikler

- Sensör donanımının fiziksel üretimi  
- Ağır tarım makinelerinin doğrudan kontrol edilmesi  
- Ticari ölçekli büyük tarım işletmeleri için özel modüller  

---

## 5. Proje Paydaşları

| Paydaş | Açıklama |
|------|------|
| Çiftçiler | Sistemi kullanarak tarım verilerini takip eder |
| Sistem Yöneticisi | Sistemi yönetir ve kontrol eder |
| Yazılım Geliştiriciler | Sistemin geliştirilmesini sağlar |
| Proje Ekibi | Projenin planlanması ve uygulanmasından sorumludur |

---

## 6. Sonuç

Akıllı Tarım Yönetim Sistemi, IoT sensörleri ve yapay zeka teknolojilerini bir araya getirerek tarım verilerinin daha verimli şekilde analiz edilmesini sağlamayı amaçlamaktadır.

---

# ⚙️ Geliştirme Ortamı Kurulumu (Ceren Çam)

## Kullanılan Araçlar

### IDE
Visual Studio Code (VS Code)

### Programlama Dili
Python 3.10+

### Backend Framework
- Django  
- Django REST Framework  

### Yapay Zeka Kütüphaneleri
- TensorFlow  
- NumPy  
- Pandas  

### Veritabanı
PostgreSQL

### IoT İletişim
MQTT

### Versiyon Kontrol
Git & GitHub

---

## Sonuç

Belirlenen geliştirme ortamı sayesinde ekip üyeleri aynı araçları kullanarak proje üzerinde çalışabilir. Bu durum ekip içi iş birliğini ve geliştirme sürecini kolaylaştırır.

---

# 📋 Gereksinim Toplama ve Analizi (Sami Yusuf Yıldız)

## Fonksiyonel Gereksinimler

- IoT sensörleri aracılığıyla sıcaklık, nem ve toprak verilerinin toplanması  
- Sensör verilerinin sunucuya gönderilmesi  
- Verilerin PostgreSQL veritabanında saklanması  
- Yapay zeka ile veri analizi yapılması  
- Sonuçların web veya mobil uygulamada gösterilmesi  
- Kullanıcıların sisteme giriş yapabilmesi  

---

## Fonksiyonel Olmayan Gereksinimler

- Sistem hızlı veri işleyebilmelidir  
- Veriler güvenli şekilde saklanmalıdır  
- Sistem farklı cihazlardan erişilebilir olmalıdır  
- Sistem modüler ve geliştirilebilir olmalıdır  
- Veri aktarımında veri bütünlüğü korunmalıdır  

---

## 📖 User Stories

**User Story 1**

Rol: Çiftçi  
İstek: Tarlamdaki toprak nemi ve sıcaklık verilerini görmek istiyorum  
Sebep: Bitkilerimin durumunu takip edebilmek  

---

**User Story 2**

Rol: Çiftçi  
İstek: Sensör verilerinin yapay zeka tarafından analiz edilmesini istiyorum  
Sebep: Sulama ve gübreleme zamanlarını doğru planlamak  

---

**User Story 3**

Rol: Çiftçi  
İstek: Mobil uygulama üzerinden verileri görmek istiyorum  
Sebep: Tarlamı uzaktan kontrol etmek  

---

**User Story 4**

Rol: Kullanıcı  
İstek: Sisteme güvenli şekilde giriş yapmak  
Sebep: Kendi verilerime erişebilmek  

---

## Sonuç

Gereksinim analizi sayesinde sistemin teknik ihtiyaçları net şekilde belirlenmiştir. Bu aşama projenin doğru planlanması ve geliştirilmesi için güçlü bir temel oluşturmuştur.
