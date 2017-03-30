#! -*- coding: utf-8 -*-
import os
from django import forms
from django.conf import settings
from json import JsonResponse
from django.views.generic import View
from origincore.forms.fileform import TempFileForm

class ProgressBarUploadView(View):

    def get(self, request):
        return JsonResponse({"status": 'ok'})

    def post(self, request):
        form = TempFileForm(self.request.POST, self.request.FILES)
        result = form.save_file(request=request, files=self.request.FILES)
        return JsonResponse(result)
