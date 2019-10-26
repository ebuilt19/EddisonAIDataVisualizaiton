import sys
from query_elasticsearch import *
import query_elasticsearch as elastic
#import matplotlib
#matplotlib.use('pdf')
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import numpy as np
import pandas as pd
from matplotlib import cm
from statistics import mean
import pylab
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import OrderedDict
#import plotly.plotly as py
#import plotly.graph_objs as go

emotions = {
        "fear": 0,
        "sadness": 1,
        "guilt": 2,
        "disgust": 3,
        "anger": 4,
        "shame": 5, 
        "joy": 6 }

def get_emotion(emotion_list, emotion):
    for em in emotion_list:
        if em['emotionName'] == emotion:
            return em['proximity']
    return 0

def extract_emotion_data(character, emotion):
    em_data_final = []
    for i in range(1,23):
        res = search(character,i)
        em_data = []
        for case in res['hits']['hits']:
            if len(case['_source']['emotionProximities']) < 7:
                em_data += [get_emotion(case['_source']['emotionProximities'], emotion)]
            else:
                em_data += [case['_source']['emotionProximities'][emotions[emotion]]['proximity']]
        em_data_final.append(em_data)
    return em_data_final

def extract_relation_data(ch1, ch2, chapter):
    res = search(ch1, chapter)
    relevance_data = []
    sentiment_data = []
    for case in res['hits']['hits']:
        for entity in case['_source']['topicEntities']:
            if is_match(entity, ch2, case['_source']['text']):
                relevance_data += [entity['relevance']]
                sentiment_data += [entity['sentimentScore']]
    return relevance_data, sentiment_data

def is_match(entity, ch, text):
    if entity['mainName'].lower() == ch.lower():
        return True
    for mention in entity['lexemePositions']:
        offset = mention['offset']
        length = mention['length']
        if text[offset: offset+length].lower() == ch.lower():
            return True
    return False

def greetings():
    print("*******************  MENU  *********************")
    print("1) Character Emotion Plot ")
    print("2) Character Relationship Plot")
    response = input("Enter plot type: ")
    if response == '1':
        return emotion_greetings()
    else:
        return relation_greetings()

def relation_greetings():
    print("******************  RELATIONSHIP PLOT  **********************")
    character1 = input("Enter the first Lord of the Rings character: ")
    character2 = input("Enter the second Lord of the Rings character: ")
    return 2, character1, character2

def emotion_greetings():
    print("******************  EMOTION PLOT  **********************")
    print("List of emotions:- "+list(emotions.keys())[0])
    for emotion in list(emotions.keys())[1:]:
        print("                 - "+emotion)
    print("****************************************")
    character = input("Enter Lord of the Rings Character: ")
    emotion = input("Enter an emotion: ")
    invalid = True
    while(invalid):
        if emotion.lower() in emotions.keys():
            invalid = False
        else:
            emotion = raw_input("Enter an emotion: ")

    return 1, character, emotion

def get_colormap():
    norm = matplotlib.colors.Normalize(vmin=-1, vmax=1)
    sm = cm.ScalarMappable(norm=norm, cmap=cm.RdYlGn)
    sm.set_clim(-1.0, 1.0)
    return sm



if __name__=='__main__':
    code, input1, input2 = greetings()
    debug=False
    if len(sys.argv) > 1 and sys.argv[1] == 'd':
        debug = True
    if code == 1:
        ch, em = input1, input2
        em_data = extract_emotion_data(ch, em)
        #em_data = filter(lambda a: a != 0, em_data)
        fig, ax = plt.subplots(nrows=4, ncols=2,constrained_layout = True)
        h=0
        for row in ax:
            for col in row:
                if h == 8:
                    break
                x_data = range(0, len(list(em_data[h])))		
                col.plot(x_data,em_data[h])
                col.scatter(x_data,em_data[h],c=em_data[h],cmap='viridis')
                col.text(-0.5,-0.5,"Average " + str(em) + ": " + str(round(mean(em_data[h])*100,2)) + "%")
                col.set_ylim([-1.0,1.0])
                col.set_title("Chapter " + str(h+1),fontsize = 10)
                h = h + 1
	
        fig, ax = plt.subplots(nrows=4, ncols=2,constrained_layout = True)
   
        h = 8
        for row in ax:
            for col in row:
                if h==16:
                    break
                x_data = range(0, len(list(em_data[h])))		
                col.plot(x_data,em_data[h])
                col.scatter(x_data,em_data[h],c=em_data[h],cmap='viridis')
                col.text(-0.5,-0.5,"Average " + str(em) + ": " + str(round(mean(em_data[h])*100,2)) + "%")
                col.set_ylim([-1.0,1.0])
                col.set_title("Chapter " + str(h+1),fontsize = 10)
                h = h + 1
	
        fig, ax = plt.subplots(nrows=3, ncols=2,constrained_layout = True)
   
        h = 16
        for row in ax:
            for col in row:
                if h==22:
                    break
                x_data = range(0, len(list(em_data[h])))		
                col.plot(x_data,em_data[h])
                col.scatter(x_data,em_data[h],c=em_data[h],cmap='viridis')
                col.text(-0.5,-0.5,"Average " + str(em) + ": " + str(round(mean(em_data[h])*100,2)) + "%")
                col.set_ylim([-1.0,1.0])
                col.set_title("Chapter " + str(h+1),fontsize = 10)
                h = h + 1	

        plt.show()
        #x_data = range(1, len(em_data)+1)
        #plt.plot(x_data, em_data)
        #plt.show()
    elif code == 2:
        ch1, ch2 = input1, input2
        agg_relevance_data = []
        agg_sentiment_data = []
        
        for i in range(1,23):
            relevance_data1, sentiment_data1 = extract_relation_data(ch1, ch2, i)
            relevance_data2, sentiment_data2 = extract_relation_data(ch2, ch1, i)
            if len(relevance_data1) >= len(relevance_data2):
                relevance_data = relevance_data1
                sentiment_data = sentiment_data1
            else:
                relevance_data = relevance_data2
                sentiment_data = sentiment_data2
            
            rel_length = len(relevance_data)
            sent_length = len(sentiment_data)
            if rel_length != 0:
                agg_relevance_data += [sum(relevance_data)/float(rel_length)]
                agg_sentiment_data += [sum(sentiment_data)/float(sent_length)]
            #agg_relevance_data += relevance_data
            #agg_sentiment_data += sentiment_data
        df = pd.DataFrame(agg_relevance_data, columns=['relevance'])
        df['sentiment'] = agg_sentiment_data
        if debug:
            print(len(agg_sentiment_data)) 
        x_data = range(len(agg_relevance_data))
        #cmap = get_colormap()
        f,ax = plt.subplots()
        ax.set_facecolor('gray')
        ax.grid(False)
        plt.title("Relationship between "+ch1+" and "+ch2)
        plt.xlabel("Chapters")
        plt.ylabel("Relevance")
        ax.plot(x_data, df['relevance'], color='white')
        points = ax.scatter(x_data, df['relevance'], c=df['sentiment'], cmap='RdYlGn',
                vmin=-0.5, vmax=0.5)
        f.colorbar(points)
        #df.plot.scatter(x='sentiment',xticks='0',  y='relevance', c='sentiment',
        #        cmap='RdYlGn', vmin=-1.0, vmax=1.0)
        plt.show()

