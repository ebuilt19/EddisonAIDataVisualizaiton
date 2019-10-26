from query_elasticsearch import *
from statistics import mean
import pylab
#import matplotlib
#matplotlib.use('pdf')
import matplotlib.pyplot as plt

emotions = {
        "fear": 0,
        "sadness": 1,
        "guilt": 2,
        "disgust": 3,
        "anger": 4,
        "shame": 5, 
        "joy": 6
        }

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

def greetings():
    print("Emotion Plots")
    print("****************************************")
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

    return character, emotion

if __name__=='__main__':
    n = ""
    ch, em = greetings()
        
    em_data = extract_emotion_data(ch, em)
		
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