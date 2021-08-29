from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Settings():
    
    def __init__(self):
        self.path_file = 'config.yaml'
        self.read_file()
    
    def read_file(self):
        with open(self.path_file, 'r') as content:
            self.data = load(content, Loader=Loader)
    
    def get_port(self):
        return self.data['port']

    def get_host_address(self):
        return self.data['host_address']
    
    def get_num_clients(self):
        return self.data['num_clients']
    
    # def set_source(self, src):
    #     self.data['src'] = src
    #     with open(self.path_file, 'w') as edit:
    #         dump(self.data, edit)