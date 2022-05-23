import pandas as pd
import plotly.express as px

# Documentation on treemap rendering can be found here:
# https://plotly.com/python/treemaps/
# https://www.roelpeters.be/make-treemap-in-python-with-plotly/



# Generate a list of files and their sizes (with full path)
raw_list = []
with open("file_list", 'rb') as raw_data:
    for line in raw_data:
        try:
            encoded = line.decode("utf-8")
            encoded = ' '.join(encoded.split()) # remove duplicate spaces
            items = encoded.split()            
            selection = [ items[4], ' '.join(items[8:]) ]
            raw_list.append(selection)
        except Exception as err:
            print(err)
print('{} items parsed. First item is: {}'.format(len(raw_list), raw_list[0]))



# Check the deepest path to explode the data
max_depth = 0
for item in raw_list:
    depth = len(item[1].split('/'))
    if depth > max_depth:
        max_depth = depth
print('Deepest path is: {}'.format(max_depth))


# Create Dataframe, make sure the number of columns matches the deepest path, rename size column properly
parsed_list = []
for item in raw_list:
    size = int(item[0])
    path = item[1].split('/')[1:]    
    path.extend( [None] * (max_depth - len(path) -1) )
    path.insert(0, size)
    parsed_list.append(path)

data = pd.DataFrame(parsed_list)
data.rename(columns={0: 'size'}, inplace=True)
data.head()


# Plot a Treemap visualization starting with the directory below /usb1; limit to files > 100MB; limit depth to 4 levels

lower_size_limit = 1024 * 1024 * 1 # 1G
depth = [2, 3, 4, 5, 6, 7]

# Filter out small files
filtered = data[data['size'] > lower_size_limit]
print('Unfiltered #files: {} #files after filtering: {}'.format(len(data), len(filtered)))

fig = px.treemap(filtered, path=depth, values='size', width=950, height=800)
fig.update_layout(    
    margin = dict(t=50, l=25, r=25, b=25))
fig.show()
