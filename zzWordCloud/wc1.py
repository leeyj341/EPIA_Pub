# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import requests
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud

def make_wordcloud(word_count):
    okt = Okt()

    sentences_tag = []
    #형태소 분석하여 리스트에 넣기

    morph = okt.pos(sentence)
    sentences_tag.append(morph)
    print(morph) #단어가 명사인지, 부사, 특수문자인지 등등 나타내준다. 
    print('-' * 30)

    print(sentences_tag)
    print('\n' * 3)

    noun_adj_list = []
    #명사와 형용사만 구분하여 리스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)

    #형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    print(tags)

    print("-"*100)
    #wordCloud생성
    #한글꺠지는 문제 해결하기위해 font_path 지정
    wc = WordCloud(font_path='../epia/static/fonts/NEXONFootballGothicB.ttf', background_color='white', width=800, height=600)
    print(dict(tags))
    #wc.to_file('clooo.png')
    #cloud = wc.generate_from_frequencies(dict(tags))
    # plt.figure(figsize=(10, 8))
    # plt.axis('off')
    # plt.imshow(cloud)
    # plt.show()
sentence = "이재용 삼성전자 부회장이 30일 소재, 부품, 장비 챙기기로 현장경영을 재개했다.대검 수사심의위원회에서 경영권 승계 의혹과 관련 불기소 권고가 나온 지 4일, 삼성전자의 생활가전사업부(23일)를 방문한 지 7일 만이다.이 부회장은 이날 삼성전자의 반도체부문 자회사인 세메스(SEMES) 천안사업장을 찾아 생산공장을 둘러보고 임직원들을 격려했다.김기남 부회장, 이동훈 삼성디스플레이 사장, 박학규 DS부문 경영지원실장(사장) 등이 동행했다.이 부회장은 이들과 함께 반도체·디스플레이 제조장비 산업 동향, 설비 경쟁력 강화 방안, 중장기 사업 전략 등을 논의한 후 생산공장을 살펴봤다.세메스는 1993년 삼성전자가 설립한 반도체·디스플레이 제조용 설비제작 전문기업이다.이 부회장의 이번 방문은 국내 반도체·디스플레이 산업의 약점으로 지적됐던 소·부·장을 직접 챙기겠다는 의도로 풀이된다.일본이 지난해 7월 반도체 핵심 소재에 대한 수출규제에 나서자 이 부회장은 일본으로 직접 출장을 다녀온 후 긴급 사장단 회의를 소집해 “흔들리지 않고 시장을 이끌어 갈 수 있도록 역량을 키우자”며 사장단에 컨틴전시 플랜(비상 계획) 마련을 주문했다."
make_wordcloud(30)