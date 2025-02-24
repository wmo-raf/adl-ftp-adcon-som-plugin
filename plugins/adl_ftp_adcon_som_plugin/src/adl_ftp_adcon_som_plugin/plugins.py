from adl.core.registries import Plugin


class PluginNamePlugin(Plugin):
    type = "adl_ftp_adcon_som_plugin"
    label = "ADL FTP Adcon Som Plugin"

    def get_urls(self):
        return []

    def get_data(self):
        return []
