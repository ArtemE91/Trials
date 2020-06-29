from django.http import JsonResponse, HttpResponseRedirect


class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        if self.request.is_ajax():
            data = {
                'pk': instance.pk,
            }
            return JsonResponse(data, status=200)
        else:
            return HttpResponseRedirect(instance.get_absolute_url())