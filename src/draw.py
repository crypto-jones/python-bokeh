import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, LabelSet, Label, ColumnDataSource
from bokeh.palettes import Spectral8

from graph import *

WIDTH = 500
HEIGHT = 500
CIRCLE_SIZE = 30

graph_data = Graph()
graph_data.debug_create_test_data()
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes)
node_indices = list(range(N))

color_list = []
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_axis_label='Time', y_axis_label='Price', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = Circle(size=CIRCLE_SIZE, fill_color='color')

# this is drawing the edges from start to end
start_indexes = []
end_indexes = []

for start_index, vertex in enumerate(graph_data.vertexes):
    for e in vertex.edges:
        start_indexes.append(start_index)
        end_indexes.append(graph_data.vertexes.index(e.destination))

#########  1. this is drawing the edges from start to end ########
graph.edge_renderer.data_source.data = dict(
    # this is a list of some kind that has to do with starting points
    start=start_indexes,
    end=[end_indexes])  # this is a list of some kind that has to do with ending points


print(graph.edge_renderer.data_source.data)
# start of layout code
# change from 8 to N to make it dynamic

x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)


plot.renderers.append(graph)

source = ColumnDataSource(data=dict(height=[196, 71, 72, 68, 58, 62],
                                    weight=[165, 189, 220, 141, 260, 174],
                                    names=['Mark', 'Amir', 'Matt', 'Greg',
                                           'Owen', 'Juan']))

# Create a new dictionary to use as a data source with 3 lists in it ordered in the same way as vertexes
# List of x values
# List of y values
# List of labels

value = [v.value for v in graph_data.vertexes]

label_source = ColumnDataSource(data=dict(x=x, y=y, v=value))

labels = LabelSet(x='x', y='y', text='v', level='glyph',
                  source=label_source, render_mode='canvas', text_align='center', text_baseline='middle')

plot.add_layout(labels)


output_file('graph.html')
show(plot)
