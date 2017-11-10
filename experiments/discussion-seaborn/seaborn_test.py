import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

iris = pd.read_csv('https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv')
# iris.head()

jp = sns.jointplot(x="petal_length", y="petal_width", data=iris, size=5)
plt.show()

ax = sns.boxplot(x="species", y="petal_width", data=iris)
plt.show()

g = sns.pairplot(iris, hue="species", palette="husl",
                 vars=["sepal_length", "sepal_width", "petal_length", "petal_width"])
plt.show()
