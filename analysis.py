import tensorflow as tf
import numpy as np

class TarimAnalizMotoru:
    """
    Tarım verileri üzerinde TensorFlow tabanlı istatistiksel analiz yapar.
    Verileri Tensor formatında işleyerek GPU hızlandırmasına ve 
    gelecekteki yapay zeka modellerine hazırlık sağlar.
    """

    @staticmethod
    def analiz_et(veri_listesi):
        if not veri_listesi:
            return None

        # 1. Veriyi TensorFlow Sabitine (Tensor) Dönüştür
        # Gelecekteki modeller float32 formatını sever
        tensor_veri = tf.constant(veri_listesi, dtype=tf.float32)

        # 2. Temel İstatistiksel Hesaplamalar
        # Ortalama: \mu = \frac{1}{n} \sum_{i=1}^{n} x_i
        ortalama = tf.reduce_mean(tensor_veri)

        # Standart Sapma: \sigma = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (x_i - \mu)^2}
        std_sapma = tf.math.reduce_std(tensor_veri)

        # Medyan: TensorFlow'da direkt reduce_median yoktur, veriyi sıralayıp ortayı buluruz
        sirali_veri = tf.sort(tensor_veri)
        n = tf.shape(sirali_veri)[0]
        
        if n % 2 == 1:
            medyan = sirali_veri[n // 2]
        else:
            medyan = (sirali_veri[n // 2 - 1] + sirali_veri[n // 2]) / 2.0

        return {
            "ortalama": float(ortalama.numpy()),
            "medyan": float(medyan.numpy()),
            "standart_sapma": float(std_sapma.numpy()),
            "veri_adedi": int(n.numpy())
        }