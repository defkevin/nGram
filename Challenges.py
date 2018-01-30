import sys, io, matplotlib.pyplot as plt,mpld3,matplotlib.patches as mpatches
# import io
# import matplotlib.pyplot as plt,mpld3
# import matplotlib.patches as mpatches
from flask import Flask, render_template, request, redirect, Response
from practiceGram import *

app = Flask(__name__)

# ../challenge_Files
# ../challenge_Files/2012

# ../challenge_Files
# ../challenge_Files/2012
dir_path = os.path.dirname(__file__ )
filename = os.path.join(dir_path,"../challenge_Files")
dictionaries = returnDictionaries(filename,2012,2016)

@app.route('/')
def output():
    # serve index template
    return render_template('index.html')

@app.route('/ngram', methods =['GET'])
def getNgram():
    wordString = request.args.get('words', '')
    words = wordString.split(',')
    s = ''
    fig, ax = plt.subplots()
    years = [2012, 2013, 2014, 2015, 2016]
    colors = ["red","blue","green","black","orange"]
    handlesList = []
    for i in range(0,len(words)):
        words[i] = words[i].strip()
        distribution = nGramDistributionByYear(dictionaries,words[i])
        ax.plot(years, distribution, label=words[i], color=colors[i])
        # match colors for legend
        patch = mpatches.Patch(color=colors[i], label=words[i].strip())
        handlesList.append(patch)

    plt.ylabel('Distribution')
    plt.xticks(np.arange(min(years), max(years) + 1, 1.0))
    plt.legend(handles=handlesList)

    s = mpld3.fig_to_html(fig)
    s += '<form action="/ngram"> Write nGrams(Separated by comma, up to 5):<br><input type="text" name="words" value="' \
         + wordString + '"><br><input type="submit" value="Submit"></form>'

    return s


if __name__ == '__main__':
    # run!
    app.run()
