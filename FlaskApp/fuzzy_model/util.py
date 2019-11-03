   
class Zero_dict(dict):
    def __getitem__(self, key):
        self.setdefault(key,0)
        return dict.__getitem__(self,key)


def get_column_vector(matrix, col_id):
  return matrix[:, col_id]
