from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from .models import customer
from django import forms

class CsvImportFrom(forms.Form):
    csv_upload = forms.FileField()

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded!!!')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for i in csv_data:
                fields = i.split(",")
                created = customer.objects.update_or_create(
                    name=fields[0],
                    balance=fields[1],
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)



        form = CsvImportFrom()
        data = {"form": form}
        return render(request, 'admin/csv_upload.html', data)

admin.site.register(customer, CustomerAdmin)

