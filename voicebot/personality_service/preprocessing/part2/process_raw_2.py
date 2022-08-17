import pandas as pd
import copy
import os

os.chdir('/home/dodev/ben_msc_project/do-voice-interaction/voicebot/personality_service/preprocessing/part2')


def make_continuous(emotion, sentiment):
    if emotion=="sadness":
        return -0.7, -0.7
    elif emotion=="fear":
        return -0.7, 0.7
    elif emotion=="surprise" and sentiment=="positive":
        return 0.1, 0.9
    elif emotion=="surprise" and sentiment=="negative":
        return -0.1, 0.9
    elif emotion=="anger":
        return -0.4, 0.8
    elif emotion=="disgust":
        return -0.9, 0.4
    elif emotion=="joy":
        return 0.7, 0.7
    return 0.0,0.0

def get_data(character):   
    df_train = pd.read_csv('./MELD_combined.csv') 
    utt = df_train['Utterance'].tolist() 
    sea_id = df_train['Season'].tolist()
    epi_id = df_train['Episode'].tolist()
    dia_id = df_train['Dialogue_ID'].tolist() 
    utt_id = df_train['Utterance_ID'].tolist() 
    emotions = df_train['Emotion'].tolist() 
    sentiments = df_train['Sentiment'].tolist()
    sets = df_train['Set'].tolist()
    speakers = df_train['Speaker'].tolist()
    # speakers_count = {s:speakers.count(s) for s in speakers}
    # speakers_count = sorted(speakers_count.items(), key=lambda item: item[1])

    dia_num=0
    dialogues=[]
    dialogue=[]
    for sp, u, sd, ed, dd, ud, set, emo, sent in zip(speakers, utt, sea_id, epi_id, dia_id, utt_id, sets, emotions, sentiments):
        if (dd==dia_num):
            dialogue.append([sp, emo, sent])
        else:
            dialogues.append(dialogue)
            dialogue=[]
            dialogue.append([sp, emo, sent])
            dia_num=dd
    dialogues.append(dialogue)

    indices=[]
    for i in range(len(dialogues)):
        for u in range(len(dialogues[i])):
            if dialogues[i][u][0]==character:
                indices.append(i)

    indices=list(dict.fromkeys(indices))    
    build_ups=[]


    # Ovidiu suggestion
    for i in indices:
        last_utterance=0
        for u in range(len(dialogues[i])):
            if (dialogues[i][u][0]==character):
                build_up=[]
                for a in range(last_utterance, u+1):
                    build_up.append(dialogues[i][a])
                build_ups.append(build_up)
                last_utterance=u+1




    build_ups_copy=copy.deepcopy(build_ups)

    with open("./"+character+".txt", "w") as f:
        for i in range(len(build_ups)):
            for Y in range(len(build_ups[i])):
                build_ups[i][Y].pop(0)
                build_ups[i][Y][0], build_ups[i][Y][1] = make_continuous(build_ups_copy[i][Y][1],build_ups_copy[i][Y][2])
            f.write(str(build_ups[i])+"\n")

    examples=[]
    labels=[]
    for b in build_ups:
        if len(b)==1:
            b.insert(0,[0.0, 0.0])
        examples.append(b[:-1])
        labels.append(b[-1])
    with open(character+"4.txt", "w") as g:
        for e, l in zip(examples, labels):
            for ex in e:
                g.write(str(ex)+"\n")
            g.write("Label: "+str(l)+"\n\n\n")

    return examples, labels

