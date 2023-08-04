from django.db import models


class GlobalSettings(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.value}"

    class Meta:
        verbose_name = "Global Settings"
        verbose_name_plural = "Global Settings"
