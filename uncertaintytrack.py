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