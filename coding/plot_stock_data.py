# filename: plot_stock_data.py

# Import required library
import matplotlib.pyplot as plt

# Plot the data
plt.figure(figsize=(14,7))
for c in stock_data.columns.values:
    plt.plot(stock_data.index, stock_data[c], lw=3, alpha=0.8,label=c)
plt.legend(loc='upper left', fontsize=12)
plt.ylabel('Price in $')
plt.show()