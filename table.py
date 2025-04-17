import pandas as pd
import matplotlib.pyplot as plt

# build the DataFrame
df = pd.DataFrame({
    'weight':     [1.25, 1.50, 1.75, 2.00],
    'BLEU (%)':   [93.65, 92.90, 88.00, 80.11],
    'true_hits':  [0.276, 0.262, 0.201, 0.168],
    'ROUGE-1 F1': [0.982, 0.972, 0.934, 0.857],
    'ROUGE-L F1': [0.982, 0.966, 0.920, 0.844]
})

fig, ax = plt.subplots(figsize=(6,2))
ax.axis('off')

# draw the table
tbl = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='center'
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.5)

plt.tight_layout()
plt.savefig('metrics_table.png', dpi=300, bbox_inches='tight')
print("Saved table image to metrics_table.png")