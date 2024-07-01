import pandas as pd
import warnings
import matplotlib.pyplot as plt
import streamlit as st

warnings.filterwarnings('ignore')


def get_exchange_rate_data(code,currency_name):
    df = pd.DataFrame()
    for page_num in range(1,6) :
        
        base_url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"
        temp = pd.read_html(base_url, encoding='cp949', header=1)
        
        df = pd.concat([df,temp[0]])
    
    total_rate_data_view(df,code,currency_name)


def total_rate_data_view(df,code,currency_name):
    plt.rc('font',family='Malgun Gothic')
    #원하는 열만 선택
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

    #데이터 표시
    #print(f"==={currency_name[code_in]}-{code}******")
    st.subheader(f"{currency_name} : {code}")
    #print(df_total.head(20))
    st.dataframe(df_total.head(20))


    # 차트작성과정
    df_total_chart = df_total.copy()
    df_total_chart = df_total_chart.set_index('날짜')
    #최신 데이터와 과거 데이터 순서를 바꿈,  역순으로 표시
    df_total_chart = df_total_chart[::-1]
    ax =df_total_chart['매매기준율'].plot(figsize=(15,6), title='환율')
    fig = ax.get_figure()
    st.pyplot(fig)
    
    # month_rate_data_veiw(df_total)



def month_rate_data_veiw(df_total):
    #월별 검색
    # 날짜 열 형변환(문자열 -> 날짜형식)
    df_total['날짜'] = df_total['날짜'].str.replace(".","").astype('datetime64[ms]')

    # '월' 파생변수 생성
    df_total['월'] = df_total['날짜'].dt.month
    month_in = int(input("검색할 월 입력 : "))
    month_df = df_total.loc[df_total['월'] ==month_in,['날짜', '매매기준율', '파실 때', '보내실 때', '받으실 때']]
    month_df.reset_index(drop=True)
    month_df_chart = month_df.copy()
    month_df_chart[::-1].reset_index(drop=True)
    month_df_chart =month_df_chart.set_index('날짜')
    month_df_chart['매매기준율'].plot(figsize=(15,6), title=f'{month_in}월 환율')
    plt.show()


def exchange_main() :
    currency_symbols_name = {'미국 달러':'USD','유럽연합 유로':'EUR','일본 엔':'JPY'}
    
    currency_name = st.selectbox('통화 선택',currency_symbols_name.keys())
    code = currency_symbols_name[currency_name]
    clicked = st.button("환율 데이터 가져오기")
    if clicked:
        get_exchange_rate_data(code,currency_name)
        
        
if __name__=="__main__":
    exchange_main()