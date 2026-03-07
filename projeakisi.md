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

---

### ✅ Sonuç
Bu mimari yapı sayesinde sistem, sensörlerden gelen verileri analiz ederek tarım süreçlerini optimize eder. Modüler yapı sayesinde sistemin geliştirilmesi ve ileride genişletilmesi kolaydır.
