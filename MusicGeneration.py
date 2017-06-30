import mido
import time
import random

def getMidiNotes(mid):
    """Converts midi message list into a list of chords (represented as arrays of notes.
    Channel 0 is represented in notes 0 to 200, channel 1 in 200 to 400 and so on"""
    track=mido.merge_tracks(mid.tracks)
    notes=[]
    result=[]
    for msg in track:
        tm=msg.dict()['time']
        try:
            current_note=(msg.dict()['note']+200*msg.dict()['channel'])
            current_velocity=msg.dict()['velocity']
            if(current_velocity==0):
                if(current_note in notes):
                    del notes[notes.index(current_note)]
                else:
                    pass
            else:
                if(current_note in notes):
                    pass
                else:
                    notes.append(current_note)
            if(tm!=0):
                if(notes==[]):
                    n=[]
                else:
                    n=list(notes)
                elm=([n,tm])
                result.append(elm)
        except:
            result.append(msg)
    return result

def generateChain(note_table):
    """Generates two lists of notes in a tuple. One is the list of all chords that exist in file.
    The other is a parralel list (in the same order) of what chords usually follow that one
    This is for random generation of a sequence of chords starting from the first one"""
    result=note_table
    result_trimmed=[]
    for i in range(len(result)):
        try:
            result[i][0]
            result_trimmed.append(result[i])
        except:
            pass

    existing_notes=[]
    note_followings=[]
    for i in range(len(result_trimmed)):
        if(result_trimmed[i] in existing_notes):
            e=existing_notes.index(result_trimmed[i])
            try:
                r=result_trimmed[i+1]
                note_followings[e].append(r)
            except:
                note_followings[e].append(None)
        else:
            existing_notes.append(list(result_trimmed[i]))
            try:
                note_followings.append([list(result_trimmed[i+1])])
            except:
                note_followings.append(None)
    return (existing_notes,note_followings)

def newSequence(chain):
    """Generates the new sequence using the two tables returned by generateChain"""
    existing_notes=chain[0]
    followings=chain[1]
    note=random.choice(existing_notes)
    result=[]
    while(note!=None):
        f=followings[existing_notes.index(note)]
        try:
            note=list(random.choice(f))
        except:
            note=None
            break
        result.append(note)
    return result

def getMessages(sequence):
    """Converts the list of chords (randomly generated by newSequence) into a list of midi messages"""
    lastNote=[]
    messages=[]
    for i in range(len(sequence)):
        currentNote=sequence[i]
        for j in range(len(currentNote[0])):
            if(not(currentNote[0][j] in lastNote)):
                note_=currentNote[0][j]%200
                velocity_=127
                channel_=currentNote[0][j]//200
                time_=0
                messages.append(mido.Message('note_on', note=note_, velocity=velocity_, time=time_,channel=channel_))
        for j in range(len(lastNote)):
            if(not((lastNote[j] in currentNote[0]))):
                note_=lastNote[j]%200
                velocity_=0
                channel_=lastNote[j]//200
                time_=0
                messages.append(mido.Message('note_on', note=note_, velocity=velocity_, time=time_,channel=channel_))
        messages[-1]=mido.Message('note_on',note=messages[-1].dict()['note'],velocity=messages[-1].dict()['velocity'],time=currentNote[1])
        lastNote=currentNote[0]
    return messages

def extend(midifile,nameout):
    """takes name of midi file as a paraeter, and the name of the output. Generates a random midi file from the input"""
    mid=mido.MidiFile(midifile)
    result=getMidiNotes(mid)
    chain=generateChain(result)
    s=newSequence(chain)
    m=getMessages(s)
    res=[]
    for i in range(len(result)):
        try:
            result[i][0]
        except:
            res.append(result[i])
    res.extend(m)
    mid = mido.MidiFile()
    mid.tracks.append(res)
    mid.save(nameout)

def execute():
    while(True):
        file=input('Enter the name of you midi file that you wish to use for music generation\n')
        name=input('Enter the name of you output generated file\n')
        extend(file,name)

execute()
