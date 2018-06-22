import time
from functools import wraps


def permission_required(permissions):
    def wrapper(func):
        def params_wrapper(*args, **kwargs):
            event, context = args
            is_admin = event.get('is_admin')
            context.log('event', event)
            context.log('context', context)
            if (event.get('datasettable') == 'table2') and (not is_admin):
                # house edit need permissions validate
                has_permissions = check_permissions(permissions, context)
                if not has_permissions:
                    return {
                        'status': 'error',
                        'message': '权限不足'
                    }

            return func(*args, **kwargs)
        return params_wrapper
    return wrapper


def log_time(func):
    def wrapper(*args):
        print(func.__name__, '<==wrapper name')
        start = time.time()
        func(*args)
        end = time.time()
        print(start-end)

    return wrapper


@log_time
def hi(*args):
    print('name:', args)


# 装饰器
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__)      # 输出 'with_logging'
        print(func.__doc__)       # 输出 None
        return func(*args, **kwargs)
    return with_logging

# 函数
@logged
def f(x):
   """does some math"""
   return x + x * x

f(20)
print(f.__name__, 'f的元信息')
