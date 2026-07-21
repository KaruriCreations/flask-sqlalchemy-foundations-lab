import ast

class StrPatch(ast.Constant):
    def __init__(self, s=None, value=None, **kwargs):
        if s is not None:
            value = s
        super().__init__(value=value)

    @property
    def s(self):
        return self.value

    @s.setter
    def s(self, val):
        self.value = val

ast.Str = StrPatch
