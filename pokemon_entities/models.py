from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
	title = models.CharField(max_length=255, null=False)
	image = models.ImageField(blank=True, upload_to='images')

	def __str__(self):
		return self.title