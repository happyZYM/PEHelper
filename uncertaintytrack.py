from sympy import symbols, sympify, diff
from mpmath import mp
from utils import GetTFactor_Double

def TrackUncertainty(data):
  confidence_level=mp.mpf(data["confidence"])
  dps=mp.mpf(data["accuracy"])
  independent_vars=[var for var in data['independent_vars']]
  independent_vars_symbols = symbols(independent_vars)
  independent_vars_symbols_dict = {var: symbols(var) for var in independent_vars}
  intermediate_variables = {}
  # 开始处理中间变量
  for var in data['intermediate_vars']:
    var_name = var['name']
    var_expr = sympify(var['expr'])
    var_expr = var_expr.subs({var_symbol: var_expr for var_expr, var_symbol in intermediate_variables.values()})
    intermediate_variables[var_name] = (var_expr, symbols(var_name))
  # 处理因变量
  dependent_var_name = data['dependent_var']['name']
  dependent_var_expr = sympify(data['dependent_var']['expr'])
  dependent_var_expr = dependent_var_expr.subs({var_symbol: var_expr for var_expr, var_symbol in intermediate_variables.values()})
  partial_derivatives = {var_name: diff(dependent_var_expr, var_symbol) for var_name, var_symbol in independent_vars_symbols_dict.items()}
  # 开始数值计算
  ret=dict()
  mp.dps = dps
  for var in data['independent_vars']:
    ret[var]={
      "value": mp.mpf(0),
      "uncertainty": mp.mpf(0)
    }
    if data['independent_vars'][var]['type'] == "single":
      scale = 1
      # check if has field scale
      if 'scale' in data['independent_vars'][var]:
        scale = mp.mpf(data['independent_vars'][var]['scale'])
      system_error = 0
      # check if has field system_error
      if 'system_error' in data['independent_vars'][var]:
        system_error = mp.mpf(data['independent_vars'][var]['system_error'])
      ret[var]["value"] = (mp.mpf(data['independent_vars'][var]['var']) - system_error) * scale
      ret[var]["uncertainty"] = mp.mpf(data['independent_vars'][var]['tolerance']) * scale * confidence_level
    elif data['independent_vars'][var]['type'] == "multiple":
      scale = 1
      # check if has field scale
      if 'scale' in data['independent_vars'][var]:
        scale = mp.mpf(data['independent_vars'][var]['scale'])
      system_error = 0
      # check if has field system_error
      if 'system_error' in data['independent_vars'][var]:
        system_error = mp.mpf(data['independent_vars'][var]['system_error'])
      t=mp.mpf(GetTFactor_Double(len(data['independent_vars'][var]['var'])-1, mp.mpf(confidence_level)))
      sum=mp.mpf(0)
      for val in data['independent_vars'][var]['var']:
        sum+=(mp.mpf(val) - system_error) * scale
      ret[var]["value"]=sum/len(data['independent_vars'][var]['var'])
      delta=mp.mpf(0)
      for val in data['independent_vars'][var]['var']:
        delta+=((mp.mpf(val) - system_error) * scale-ret[var]["value"])**2
      error_A=t*mp.sqrt(delta/(len(data['independent_vars'][var]['var'])*(len(data['independent_vars'][var]['var'])-1)))
      error_B=mp.mpf(data['independent_vars'][var]['tolerance']) * scale * confidence_level
      ret[var]["uncertainty"]=mp.sqrt(error_A**2+error_B**2)
    else:
      ret[var]["value"]=mp.mpf(data['independent_vars'][var]['var'])
      ret[var]["uncertainty"]=mp.mpf(data['independent_vars'][var]['uncertainty'])
  independent_var_values={var: ret[var]["value"] for var in independent_vars}
  partial_derivative_values = {var_name: derivative.subs(list(zip(independent_vars_symbols, list(independent_var_values.values())))).evalf(mp.dps) for var_name, derivative in partial_derivatives.items()}
  for var_name in independent_vars:
    ret[var_name]["derivative"]=partial_derivative_values[var_name]
  ret[dependent_var_name] = {
    "value": dependent_var_expr.subs(list(zip(independent_vars_symbols, list(independent_var_values.values())))).evalf(mp.dps),
    "uncertainty": mp.sqrt(mp.fsum([partial_derivative_values[var]**2*ret[var]["uncertainty"]**2 for var in independent_vars]))
  }
  return ret

if __name__ == "__main__":
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
  mp.dps = 1000
  independent_var_values = {var: mp.mpf(input(f"输入 {var} 的值: ")) for var in independent_vars}

  # 计算偏导数在给定点的值
  partial_derivative_values = {var_name: derivative.subs(list(zip(independent_vars_symbols, list(independent_var_values.values())))) for var_name, derivative in partial_derivatives.items()}

  # 打印偏导数的值
  print(f"\n{dependent_var_name} 对 {', '.join(independent_vars)} 的偏导数:")
  for var_name, partial_derivative_value in partial_derivative_values.items():
    print(f"∂{dependent_var_name}/∂{var_name} 在 {', '.join([f'{var}={independent_var_values[var]}' for var in independent_vars])} 时的值: {partial_derivative_value}")