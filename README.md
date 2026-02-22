# NaverStock_Crawling

pandas + Selenium + ChromeDriver를 사용해 네이버 금융의 시가총액 페이지를 순회하며
종목 데이터를 CSV로 저장하는 크롤링 연습.

이 README는 `market_cap.py`(주석 기준) 흐름이 그대로 드러나도록 작성.
## 1) 프로젝트 목적

- 네이버 금융 시가총액 페이지(`sise_market_sum.naver`)에서 여러 페이지의 종목 데이터를 수집
- 기본 선택 항목을 해제한 뒤 원하는 항목만 다시 선택해 조회
- 수집 결과를 `sise.csv`로 누적 저장

## 2) 사용 기술

- Python
- pandas
- selenium
- ChromeDriver

## 3) 실행 환경 준비

1. Python 가상환경 생성(선택)
2. 패키지 설치

```bash
pip install pandas selenium lxml
```

3. Chrome 브라우저 버전에 맞는 ChromeDriver 준비
- PATH에 등록하거나 실행 파일 경로를 코드에서 지정
- 예시 코드에서는 `webdriver.Chrome()`을 사용하므로 환경에서 자동 탐색되도록 맞추는 방식

## 4) 실행 방법

```bash
python NaverFinance/market_cap.py
```

실행이 끝나면 현재 작업 디렉터리에 `sise.csv`가 생성(또는 갱신)됩니다.

## 5) 크롤링 상세 과정 (코드 주석 순서 기준)

### Step 0. 브라우저 실행
- `webdriver.Chrome()`으로 크롬 드라이버 실행
- `maximize_window()`로 브라우저 창 최대화

### Step 1. 대상 페이지 접속
- 기본 URL:
  - `https://finance.naver.com/sise/sise_market_sum.naver?page=`
- 먼저 해당 페이지를 열어 필터 체크박스 조작 준비

### Step 2. 체크되어 있는 항목 해제 (`#2`)
- `name='fieldIds'`인 모든 체크박스를 가져옴
- `is_selected()`가 `True`인 체크박스는 클릭해서 해제
- 목적: 이전 기본/잔여 필터 상태를 초기화해 결과 일관성 확보

### Step 3. 조회 항목 설정 (`#3`)
- 선택 대상: `['시가', '고가', '저가']`
- 각 체크박스의 부모 요소에서 `label` 텍스트를 읽어 항목명 판별
- 항목명이 리스트에 있으면 체크
- 즉, "원하는 컬럼만 선택"하는 핵심 단계

### Step 4. 적용하기 버튼 클릭 (`#4`)
- `javascript:fieldSubmit()` 링크를 찾아 클릭
- 체크박스 설정을 실제 조회 결과에 반영

### Step 5. 페이지 반복 수집 (`for index in range(1,40)`)
- 1페이지부터 39페이지까지 순회 시도
- 매 반복마다 `url + str(index)`로 이동
- 현재 페이지 HTML에서 표를 `pd.read_html(browser.page_source)[1]`로 읽어 DataFrame 생성
  - 네이버 금융 페이지에서 실제 종목 테이블이 두 번째 테이블(index 1)인 구조를 가정

### Step 6. 결측치 정리
- `dropna(axis='index', how='all')`: 행 전체가 NaN이면 제거
- `dropna(axis='columns', how='all')`: 열 전체가 NaN이면 제거
- 정리 후 `len(df) == 0`이면 루프 종료
  - 유효 데이터가 없다는 뜻으로 간주

### Step 7. CSV 저장 (`#6`)
- 파일명: `sise.csv`
- 파일이 이미 있으면:
  - `mode='a'`, `header=False`로 헤더 중복 없이 이어쓰기
- 파일이 없으면:
  - 헤더 포함하여 새로 저장
- 페이지마다 `"n 페이지 완료"` 로그 출력

### Step 8. 브라우저 종료
- 모든 작업 후 `browser.quit()`으로 드라이버 종료

## 6) 결과 파일

- 출력 파일: `sise.csv`
- 인코딩: `utf-8-sig` (엑셀 한글 호환 목적)
- 페이지 단위 append 저장 방식이라 중간까지의 데이터도 남길 수 있음

## 7) 코드 주석과 실제 동작 매핑

- `#2 체크되어있는 항목 해제` → 기존 필터 상태 초기화
- `#3 조회 항목 설정` → 원하는 컬럼(시가/고가/저가)만 선택
- `#4 적용하기 버튼 클릭` → 선택된 항목을 테이블에 반영
- `#5 데이터 추출` → HTML 표를 DataFrame으로 변환
- `#6 파일 저장` → CSV 생성/누적 저장

## 8) 주의사항

- 네이버 금융 HTML 구조가 바뀌면 `read_html(...)[1]` 인덱스가 달라질 수 있음
- 사이트 응답 지연 시 `WebDriverWait` 기반 대기 로직을 추가하는 것이 안정적
- 대량 수집 시 과도한 요청을 피하도록 간격 조절(예: `time.sleep`) 권장

## 9) 개선 아이디어

- `argparse`로 페이지 범위/저장 파일명을 인자로 받기
- 예외 처리(`try/except`) 및 로그 파일 기록
- 중복 종목 제거, 날짜 컬럼 추가, 자동 백업 파일 생성
