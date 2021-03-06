import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import random
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('popular', quiet=True)

f=open('faq.txt','r',errors = 'ignore')
raw=f.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
GREETING_INPUTS = ("namastey","namaskaram","hello", "hi", "whats up","hey")
GREETING_RESPONSES = ["namastey","namaskaram","hello", "hi", "whats up","hey"]

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def response(user_response):
    robot_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robot_response=robot_response+"I think I need to read more about that..."
        return robot_response
    else:
        robot_response = robot_response+sent_tokens[idx]
        return robot_response


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def main() :
    flag=True
    print("EduBot: Hello I am Edulper Bot. I am here to help you with the application. Ask away any doubts!")

    while(flag==True):
        user_response = input()
        user_response=user_response.lower()
        if(user_response!='bye!!'):
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                print("EduBot: Anytime")
            else:
                if(greeting(user_response)!=None):
                    print("EduBot: "+greeting(user_response))
                else:
                    print("EduBot: ",end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
        else:
            flag=False
            print("EduBot: take care..")

if __name__=="__main__":
    main()