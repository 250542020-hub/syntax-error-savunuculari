from django.shortcuts import render, redirect
from api.models import SensorData
from api.validators import sensor_verisini_dogrula

# ─────────────────────────────────────────────
# DÜZELTME 1: timezone ve timedelta import'ları
# kullanılmıyordu, kaldırıldı.
# ─────────────────────────────────────────────

def _filtrelenmis_veriler(request):
    """
    DÜZELTME 2: Filtreleme mantığı dashboard() içinde
    tekrarlanıyordu. Tek fonksiyona taşındı.
    sensor_listesi() de ihtiyaç duyarsa buradan çağırır.
    """
    baslangic = request.GET.get('baslangic')
    bitis     = request.GET.get('bitis')
    cihaz     = request.GET.get('cihaz', '')

    veriler = SensorData.objects.order_by('-timestamp')  # DÜZELTME 3: gereksiz .all() kaldırıldı

    if baslangic:
        veriler = veriler.filter(timestamp__date__gte=baslangic)
    if bitis:
        veriler = veriler.filter(timestamp__date__lte=bitis)
    if cihaz:
        veriler = veriler.filter(device_id__icontains=cihaz)

    return veriler, baslangic, bitis, cihaz


def _grafik_verisi_olustur(veriler, limit=20):
    """
    DÜZELTME 4: Grafik verisi oluşturma dashboard() içinde
    satır içi yazılmıştı. Okunabilirlik için ayrı fonksiyon.
    """
    return [
        {
            'timestamp':    v.timestamp.strftime('%H:%M:%S'),
            'temperature':  v.temperature,
            'humidity':     v.humidity,
            'soil_moisture': v.soil_moisture,
            'device_id':    v.device_id,
        }
        for v in veriler[:limit]
    ]


def dashboard(request):
    veriler, baslangic, bitis, cihaz = _filtrelenmis_veriler(request)

    context = {
        'veriler':          veriler[:50],
        'grafik_verisi':    _grafik_verisi_olustur(veriler),
        'son_veri':         veriler.first(),
        'toplam':           veriler.count(),
        'cihazlar':         SensorData.objects.values_list('device_id', flat=True).distinct(),
        'filtre_baslangic': baslangic or '',
        'filtre_bitis':     bitis or '',
        'filtre_cihaz':     cihaz,
    }
    return render(request, 'dashboard/dashboard.html', context)


def sensor_listesi(request):
    cihazlar = SensorData.objects.values('device_id').distinct()
    return render(request, 'dashboard/sensor_listesi.html', {'cihazlar': cihazlar})


def sensor_ekle(request):
    if request.method == 'POST':
        veri = {
            'device_id':    request.POST.get('device_id', ''),
            'temperature':  float(request.POST.get('temperature', 0)),
            'humidity':     float(request.POST.get('humidity', 0)),
            'soil_moisture': float(request.POST.get('soil_moisture', 0)),
        }

        # DÜZELTME 5: Doğrulama yoktu, herhangi bir değer
        # veritabanına yazılabiliyordu. validators.py entegre edildi.
        dogrulama = sensor_verisini_dogrula(veri)
        if not dogrulama['gecerli']:
            return render(request, 'dashboard/sensor_ekle.html', {
                'hatalar': dogrulama['hatalar']
            })

        SensorData.objects.create(**veri)
        return redirect('dashboard')

    return render(request, 'dashboard/sensor_ekle.html')


def sensor_sil(request, device_id):
    # DÜZELTME 6: GET isteğiyle de silme yapılabiliyordu.
    # Sadece POST ile silmeye izin verildi (zaten öyleydi, korundu).
    if request.method == 'POST':
        SensorData.objects.filter(device_id=device_id).delete()
    return redirect('sensor_listesi')
