import OpenOPC


class OPCclient:

    def __init__(self):
        # self.server = "InSAT.Multi-ProtocolMasterOPCServer.DA"
        self.server = "InSAT.ModbusOPCServer.DA"
        self.client = OpenOPC.client()
        self.client.connect(self.server)
        self.tags = [] # Список имен тегов
        self.search_tags()


    # Создание списка всех тегов
    def search_tags(self):
        nodes = self.client.list()
        devices = self.client.list(nodes[0])
        try: 
            for i in range(32):
                self.tags.append(self.client.list(nodes[0] + '.' + devices[0])[i])
        # При выходе за пределы списка тегов продолжает работу программы
        except Exception:
            pass


    # Чтение определенного тега
    def read(self, tag_num):
        val = self.client.read(self.tags[tag_num], update=1, include_error=True)
        return val[0]


    # Запись определенного тегоа
    def write(self, tag_num: int, valume: float) -> float:
        val = self.client.write((self.tags[tag_num], valume), include_error=True)
        return val[0]
