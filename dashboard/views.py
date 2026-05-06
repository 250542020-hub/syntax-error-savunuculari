from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from api.models import SensorData


@login_required
def dashboard(request):
    baslangic = request.GET.get('baslangic')
    bitis = request.GET.get('bitis')
    cihaz = request.GET.get('cihaz', '')

    veriler = SensorData.objects.all().order_by('-timestamp')

    # Filtre degerleri gecersizse sessizce yoksay
    # (SQL injection / bozuk girdi koruması — view'in cokmesini engeller)
    try:
        if baslangic:
            veriler = veriler.filter(timestamp__date__gte=baslangic)
        if bitis:
            veriler = veriler.filter(timestamp__date__lte=bitis)
        if cihaz:
            # device_id 50 karakterle sinirli, daha uzun girdileri kes
            veriler = veriler.filter(device_id__icontains=cihaz[:50])
    except (ValidationError, ValueError):
        veriler = SensorData.objects.none()

    grafik_verisi = [
        {
            'timestamp': v.timestamp.strftime('%H:%M:%S'),
            'temperature': v.temperature,
            'humidity': v.humidity,
            'soil_moisture': v.soil_moisture,
            'device_id': v.device_id,
        }
        for v in veriler[:20]
    ]

    son_veri = veriler.first()
    toplam = veriler.count()

    context = {
        'veriler': veriler[:50],
        'grafik_verisi': grafik_verisi,
        'son_veri': son_veri,
        'toplam': toplam,
        'cihazlar': SensorData.objects.values_list('device_id', flat=True).distinct(),
        'filtre_baslangic': baslangic or '',
        'filtre_bitis': bitis or '',
        'filtre_cihaz': cihaz,
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
            device_id = (request.POST.get('device_id') or '').strip()
            temperature = float(request.POST.get('temperature', 0))
            humidity = float(request.POST.get('humidity', 0))
            soil_moisture = float(request.POST.get('soil_moisture', 0))
        except (ValueError, TypeError):
            return render(request, 'dashboard/sensor_ekle.html',
                          {'hata': 'Sayisal alanlara gecerli sayi girin.'})

        if not device_id or len(device_id) > 50:
            return render(request, 'dashboard/sensor_ekle.html',
                          {'hata': 'Cihaz ID bos olamaz, en fazla 50 karakter.'})

        if not (-10 <= temperature <= 60 and 0 <= humidity <= 100 and 0 <= soil_moisture <= 100):
            return render(request, 'dashboard/sensor_ekle.html',
                          {'hata': 'Degerler gecerli aralik disinda.'})

        SensorData.objects.create(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            soil_moisture=soil_moisture,
        )
        return redirect('dashboard')
    return render(request, 'dashboard/sensor_ekle.html')


@login_required
@require_POST
def sensor_sil(request, device_id):
    SensorData.objects.filter(device_id=device_id).delete()
    return redirect('sensor_listesi')