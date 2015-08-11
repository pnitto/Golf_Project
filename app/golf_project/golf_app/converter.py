import matplotlib.pyplot as plt
from base64 import b64encode
import io



def scatter_to_base64(data, user):
    plt.bar(*data, align='center', color=['r','b','g','c','m','y','k'])
    plt.ylabel('Score Totals', weight="bold", fontsize="18")
    plt.xlabel('Course Names')
    plt.title('Bar Graph of Score Totals per Scorecard', weight="bold", fontsize="18")
    plt.xticks(data[0], user.golfer.scorecard_names,rotation="65", fontsize="12", weight="bold")
    plt.ylim(0,)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base641(data,user):
    plt.plot(*data, color='g')
    plt.ylabel('GIR Totals(%)', weight="bold", fontsize="18")
    plt.xlabel('Course Names')
    plt.title('Line Graph of Green In Regulation Totals(%) per Scorecard', fontsize="18", weight="bold")
    plt.xticks(data[0], user.golfer.scorecard_names, rotation="13", fontsize="12", weight="bold")
    plt.ylim(0,100)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base642(data,user):
    plt.plot(*data, color='k')
    plt.ylabel('FIR Totals(%)', weight="bold", fontsize="18")
    plt.xlabel('Course Names')
    plt.title('Line Graph of Fairway in Regulation Totals(%) per Scorecard', fontsize="18", weight="bold")
    plt.xticks(data[0], user.golfer.scorecard_names, rotation="13", fontsize="12", weight="bold")
    plt.ylim(0,100)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')