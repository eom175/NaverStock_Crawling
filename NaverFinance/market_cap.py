import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()


url = 'https://finance.naver.com/sise/sise_market_sum.naver?page=' 
browser.get(url)

#2. 체크되어있는 항목 해제
checkboxes = browser.find_elements(By.NAME, 'fieldIds') # 모든 체크박스 가져옴
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크되어 있는 경우
        checkbox.click() # 체크 해제


#3. 조회 항목 설정(원하는 항목)
items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element 조회
    label = parent.find_element(By.TAG_NAME, 'label') # 하위에 label Tag이름 가지는 element 조회해서 반환
    # print(label.text)
    if label.text in items_to_select:
        checkbox.click() # 리스트에 있는 항목과 동일한 항목은 체크박스에 체크 표시

#4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for index in range(1,40): # 1이상 40미만 페이지 반복


    #사전작업: 페이지 이동 -> 뒤에다가 index 추가
    browser.get(url+str(index))

    #5. 데이터 추출
    df = pd.read_html(browser.page_source)[1] # 데이터 프레임 구성

    # 결측치 삭제 -> NAN 데이터 삭제
    df.dropna(axis= 'index', how = 'all', inplace = True) # 한 줄이 모두 결측치일때 삭제

    df.dropna(axis= 'columns', how = 'all', inplace = True) # 세로줄이 모두 결측치일 때 삭제    
    if len(df)== 0:
        break


    #6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): #파일이 있다면 헤더제외
        df.to_csv(f_name, encoding = 'utf-8-sig', index = False, mode = 'a', header = False)
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding = 'utf-8-sig', index = False)

    print(f'{index} 페이지 완료')

browser.quit()
