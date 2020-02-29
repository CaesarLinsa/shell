# -*- encoding:utf-8 -*-
from inspect import signature
from functools import wraps


def expose(*type_args, **type_kwargs):
    def decorate(func):
        # 获取所装饰的方法的对象sig
        sig = signature(func)
        if "return_type" in type_kwargs:
            return_type = type_kwargs.pop("return_type")
        # OrderedDict([('args', <class 'int'>)])
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # 参数和值tuple 形成的有序字典 OrderedDict([('x', 1)])
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                        )
            # 如果未设置返回类型，则不作判断，否则进行类型判断
            if return_type is None:
                return func(*args, **kwargs)
            else:
                f = func(*args, **kwargs)
                if not isinstance(f, return_type):
                    raise TypeError(
                        'Argument {} must be {}'.format(f, return_type)
                    )
                return f

        return wrapper
    return decorate
