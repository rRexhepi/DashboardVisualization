from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models import Div

# Define the output HTML file path
output_html_path = 'data/output/minimal_test.html'
print(f"Generating minimal Bokeh dashboard at: {output_html_path}")

# Configure the output file
output_file(output_html_path, title='Minimal Bokeh Test Dashboard')

# Create simple Div components
div1 = Div(text="<h1>Hello, Bokeh!</h1>", width=400, height=100)
div2 = Div(text="<p>This is a test of your Bokeh installation.</p>", width=400, height=100)

# Arrange Divs in a column layout
layout = column(div1, div2)

# Display the layout
show(layout)
