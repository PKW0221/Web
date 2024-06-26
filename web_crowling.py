from google.colab import drive
drive.mount('/gdrive') # 구글 드라이브를 'gdrive`라는 폴더에 연결

import pandas as pd

"""## 웹스크래핑

인터넷에서 웹페이지를 가져오기 위해서는 `requests` 모듈을 사용합니다. 이 외에도 `urlib` 등 웹페이지를 파이썬의 객체로 저장해 주는 다양한 모듈이 있으나 사용방법은 크게 다르지 않습니다.

"""

#파이썬으로 웹 데이터를 가져오기 위한 모듈
import requests

"""웹페이지를 파이썬으로 스크렙하기 위해서는  가져오기 위해서는 해당 웹페이지의 `url`이 필요합니다. `url`이란 `uniform resource locator`의 약자로 우리가 흔히 말하는 웹페이지의 주소입니다. 인터넷 상의 어떤 공간을 특정하는 정보라고 생각하시면 됩니다. 다음과 같은 형식으로 페이지를 호출합니다.

```
requests.get(url)
```


여기에서는 웹 스크래핑을 실습해 보기 위해서 [imdb](https://www.imdb.com/)에서 미나리(2020)에 관한 정보를 가져와 보도록 하겠습니다.

웹 페이지를 스크랩하면 아래와 같이 `Response [200]`이라는 결과가 나옵니다. 이는 웹페이지를 파이썬이 성공적으로 수집해 왔음을 의미합니다. 이 외에도 다양한 형태의 응답 메시지가 나오는데 일반적으로 우리가 많이 접할 응답 메시지는 다음과 같습니다. <br></br>

|응답메시지|의미|
|---|---|
|200|웹 페이지를 성공적으로 수집했음|
|403|웹 페이지에 대한 접근이 거부 됨|
|404|웹 페이지가 존재하지 않음|
"""

# imdb의 미나리페이지
url = "https://www.imdb.com/title/tt10633456/?ref_=fn_al_tt_1"  # 미나리 URL을 저장

# 존재하는 URL 스크랩
requests.get(url)

"""네이버 같이 python requests를 사용한 스크랩을 막아 놓은 경우 (`Response [403]`)에러가 뜹니다."""

url2= 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=056&aid=0011012482'
requests.get(url2)

"""만약에 존재하지 않는 페이지를 저장하려고 하면 다음과 같이 `Response [404]`에러가 뜹니다."""

# 존재하지 않는 URL 스크랩
url3 = 'https://www.imdb.com/title/tt10633sadf2346'
requests.get(url3)

"""`requests.get`을 통해 수집한 데이터 또안 변수화 할 수 있습니다."""

res = requests.get(url) # 미나리 수집 데이터를 저장

"""저장된 html 웹페이지를 보기 위해서는 다음과 같이 `.content` 메서드를 사용합니다. 실제 웹페이지를 살펴보면 수집된 데이터와 동일한 것을 확인할 수 있습니다."""

print('실제 웹페이지: %s' %url)
res.content # 수집된 HTML cnffur

"""##HTML 파싱

파싱(parsing)은 수집된 html을 데이터 화하기 위해서 수행하는 작업으로, 일반적으로 데이터사이언스 프로젝트에서 html형태로 저장된 페이지의 특정 부분을 가져오는 작업을 가리키는 경우가 많습니다.

웹의 데이터를 가져와 파싱하기 위해서는 [`bs4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)라는 모듈을 주로 사용합니다.

참조: [bs4의 한글메뉴얼](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ko/)
"""

# bs4 불러오기
import bs4

"""###bs4의 기본

이미 저장되어 있는 데이터를 파싱할 수 있는 형태로 만들기 위해서는 `bs4` 모듈의 `BeautifulSoup` 함수를 사용합니다. 파씽을 위한 해석 라이브러리에는 `html.parser` 외에도 `lmxl`이나 `xml`등이 존재합니다.

```
bs4.BeautifulSoup(웹페이지.content, 파씽을 위한 해석라이브러리)
```


"""

soup = bs4.BeautifulSoup(res.content, 'html.parser')

# 읽으수 있는 형태로 만듦
soup

"""###원하는 데이터 찾기

`bs4`를 이용하여 스크랩한 데이터에서 원하는 데이터를 가져오기 위해서는 html과 css의 태그를 이용하거나 아니면 selector를 이용해야합니다.

여기에서는 먼저 tag를 이용하여 데이터를 가져와 보도록 하겠습니다.

####하나씩 찾기(find)와 전부 찾기(find_all)

스크랩한 html 데이터에서 자신이 원하는 특정 데이터를 찾기 위해서는 `find`와 `find_all`을 사용해야 합니다. `find`의 경우 찾으려는 조건에 부합하는 가장 첫 결과물을 반환하지만 `find_all`의 경우 조건에 부합하는 모든 데이터를 반환합니다.

먼저 `find`의 경우 다음과 같은 형식을 사용합니다.

```
파싱된데이터.find(찾으려는태그)
```

원하는 데이터를 찾기 위해선, 본인이 찾으려는 하는 데이터가 어떤 태그를 사용하였는지를 알 필요가 있습니다. 예를 들어 `h1`의 경우 가장 높은 수준의 장, 절, 구, 처럼 가장 높은 수준의 문서를 나타냅니다.

참조: [html tag referece](https://www.w3schools.com/tags/default.asp)
"""

# h1태그를 가진 첫번째 값을 찾아 html 코드 출력
soup.find('h1')

"""`.find_all()`을 사용하는 경우 조건에 맞는 모든 값을 돌려줍니다. 이 때 리스트의 형태로 돌려준다는 점을 유의해야합니다."""

# h1태그를 가진 모든 값 출력
soup.find_all("h1")

"""웹 페이지를 살펴보면 `h1` tag는 한 번 박에 사용되지 않았지만 `h2`의 경우 여러번 사용된 것을 알 수 있습니다. 아래의 경우에서 확인해 볼 수 있듯이 같은 태그가 여러게 있는 경우 `find`는 가장 먼저 조건을 만족하는 부분을 `find_all`은 조건을 만족하는 모든 부분을 반환합니다."""

soup.find('h2')

soup.find_all('h2')

"""찾은 데이터에 다음 메서드를 사용하면 원하는 결과를 반환 받을 수 있습니다.

|메서드|결과|
|---|---|
|.name|tag네임 반환|
|.a|링크 반환|
|.text|텍스트 반환|


"""

soup.find('h1')

soup.find('h1').name

soup.find('h1').a

soup.find('h1').text

# 만약 값이 존재하지 않으면 아무것도 반환하지 않음
soup.find('h2').a

soup.find('h2').text

soup.find('h1').text

"""html코드 형식으로 텍스트가 쓰여져 있기 때문에 데이터프로젝트의 필요에 맞게 텍스트 데이터를 바꿀 필요가 있습니다. <br> 특히 위의 경우 `\xa0`의 경우 빈칸을 의미하고, 실제 데이터 분석에서 필요없는 경우가 많습니다. 필요에 따라 해당 문자열을 없애줄 필요가 있습니다. 이 때 가져온 문자열 데이터에서 `\xa0`을 없애주기 위해서는 `replace`를 사용하여 해당 문자를 빈칸이나 아니면 칸이없는 것을 바꿔줄 필요가 있습니다.  

문자열에서 특정 문자열 바꾸기
```
문자열.replace("바꿀문자열", "바뀔문자열)"
```

또한 위의 문자열의 경우 오른쪽 공백 또한 존재함으로 만약 오른쪽 공백을 지우고 싶다면 다음과 같이 `rstrip()`을 사용합니다. 만약 왼쪽 공백을 지우고 싶다면 `lstrip()`을 사용합니다.
```
문자열.rstrip()
```

참조: `rstrip()`과 `lstrip`은 공백이 아닌 원하는 문자를 지정하여 지울 수도 있습니다. 이에 대한 자세한 방법은 이 [링크](https://www.w3schools.com/python/ref_string_rstrip.asp)를 확인 하시기 바랍니다.
"""

soup.find('h1').text.replace('\xa0', ' ').rstrip()

soup.find('h1').text

"""만약 tag에 해당되는 값이 많은 경우 리스트 형태로 반환됩니다."""

soup.find_all("h2")

soup.find('div')

soup.find_all('div')

"""####css selector를 사용하여 원하는 데이터 가져오기

html tag외에도 css selector를 사용하여 html의 특정 부분을 가져올 수 있습니다. css selector를 사용하면 html의 원하는 부분을 꼭집어서 가져올 수 있다는 장점 있습니다. 다만 html의 구조가 복잡해질수록, 원하는 곳을 가져오기가 복잡해질 수 있음으로 사용하는 데 주의할 필요가 있습니다.

html문서의 각 부분의 css selector는 chome에서 확인할 수 있습니다.

참조: [css selector reference](https://www.w3schools.com/cssref/css_selectors.asp)

"""

#'#title-overview-widget > div.vital > div.title_block > div > div.ratings_wrapper > div.imdbRating > div.ratingValue'

soup.select('#title-overview-widget > div.vital > div.title_block > div > div.ratings_wrapper > div.imdbRating > div.ratingValue')

soup.select('#title-overview-widget > div.vital > div.title_block > div > div.ratings_wrapper > div.imdbRating > div.ratingValue')[0].text

soup.select('#titleCast')

soup.select('#titleCast > table')

"""####특정 tag 중 특정 class만 가져오기

위에서 살펴본 것처럼, html tag를 사용하면 특정 tag를 전부 가져올 수 있습니다. 이 때 특정 tag에서 비슷한 유형의 html 데이터를 가져오기 위해서는 html tag의 class 활용해야 합니다.

```
soup.find_all(태크, {attribute:'명칭'})
```

사용할 수 있는 attribute에는 `'class'` `'id'` 등이 있습니다. `class`는 여러 개체가 공유할 수 있고, `id`는 고유 식별 번호라고 할 수 있습니다.


"""

soup.find_all('div', {'class':'ratingValue'})

# 특정 id를 가진 div태그 수집
soup.find_all('div', {'id':'titleImageStrip'})

"""###Cast list 가져오기

캐스트와 각 배우의 극 중 이름이 테이블에 있다는 점에 착안하면 배우와 극중 역할을 데이터화 할 수 있습니다.
"""

soup.find_all("td")

# td 태그만 가져오기
soup.find_all("td", {"class":"primary_photo"})

for i in soup.find_all("td", {"class":"primary_photo"}):
  print(i.find('img', alt=True)['title'])

# 배우이름
list(map(lambda i: i.find('img',alt=True)['title'],
         soup.find_all("td", {"class":"primary_photo"})))

soup.find_all("td", {"class":"character"})[0]

# 극중이름
list(map(lambda x: x.find('a').text,
         soup.find_all("td", {"class":"character"})))

"""##온라인 커뮤니티에서 글과 댓글가져오기

웹스크랩핑과 html 파싱을 위해서, 주요 온라인 커뮤니티 중 하나인 [clien](https://www.clien.net/)에서 추천 글의 리스트와 개별 글을 스크랩해보도록 하겠습니다.

###추천게시판에서 추천글 리스트가져오기
"""

res = requests.get('https://www.clien.net/service/recommend')
res.content
soup2 = bs4.BeautifulSoup(res.content, 'html.parser')

title_list = list(map(lambda x: x.text, soup2.find_all("span", {"class":"subject_fixed"})))

# k를 제거하기 위해 인덱싱
soup2.find_all("span", {"class":"hit"})[0].text[:-2]

# 조회수
hit_list = list(map(lambda x: float(x.text) if 'k' not in x.text else float(x.text[:-2])*1000, soup2.find_all("span", {"class":"hit"})))

# 데이터
sympathy_list = list(map(lambda x:int(x.text), soup2.find_all("span", {"class":"rSymph05"})))

# 날짜
date_list = list(map(lambda x: x.text, soup2.find_all("span", {"class":"timestamp"})))

pd.DataFrame({'title':title_list, 'hit':hit_list, 'sympathy':sympathy_list, 'date_list':date_list})

# 데이터 프레임을 만듭니다.
df1 = pd.DataFrame({'title':title_list, 'hit':hit_list, 'sympathy':sympathy_list, 'date_list':date_list})

"""### 하나의 글에서 본문과 댓글가져오기

이 부분은 반복이 되기 때문에 실제로 강의에서는 다루지 않습니다. 다만 지금까지와 같은 방법으로 데이터를 스크랩하고, 이를 파씽하는 방법을 통해서 원하는 데이터를 가져올 수 있습니다. 지금까지와 같은 방법으로 개발자 도구를 사용해서 원하는 태그를 찾고, 그 태그에 저장되어 있는 값들을 저장할 수 있습니다.

아래의 코드를 확인해보기 위해서 실제 `url3`에 해당되는 페이지에 가서 데이터를 분석해도록 하세요. **만약에 아래의 페이지가 존재하지 않는다면 클리앙의 게시물 중 어느 하나를 선택하셔도 됩니다.**
"""

url3 = "https://www.clien.net/service/board/park/15995038?type=recommend"

# 스크랩과 파싱 준비
import requests, bs4
res = requests.get(url3)
res.content
soup3 = bs4.BeautifulSoup(res.content, 'html.parser')

# 스크랩과 파싱 준비
res = requests.get(url3)
res.content
soup3 = bs4.BeautifulSoup(res.content, 'html.parser')

"""###본문가져오기"""

#본문의 태그를 확인하고 텍스트 가져오기
soup3.find_all("div", {"class":"post_article"})[0].text

# 텍스트에 \n(한칸띄기) \xa0 (빈칸)이 있기에 replace를 사용해서 제거
soup3.find_all("div", {"class":"post_article"})[0].text.replace("\n","").replace("\xa0","")

"""###댓글 가져오기

게시물에 달린 댓글과 각 댓글의 공감 수 또한 같은 방법으로 가져옵니다. html의 tag와 class를 사용하서 데이터를 가져오고 이를 정제하여 리스트 형식으로 저장합니다.
"""

#코멘트의 공감수가져오기 button 태그의 comment_symph임을 확인 할 것
soup3.find_all("button", {"class":"comment_symph"})

# 댓글이 어떤 형식으로 저장되어 있는지 확인
soup3.find_all("div", {"class":"comment_view"})

# 코멘트 수집
comment = list(map(lambda x: x.text.replace("\n","").replace("\t",""),
                   soup3.find_all("div", {"class":"comment_view"})))

comment

# 공감수가 어떤 형식으로 저장되어있는지 확인
soup3.find_all("button", {"class":"comment_symph"})

# map과 lamda를 사용하여 저장
like = list(map(lambda x: int(x.text), soup3.find_all("button", {"class":"comment_symph"})))

df2 = pd.DataFrame({'comment':comment, 'like':like})
df2.shape

"""##데이터 저장

앞선 시간에서는 데이터프레임을 새로 민들거나 아니면 특정 데이터 셋의 일부분만을 따로 분리하여 새로운 데이터프레임을 만들었습니다. 이 때 새로 작업한 데이터 프레임을 파일로 저장하고 이를 필요한 경우만 불러 낼 수 도 있습니다.

예를 들어 설명해보겠습니다. 이전에 사용한 데이터 셋의 일정부분을 때어냈다고 생각해봆디. 이 데이터를 새로운 `csv`로 저장하기 위해서는 `to_csv`라는 메서드를 써야 합니다.

데이터를 `csv`형태로 저장하기 위해서는 다음과 같은 형식을 사용합니다. 이 때 인덱스를 지정하지 않으려면 `index=False`라는 아규먼트를 또 쉼표(,)가 아닌 다른 형식으로 각 행(혹은 필드)를 구분하려면 (예를 들어 \t) `sep="\t"` 아규먼트를 사용해야 합니다.

```
데이터프레임.to_csv("파일경로")
```
"""

df1

df2

# Test CSV로 저장
df1.to_csv('/gdrive/My Drive/DSC2001/data/dsc2001_unit10_test1.csv', index=False)

# Test CSV로 저장
df2.to_csv('/gdrive/My Drive/DSC2001/data/dsc2001_unit10_test2.csv', index=False, sep="\t")

df3 = pd.read_csv('/gdrive/My Drive/DSC2001/data/dsc2001_unit10_test1.csv')

df3.head()

df4 = pd.read_csv('/gdrive/My Drive/DSC2001/data/dsc2001_unit10_test2.csv', sep="\t")

df4
