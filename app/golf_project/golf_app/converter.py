import matplotlib as matplotlib
import matplotlib.pyplot as plt

from base64 import b64encode
import io

matplotlib.use('Agg')

def scatter_to_base64(data, user):
    plt.barh(*data, align='center', color=['r','b','g','c','m','y','k'])
    plt.xlabel('Score Totals', weight="bold", fontsize="18")
    plt.ylabel('Course Names',weight="bold", fontsize="18", labelpad=10)
    plt.title('Bar Graph of Score Totals per Scorecard', weight="bold", fontsize="18")
    plt.yticks(data[0], user.golfer.scorecard_names, fontsize="12", weight="bold")
    plt.tight_layout(pad=0.85)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.close()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base641(data,user):
    plt.scatter(*data, color='k')
    plt.ylabel('GIR Totals(%)', weight="bold", fontsize="18")
    plt.xlabel('Par Type',weight="bold", fontsize="18")
    plt.title('Scatter Plot of Green In Regulation Totals(%) per Par Type', fontsize="18", weight="bold")
    plt.xticks(data[0], fontsize="12", weight="bold")
    plt.ylim(0,100)
    plt.tight_layout(pad=0.85)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.close()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base642(data_1,user):
    plt.scatter(*data_1, color='k')
    plt.ylabel('FIR Totals(%)', weight="bold", fontsize="18")
    plt.xlabel('Par Type', weight="bold", fontsize="18")
    plt.title('Scatter Plot of Fairway in Regulation Totals(%) per Par Type', fontsize="18", weight="bold")
    plt.xticks(data_1[0], fontsize="12", weight="bold")
    plt.ylim(0,100)
    plt.tight_layout(pad=0.85)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.close()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')
