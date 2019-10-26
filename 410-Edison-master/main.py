import Carmen_API
import os
import pandas as pd
import _pickle as cPickle

project_name = 'LOTR'                              

def process_chapter(emotion_data, ch_no, part, response):
    x = 10
    emo_proximities = get_emotions(response)
    emo_proximities['Chapter'] = str(ch_no)+'-'+str(part)
    emotion_data = emotion_data.append(emo_proximities, ignore_index=True)
    return emotion_data

def analyze_text(emotion_data, full_text, fa, ch_no):
    i = 0
    part = 1
    while(i < len(full_text)):
        text_to_upload = full_text[i : i + 6000]
        i += 6000
        response = fa.process_text(project_name, text_to_upload)
        response['text'] = None
        emotion_data = process_chapter(emotion_data, ch_no, part, response['searchResult']['emotionProximities'])
        part += 1
    x = 12
    return emotion_data

def get_emotions(response):
    result = {}
    for v in response:
        result[v['className']] = v['proximity']
    return result


if __name__ == "__main__":
    login_name = 'admin'       
    login_password = 'umassbostontopos'             
    server = 'feeds-api.demo004-feeds.toposlabs-1.com'   
    # Feeds API. This points towards your server
    text_to_upload = 'SAMPLE_TEXT'                  
    # Text you will upload. This will be replaced by the text in your save_files folder
    # The name of the project (campaign) you're uploading to
    port = 443                                      
    # Port #. This is the same for all servers

    print()
    fa = Carmen_API.Feeds_APIs(server, port, login_name, login_password) 
    # Creates a session to connect to the feeds API for your server and logins.

    # Get current file path and text files
    THIS_FILE_PATH = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
    save_files_dir = os.path.join(THIS_FILE_PATH, 'Book_Chapters')
    text_folder = os.listdir(save_files_dir)
    #text_folder.remove('.DS_Store')                 
    # On Mac .DS_Store is created as a hidden file to hold metadata for the folder.
    # Delete it so we don't accidentally point to it.

    # Create text folder path.
    #text_file_to_open = os.path.join(save_files_dir, text_folder[0])
    text_file_to_open = save_files_dir
    index = 1

    emotion_data = pd.DataFrame(columns=
            ['Chapter', 'anger', 'disgust', 'shame', 'joy', 'sadness', 'fear', 'guilt'])
    # For each text file in text files, save text to text_to_upload and upload
    for ch_no, text_file in enumerate(os.listdir(text_file_to_open)):
        ch_no+=1
        if text_file.startswith("ch"):
            text_file_path = os.path.join(text_file_to_open, text_file) 
            # Full file path to be opened for open function
            
            
            text_file_path = os.path.join(text_file_path, os.listdir(text_file_path)[0])
            with open(text_file_path, 'r') as current_file:
                full_text = current_file.read().replace('\n', ' ')
                
            emotion_data = analyze_text(emotion_data, full_text, fa, ch_no)
            #response = fa.process_text(project_name, text_to_upload)
            # Set this to whatever chapter you want as a String. 
            # This will tagged to the text you're processing in case you want to query it.
            print("Uploading", index, "/", len(os.listdir(text_file_to_open)))
            print("Chapter "+ str(ch_no)+" done")
            index+=1

    cPickle.dump(emotion_data, "JSON/emotion_data.pickle")


# EXAMPLE QUERY:
# This will return all documents that are tagged with a "1" in office365EmailType
#and a "2" in office365EmailIncludeMode
#{
#  "query": {
#    "bool": {
#      "must": [
#        {
#          "match": {
#            "office365EmailType": "1"
#          }
#        },
#       {
#          "match": {
#            "office365EmailsIncludeMode": "2"
#          }
#        }
#      ]
#    }
#  }
#}
#
# Elasticsearch Query DSL Documentation:
# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html


