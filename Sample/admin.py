from django.contrib import admin
from .models import Trials, Sample, SampleMaterial, SampleType, ReceivedValues


admin.site.register(Trials)
admin.site.register(Sample)
admin.site.register(SampleMaterial)
admin.site.register(SampleType)
admin.site.register(ReceivedValues)
