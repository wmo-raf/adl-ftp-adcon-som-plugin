from adl_ftp_plugin.registries import ftp_decoder_registry
from django.apps import AppConfig

from .decoders import AdconSOMDecoder


class PluginNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "adl_ftp_adcon_som_plugin"
    
    def ready(self):
        ftp_decoder_registry.register(AdconSOMDecoder())
