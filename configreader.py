import ast
import operator

class ConfigException(Exception):
    pass

class Config(dict):
    def __init__(self,filelike,namespace={}):
        self._file = filelike
        self._file.seek(0)
        self._lines = self._file.read().splitlines()
        self._file.seek(0)
        self._load(namespace)

    def _load(self,namespace):
        tree = ast.parse(self._file.read())
        evaluator = Evaluator(namespace)
        for node in tree.body:
            if isinstance(node,ast.Assign):
                key = node.targets.pop().id
                try:
                    value = evaluator.eval(node.value)
                    self[key] = value
                    # also update our namespace
                    evaluator._safe_names[key] = value
                except Exception as e:
                    raise ConfigException(
                        'couldn\'t evaluate: {0}'.format(
                            self._lines[node.lineno-1]))


class Evaluator(object):
    _safe_names = {'None': None, 'True': True, 'False': False}

    def __init__(self,namespace):
        self._namespace = namespace

    def Str(self,node):
        return node.s

    def Num(self,node):
        return node.n

    def Name(self,node):
        if node.id in self._safe_names:
            return self._safe_names[node.id]
        else:
            print('not in safe namespace',node.id)

    def Tuple(self,node):
        return tuple(map(self.eval, node.elts))

    def List(self,node):
        return tuple(map(self.eval, node.elts))

    def Dict(self,node):
        return {self.eval(k):self.eval(v) for k, v
                    in zip(node.keys, node.values)}

    def UnaryOp(self,node):
        operand = self.eval(node.operand)
        opname = node.op.__class__.__name__.lower()
        if hasattr(operator,opname):
            return getattr(operator,opname)(operand)
        elif hasattr(operator,'%s_'%opname):
            return getattr(operator,'%s_'%opname)(operand)

    def BinOp(self,node):
        left = self.eval(node.left)
        right = self.eval(node.right)
        opname = node.op.__class__.__name__.lower()
        if hasattr(operator,opname):
            return getattr(operator,opname)(left,right)
        elif hasattr(operator,'%s_'%opname):
            return getattr(operator,'%s_'%opname)(left,right)

    def _get_func(self,value,attr):
        """ get the whole function path """
        if isinstance(value,ast.Attribute):
            return self._get_func(value.value,'%s.%s'%(value.attr,attr))
        else:
            return '%s.%s'%(value.id,attr)

    def Call(self,node):
        func = self._get_func(node.func.value,node.func.attr)
        args = [self.eval(arg) for arg in node.args]
        if func in self._namespace:
            return self._namespace[func](*args)
        else:
            raise ConfigException('"{0}" is not allowed'.format(func))

    def eval(self,node):
        return getattr(self,node.__class__.__name__)(node)

