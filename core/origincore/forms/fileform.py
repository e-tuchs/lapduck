#! -*- coding: utf-8 -*-
import os

class TempFileForm(forms.Form):
    file_name = []

    def __init__(self, *args, **kwargs):
        super(TempFileForm, self).__init__(*args, **kwargs)
