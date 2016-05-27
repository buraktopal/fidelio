from django.db import models


class FidelioImage(models.Model):
    file_path = models.CharField(max_length=200, blank=True, null=True, default='N/A')

    class Meta(object):
        verbose_name = 'Image'
        verbose_name_plural = 'Image'

    def __str__(self):
        if self.file_name.lower() == 'n/a':
            return str(self.file_path) + str(self.pk)
        else:
            return str(self.file_path)


class Sound(models.Model):
    file_name = models.CharField(max_length=100, blank=True, null=True, default='N/A')
    samplerate = models.IntegerField(default=44100, blank=True, null=True)
    md5 = models.CharField(max_length=100, blank=True, null=True, default='N/A')
    images = models.ManyToManyField(FidelioImage)
    gif = models.CharField(max_length=100, blank=True, null=True, default='N/A')

    class Meta(object):
        verbose_name = 'Sound'
        verbose_name_plural = 'Sounds'

    def __str__(self):
        if self.file_name.lower() == 'n/a':
            return str(self.file_name) + str(self.pk)
        else:
            return str(self.file_name)