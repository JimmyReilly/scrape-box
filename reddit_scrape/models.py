from django.db import models

class Link(models.Model):
	title = models.CharField(max_length=2000)

	def __str__(self):
		return self.title