

class FileService:

    @classmethod
    def create_file(cls, namearchivo: str, data: dict,config):
        archiv = "".join([namearchivo, config.fecha])
        with open(archiv, "a") as file:
            for key, value in data.items():
                file.writelines(f"{key} - {value}\n")

