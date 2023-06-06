# 네이버 상품에서 내가 원하는 상품의 가격을 알려주는 프로그램
# 해당 상품의 최저가와 최고가를 알려준다.
# 상품의 리뷰, 별점, 상품의 이미지를 보여준다.

# 상품의 태그들을 list로 가져온다.
# 상품의 태그 중에서 가격, 리뷰, 별점, 이미지를 가져온다.
# 가져온 태그들을 상품(list)마다 출력한다.
# 가져온 태그들을 json 형태로 저장한다.

# 현재 모든 출력 결과가 None을 반환하는 오류가 있다.
# 이 오류를 해결해야 한다.
# 크롤링을 할 때, 모든 항목에 해당 태그가 존재하지 않는 경우이다.
# 이를 해결하기 위해서는 해당 값을 갖는 태그를 정확히 선택하는 것이 중요하다.
# 이를 위해서는 크롬 개발자 도구를 사용해야 한다.
# 크롬 개발자 도구를 사용하여 해당 태그를 정확히 선택하고, 그 태그가 존재하지 않는 경우에 대한 예외처리를 해야 한다.

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import sys
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# 네이버 상품을 직접 검색한 url로 접속한다.
# 검색을 원하는 상품명을 입력받는다.
# 네이버 쇼핑은 스크롤을 내려야 상품의 정보가 나타난다.
# 상품의 정보를 가져오기 위해서는 스크롤을 내려야 한다.
# 스크롤을 내리는 것은 selenium을 사용해야 한다. (일단 보류)
def get_product_info(product_name):
    url = "https://search.shopping.naver.com/search/all.nhn?query=" + product_name + "&cat_id=&frm=NVSHATC"
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# 상품들의 목록 태그를 가져온다.
# <li class="basicList_item__2XT81">...</li>
# 해당 태그를 가진 모든 태그를 찾아서 배열에 저장한다.
def get_product_list(soup):
    product_list = soup.select('.basicList_item__2XT81')
    return product_list

# 상품의 가격을 가져오는 함수
# <span data-testid="SEARCH_PRODUCT_PRICE">33,000원</span>
# 해당 data-testid="SEARCH_PRODUCT_PRICE 를 가진 태그를 찾아서 그 안의 텍스트를 가져온다.
# 가져온 텍스트를 가져온 인덱스 순서대로 배열에 저장한다.
def get_product_price(soup):

    # 해당 태그가 존재하지 않을 때까지 반복문으로 상품의 가격을 가져온다.
    # 해당 태그가 존재하지 않는 경우, None을 반환한다.
    # 해당 태그가 존재하는 경우, 해당 태그 안의 텍스트를 가져온다.
    # 가져온 텍스트를 가져온 인덱스 순서대로 배열에 저장한다.
    # 값을 한개밖에 가져오지 못하는 문제가 있다.
    # data-testid='SEARCH_PRODUCT_PRICE' 를 가진 태그가 여러개 존재하는 경우, 모든 태그를 가져오도록 수정해야 한다.

    price = soup.find('span', {'data-testid': 'SEARCH_PRODUCT_PRICE'}).text
    return price

    


# 상품의 리뷰를 알려준다.
def get_product_review(soup):
    review = soup.select('.info_cell')
    if len(review) >= 3:  # review 리스트에 3개 이상의 요소가 있는지 확인
        review = review[2].text
        review = review.replace('리뷰', '')
        review = review.replace(',', '')
        review = int(review)
        return review
    else:
        return None  # review 리스트에 3개 미만의 요소가 있다면 None을 반환


# 상품의 별점을 알려준다.
def get_product_star(soup):
    star = soup.select('.info_cell')
    if len(star) >= 4:  # star 리스트에 4개 이상의 요소가 있는지 확인
        star = star[3].text
        star = star.replace('별점', '')
        star = star.replace(',', '')
        star = float(star)
        return star
    else:
        return None  # star 리스트에 4개 미만의 요소가 있다면 None을 반환


# 상품의 이미지를 알려준다.
def get_product_image(soup):
    image = soup.select('.img_area')
    if image:  # image 리스트가 비어있지 않은지 확인
        image = image[0].find('img')
        image = image.get('src')
        return image
    else:
        return None  # image 리스트가 비어있다면 None을 반환


# 상품의 가격이 내가 원하는 가격보다 낮으면 알림을 보내주는 기능은 일단 개발하지 않고 보류한다.

# 메인 함수
# 원하는 상품을 입력받고 해당 상품의 최저가, 최고가, 리뷰, 별점, 이미지를 알려준다.
def main():
    product_name = input("원하는 상품명을 입력하세요 : ")
    soup = get_product_info(product_name)
    price = get_product_price(soup)
    review = get_product_review(soup)
    star = get_product_star(soup)
    image = get_product_image(soup)
    print("최저가 : ", price)
    print("리뷰 : ", review)
    print("별점 : ", star)
    print("이미지 : ", image)

if __name__ == "__main__":
    main()