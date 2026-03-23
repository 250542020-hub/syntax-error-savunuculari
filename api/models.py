from django.db import models

class SensorData(models.Model):
    device_id = models.CharField(max_length=50, verbose_name="Cihaz Kimliği")
    temperature = models.FloatField(verbose_name="Sıcaklık (°C)")
    humidity = models.FloatField(verbose_name="Hava Nemi (%)")
    soil_moisture = models.FloatField(verbose_name="Toprak Nemi (%)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Zamanı")

    class Meta:
        verbose_name_plural = "Sensör Verileri"

    def __str__(self):
        return f"{self.device_id} - {self.timestamp}"