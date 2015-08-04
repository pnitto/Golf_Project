import matplotlib.pyplot as plt
from base64 import b64encode
import io


def scatter_to_base64(data):
    plt.scatter(*data)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')
