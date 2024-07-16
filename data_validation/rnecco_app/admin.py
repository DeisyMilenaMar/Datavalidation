from django.contrib import admin
from constance.admin import ConstanceAdmin, ConstanceForm, Config

class CustomConstanceForm(ConstanceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes personalizar el formulario si lo deseas

class CustomConstanceAdmin(ConstanceAdmin):
    change_list_form = CustomConstanceForm
    change_list_template = 'admin/constance/change_list.html'

admin.site.unregister([Config])
admin.site.register([Config], CustomConstanceAdmin)