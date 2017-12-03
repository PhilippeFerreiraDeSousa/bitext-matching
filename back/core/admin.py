from django.contrib import admin

from . import models

admin.site.register(models.Message) # For the model to be administered in the admin pannel
admin.site.register(models.Category)
admin.site.register(models.Ingredient)
admin.site.register(models.Link)
