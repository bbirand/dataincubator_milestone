import Quandl
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Spectral6, RdYlGn4

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  # Read the query string to get the name of the object
  if "symbol" not in request.args:
      # If symbol wasn't given, return the empty template
      return render_template('index.html')

  #Parse "features" for getting a list of the attributes to show, use that instead of just "Open"
  features =request.args.getlist('features')

  # We were given the symbol
  stock_name = request.args["symbol"]
  quandl_stock_name = "WIKI/{}".format(stock_name)

  # Call Quandl to get the stock
  dat = Quandl.get(quandl_stock_name, authtoken="tRQEod_Z4qdGBEzjjGxo")
  #dat = dat["Open"]

  # Create bokeh graph using `figure()`
  p = figure(x_axis_type="datetime", plot_width=700)

  #Plot several figures, not just one
  for i_f, f in enumerate(features):
      p.line(dat.index, dat[f], line_width=2, color=RdYlGn4[i_f], legend=f)

  # Call `components` on this graph
  script, div = components(p)

  # Insert these variables into the template
  return render_template('index.html', stock_name = stock_name, dat_script = script, dat_div = div)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=33507)
