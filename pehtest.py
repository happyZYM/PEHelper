from sympy import symbols, sympify, diff
from mpmath import mp
from sympy import symbols, sympify, diff
from mpmath import mp

def evaluate_expression(expr, variable_values):
  return expr.subs(variable_values)

# 获取用户输入
num_independent_vars = int(input("输入自变量的数量: "))
independent_vars = [input(f"输入第{i+1}个自变量的名称: ") for i in range(num_independent_vars)]

# 构建符号变量
independent_vars_symbols = symbols(independent_vars)
independent_vars_symbols_dict = {var: symbols(var) for var in independent_vars}

# 存储中间变量和它们的表达式
intermediate_variables = {}

# 获取中间变量的定义
while True:
  intermediate_expr_str = input("输入中间变量的定义（例如：z=x**2+y**2），输入空字符串结束: ")
  if not intermediate_expr_str:
    break
  var_name, var_expr_str = intermediate_expr_str.split('=')
  var_name = var_name.strip()
  var_expr = sympify(var_expr_str)

  # 代入之前的中间变量值
  var_expr = var_expr.subs({var_symbol: var_expr for var_expr, var_symbol in intermediate_variables.values()})

  intermediate_variables[var_name] = (var_expr, symbols(var_name))  # 存储符号而不是表达式

# 获取最终因变量的名称和表达式
dependent_var_name, dependent_var_expr_str = input("输入最终因变量的定义（例如：f=z*x+y）: ").split('=')
dependent_var_name = dependent_var_name.strip()
dependent_var_expr = sympify(dependent_var_expr_str)

# 代入之前的信息
dependent_var_expr = dependent_var_expr.subs({var_symbol: var_expr for var_expr, var_symbol in intermediate_variables.values()})

# 求偏导数
partial_derivatives = {var_name: diff(dependent_var_expr, var_symbol) for var_name, var_symbol in independent_vars_symbols_dict.items()}

# 获取每个自变量的值，使用高精度的mp类型
mp.dps = 50
independent_var_values = {var: mp.mpf(input(f"输入 {var} 的值: ")) for var in independent_vars}

# 计算偏导数在给定点的值
partial_derivative_values = {var_name: derivative.subs(list(zip(independent_vars_symbols, list(independent_var_values.values())))) for var_name, derivative in partial_derivatives.items()}

# 打印偏导数的值
print(f"\n{dependent_var_name} 对 {', '.join(independent_vars)} 的偏导数:")
for var_name, partial_derivative_value in partial_derivative_values.items():
  print(f"∂{dependent_var_name}/∂{var_name} 在 {', '.join([f'{var}={independent_var_values[var]}' for var in independent_vars])} 时的值: {partial_derivative_value}")