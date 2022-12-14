from io import BytesIO
from flask import Flask, request, Response, render_template
from task import parse_function, latex_fourier_series, draw_plot, parse_number
from matplotlib.backends.backend_agg import FigureCanvasAgg

app = Flask(
    __name__,
    static_folder='web/static',
    template_folder='web/templates'
)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/fourier_series', methods=['POST'])
def fourier_series():
    try:
        return latex_fourier_series(*get_request_params())
    except:
        return Response(status=400)


@app.route("/plot", methods=['POST'])
def plot():
    try:
        fig = draw_plot(*get_request_params())
        output = BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return Response(status=400)


def get_request_params():
    data = request.get_json()
    function = parse_function(data['function'])
    return [
        function[0],
        function[1],
        int(data['order']),
        (parse_number(data['start']), parse_number(data['end']))
    ]


if __name__ == "__main__":
    app.run()
