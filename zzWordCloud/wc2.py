# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import requests
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import random
import webbrowser
import pytagcloud
# get_tags 새함수 만듦:
# 기능 1. 댓글별로 명사만 추출
# 기능 2. 명사 빈도수 집계
# 기능 3. 단어구름에 표시할 명사에 3가지 시각화 속성
#        (색상'color', 단어'tag', 크기'size')부여
# 
# # 입력변수- text : 댓글, ntags : 표시할 단어수, multiplier : 크기가중치
def get_tags(text, ntags=20, multiplier=2):
    t = Okt()
    nouns = []

# 모든 댓글에서 명사만 추출하고 nouns변수에 누적해 저장함
    for sentence in text:
        for noun in t.nouns(sentence):
            nouns.append(noun)
            # 각 명사별로 빈도계산
            count = Counter(nouns)
    # n : 명사, c : 빈도
    return [{'color': color(),'tag':n,'size':2*c*multiplier} for n,c in count.most_common(ntags)]

# draw_cloud 새함수 만듦:
# 기능 1. pytagclud 모듈을 사용해 단어구름 이미지를 만듦
# 기능 2. 단어구름 이미지를 파일로 저장함
# 기능 3. 화면에 단어구름을 표시함
# # 입력변수 tags : get_tags()에서 리턴되는 color, tag, size(이미지크기) 값이 전달됨.
# fontname : Noto Sans CJK - 한글폰트
def draw_cloud(tags, filename, fontname = 'Arial',size1 = (1300,800)):
    pytagcloud.create_tag_image(tags,filename,fontname=fontname,size=size1)
    # 저장된 단어구름 이미지파일(wc1.png)을 내 컴퓨터에 띄움
    webbrowser.open(filename)
    ####################################################
# 명사에 적용할 색상 랜덤지정
r = lambda: random.randint(0, 255)
color = lambda: (r(), r(), r())
# 옥자 댓글(okja1.txt) 읽기 전용으로 읽어들임.
script = ["이재용 삼성전자 부회장이 30일 소재, 부품, 장비 챙기기로 현장경영을 재개했다.대검 수사심의위원회에서 경영권 승계 의혹과 관련 불기소 권고가 나온 지 4일, 삼성전자의 생활가전사업부(23일)를 방문한 지 7일 만이다.이 부회장은 이날 삼성전자의 반도체부문 자회사인 세메스(SEMES) 천안사업장을 찾아 생산공장을 둘러보고 임직원들을 격려했다.김기남 부회장, 이동훈 삼성디스플레이 사장, 박학규 DS부문 경영지원실장(사장) 등이 동행했다.이 부회장은 이들과 함께 반도체·디스플레이 제조장비 산업 동향, 설비 경쟁력 강화 방안, 중장기 사업 전략 등을 논의한 후 생산공장을 살펴봤다.세메스는 1993년 삼성전자가 설립한 반도체·디스플레이 제조용 설비제작 전문기업이다.이 부회장의 이번 방문은 국내 반도체·디스플레이 산업의 약점으로 지적됐던 소·부·장을 직접 챙기겠다는 의도로 풀이된다.일본이 지난해 7월 반도체 핵심 소재에 대한 수출규제에 나서자 이 부회장은 일본으로 직접 출장을 다녀온 후 긴급 사장단 회의를 소집해 “흔들리지 않고 시장을 이끌어 갈 수 있도록 역량을 키우자”며 사장단에 컨틴전시 플랜(비상 계획) 마련을 주문했다."

]
####################################################
# 댓글 명사추출 및 빈도분석(get_tags) 실시
tags = get_tags(script)
print(tags)
# 관심명사 단어구름 이미지 파일 저장 및 출력하기
draw_cloud(tags,'wc1.png')
