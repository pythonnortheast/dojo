from django.contrib import admin
from models import Country, CountryScore

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','total_score')


class CountryScoreAdmin(admin.ModelAdmin):
    list_display = ('for_country','from_country','score')
    list_filter = ('for_country','from_country')


admin.site.register(Country, CountryAdmin)
admin.site.register(CountryScore, CountryScoreAdmin)