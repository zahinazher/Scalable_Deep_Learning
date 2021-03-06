# -*- coding: utf-8 -*-
import csv #to read csv files
import cv2 #to generate images from the video
import os #to get file paths
#adapted from github: https://github.com/dllatas/deepLearning/blob/master/helper/generate_frame_from_video.py
"""
1 (e) Angry
- AU 4+5+15+17,
2 (f) Contempt - AU 14,
3 (a) Disgust - AU 1+4+15+17,
4 (d) Fear
- AU 1+4+7+20,
5 (b) Happy
- AU 6+12+25,
6 (g) Sadness - AU 1+2+4+15+17
7 (c) Surprise - AU 1+2+5+25+27
SURPRISE AND FEAR GG
"""

def change_to_video_name(csv_name, suffix):
    """
    The name of the csv and the video is the same, only the suffix is diffferent.
    With this function we get the video name with the flv suffix
    params: name of csv file and the suffix (like flv)
    """
    return csv_name[:-10]+"."+suffix


def generate_frame(video_path, video_name, second, label, dest_path):
    """
    Generate Frame is used to generate the frame from a video. The frame is taken from a specific moment in time.
    We safe the image in the format: video-name_second_label.jpg 
    In this format we can see from which video the image was, at what moment it was taken, and what the label was, for example whether a person is happy or not.
    Params used: the path to the video, the video name, the second on which the image should be taken, the label and the destination folder
    """
    print "video_path", video_path
    print 'video_name',video_name
    print 'second',second
    print 'label',label
    print 'dest_path',dest_path

    vidcap = cv2.VideoCapture(os.path.join(video_path, video_name))
    vidcap.set(0, int(second*1000))
    success, image = vidcap.read()
    if success:
        cv2.imwrite(os.path.join(dest_path, video_name+"_"+str(second)+"_"+str(label)+".jpg"), image)

def check_angry(content):
    baseline = 50
    #disgust = ["AU4", "AU15", "AU17"]
    sadness = ["AU2", "AU4", "AU15", "AU17"]
    #angry = ["AU4", "AU5", "AU15", "AU17"]
    label = 1 # 159

    # print 'content:',content
    emotion_time = content[0][1]
    emotion = []
    for c in content:
        for h in sadness:
            if c[0] == h:
                emotion.append(c[1])
    print emotion
    factor = sum(emotion)/len(sadness)
    if factor >= (baseline/100):
        return emotion_time, label

def check_contempt(content):
    baseline = 100
    contempt = ["AU14"]
    label = 2
    emotion_time = content[0][1]
    for c in content:
        for h in contempt:
            if c[0] == h and c[1] >= baseline:
                return emotion_time, label

def check_happiness(content):
    """
    The check_hapiness function is used to check for which time a person is happy and store the time and happy label
    The information to see whether a person is extracted from the csv file. If the identification of the smile a person has is above a certain threshold the
    label and the time are returned. We store the labels in numbers, so we can easier use them when calculating. For hapiness we use label five
    Params: the content of the row in the csv file
    """
    baseline = 100
    happiness = ["Smile"]
    label = 5
    # print content
    emotion_time = content[0][1]
    # print 'emotion_time',emotion_time
    for c in content:
        for h in happiness:
            # print h
            if c[0] == h and c[1] >= baseline:
                print 'emotion & label',emotion_time, label
                return emotion_time, label

def check_happiness(content):
    """
    The check_hapiness function is used to check for which time a person is happy and store the time and happy label
    The information to see whether a person is extracted from the csv file. If the identification of the smile a person has is above a certain threshold the
    label and the time are returned. We store the labels in numbers, so we can easier use them when calculating. For hapiness we use label five
    Params: the content of the row in the csv file
    """
    baseline = 50
    happiness = ["Smile"]
    label = 5
    # print content
    emotion_time = content[0][1]
    # print 'emotion_time',emotion_time
    for c in content:
        for h in happiness:
            # print h
            if c[0] == h and c[1] >= baseline:
                print 'emotion & label',emotion_time, label
                return emotion_time, label

def check_nonHappiness(content):
    """
    The check_nonHapiness function is used to see if a person is not happy.
    A person is not happy, when there is no smile and the AU12 baseline is less than 20
    For the nonHapiness we use the label 50
    Params: the content of the row in the csv file
    """
    baseline = 0
    happiness = ["Smile"]
    AU12baseline = 20
    label = 50
    # print content
    emotion_time = content[0][1]
    # print 'emotion_time',emotion_time
    for c in content:
        for h in happiness:
            # print h
            # the hapiness value is exactly 0 and AU12 is below AU12 baseline, then a person is non happy
            if c[0] == h and c[1] == baseline and content[12][1] <= AU12baseline and content[13][1] <= AU12baseline:
                print 'emotion & label',emotion_time, label
                return emotion_time, label

def get_content(header, row):
    """
    The get_content function returns the content of the csv file on the specific row
    Params, the header to append the data to, the row number for which the content is wanted. 
    return: time frames for each AU in video
    """
    # print 'row',row
    content = row[0:]
    result = []
    for h in header:
        # print 'ts',h
        result.append([h[0], float(content[h[1]])])
    # print result
    return result


def get_header_au(row):
    """
    Function to return the information for this row
    param: The specific row with the information
    return: The time, if a person is smiling, and all the AU gestures
    """
    rules = ["Time", "Smile", "AU"]
    #header = row[0:2]
    header=row
    #print row
    result = []
    i = 0
    #for all values in the header
    for h in header:
        print h
        if h in rules or h[0:2] in rules or 'AU' in h:
            result.append([h, i])
        i = i + 1
    # print result
    return result

def process_video_happiness(csv_path, video_path, dest_path, suffix):
    """
    we walk through the directory and read the csv file for every video
    then for every row in the csv file we first get the header information, so the time, the smile and the au labels
    We then get the content for each row. For that content we then check for the emotion e.g. happy or sad.
    We then generate a frame for each of these emotions. 
    If the emotion continues for a longer time period e.g. 2 seconds then we can take multiple frames pictures.
    There can be a maximum of 14 frames per second taken
    This function calls the functions:
    get_header_au
    get_content
    check_happiness or check nonHappiness
    generate_frame
    change_to_video_name
    params: the csv_path, the video path that needs to be given for generating the frame, the destination path for the pictures, the suffix for the video in this case flv.
    """
    for root, dirs, files in os.walk(csv_path, True):
        for name in files:
            with open(os.path.join(root, name), 'rU') as csvfile:
                reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter=',', quotechar='|')
                for row in reader:
                    # print row
                    if reader.line_num == 1:
                        header = get_header_au(row)
                    else:
                        # print 'h',header
                        content = get_content(header, row)
                        # if len(header) > 0:
                        if len(header) > 0:
                            if content:
                                content = get_content(header, row)
                                # emotion = check_angry(content)
                                emotion = check_happiness(content)
                                if emotion is not None:
                                    # print emotion[0]
                                    # print emotion[1]
                                    generate_frame(video_path,
                                        change_to_video_name(name, suffix), emotion[0], emotion[1], dest_path)
                                        
def process_video_non_happiness(csv_path, video_path, dest_path, suffix):
    """
    we walk through the directory and read the csv file for every video
    then for every row in the csv file we first get the header information, so the time, the smile and the au labels
    We then get the content for each row. For that content we then check for the emotion e.g. happy or sad.
    We then generate a frame for each of these emotions. 
    If the emotion continues for a longer time period e.g. 2 seconds then we can take multiple frames pictures.
    There can be a maximum of 14 frames per second taken
    This function calls the functions:
    get_header_au
    get_content
    check_happiness or check nonHappiness
    generate_frame
    change_to_video_name
    params: the csv_path, the video path that needs to be given for generating the frame, the destination path for the pictures, the suffix for the video in this case flv.
    """
    for root, dirs, files in os.walk(csv_path, True):
        for name in files:
            with open(os.path.join(root, name), 'rU') as csvfile:
                reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter=',', quotechar='|')
                for row in reader:
                    # print row
                    if reader.line_num == 1:
                        header = get_header_au(row)
                    
                    else:
                        # print 'h',header
                        content = get_content(header, row)
                        # if len(header) > 0:

                        if len(header) > 0:
                            if content:
                                content = get_content(header, row)
                                #emotion = check_angry(content)
                                # print emotion
                                emotion = check_nonHappiness(content)
                                #emotion = check_happiness(content)
                                if emotion is not None:
                                    print emotion[0]
                                    print emotion[1]
                                    generate_frame(video_path,
                                        change_to_video_name(name, suffix), emotion[0], emotion[1], dest_path) 
                                        


                               

def main(argv=None): # pylint: disable=unused-argument
"""
the main function initiates the csv path, the video path, the suffic and the destination path
It calls the process_video_happiness or process_video_nonHapiness
"""
    csv_path = "AMFED/AMFED/AU_Labels"
    video_path = "AMFED/AMFED/Videos_FLV"
    #destination path for hapiness
    #dest_path = "AMFED/AMFED/happiness"
    suffix = "flv"
    #process_video_hapiness(csv_path, video_path, dest_path, suffix)
    #destination path for sadness
    #dest_path = "AMFED/AMFED/sadness"
    dest_path = "AMFED/AMFED/happiness"
    process_video_happiness(csv_path, video_path, dest_path, suffix)

if __name__ == '__main__':
    main()
