import base64
import urllib
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import re
from nltk.stem import WordNetLemmatizer

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from .models import TestQuestion, TestChoice, PersonalityType, PersonalityQuestion
from .utils import clear_test_session
from .trait_provider import trait_provider

User = get_user_model()
classifer_base = os.path.join(settings.BASE_DIR, 'app2', 'classifiers')


def preprocessing(data):
    # Data PreProcessing
    # Removing URLs
    data['posts'] = data['posts'].apply(lambda x: re.sub(r'https?:\/\/.*?[\s+]', '', x.replace("|", " ") + " "))
    # Removing End Tokens like '?', ',' '.'
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'\.', ' ', x + " "))
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'\?', ' ', x + " "))
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'!', ' ', x + " "))
    # Remove words that contain digits
    data['posts'] = data['posts'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', x))
    # Lower casing words
    data['posts'] = data['posts'].apply(lambda x: x.lower())
    # Removing multiple letters repeating words
    data["posts"] = data["posts"].apply(lambda x: re.sub(r'([a-z])\1{2,}[\s|\w]*', '', x))
    # Remove parenthesis
    data["posts"] = data["posts"].apply(lambda x: re.sub('(\[|\()*\d+(\]|\))*', ' ', x))
    # Remove spaces more than 1
    data["posts"] = data["posts"].apply(lambda x: re.sub(' +', ' ', x).lower())
    # Lemmatization
    data['posts'] = data['posts'].apply(lambda x: WordNetLemmatizer().lemmatize(x))
    return data

class AptitudeTest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.applicant.taken_apt_test and not request.user.is_staff:
            qs = TestQuestion.objects.all()[:10]
            
            context = {
                'questions': qs
            }
        else:
            context = {}
        return render(request, 'aptitude_test.html', context)
    
    def post(self, request, *args, **kwargs):
        if not request.user.applicant.taken_apt_test and not request.user.is_staff:
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            choices = [request.POST.get(str(q+1)) for q in range(10)]
            score = 0
            user_choices = TestChoice.objects.filter(pk__in=choices)
            correct_answers = TestChoice.objects.filter(is_answer=True)
            correct_ids = [x.id for x in correct_answers]
            for uc in user_choices:
                if(uc.id in correct_ids):
                    score += 10
            print(score)
            print(age, gender)
            user = User.objects.get(username=request.user.username)
            user.applicant.test_score = score
            user.applicant.taken_apt_test = True
            user.applicant.age = age
            user.applicant.gender = gender
            user.applicant.save()
            return redirect('aptitude_finished')
        else:
            return render(request, 'aptitude_test.html', {})
        

class PersonalityTest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.applicant.taken_personality_test and not request.user.is_staff:
            qs = PersonalityType.objects.all()
            type_o = PersonalityType.objects.get(id=1)
            type_c = PersonalityType.objects.get(id=2)
            type_e = PersonalityType.objects.get(id=3)
            type_a = PersonalityType.objects.get(id=4)
            type_n = PersonalityType.objects.get(id=5)

            context = {
                'type_o': type_o,
                'type_c': type_c,
                'type_e': type_e,
                'type_a': type_a,
                'type_n': type_n,
            }
        else:
            context = {}
        return render(request, 'personality_test.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.applicant.taken_personality_test and not request.user.is_staff:
            request_count = len(request.POST)-2
            # print(request.POST, request_count)
            choices = [int(request.POST.get('choice'+str(q+1))) for q in range(request_count)]
            print(choices)
            average = sum(choices)/5
            print(average)

            user = User.objects.get(username=request.user.username)
            
            test_type = request.POST.get('test_type')

            if test_type == '1':
                print('Openness Test')
                request.session['avg_o'] = sum(choices)/5
                user.applicant.o_score = sum(choices)/5
                user.applicant.save()
                request.session['done_o'] = True
            elif test_type == '2':
                print('Conscientiousness Test')
                request.session['avg_c'] = sum(choices)/5
                user.applicant.c_score = sum(choices)/5
                user.applicant.save()
                request.session['done_c'] = True
            elif test_type == '3':
                print('Extraversion Test')
                request.session['avg_e'] = sum(choices)/5
                user.applicant.e_score = sum(choices) / 5
                user.applicant.save()
                request.session['done_e'] = True
            elif test_type == '4':
                print('Agreeableness Test')
                request.session['avg_a'] = sum(choices)/5
                user.applicant.a_score = sum(choices)/5
                user.applicant.save()
                request.session['done_a'] = True
            elif test_type == '5':
                print('Neuroticism Test')
                request.session['avg_n'] = sum(choices)/5
                user.applicant.n_score = sum(choices)/5
                request.session['done_n'] = True
                
                user.applicant.taken_personality_test = True
                user.applicant.save()

                return redirect('personality_completed')
        
        return redirect('personality_test')


class PersonalityCompleted(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.applicant.taken_personality_test and not request.user.is_staff:
            user = User.objects.get(username=request.user.username)
            age = user.applicant.age
            gender = user.applicant.gender
           # print(age, gender)
            if gender == 'Male':
                genderbit = 1
            else:
                genderbit = 0
            avg_o = request.session.get('avg_o', None) 
            avg_c = request.session.get('avg_c', None) 
            avg_e = request.session.get('avg_e', None) 
            avg_a = request.session.get('avg_a', None) 
            avg_n = request.session.get('avg_n', None)
            dataset = [genderbit, age, avg_o, avg_n, avg_c, avg_a, avg_e]
            # dataset = [1, 20, 3.1, 3.1, 3.2, 3.2, 1.9]
            if None in dataset:
                completed = False
                context = {'completed': completed}
            else:
                print(dataset)
                model = open(os.path.join(classifer_base, 'Logistic Regression.pkl'), 'rb')
                model = pickle.load(model)
                predpers = model.predict([dataset])
                personality = np.array_str(predpers).replace("['", "").replace("']", "")
                print(personality)
                user.applicant.predicted_personality_type = personality
                user.applicant.save()
                nn = [' Openness ', ' Conscientiousness ', ' Extraversion ', ' Agreeableness ', 'Neuroticism ']
                yy = [avg_o, avg_c, avg_e, avg_a, avg_n]
                # yy = [5.1, 3.4, 6.8, 4, 7]
                plt.ylim([0, 10])
                plt.bar(nn, yy)
                plt.xticks(rotation=15)
                plt.savefig("output.png")
                iobytes = io.BytesIO()
                plt.savefig(iobytes, format='png')
                iobytes.seek(0)
                blob = base64.b64encode(iobytes.read())
                uri = 'data:image/png;base64,' + urllib.parse.quote(blob)
                plt.close()
                clear_test_session(request)
                user = User.objects.get(username=request.user.username)
                user.applicant.save()
                completed = True
                context = {
                    'completed': completed,
                    'personality': personality,
                    'image': uri
                }
        return render(request, 'personality_completed.html', context)


class mbtitest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.applicant.taken_mbti_test and not request.user.is_staff:
            context = {}
            return render(request, 'mbti_personality_home.html', context)
        else:
            user = User.objects.get(username=request.user.username)
            mbti_type = user.applicant.mbti_type
            trait_def = trait_provider(mbti_type)
            context = {'trait_def': trait_def}
            return render(request, 'mbti_personality_home.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.applicant.taken_mbti_test and not request.user.is_staff:
            statement = request.POST.get('statement')
            #print(statement)

            data = [['xxxx', statement]]
            myStatement = pd.DataFrame(data, columns=['type', 'posts'])
            my_posts = preprocessing(myStatement)
            print(my_posts)

            SVM_IE = pickle.load(open(os.path.join(classifer_base, 'SVM_IE_model.pkl'), 'rb'))
            SVM_NS = pickle.load(open(os.path.join(classifer_base, 'SVM_NS_model.pkl'), 'rb'))
            SVM_FT = pickle.load(open(os.path.join(classifer_base, 'SVM_FT_model.pkl'), 'rb'))
            SVM_PJ = pickle.load(open(os.path.join(classifer_base, 'SVM_PJ_model.pkl'), 'rb'))

            cv = pickle.load(open(os.path.join(classifer_base, 'count_vectorizer.pkl'), 'rb'))
            xCV = cv.transform(my_posts['posts'])
            tfidf = pickle.load(open(os.path.join(classifer_base, 'tfidfTransformer.pkl'), 'rb'))
            X_tfidf = tfidf.transform(xCV).toarray()

            Y_pred_IE = SVM_IE.predict(X_tfidf)
            Y_pred_NS = SVM_NS.predict(X_tfidf)
            Y_pred_FT = SVM_FT.predict(X_tfidf)
            Y_pred_PJ = SVM_PJ.predict(X_tfidf)

            mbti_type = np.array_str(Y_pred_IE).replace("['", "").replace("']", "") + np.array_str(Y_pred_NS).replace("['","").replace("']", "") + np.array_str(Y_pred_FT).replace("['", "").replace("']", "") + np.array_str(Y_pred_PJ).replace("['", "").replace("']", "")
            print(mbti_type)
            trait_def = trait_provider(mbti_type)
            user = User.objects.get(username=request.user.username)
            user.applicant.mbti_statement = statement
            user.applicant.taken_mbti_test = True
            user.applicant.mbti_type = mbti_type
            user.applicant.save()
            context = { 'trait_def' : trait_def }
            return redirect('mbti_personality_home')
        else:
            user = User.objects.get(username=request.user.username)
            mbti_type = user.applicant.mbti_type
            trait_def = trait_provider(mbti_type)
            context = { 'trait_def' : trait_def }
            return render(request, 'mbti_personality_home.html', context)





