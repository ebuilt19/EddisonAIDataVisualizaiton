import matplotlib.pyplot as plt
#ploting example
def plot_data (emotion):
    #emotion passed as a percentage 0-100
    #chapters and emotion
    plt.plot([1,2,3,4,4,5,6,7,8,9,11,12],emotion)
    ##plt.plot([9,8,7,6,5],[1,2,3,4,5])
    plt.title('Character Emotions')
    plt.ylabel('Emotion')
    plt.xlabel('Chapter')
    plt.show()


plot_data([9,8,7,6,5,4,3,2,1,0,0,0])
