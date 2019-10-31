   
class Zero_dict(dict):
    def __getitem__(self, key):
        self.setdefault(key,1<<50)
        return dict.__getitem__(self,key)