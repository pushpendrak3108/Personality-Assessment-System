# Importing all libraries
import pandas as pd
import numpy as np
import pickle as pkl

# Text Processing
import re
from nltk.stem import WordNetLemmatizer

# Ignore noise warning
import warnings
warnings.filterwarnings("ignore")

def preprocessing(data):
    #Data PreProcessing
    #Removing URLs
    data['posts'] = data['posts'].apply(lambda x: re.sub(r'https?:\/\/.*?[\s+]', '', x.replace("|"," ") + " "))
    #Removing End Tokens like '?', ',' '.'
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'\.', ' ', x + " "))
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'\?', ' ', x + " "))
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'!', ' ', x + " "))
    #Remove words that contain digits
    data['posts'] = data['posts'].apply(lambda x: re.sub(r'[^a-zA-Z\s]','',x))
    #Lower casing words
    data['posts'] = data['posts'].apply(lambda x: x.lower())
    #Removing multiple letters repeating words
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'([a-z])\1{2,}[\s|\w]*','',x))
    #Remove parenthesis
    data["posts"] = data["posts"].apply(lambda x: re.sub('(\[|\()*\d+(\]|\))*', ' ', x))
    #Remove spaces more than 1
    data["posts"] = data["posts"].apply(lambda x: re.sub(' +', ' ', x).lower())
    # Lemmatization
    data['posts'] = data['posts'].apply(lambda x: WordNetLemmatizer().lemmatize(x))
    return data

#Personality Prediction of an example
statement= "I have been try to meet you but stuck in some work ||| I am really concern about him for his bad health ||| I will get some time from my busy schedule to plant trees around you so that you will be more benefited.||| He is so sweet in nature ||| I like to wear good apperals. I love to travel and i went to California once where I enjoyed a lot. I wanna do cooking in most of my free time"
statement2 = "I fully believe in the power of being a protector, to give a voice to the voiceless. So in that spirit I present this film, and hope it it recieved in the spirit of compassion.  Om Mani Padme Hum ...|||Yes, you are quite right. But many times this help has to come from outside the relationship. A partner can be supportive, and helpful but I think getting the right help is critical.  Finding a good...|||If he doesn't feel worthy of being loved, nothing you say or do will make a difference.|||Bossy1,  I think Jawz is very much on to something here, and further I think this is indicative of much deeper issues that were around long before you two met. It very well might mean your friend...|||LookingGlass,  Thanks for making this point. Unfortunately this corrupted Christianity speaks with a very loud voice, so the Still Small Voice has been forgotten.  Very few Christians today have...|||This has been my curse as well and I gotta tell you, most people prefer to remain stuck in their own neuroses, with all the excuses that go along with that. Of course in spite of all the scars I've...|||I know this must be very painful Callie, but honestly I think you dodged a bullet here. I'm sure he's a good person but it sounds as if he has some emotional maturing to do.  Being involved with...|||You guys are singing my song :)  I've been doing some research on heuristics (mental shortcuts) and cognitive biases, that explain a lot of why people do what they do. For some it's the principle of...|||I empathize with the sentiment behind this, but I think truly that while religion contains much of what we need as a society, it can easily be manipulated and used as a control. This is the dualistic...|||I think sometimes we forget that our type is only one part of what makes us a person. Emotional and Social competencies, past hurts and issues, value memes, etc.. I saw an experiment in a crowded...|||I don't feel rare as much as I feel well done.|||Thank you UK, you sound like a reasonable and compassionate person. I think Neitzsche's quote: Beware if you fight monsters lest you become one in the process is appropriate here. Here in Colorado...|||It might surprise you to learn that cognitive brain science has discovered that we humans are actually hard-wired for empathy. Read Goleman's Social Intelligence and it will help you to understand...|||You must understand, Aegis is really not to blame. Yes he seems like an inhuman monster for trying to justify marginalizing another human being, but people like that really don't understand what they...|||You know these ideas of yours are so riddled with fallacy and linquistic manipulation it isn't worth my time to continue this conversation. Hopefully as the years pass by you can learn to think and...|||An elephant swallowed by a boa constrictor!  Love that book!  I cried a little at the end.|||A thoughtful philosophy to be sure, and I like the line from  The Little Prince in your signature block, I used to use it as well :)|||.  According to your logic on tolerance we should accept intolerance if we are to consider ourselves tolerant?      Homosexuality is not violent behavior, conflating the two is extremely...|||Okay guys, for the record, I think healthy debate can help us all to move forward beyond the simple heuristics and the accompanying cognitive bias that is prevalent in religion. Critical thinking...|||Looks like this has already been explained, and I'm sorry I didn't notice the post, didn't mean to ignore you.  The teleological argument definitely has a major flaw in that the conclusion drawn...|||Okay first, you have attributed someone else's quote to me. Second this is what you had a problem with:   This post is what you say is a logical fallacy by introducing the straw-man of the...|||No problem, just look into this light for a moment...|||Re-framing the argument. No one introduced the idea of being tolerant of everything.  Clever use of the slippery slope though.  Don't blame you for not touching gay marriage, there is no good...|||I would not go so far as to say faith and reason are inherently contradictory which is why I worded my post the way I did. You must understand I have spent most of my life studying religion and...|||No one is supposed to know about the Inner Council !  we can't have people aware that we can communicate telepathically with each other, for years we have disguised ourselves as regular folk and...|||So who gets to decide what is good for us?  And I wouldn't go around using words like logic where religion is concerned, there is little in religion that can stand up to critical inquiry.|||Old School INFJ theme song: Veteran of the Psychic Wars, Blue Oyster Cult|||Okay, but what with the world being bullshit, I'm gonna have to change my whole frame of reference. Up to this point I've been operating under the thought that the world is a vampire :p|||Define getting older :P  For most of my life it seems I tried to squeeze myself into the roles that I thought I needed to in order to get along. I think many people here know what it's like to...|||You have quite a full plate there pardner ;)  Pretty typical though, I'll bet there is more stuff going on inside you than you can reasonably articulate.  This is what I love about this...|||I like the cards that don't have anything written in them so you can be creative. After an argument with my wife I found one with a little dog on the front, and I wrote: if i ran away, and you...|||Love this thread! :)  Over the years I have practiced many religions and philosophies, I think being an INFJ means being an explorer to some extent. During each phase of my explorations I practiced...|||I think I hate that crap because it is meaningless and empty and usually used to make people feel good about themselves.  The truth is most people are self-centered and don't understand love and...|||I understand. It bothers me a lot sometimes because I can walk around the store feeling angry and judgmental and that just adds up to sapped energy and a feeling that I don't like myself very much...|||The great sage Linus Van Pelt once said:  I love mankind, it's people I can't stand  I have always found myself on the other end of that. Individually I love people, but in a group they can be...|||Funny how you can see that coming a long ways off. Sometimes I try to talk myself out of it, like oh man you don't know that for sure give her a chance but it most always comes back to the first...|||According to cognitive brain science, when you are truly in tune with another human being there is a synchrony in our brain waves.  With the discovery of Mirror Neurons we can see just how that...|||Looks like you have stumbled upon what Buddhists call the First Noble Truth :)|||Okay, I'm gonna say something that might sound lame, but here goes:  You are never going to find out who you are because what that really is keeps changing and growing, this is the nature of...|||Ever try to make friends with a stray cat? The same rules apply, don't chase us, we will run, just provide a safe and friendly harbor and watch how quickly we become affectionate.|||Well, if you really like someone's post you can thank them, un thank them just so you can thank them again!|||Oh and Chazz? That feeling comes and goes, I wouldn't put too much meaning on it. Ever since I can remember I never felt like I belonged anywhere. As a child I had the impression that my presence on...|||Okay, totally agree with your post... but I couldn't help getting a visual on an Intimidating Typist I keep seeing Roz from Monsters Inc.|||It takes a little time to tell the difference between an anxious perception and a clear intuition. That being said, even after all these years I do manage to screw it up royally at times. :P|||Great movies all!  I think the movie that still moves me the most is  Wings Of Desire  This film was done old school style even for the 80s, directed by Wim Wenders and featuring the talent of...|||I'm not sure if you experience this, or maybe because I'm middle aged that I see things this way. I have been a musician, artist, salesman, soldier, nurse (CNA), technician, Christian, Buddhist,...|||I first found out about mirror neurons from reading Daniel Goleman's Social Intelligence  though the credit for the research goes to an Italian research scientist whose name escapes me for the...|||Aint it fun to be us?  :P  I've been doing some reading on mirror neurons and how when we are genuinely engaged with another human being our brains are actually in sync.    Now to me that is...|||Has anyone compiled information about linking MB types and Soma types?|||I wonder if our expectations of ourselves are a little unrealistic at times. Sometimes I feel emotionally raw and wounded and need to withdraw. Oddly enough at times like that there is a little...'"
statement3 = "Hey, they call me the Commander, I create plans and strategies for everything, I solve problems using highly optimized solutions, and I use my intuition to predict possible scenarios in the future, some people consider me as bossy, but I'm not, recognized me?"

data = [['xxxx',statement3]]
myStatement = pd.DataFrame(data,columns=['type','posts'])
my_posts = preprocessing(myStatement)
print(my_posts)

SVM_IE = pkl.load(open('SVM_IE_model.pkl','rb'))
SVM_NS = pkl.load(open('SVM_NS_model.pkl','rb'))
SVM_FT = pkl.load(open('SVM_FT_model.pkl','rb'))
SVM_PJ = pkl.load(open('SVM_PJ_model.pkl','rb'))

cv = pkl.load(open('count_vectorizer.pkl','rb'))
xCV = cv.transform(my_posts['posts'])
tfidf = pkl.load(open('tfidfTransformer.pkl','rb'))
X_tfidf =  tfidf.transform(xCV).toarray()

Y_pred_IE = SVM_IE.predict(X_tfidf)
Y_pred_NS = SVM_NS.predict(X_tfidf)
Y_pred_FT = SVM_FT.predict(X_tfidf)
Y_pred_PJ = SVM_PJ.predict(X_tfidf)

print(np.array_str(Y_pred_IE).replace("['", "").replace("']", "")+np.array_str(Y_pred_NS).replace("['", "").replace("']", "")+np.array_str(Y_pred_FT).replace("['", "").replace("']", "")+np.array_str(Y_pred_PJ).replace("['", "").replace("']", ""))