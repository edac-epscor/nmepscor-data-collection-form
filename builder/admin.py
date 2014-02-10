from django.contrib import admin

from models import metadataModel
# Register your models here.


class metadataModelAdmin(admin.ModelAdmin):
    model = metadataModel

    list_filter = ('username', 'finalized')
    list_display = ('identifier', 'username', 'finalized', 'started', 'modified')
    list_display_links = ('identifier', )
    search_fields = ('username', 'identifier')

    readonly_fields = ('username', 'finalized', 'modified', 'started')


admin.site.register(metadataModel, metadataModelAdmin)
