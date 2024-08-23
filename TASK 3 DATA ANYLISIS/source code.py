import pandas as pd
import matplotlib.pyplot as plt

data = {
    'City': ['Karachi', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Islamabad', 'Multan', 'Peshawar', 'Quetta'],
    'Population': [14.91, 11.13, 3.2, 2.1, 1.2, 1.87, 1.97, 1.14]
}




df = pd.DataFrame(data)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))


axes[0].bar(df['City'], df['Population'], color='skyblue')
axes[0].set_title('Population of Different Cities in Pakistan')
axes[0].set_xlabel('City')
axes[0].set_ylabel('Population (millions)')
axes[0].set_xticklabels(df['City'], rotation=45)

axes[1].plot(df['City'], df['Population'], marker='o', color='green', linestyle='-')
axes[1].set_title('Population Trend in Different Cities of Pakistan')
axes[1].set_xlabel('City')
axes[1].set_ylabel('Population (millions)')
axes[1].set_xticklabels(df['City'], rotation=45)



plt.tight_layout()
plt.show()