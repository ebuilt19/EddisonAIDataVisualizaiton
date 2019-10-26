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

def extract_emotion_data(character, emotion, chapter):
    res = search(character,str(chapter))
    em_data = []
    for case in res['hits']['hits']:
        if len(case['_source']['emotionProximities']) < 7:
            em_data += [get_emotion(case['_source']['emotionProximities'], emotion)]
        else:
            em_data += [case['_source']['emotionProximities'][emotions[emotion]]['proximity']]
    return em_data

def greetings():
    print("Emotion Plots")
    print("****************************************")
    print("List of emotions:- "+list(emotions.keys())[0])
    for emotion in list(emotions.keys())[1:]:
        print("                 - "+emotion)
    print("****************************************")
    character = input("Enter Lord of the Rings Character: ")
    emotion = input("Enter an emotion: ")
    chapter = input("Enter chapter(1-22): ")
    invalid = True
    while(invalid):
        if emotion.lower() in emotions.keys():
            invalid = False
        else:
            emotion = raw_input("Enter an emotion: ")

    return character, emotion, chapter

if __name__=='__main__':
    n = ""
    while n!= "y":
        ch, em, chpt = greetings()
        em_data = extract_emotion_data(ch, em, chpt)
	
        x_data = range(1, len(list(em_data))+1)
    
    
        plt.figure(1)
        plt.plot(x_data,em_data)
        pylab.ylim([-1.0,1.0])
        plt.scatter(x_data,em_data,c=em_data,cmap='viridis')
        plt.text(-0.5,-0.5,"Average " + em + ": " + str(round(mean(em_data)*100,2)) + "%")
        plt.title("Chapter " + str(chpt),fontsize = 10)
        plt.show()
        n = input("Do you want to exit?")
