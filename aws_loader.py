import requests
import os
import csv

def load_aws(year, month, key):

    # 파일 이름a
    directory_name = "AWS"
    # 디렉토리가 없으면 생성
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"디렉토리 '{directory_name}'가 생성되었습니다.")
        
    year = year
    month = month
    key = key
    for day in range(1,32):
        for hour in range(0,24):
            for minute in range(0,60,5):
                date = f'{year}{month:02d}{day:02d}{hour:02d}{minute:02d}'
                url = f'https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min?tm2={date}&stn=0&disp=0&help=1&authKey={key}'

                # 지정한 URL로 GET 요청을 보내고 응답을 받습니다.
                response = requests.get(url)
                if response.status_code == 200:
                    # 응답으로 받은 데이터를 바이트 스트링에서 일반 문자열로 변환하고, cp949 인코딩을 사용하여 줄별로 나눕니다.
                    data = response.content
                    lines = data.decode('cp949').split('\n')

                    # 빈 줄이나 '#'로 시작하는 줄을 제외하고, 데이터 헤더와 행으로 나눕니다.
                    headers = lines[20].split()  # 20번째 줄에 있는 데이터 헤더를 추출합니다.
                    headers = headers[1:]  # 첫 번째 열은 버립니다.
                    lines = [line for line in lines if line and not line.startswith('#')]

                    data_rows = [line.split() for line in lines[:]]  # 모든 행을 데이터 행으로 나눕니다.

                    # 데이터를 CSV 파일로 저장합니다.
                    csv_filename = f"./AWS/AWS_{date}.csv"
                    print(f'{year}.{month:02d}.{day:02d} {hour:02d}:{minute:02d} 자료를 저장했습니다')
                    with open(csv_filename, 'w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(headers)  # 헤더를 CSV 파일에 작성합니다.
                        csv_writer.writerows(data_rows)  # 데이터 행들을 CSV 파일에 작성합니다.
                else:
                    print('비정상적인 자료요청입니다. 프로그램을 재시작해주세요')
                    break  # 가장 안쪽의 for 루프를 종료
            else:
                continue  # 내부의 for 루프가 정상적으로 종료되었을 때 실행되는 블록
            break  # 내부의 for 루프가 break를 통해 종료되었을 때 실행되는 블록
        else:
            continue  # 외부의 for 루프가 정상적으로 종료되었을 때 실행되는 블록
        break  # 외부의 for 루프가 break를 통해 종료되었을 때 실행되는 블록

    else:
        print("프로그램 종료")

# 날씨 정보를 가져오기 위해 사용할 인증키와 요청할 URL을 변수로 지정합니다.
print('AWS 5분 간격 데이터 수집 프로그램')
print('년, 월 , 인증키를 입력하면 해당 기간의 자료가 5분 간격으로 수집됩니다')
year = int(input(' 자료의 년도를 입력하세요: '))
month = int(input(' 월을 입력하세요 : '))
key = input('Key를 입력하세요 : ')

load_aws(year,month, key)

