import seaborn as sns
labels = ['LEVEL','NUMBER','POSTCODE','POSTNAVN','STREET','UNIT','VEJBY']
matrix = [[1.0, 0, 0, 0, 0, 0, 0],
         [0, 0.99606, 0, 0, 0, 0.004, 0],
         [0, 0, 0.99713, 0, 0, 0.003, 0],
         [0, 0, 0, 0.93020, 0.003, 0, 0.0668],
         [0, 0, 0, 0, 0.96054, 0, 0],
         [0, 0, 0.001, 0, 0, 0.99831, 0],
         [0, 0, 0, 0.638, 0.19099, 0, 0.17101]]
ax = sns.heatmap(matrix, annot=True, cmap='Blues',xticklabels=labels,yticklabels=labels,fmt='.3f')
fig = ax.get_figure()
fig.savefig("Flair_confusion_matrix.png")