from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
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

    # Filtre degerleri gecersizse sessizce yoksay
    try:
        if baslangic:
            veriler = veriler.filter(timestamp__date__gte=baslangic)
        if bitis:
            veriler = veriler.filter(timestamp__date__lte=bitis)
        if cihaz:
            veriler = veriler.filter(device_id__icontains=cihaz[:50])
    except (ValidationError, ValueError):
        veriler = SensorData.objects.none()

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


@login_required
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


@login_required
def sensor_listesi(request):
    cihazlar = SensorData.objects.values('device_id').distinct()
    return render(request, 'dashboard/sensor_listesi.html', {'cihazlar': cihazlar})


@login_required
@require_http_methods(["GET", "POST"])
def sensor_ekle(request):
    if request.method == 'POST':
        try:
            veri = {
                'device_id':     (request.POST.get('device_id') or '').strip(),
                'temperature':   float(request.POST.get('temperature', 0)),
                'humidity':      float(request.POST.get('humidity', 0)),
                'soil_moisture': float(request.POST.get('soil_moisture', 0)),
            }
        except (ValueError, TypeError):
            return render(request, 'dashboard/sensor_ekle.html',
                          {'hata': 'Sayisal alanlara gecerli sayi girin.'})

        # Ek guvenlik: device_id uzunlugu (XSS payload korumasi)
        if not veri['device_id'] or len(veri['device_id']) > 50:
            return render(request, 'dashboard/sensor_ekle.html',
                          {'hata': 'Cihaz ID bos olamaz, en fazla 50 karakter.'})

        # validators.py entegrasyonu
        dogrulama = sensor_verisini_dogrula(veri)
        if not dogrulama['gecerli']:
            return render(request, 'dashboard/sensor_ekle.html', {
                'hatalar': dogrulama['hatalar']
            })

        SensorData.objects.create(**veri)
        return redirect('dashboard')

    return render(request, 'dashboard/sensor_ekle.html')


@login_required
@require_POST
def sensor_sil(request, device_id):
    # @require_POST dekoratörü ile sadece POST kabul edilir
    SensorData.objects.filter(device_id=device_id).delete()
    return redirect('sensor_listesi')