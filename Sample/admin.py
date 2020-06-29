from django.contrib import admin
from .models import Sample, SampleMaterial, SampleType


admin.site.register(Sample)
admin.site.register(SampleMaterial)
admin.site.register(SampleType)

