from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Concursante(models.Model):
	competencia			= models.CharField(max_length=150)
	evento	 			= models.CharField(max_length=150)
	fecha_subida		= models.DateTimeField(auto_now_add=True)
	 	
	aprendices 			= models.CharField(max_length=1000)		
	region	 			= models.CharField(max_length=150)
	total	 			= models.IntegerField()
	dia_1	 			= models.IntegerField()
	dia_2	 			= models.IntegerField()
	dia_3	 			= models.IntegerField()
	dia_4	 			= models.IntegerField()

	def __unicode__ (self):
		return self.competencia +" "+ self.aprendices +" "+ self.region +" "+ str(self.total)+" "+ str(self.dia_1)+" "+ str(self.dia_2)+" "+ str(self.dia_3)+" "+ str(self.dia_4)



