import pandas as pd
import matplotlib.pyplot as plt

# Build DataFrame
df = pd.DataFrame({
    'weight': [1.25, 1.50, 1.75, 2.00],
    'BLEU':    [93.65, 92.90, 88.00, 80.11],
    'true_hits':[0.276,0.262,0.201,0.168],
    'rouge1_F1':[0.982,0.972,0.934,0.857],
    'rougL_F1': [0.982,0.966,0.920,0.844]
})

plt.figure(figsize=(8,4))
for col in ['BLEU','rouge1_F1','rougL_F1']:
# for col in ['BLEU','true_hits']:
    plt.plot(df.weight, df[col], marker='o', label=col)
plt.xlabel('Debias Weight')
plt.title('BLEU and ROUGE vs Debias Weights')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('bleu_rouge.png')
print("Saved plot to metrics_vs_weight.png")