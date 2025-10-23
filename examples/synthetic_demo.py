import numpy as np
from mareval import CHOModel, compute_auc, delta_auc_test, bias_assessment, phi, print_summary

np.random.seed(42)
U = np.eye(10)
model = CHOModel(U)

g_signal = np.random.normal(1, 0.2, (10, 100))
g_noise = np.random.normal(0, 0.2, (10, 100))
t_signal, t_noise, _ = model.compute_test_statistic(g_signal, g_noise)

auc_baseline = [compute_auc(t_signal, t_noise) for _ in range(5)]
auc_mar = [a + np.random.uniform(0.01, 0.03) for a in auc_baseline]

p_value, delta_auc = delta_auc_test(auc_baseline, auc_mar)
bias = bias_assessment(auc_baseline, auc_mar)

print_summary(auc_baseline, auc_mar, p_value, bias)
