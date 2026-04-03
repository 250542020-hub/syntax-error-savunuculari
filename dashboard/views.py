from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from api.models import SensorData


def dashboard(request):
    # Filtreleme
    baslangic = request.GET.get('baslangic')
    bitis = request.GET.get('bitis')
    cihaz = request.GET.get('cihaz', '')

    veriler = SensorData.objects.all().order_by('-timestamp')

    if baslangic:
        veriler = veriler.filter(timestamp__date__gte=baslangic)
    if bitis:
        veriler = veriler.filter(timestamp__date__lte=bitis)
    if cihaz:
        veriler = veriler.filter(device_id__icontains=cihaz)

    # Grafik için son 20 veri
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

    # Özet istatistikler
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


def sensor_listesi(request):
    cihazlar = SensorData.objects.values('device_id').distinct()
    return render(request, 'dashboard/sensor_listesi.html', {'cihazlar': cihazlar})


def sensor_ekle(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        temperature = float(request.POST.get('temperature', 0))
        humidity = float(request.POST.get('humidity', 0))
        soil_moisture = float(request.POST.get('soil_moisture', 0))
        SensorData.objects.create(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            soil_moisture=soil_moisture,
        )
        return redirect('dashboard')
    return render(request, 'dashboard/sensor_ekle.html')


def sensor_sil(request, device_id):
    if request.method == 'POST':
        SensorData.objects.filter(device_id=device_id).delete()
    return redirect('sensor_listesi')
