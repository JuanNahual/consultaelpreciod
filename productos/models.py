# productos/models.py
import os
from django.db import models
from django.conf import settings  # Agrega esta línea

import qrcode

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Asegúrate de que el directorio 'qrcodes' exista
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'qrcodes'), exist_ok=True)

        super().save(*args, **kwargs)

        # Genera el código QR y guárdalo como una imagen
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://consultaelpreciod.pythonanywhere.com/productos/detalle/{self.id}/")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = os.path.join('qrcodes', f"{self.id}_qr.png")
        img_full_path = os.path.join(settings.MEDIA_ROOT, img_path)
        img.save(img_full_path)

        # Guarda la ruta de la imagen en el campo qr_code del producto
        self.qr_code.name = img_path
        super().save(*args, **kwargs)
