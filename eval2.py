import pandas as pd
import matplotlib.pyplot as plt

# Data
df = pd.DataFrame({
    'weight': [1.25, 1.50, 1.75, 2.00],
    'BLEU':    [93.65, 92.90, 88.00, 80.11],
    'true_hits':[0.276,0.262,0.201,0.168],
})

# Plot
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df.weight, df.BLEU, marker='o', label='BLEU')
ax1.set_xlabel('Debias Weight')
ax1.set_ylabel('BLEU Score')
ax1.set_ylim(75, 100)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(df.weight, df.true_hits, marker='s', linestyle='--', label='True Hits')
ax2.set_ylabel('True Hits')
ax2.set_ylim(0.1, 0.3)

# Legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper right')

plt.title('BLEU and True Hits vs. Debias Weights')
plt.tight_layout()
plt.show()
