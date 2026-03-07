# 🌱 Akıllı Tarım Yönetim Sistemi

## 👥 Grup Üyeleri ve Görev Dağılımı
- **Ahmet Enes Altun** → Proje Mimari Tasarımı
- **Hayat Ay** → Proje Analizi ve Kapsam Belirleme  
- **Sami Yusuf Yıldız** → Gereksinim Toplama ve Analizi 
- **Ebubekir Yılmaz** → Teknoloji Araştırması ve Seçimi
- **Ceren Çam** → Geliştirme Ortamı Kurulumu

---

## 📌 Proje Açıklaması
Bu proje, sensör verileri ve yapay zeka kullanarak tarım süreçlerini optimize etmeyi amaçlamaktadır.  
Toprak nemi, sıcaklık ve hava durumu gibi veriler analiz edilerek sulama, gübreleme ve ilaçlama işlemleri daha verimli bir şekilde yönetilecektir.  

Sistem, tarım alanından toplanan verileri analiz ederek çiftçilere doğru kararlar almalarında yardımcı olur. Böylece hem verimlilik artırılır hem de su ve gübre gibi kaynakların gereksiz kullanımı azaltılır.

---

## 🛠️ Kullanılan Teknolojiler
- Python  
- TensorFlow  
- IoT Sensörleri  
- Django  
- PostgreSQL  

---

## 📦 Teslim Edilecek Modüller
- ✅ Sensör veri toplama modülü  
- ✅ Yapay zeka tabanlı analiz motoru  
- ✅ Web tabanlı yönetim paneli  
- ✅ Mobil uygulama  

---

## 🏗️ Proje Mimari Tasarımı (Ahmet Enes Altun)

### 📝 Genel Mimari
Akıllı Tarım Yönetim Sistemi, tarım alanına yerleştirilen IoT sensörlerinden veri toplayan, bu verileri analiz eden ve kullanıcıya web veya mobil uygulama üzerinden sunan bir sistemdir.

Sistem şu şekilde çalışır:  
- IoT sensörleri çevresel verileri toplar  
- Toplanan veriler backend API (Django) aracılığıyla sunucuya iletilir  
- Veriler PostgreSQL veritabanında saklanır  
- TensorFlow tabanlı yapay zeka modeli verileri analiz eder  
- Analiz sonuçları web paneli ve mobil uygulama üzerinden kullanıcıya sunulur  

---

### 🔧 Sistem Modülleri
- Sensör Veri Toplama Modülü  
- Veri İşleme ve Depolama Modülü  
- Yapay Zeka Analiz Modülü  
- Web Yönetim Paneli  
- Mobil Uygulama  

---

### 🧩 Bileşenler Arasındaki İlişki
IoT Sensörleri → Django API → PostgreSQL Veritabanı → TensorFlow Analiz Motoru → Web Paneli / Mobil Uygulama  

Sensörlerden gelen veriler backend tarafından alınır, veritabanında saklanır ve AI motoru ile analiz edilerek kullanıcılara öneriler ve otomatik kontrol sağlar.

---

### 🏛️ Kullanılan Tasarım Desenleri
- **Katmanlı Mimari (Layered Architecture)**: Veri katmanı, iş mantığı katmanı ve sunum katmanı olarak ayrılmıştır  
- **MVC (Model-View-Controller)**: Django frameworkü backend geliştirilmesinde bu yapıyı kullanır  

---

### 📊 Mimari Diyagram
![Akıllı Tarım Mimari Diyagramı](architecture.png)  
*(architecture.png dosyasını GitHub repo kök dizinine yükleyin)*
### ✅ Sonuç
Bu mimari yapı sayesinde sistem, sensörlerden gelen verileri analiz ederek tarım süreçlerini optimize eder. Modüler yapı sayesinde sistemin geliştirilmesi ve ileride genişletilmesi kolaydır.


---

# 🏗️ Teknoloji Araştırması ve Seçim Gerekçeleri (Ebubekir Yılmaz)

## 1. Programlama Dili: Python
Projenin ana geliştirme dili olarak **Python 3.10+** seçilmiştir.

* **Neden?** IoT cihazlarından veri çekme, TensorFlow ile yapay zeka modeli eğitme ve Django ile web sunucusu geliştirme süreçlerinin tamamını tek bir dil ekosisteminde birleştirerek ekip içi iş birliğini maksimize eder.
* **Gerekçe:** Geniş kütüphane desteği. Sensör verisi işleme için `Pandas`, karmaşık matematiksel hesaplamalar için `NumPy` gibi endüstri standardı araçlara sahiptir.

## 2. Backend Framework: Django & Django REST Framework (DRF)
Sistem mimarisinin web uygulama çatısı olarak **Django** tercih edilmiştir.

* **Neden?** "Pilleri dahil" (batteries-included) felsefesi sayesinde kullanıcı yönetimi, admin paneli ve veritabanı güvenliği hazır olarak sunulur. **DRF** ise mobil uygulama ve IoT cihazları için standartlara uygun bir API katmanı sağlar.
* **Gerekçe:** Veri güvenliği ve hızlı prototipleme yeteneği. Tarım verilerinin tutarlılığı için Django'nun gelişmiş ORM (Object-Relational Mapping) yapısı en güvenilir çözümdür.

## 3. Veritabanı: PostgreSQL (+ TimescaleDB)
Veri depolama birimi olarak ilişkisel veritabanı lideri **PostgreSQL** seçilmiştir.

* **Neden?** Çiftçi bilgileri ve tarla konumları gibi yapılandırılmış veriler için en sağlam açık kaynaklı çözümdür.
* **Gerekçe:** Tarım sensörlerinden gelen veriler "zaman serisi" (Time-series) niteliğindedir. **TimescaleDB** eklentisi ile milyonlarca satırlık veri üzerinde yüksek performanslı analizler yapılabilmektedir.

## 4. Yapay Zeka: TensorFlow & Keras
Analiz motoru ve karar destek mekanizması için **TensorFlow** kütüphanesi kullanılmaktadır.

* **Neden?** Derin öğrenme (Deep Learning) modelleri için dünya çapında standarttır.
* **Gerekçe:** Özellikle görüntü işleme (bitki hastalığı teşhisi) ve çok değişkenli hava durumu tahminleri için esnek ve güçlü bir altyapı sunar.

## 5. IoT İletişim Protokolü: MQTT (Mosquitto)
Sensör ve sunucu arasındaki haberleşme için **MQTT** protokolü belirlenmiştir.

* **Neden?** Standart HTTP protokolünün IoT cihazları için oluşturduğu yükü (overhead) ortadan kaldırır. Düşük enerji tüketimi için optimize edilmiştir.
* **Gerekçe:** Tarladaki sensörlerin pil ömrünü korur ve zayıf internet bağlantısı olan kırsal bölgelerde bile veri iletimini garanti eder.

---

## 📊 Özet Karşılaştırma Tablosu

| Bileşen | Seçilen Araç | En Büyük Avantajı |
| :--- | :--- | :--- |
| **Dil** | Python 3.10+ | Ekosistem birliği (AI + Web + Scripting) |
| **Veri Analizi** | Pandas / NumPy | Sensör verilerini temizleme ve işleme hızı |
| **Haberleşme** | MQTT / WebSockets | Gerçek zamanlı veri akışı ve düşük enerji tüketimi |
| **Deployment** | Docker | Ortam bağımsız, hızlı ve hatasız kurulum |
