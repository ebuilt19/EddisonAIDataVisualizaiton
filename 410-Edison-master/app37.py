from query_elasticsearch37 import *
import pylab
#import matplotlib
# matplotlib.use('pdf')
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
    res = search(character)
    em_data = []
    for case in res['hits']['hits']:
        if len(case['_source']['emotionProximities']) < 7:
            em_data += [get_emotion(case['_source']
                                    ['emotionProximities'], emotion)]
        else:
            em_data += [case['_source']['emotionProximities']
                        [emotions[emotion]]['proximity']]
    return em_data


def greetings():
    print("Emotion Plots")
    print("****************************************")
    print("List of emotions:- " + list(emotions.keys())[0])
    for emotion in list(emotions.keys())[1:]:
        print("                 - " + emotion)
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


if __name__ == '__main__':
    ch, em = greetings()
    em_data = extract_emotion_data(ch, em)
    # print(list(em_data))
    #em_data = filter(lambda a: a != 0, em_data)
    x_data = range(1, len(list(em_data)) + 1)
    # print(x_data)
    # print(list(em_data))
    plt.title('Character Emotions')
    plt.ylabel(em)
    plt.xlabel('Chapter')
    plt.plot(x_data, list(em_data))
    pylab.xlim([0,100])
    pylab.ylim([-1.0,1.0])
    plt.show()
