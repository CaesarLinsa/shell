python中获取程序内存，搭配pdb，可以获取每行代码的内存使用
```python
from memory_profiler import memory_usage
print(memory_usage(-1, interval=.2, timeout=.2));
```

