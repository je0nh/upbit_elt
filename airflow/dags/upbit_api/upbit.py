import requests

class Api:
    def call(self, quotation: str):
        """
        Args:
            quotation (str): upbit 요청 주소
        """
        url = 'https://api.upbit.com/v1/' + quotation
        headers = {"accept": "application/json"}
        return requests.get(url, headers=headers)
    
    def market_code(self, is_details='false') -> list:
        """Upbit 마켓 이름 출력
        
        Args:
            is_details (str): 유의종목 필드과 같은 상세 정보 노출 여부(선택 파라미터). Defaults to 'false'.
        """
        quotation = f'market/all?isDetails={is_details}'
        res = self.call(quotation)
        return res.json()
    
    def candles(self, type: str, market: str, unit=1, to='', count=1, convertingPriceUnit='KRW') -> list:
        """Upbit candle 출력

        Args:
            type (str): candle 종류. 가능한 값: 'minutes', 'days', 'weeks', 'months'.
            market (str): marker 코드. ex> KWR-BTC.
            unit (int): 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240. Defaults to 1.
            to (str): 마지막 캔들 시각 (exclusive). 비워서 요청시 가장 최근 캔들. Defaults to ''.
            count (int): 캔들 개수(최대 200개까지 요청 가능). Defaults to 1.
            convertingPriceUnit (str): 종가 환산 화폐 단위 (생략 가능, KRW로 명시할 시 원화 환산 가격을 반환.). Defaults to 'KRW'.
        """
        if type == 'minutes':
            quotation = f'candles/{type}/1?market={market}&unit={unit}&to={to}&count={count}&convertingPriceUnit={convertingPriceUnit}'
        elif type == 'days':
            quotation = f'candles/{type}/1?market={market}&to={to}&count={count}&convertingPriceUnit={convertingPriceUnit}'
        else:
            quotation = f'candles/{type}/1?market={market}&to={to}&count={count}'
        response = self.call(quotation)
        return response.json()
