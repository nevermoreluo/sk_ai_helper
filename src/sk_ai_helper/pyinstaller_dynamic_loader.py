import importlib.util
import os
import sk_ai_helper.ai_helper

# 获取 module.py 文件的路径
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sk_ai_helper", 'ai_helper.py')


# 动态加载 module.py
spec = importlib.util.spec_from_file_location("module", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# 调用 module.py 中的函数
result = module.main()

