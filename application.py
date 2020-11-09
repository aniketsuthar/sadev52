from flask import Flask, render_template, request
from pandas_datareader import data
from pandas import DataFrame
from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import LabelSet, HoverTool, ColumnDataSource
from datetime import datetime
from pandas_datareader._utils import RemoteDataError

application = Flask(__name__)

script1, div1 = ('', '')
js_files, css_files = '', ''
error = ''


@application.route('/plot', methods=['POST'])
def draw_plot():
    if request.method == 'POST':
        try:
            date = datetime.now().strftime("%Y,%m,%d")
            date = date.split(",")
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            code = request.form['code']
            start = datetime(year, month - 1, 1)
            global error
            error = 'please enter correct code'

            end = datetime(year, month, day)

            df = data.DataReader(code.upper(), 'yahoo', start=start, end=end)

            # if code == '' or df:

            # df.index[df.Close > df.Open]

            def inc_dec(c, o):
                if c > o:
                    return "Increase"
                elif c < o:
                    return "Decrease"
                else:
                    return "Equal"

            df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
            df["Middle"] = (df.Open + df.Close) / 2
            df["Width"] = 12 * 60 * 60 * 1000
            df["Height"] = abs(df.Open - df.Close)

            f = figure(x_axis_type="datetime", width=1000, height=700, sizing_mode="scale_width")
            f.xaxis.axis_label = 'Date'
            f.yaxis.axis_label = 'Price in $'
            f.title.text = "Candlestick Graph for " + code.upper()

            f.grid.grid_line_alpha = 0.5
            cds = ColumnDataSource(df)
            cds1 = ColumnDataSource(df[df.Status == "Increase"])
            cds2 = ColumnDataSource(df[df.Status == "Decrease"])
            tooltip = HoverTool(
                tooltips=[("High", "@High{111.11111}"), ("Low", "@Low{111.11111}"), ("Open", "@Open{111.111111}"),
                          ("Close", "@Close{111.11111}")])

            f.add_tools(tooltip)

            f.segment(x0="Date", y0="High", x1="Date", y1="Low", line_color="black", line_width=1, source=cds)

            f.rect(x="Date", y="Middle",
                   width="Width",
                   height="Height", fill_color="green", line_color='black', source=cds1)

            f.rect(x="Date", y="Middle",
                   width="Width",
                   height="Height", fill_color="red", line_color='black', source=cds2)
            global script1, div1, js_files, css_files

            js_files = CDN.js_files[0]
            script1, div1 = components(f)
            js_files = CDN.js_files[0]
            return render_template("plot.html", script1=script1, div1=div1, js_files=js_files, css_files=css_files)
        except RemoteDataError as error:
            error = error
            return render_template("plot.html", script1=script1, div1=div1, js_files=js_files, css_files=css_files,
                                   error=error)


@application.route('/plot')
def plot():
    return render_template("plot.html", script1=script1, div1=div1, js_files=js_files, css_files=css_files)


@application.route('/')
def home():
    return render_template("/home.html")


@application.route('/about')
def about():
    return render_template("/about.html")


if __name__ == "__main__":
    application.run(debug=True)
