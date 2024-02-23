import scipy.stats as stats
import mpmath
def GetTFactor_Double(n, confidence_level=0.95):
  # 设置自由度（degrees of freedom）
  df = n - 1
  # 计算双侧95%置信度下的t值
  alpha = (1 - confidence_level) / 2  # 每个尾部的概率
  return stats.t.ppf(1 - alpha, df)
