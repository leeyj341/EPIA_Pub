from django.shortcuts import render, redirect, get_object_or_404
from .models import Answer, Keyword, Face
from epia.models import Company, Position, Question, Ceo
from interviews.models import Answer, Keyword
from bs4 import BeautifulSoup
import requests
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
from django.http import JsonResponse, HttpResponse
from html import escape
import time, random

# [START speech_transcribe_async]
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
from IPython import embed
from django.contrib.auth.decorators import login_required

# [open_cv]
import cv2, os

# Create your views here.

# 면접 시작하기
@login_required
def interview(request):
    # form으로 보낸 데이터 받음
    mode = request.GET.get('mode') or False
    company_id = request.GET.get("company")
    position_id = request.GET.get("position")
    question_id = request.GET.get("question")
   
    # 데이터로 DB에서 불러오기
    company = Company.objects.get(pk=company_id)
    position = Position.objects.get(pk=position_id)
    question = Question.objects.get(pk=question_id)
    ceo = Ceo.objects.get(company=company,mode=bool(mode))
    
    context = {
        "company": company,
        "position": position,
        "question": question,
        "ceo":ceo,
        "mode":bool(mode)
    }
    return render(request, "interviews/interview.html", context)

# 면접 결과 음성 파일 저장 및 사진 찍기
def save_audio(request):
    customHeader = request.META.get("HTTP_MYCUSTOMHEADER")
    
    # 녹화된 blob 파일을 webm 파일로 써서 저장
    uploadingFile = open(file=f"{audio_path(request, customHeader)}.webm", mode="wb",)
    blob = request.FILES['blob'].file.read()
    uploadingFile.write(blob)
    uploadingFile.close()
    # webm -> wav 변환
    import subprocess
    # 이건 우리 컴퓨터 환경에서 실행할 때 사용하는 경로
    command = f"ffmpeg -i C:/iot/EPIA/{audio_path(request, customHeader)}.webm -ab 160k -ac 2 -ar 44100 -vn C:/iot/EPIA/{audio_path(request, customHeader)}.wav"
    # 배포 환경에서 사용하는 경로 고로 push 할 때 이걸로 올려주세요!
    # command = f"ffmpeg -i /home/ubuntu/epiaproject/{audio_path(request, customHeader)}.webm -ab 160k -ac 2 -ar 44100 -vn  /home/ubuntu/epiaproject/{audio_path(request, customHeader)}.wav"

    subprocess.call(command, shell=True)
    # 사진 촬영을 위한 랜덤 시간대를 가져온다
    time = random.randint(1, 55)
    # opencv를 사용해서 동영상 파일을 읽어온다.
    cam = cv2.VideoCapture(f'media/user_{request.user.pk}_{customHeader}.webm')
    # 촬영할 시간대 설정
    cam.set(cv2.CAP_PROP_POS_MSEC,time * 1000)

    try:
        # imgdata 폴더가 없으면 생성
        if not os.path.exists('interviews/static/interviews/path'): 
            os.makedirs('interviews/static/interviews/path') 
    # 에러가 발생하면 만들어지지 않도록
    except OSError:
        print('Error: Creating Directory of Data')
    # 사진 찍기에 성공하면 결과를 저장한다
    success, image = cam.read()
    if success:
        name = 'media/path/image'+ str(customHeader) + '.jpg'
        cv2.imwrite(name,image)
    else:
        pass
    
    # STT API로 변환한 text 결과를 반환
    content = recognize(f'media/user_{request.user.pk}_{customHeader}.wav')
    # 찍은 결과와 답변 결과(STT의 결과)를 DB에 저장
    img = 'path/image'+ str(customHeader)+'.jpg'
    path = f'media/path/image{str(customHeader)}.jpg'
    question_pk = request.POST.get('question_pk')
    answer = Answer.objects.create(question_id=question_pk, user=request.user, content=content)
    face = Face.objects.create(answer_id=answer.pk, user=request.user, path=path, image=img)
    # 사용한 cam 객체 반납
    cam.release()
    cv2.destroyAllWindows()
    # STT를 거쳐 만들어진 answer 텍스트를 바탕으로 형태소 분석한다.-> 정의 함수 : def sort_word(sentence, word_count, answer_pk)
    #sort_word의 반환값이 sorted_word (리스트) sort_word함수를 실행하면 Keyword테이블에 생성된다. 
    sorted_word = sort_word(content, 30, answer.pk)
    context = {
        'answer_pk' : answer.pk,
        'face_pk' : face.pk,
    }

    return JsonResponse(context)

# 면접 결과보기
@login_required
def interview_result(request):
    if request.method == "POST":
        # 면접 본 후 해당 면접의 결과 가져오기
        question_pk = request.POST.get('question_pk')
        answer_pk = request.POST.get('answer_pk')
        face_pk = request.POST.get('face_pk')
        answer = Answer.objects.get(pk=answer_pk, question_id=question_pk, user=request.user)
        face = Face.objects.get(pk=face_pk,answer_id=answer_pk,user=request.user)
    else :
        # 마이 페이지 결과 리스트에서 들어갈 때
        answer_pk = request.GET.get('answer_pk')
        answer = Answer.objects.get(pk=answer_pk)
        face = Face.objects.get(answer_id=answer_pk,user=request.user)
        
    sentence = answer.content
    path = face.path
    
    # repr : 내부적으로 정의되어 있는... __str__과 같이 출력을 담당하는 역할의 메서드
    # escape : ""와 같은 문자열은 문자열의 끝으로 판단되어 무시되기 때문에 escape메서드로 escape문자열 처리해줌
    context = {
        'sentence':sentence,
		'path':path,
        'answer_pk':answer_pk,
        'face':face
    }
    return render(request, "interviews/interview_result.html", context)
    
# =========== media 안 경로 지정 ===================================================
def audio_path(instance, filename):
    return f"media/user_{instance.user.pk}_{filename}"

# =========== 단어를 형태소별로 쪼개서 리스트로 만들고 Keyword테이블에 저장하는 함수 ======================
def sort_word(sentence, word_count, answer_pk): 
    # Okt konelpy의 형태소 분석해주는 객체 생성
    okt = Okt()
    sentences_tag = []
    
    #형태소 분석하여 리스트에 넣기
    morph = okt.pos(sentence)
    sentences_tag.append(morph)
    
    noun_adj_list = []
    noun_list=[]
    adjective_list=[]
    alpha_list=[]
    
    #명사와 형용사만 구분하여 리스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if len(word) > 1 :
                if tag == "Noun" :
                    noun_list.append(word)
                    noun_adj_list.append(word)
                elif tag == "Adjective" :
                    adjective_list.append(word)
                    noun_adj_list.append(word)
                elif tag == "Alpha" :
                    alpha_list.append(word)
                    noun_adj_list.append(word)
                
    #형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(int(word_count))
    
    # wordCloud생성
    # 한글꺠지는 문제 해결하기위해 font_path 지정
    # wc = WordCloud(font_path="../epia/static/fonts/NEXONFootballGothicB.ttf", background_color="white", width=800, height=600)
    sorted_words = []
    
    # 분석한 데이터 DB에 저장하는 과정
    for data in tags:
        key, val = data
        if key in noun_list :
            sorted_words.append({'word': key, 'count': val, 'color':1})
            Keyword.objects.create(answer_id=answer_pk, word=key, count=val, wordtype=1)
        elif key in adjective_list :
            sorted_words.append({'word': key, 'count': val, 'color':2})
            Keyword.objects.create(answer_id=answer_pk, word=key, count=val, wordtype=2)
        elif key in alpha_list :
            sorted_words.append({'word': key, 'count': val, 'color':3})
            Keyword.objects.create(answer_id=answer_pk, word=key, count=val, wordtype=3)
            
    return sorted_words

# =============Keyword 테이블에서 정보를 가져오는 함수===============================
# ===============interview_result.html에서 axios로 요청============================
def keywordCall(request):
    answer_pk = request.GET.get('answer_pk')
    
    keyword_raw = Keyword.objects.filter(answer_id=answer_pk)
    keywords = list(keyword_raw.values())

    context = {
        'keywords' : keywords,
    }

    return JsonResponse(context)

# 마이페이지 > 지금까지의 면접 결과들 확인 페이지
@login_required
def mypage_resultlist(request):
    answers = Answer.objects.filter(user=request.user)
    newAnswers = []
    
    # 얼굴 사진을 불러오기 위해 dict를 포함하는 list 새로 생성
    for answer in answers:
        newAnswer = {
            'pk': answer.pk,
            'user':answer.user,
            'question':answer.question,
            'content':answer.content,
            'created_at':answer.created_at,
        }
        # 사진 결과가 없는 레코드를 위한 예외처리
        count = Face.objects.get(user=request.user, answer_id=answer.pk)
        print("count는요?", count)
        
        if count :
            newAnswer['face_path'] = Face.objects.get(user=request.user, answer=answer).path
            newAnswer['face_image'] = Face.objects.get(user=request.user, answer=answer).image
            
        else:
            newAnswer['face_path'] = 'interviews/images/epia_logo.png'

        newAnswers.append(newAnswer)
    print(newAnswers)
    context = {
        'answers' : newAnswers
    }

    return render(request, "interviews/mypage_resultlist.html", context)
    
def recognize(local_file_path):
    import os 
    # 배포 환경
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ubuntu/epiaproject/speech_to_text/studious-rhythm-281507-6fd0a2b80156.json'
    # print('==이후==')
    # print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    # client = speech_v1.SpeechClient().from_service_account_json(
    #     '/home/ubuntu/epiaproject/speech_to_text/studious-rhythm-281507-6fd0a2b80156.json')
    
    # 로컬 환경
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'epiaproject-47b0ace79186.json'
    print('==이후==')
    print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    client = speech_v1.SpeechClient().from_service_account_json('epiaproject-47b0ace79186.json')

    # The language of the supplied audio
    language_code = "ko-KR"

    # Sample rate in Hertz of the audio data sent
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    audio_channel_count=2
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count":audio_channel_count,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")

    response = operation.result()

    for result in response.results:
        alternatives = result.alternatives
        for alternative in alternatives:
            # alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
            print(u"Confidence: {}".format(alternative.confidence))
            trans = u"{}".format(alternative.transcript)
        return trans