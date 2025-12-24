from config.mapper import Mapper


class ServiceBase:

    def __init__(self, model_mapper: Mapper):
        self.model_mapper = model_mapper
        self.message_upload_password = ""
        self.message_reset_password = ""
        self.message_save = ""
        self.message_update = ""
        self.message_delete = ""
        self.path_base_front = ""
 
    