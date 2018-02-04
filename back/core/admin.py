from django.contrib import admin

from . import models

admin.site.register(models.Bitext) # For the model to be administered in the admin pannel
admin.site.register(models.Text)
admin.site.register(models.Paragraph)
admin.site.register(models.Sentence)
