import matplotlib.pyplot as plt
from base64 import b64encode
import io



def scatter_to_base64(data, user):
    plt.bar(*data, align='center', color=['r','b','g','c','m','y','k'])
    plt.ylabel('Scorecard Totals')
    plt.xlabel('Course Names')
    plt.title('Bar Graph of Golfer Score Totals per Scorecard')
    plt.xticks(data[0], user.golfer.scorecard_names,rotation="15")
    #plt.figure.figure(edgecolor="black")
    plt.ylim(0,)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base641(data,user):
    plt.plot(*data)
    plt.ylabel('Scorecard GIR Totals(%)')
    plt.xlabel('Course Names')
    plt.title('Line Graph of Green In Regulation Totals(%) per Scorecard')
    plt.xticks(data[0], user.golfer.scorecard_names)
    plt.ylim(0,100)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')

def scatter_to_base642(data,user):
    plt.plot(*data)
    plt.ylabel('Scorecard FIR Totals(%)')
    plt.xlabel('Course Names')
    plt.title('Line Graph of Fairway in Regulation Totals(%) per Scorecard')
    plt.xticks(data[0], user.golfer.scorecard_names)
    plt.ylim(0,100)
    image_file = io.BytesIO()
    plt.savefig(image_file, format="png")
    image_file.seek(0)
    plt.clf()
    return "data:image/png;base64, " + b64encode(image_file.read()).decode('utf-8')