from django.db import models
from django.contrib.auth.models import User as AuthUser


class Image(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(
        max_length=10,
        choices=[
            ('jpg', 'JPEG'),
            ('jpeg', 'JPEG'),
            ('png', 'PNG'),
            ('gif', 'GIF'),
            ('bmp', 'BMP'),
            ('webp', 'WEBP'),
            ('svg', 'SVG'),
            ('tiff', 'TIFF'),
            ('ico', 'ICO')
        ],)

    uploaded_by = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='images_uploaded'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-created_at']
