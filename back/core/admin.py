from django.contrib import admin

from . import models

admin.site.register(models.Bitext) # For the model to be administered in the admin pannel
admin.site.register(models.Text)
admin.site.register(models.Paragraph)
admin.site.register(models.Sentence)
admin.site.register(models.Alignment)
admin.site.register(models.Word)
admin.site.register(models.Translation)
