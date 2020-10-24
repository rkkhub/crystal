import pandas as pd

dfs = pd.read_html('http://www.contextures.com/xlSampleData01.html', header=0)

print(dfs[0].head(5))
print