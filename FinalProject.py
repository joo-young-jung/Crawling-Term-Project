import pandas as pd
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *

def dataProcessing():
     # 공공데이터 포탈에서 csv파일로 저장이 안되는 오류가 있음.
     # 따라서, 엑셀파일 읽은 후 csv파일로 저장하는 과정이 필요.

     # 엑셀파일 읽어오기
     df = pd.ExcelFile('데이터원본.xls').parse(sheet_name=0, dtype=object, engine='xlrd', verbose=True)

     # 구분자(,)가 데이터에 존재하지만 str형이 아닌 숫자이므로 치환이 필요 없음.
     # 엑셀파일을 csv파일로 변환하여 저장
     df.to_csv(path_or_buf='데이터원본.csv', sep=',', header=True, index=False, mode='w', encoding='CP949')

     # csv파일 읽기
     df = pd.read_csv('데이터원본.csv', engine='c', dtype=str, sep=',', encoding='CP949')

     # 합계만 따로 관리하기 위해 자치구가 합계가 아닌 행을 모두 삭제 후
     df_total = df
     idx_del = df_total[df_total['자치구']!='합계'].index
     df_total = df_total.drop(idx_del)

     # 발생건수의 합계만 데이터가공_발생건수_합계.csv로 따로 저장
     idx_del = df_total[df_total['구분']!='발생건수'].index
     df_total_1 = df_total.drop(idx_del)
     
     df_total_1.to_csv(path_or_buf='데이터가공_발생건수_합계.csv', sep=',', header=True, index=False, mode='w', encoding='CP949')

     # 사망자수의 합계만 데이터가공_사망자수_합계.csv로 따로 저장
     idx_del = df_total[df_total['구분']!='사망자수'].index
     df_total_2 = df_total.drop(idx_del)
     
     df_total_2.to_csv(path_or_buf='데이터가공_사망자수_합계.csv', sep=',', header=True, index=False, mode='w', encoding='CP949')
     
     
     # 필요 없는 열 삭제
     del df['기타불명']
     # 막대 그래프에서는 자치구가 합계인 행 필요 없으므로 삭제
     idx_del = df[df['자치구']=='합계'].index
     df = df.drop(idx_del)
     # 막대 그래프에서 사망자 수만 필요하므로 구분이 부상자수인 행 삭제
     idx_del = df[df['구분']=='부상자수'].index
     df = df.drop(idx_del)

     # '-'가 존재하는 열만 '-'를 0으로 변경
     df['합계'] = np.where(df['합계'] == "-", 0, df['합계'])
     df['5년 미만'] = np.where(df['5년 미만'] == "-", 0, df['5년 미만'])
     df['10년 미만'] = np.where(df['10년 미만'] == "-", 0, df['10년 미만'])
     df['15년 미만'] = np.where(df['15년 미만'] == "-", 0, df['15년 미만'])
     df['15년 이상'] = np.where(df['15년 이상'] == "-", 0, df['15년 이상'])

     # (2012~2018)년도 별 csv파일 생성
     for index in range(2012, 2019):
          df_years = df[df['기간'] == '%d' %index]
          df_years.to_csv(path_or_buf='데이터가공_%d.csv' %index, sep=',', header=True, index=False, mode='w', encoding='CP949')


def main():
     # 데이터 가공 
     dataProcessing()

     # 1. 연도 별 면허 소지 기간에 따른 총 발생건 수 비교 꺾은 선 그래프
     # 2. 연도, 자치구 별 면허 소지 기간에 따른 발생건수 및 사망건수 막대 그래프 및 파이 그래프
     dataVisualization()

     

def dataVisualization():
     font_name = mpl.font_manager.FontProperties(fname='C:/Windows/Fonts/malgun.ttf').get_name()
     mpl.rc('font', family=font_name)
     
     df = pd.read_csv('데이터가공_발생건수_합계.csv', engine='c', dtype=str, sep=',', encoding='CP949')     
     df_dead = pd.read_csv('데이터가공_사망자수_합계.csv', engine='c', dtype=str, sep=',', encoding='CP949')

     # 연도 별 발생건수 합계를 리스트로 저장
     data_1 = df['5년 미만']
     data_2 = df['10년 미만']
     data_3 = df['15년 미만']
     data_4 = df['15년 이상']
     data_5 = df['기타불명']
     data_year = df['기간']

     # 연도 별 사망자수 합계를 리스트로 저장
     data_1_dead = df_dead['5년 미만']
     data_2_dead = df_dead['10년 미만']
     data_3_dead = df_dead['15년 미만']
     data_4_dead = df_dead['15년 이상']
     data_5_dead = df_dead['기타불명']
     
     total_1 = []
     total_2 = []
     total_3 = []
     total_4 = []
     total_5 = []
     total_1_dead = []
     total_2_dead = []
     total_3_dead = []
     total_4_dead = []
     total_5_dead = []
     year = []
     
     for idx in range(len(data_year)):
          year.append(str(data_year[idx]))
          total_1.append(int(data_1[idx]))
          total_2.append(int(data_2[idx]))
          total_3.append(int(data_3[idx]))
          total_4.append(int(data_4[idx]))
          total_5.append(int(data_5[idx]))
          total_1_dead.append(int(data_1_dead[idx]))
          total_2_dead.append(int(data_2_dead[idx]))
          total_3_dead.append(int(data_3_dead[idx]))
          total_4_dead.append(int(data_4_dead[idx]))
          total_5_dead.append(int(data_5_dead[idx]))


     # 1. 연도 별 면허 소지 기간에 따른 총 발생건 수 비교 꺾은 선 그래프 그리기
     fig = pylab.figure(figsize=(12, 8))
     ax = fig.add_subplot(1, 1, 1)
     ax.plot(year, total_1, marker='o')
     ax.plot(year, total_2, marker='o')
     ax.plot(year, total_3, marker='o')
     ax.plot(year, total_4, marker='o')
     ax.plot(year, total_5, marker='o')
     
     ax.set_xlabel('연도')
     ax.set_ylabel('발생건수')
     
     ax.legend(['5년 미만', '10년 미만', '15년 미만', '15년 이상', '기타 불명'])
     plt.title('(2012-2018) 연도 별 면허 소지 기간에 따른 총 발생건 수 비교')
     plt.savefig('(2012-2018)년 비교 시각화.png')
          


     
     # 2. 연도, 자치구 별 면허 소지 기간에 따른 발생건수 및 사망건수 막대 그래프
     for year in range(2012, 2019):
          df = pd.read_csv('데이터가공_%d.csv' %year, engine='c', dtype=str, sep=',', encoding='CP949')
          df2 = df.drop_duplicates(['자치구'])
          
          # x축으로 사용될 ['자치구']를 list로 저장 - 중복 제거
          gu = df2['자치구']
          
          # 중복제거로 인해 인덱스가 맞지 않아 다시 list로 저장해준다.
          X_name = []
          for idx in range(0,len(gu)):
               X_name.append(gu[idx*2])

          # 5년 미만의 값을 가져옴
          data_1 = df['5년 미만']
          data_1_top = []
          data_1_bottom = []
          for idx in range(0,len(data_1)):
               if idx%2==0:
                    data_1_top.append(int(data_1[idx]))
               else:
                    data_1_bottom.append(int(data_1[idx]))
          
          # 10년 미만의 값을 가져옴
          data_2 = df['10년 미만']
          data_2_top = []
          data_2_bottom = []
          for idx in range(0,len(data_2)):
               if idx%2==0:
                    data_2_top.append(int(data_2[idx]))
               else:
                    data_2_bottom.append(int(data_2[idx]))
                    
          # 15년 미만의 값을 가져옴
          data_3 = df['15년 미만']
          data_3_top = []
          data_3_bottom = []
          for idx in range(0,len(data_3)):
               if idx%2==0:
                    data_3_top.append(int(data_3[idx]))
               else:
                    data_3_bottom.append(int(data_3[idx]))
                    
          # 15년 이상의 값을 가져옴
          data_4 = df['15년 이상']
          data_4_top = []
          data_4_bottom = []
          for idx in range(0,len(data_4)):
               if idx%2==0:
                    data_4_top.append(int(data_4[idx]))
               else:
                    data_4_bottom.append(int(data_4[idx]))

          # 자치구 별 총 발생건 수
          data_top_list = [data_1_top, data_2_top, data_3_top, data_4_top]

          # 자치구 별 사망자 수
          data_bottom_list = [data_1_bottom, data_2_bottom, data_3_bottom, data_4_bottom]

          n_group = len(X_name)
          index = np.arange(n_group)
          bar_width = 0.15

          # figure 사이즈
          fig = pylab.figure(figsize=(18, 10))
          # 그래프 위치 선정
          ax = fig.add_subplot(2, 1, 1)

          # 다중 누적 그래프를 위한 for문          
          for idx, i in enumerate(data_bottom_list):
               pos = index + bar_width*idx
               plt.bar(pos, i, bar_width, tick_label=X_name, align='center')
               plt.bar(pos, data_top_list[idx], bar_width, bottom=i, tick_label=X_name, align='center')
               

          plt.title('[ %d ] 년 자치구별 면허 소지 기간에 따른 사고 발생건수, 사망자수 비교' %year)
          plt.grid(color='gray', linewidth=0.5, linestyle="--", b=True, which='both', axis='y')
          plt.ylabel('발생건수')
          plt.xlabel('서울 자치구')
          plt.legend(['5년미만-사망자수','5년미만-발생건수','10년미만-사망자수','10년미만-발생건수','15년미만-사망자수','15년미만-발생건수','15년이상-사망자수','15년이상-발생건수'])


          labels = ['5년미만', '10년미만', '15년미만', '15년이상', '기타불명']

          # 연도 별 면허 소지 기간에 따른 발생 건수를 퍼센트로 나타내기 위해 파이차트 사용
          ax2 = fig.add_subplot(2, 2, 3)
          # 데이터 비율에 따라 파이 그래프를 그린다.
          plt.pie([total_1[year-2012], total_2[year-2012], total_3[year-2012], total_4[year-2012], total_5[year-2012]], labels = labels, autopct='%1.1f%%', shadow=True, startangle=90)
          plt.title('[ %d ] 년 면허 소지 기간에 따른 발생 건수 비교' %year)
          
          # 연도 별 면허 소지 기간에 따른 사망자수를 퍼센트로 나타내기 위해 파이차트 사용
          ax3 = fig.add_subplot(2, 2, 4)
          # 데이터 비율에 따라 파이 그래프를 그린다.
          plt.pie([total_1_dead[year-2012], total_2_dead[year-2012], total_3_dead[year-2012], total_4_dead[year-2012], total_5_dead[year-2012]], labels = labels, autopct='%1.1f%%', shadow=True, startangle=90)
          plt.title('[ %d ] 년 면허 소지 기간에 따른 사망자수 비교' %year)

          plt.suptitle('%d년 분석' %year)
          plt.savefig('%d년 시각화.png' %year)
          
     plt.show()

     
if __name__ == '__main__':
     main()
