### 모듈 임포트 ###
import websockets
import json
import requests
import os
import asyncio
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

key_bytes = 32


### 함수 정의 ###

# AES256 DECODE
def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))


def get_approval(key, secret):
    """웹소켓 접속키 발급"""
    url = 'https://openapi.koreainvestment.com:9443'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key


# 주식체결 출력라이브러리
def stockhoka_domestic(data):
    """ 넘겨받는데이터가 정상인지 확인
    print("stockhoka[%s]"%(data))
    """
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("유가증권 단축 종목코드 [" + recvvalue[0] + "]")
    print("영업시간 [" + recvvalue[1] + "]" + "시간구분코드 [" + recvvalue[2] + "]")
    print("======================================")
    print("매도호가10 [%s]    잔량10 [%s]" % (recvvalue[12], recvvalue[32]))
    print("매도호가09 [%s]    잔량09 [%s]" % (recvvalue[11], recvvalue[31]))
    print("매도호가08 [%s]    잔량08 [%s]" % (recvvalue[10], recvvalue[30]))
    print("매도호가07 [%s]    잔량07 [%s]" % (recvvalue[9], recvvalue[29]))
    print("매도호가06 [%s]    잔량06 [%s]" % (recvvalue[8], recvvalue[28]))
    print("매도호가05 [%s]    잔량05 [%s]" % (recvvalue[7], recvvalue[27]))
    print("매도호가04 [%s]    잔량04 [%s]" % (recvvalue[6], recvvalue[26]))
    print("매도호가03 [%s]    잔량03 [%s]" % (recvvalue[5], recvvalue[25]))
    print("매도호가02 [%s]    잔량02 [%s]" % (recvvalue[4], recvvalue[24]))
    print("매도호가01 [%s]    잔량01 [%s]" % (recvvalue[3], recvvalue[23]))
    print("--------------------------------------")
    print("매수호가01 [%s]    잔량01 [%s]" % (recvvalue[13], recvvalue[33]))
    print("매수호가02 [%s]    잔량02 [%s]" % (recvvalue[14], recvvalue[34]))
    print("매수호가03 [%s]    잔량03 [%s]" % (recvvalue[15], recvvalue[35]))
    print("매수호가04 [%s]    잔량04 [%s]" % (recvvalue[16], recvvalue[36]))
    print("매수호가05 [%s]    잔량05 [%s]" % (recvvalue[17], recvvalue[37]))
    print("매수호가06 [%s]    잔량06 [%s]" % (recvvalue[18], recvvalue[38]))
    print("매수호가07 [%s]    잔량07 [%s]" % (recvvalue[19], recvvalue[39]))
    print("매수호가08 [%s]    잔량08 [%s]" % (recvvalue[20], recvvalue[40]))
    print("매수호가09 [%s]    잔량09 [%s]" % (recvvalue[21], recvvalue[41]))
    print("매수호가10 [%s]    잔량10 [%s]" % (recvvalue[22], recvvalue[42]))
    print("======================================")
    print("총매도호가 잔량        [%s]" % (recvvalue[43]))
    print("총매도호가 잔량 증감   [%s]" % (recvvalue[54]))
    print("총매수호가 잔량        [%s]" % (recvvalue[44]))
    print("총매수호가 잔량 증감   [%s]" % (recvvalue[55]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[45]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[46]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[56]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[57]))
    print("예상 체결가            [%s]" % (recvvalue[47]))
    print("예상 체결량            [%s]" % (recvvalue[48]))
    print("예상 거래량            [%s]" % (recvvalue[49]))
    print("예상체결 대비          [%s]" % (recvvalue[50]))
    print("부호                   [%s]" % (recvvalue[51]))
    print("예상체결 전일대비율    [%s]" % (recvvalue[52]))
    print("누적거래량             [%s]" % (recvvalue[53]))
    print("주식매매 구분코드      [%s]" % (recvvalue[58]))


# 해외주식체결 출력라이브러리
def stockhoka_overseas(data):
    """ 넘겨받는데이터가 정상인지 확인
    print("stockhoka[%s]"%(data))
    """
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("실시간종목코드 [" + recvvalue[0] + "]" + ", 종목코드 [" + recvvalue[1] + "]")
    print("소숫점자리수 [" + recvvalue[2] + "]")
    print("현지일자 [" + recvvalue[3] + "]" + ", 현지시간 [" + recvvalue[4] + "]")
    print("한국일자 [" + recvvalue[5] + "]" + ", 한국시간 [" + recvvalue[6] + "]")
    print("======================================")
    print("매수총 잔량        [%s]" % (recvvalue[7]))
    print("매수총잔량대비      [%s]" % (recvvalue[9]))
    print("매도총 잔량        [%s]" % (recvvalue[8]))
    print("매도총잔략대비      [%s]" % (recvvalue[10]))
    print("매수호가           [%s]" % (recvvalue[11]))
    print("매도호가           [%s]" % (recvvalue[12]))
    print("매수잔량           [%s]" % (recvvalue[13]))
    print("매도잔량           [%s]" % (recvvalue[14]))
    print("매수잔량대비        [%s]" % (recvvalue[15]))
    print("매도잔량대비        [%s]" % (recvvalue[16]))

    
# 국내주식체결처리 출력라이브러리
def stockspurchase_domestic(data_cnt, data):
    print("============================================")
    menulist = "유가증권단축종목코드|주식체결시간|주식현재가|전일대비부호|전일대비|전일대비율|가중평균주식가격|주식시가|주식최고가|주식최저가|매도호가1|매수호가1|체결거래량|누적거래량|누적거래대금|매도체결건수|매수체결건수|순매수체결건수|체결강도|총매도수량|총매수수량|체결구분|매수비율|전일거래량대비등락율|시가시간|시가대비구분|시가대비|최고가시간|고가대비구분|고가대비|최저가시간|저가대비구분|저가대비|영업일자|신장운영구분코드|거래정지여부|매도호가잔량|매수호가잔량|총매도호가잔량|총매수호가잔량|거래량회전율|전일동시간누적거래량|전일동시간누적거래량비율|시간구분코드|임의종료구분코드|정적VI발동기준가"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1

# 해외주식체결처리 출력라이브러리
def stockspurchase_overseas(data_cnt, data):
    print("============================================")
    menulist = "실시간종목코드|종목코드|수수점자리수|현지영업일자|현지일자|현지시간|한국일자|한국시간|시가|고가|저가|현재가|대비구분|전일대비|등락율|매수호가|매도호가|매수잔량|매도잔량|체결량|거래량|거래대금|매도체결량|매수체결량|체결강도|시장구분"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1

# 국내주식체결통보 출력라이브러리
def stocksigningnotice_domestic(data, key, iv):
    menulist = "고객ID|계좌번호|주문번호|원주문번호|매도매수구분|정정구분|주문종류|주문조건|주식단축종목코드|체결수량|체결단가|주식체결시간|거부여부|체결여부|접수여부|지점번호|주문수량|계좌명|체결종목명|신용구분|신용대출일자|체결종목명40|주문가격"
    menustr1 = menulist.split('|')

    # AES256 처리 단계
    aes_dec_str = aes_cbc_base64_dec(key, iv, data)
    pValue = aes_dec_str.split('^')

    i = 0
    for menu in menustr1:
        print("%s  [%s]" % (menu, pValue[i]))
        i += 1
            
# 해외주식체결통보 출력라이브러리
def stocksigningnotice_overseas(data, key, iv):
    menulist = "고객 ID|계좌번호|주문번호|원주문번호|매도매수구분|정정구분|주문종류2|주식단축종목코드|체결 수량|체결단가|주식체결시간|거부여부|체결여부|접수여부|지점번호|주문수량|계좌명|체결종목명|해외종목구분|담보유형코드|담보대출일자"
    menustr1 = menulist.split('|')

    # AES256 처리 단계
    aes_dec_str = aes_cbc_base64_dec(key, iv, data)
    pValue = aes_dec_str.split('^')

    i = 0
    for menu in menustr1:
        print("%s  [%s]" % (menu, pValue[i]))
        i += 1

        
### 웹소켓 연결 ###

async def connect():
    
    g_appkey = "앱키를 입력하세요"
    g_appsceret = "앱 시크릿키를 입력하세요" 
    g_approval_key = get_approval(g_appkey, g_appsceret)
    print("approval_key [%s]" % (g_approval_key))

    # url = 'ws://ops.koreainvestment.com:31000' # 모의투자계좌
    url = 'ws://ops.koreainvestment.com:21000' # 실전투자계좌

    # 원하는 호출을 [tr_type, tr_id, tr_key] 순서대로 리스트 만들기
    code_list = [['1','H0STASP0','005930'],['1','H0STCNT0','005930'],['1','H0STCNI0','HTS ID를 입력하세요'],
                 ['1','H0STASP0','DNASAAPL'],['1','HDFSCNT0','DNASAAPL'],['1','H0GSCNI0','HTS ID를 입력하세요']]
    
    senddata_list=[]
    
    for i,j,k in code_list:
        temp = '{"header":{"approval_key": "%s","custtype":"P","tr_type":"%s","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}'%(g_approval_key,i,j,k)
        senddata_list.append(temp)
        
    while True:
        
        async with websockets.connect(url, ping_interval=30) as websocket:

            for senddata in senddata_list:
                await websocket.send(senddata)
                time.sleep(0.5)
                print(f"Input Command is :{senddata}")

            while True:
                
                try:

                    data = await websocket.recv()
                    time.sleep(0.5)
                    # print(f"Recev Command is :{data}")

                    if data[0] == '0':
                        recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                        trid0 = recvstr[1]

                        if trid0 == "H0STASP0":  # 주식호가tr 일경우의 처리 단계
                            print("#### 주식호가 ####")
                            stockhoka_domestic(recvstr[3])
                            time.sleep(1)

                        elif trid0 == "H0STCNT0":  # 주식체결 데이터 처리
                            print("#### 주식체결 ####")
                            data_cnt = int(recvstr[2])  # 체결데이터 개수
                            stockspurchase_domestic(data_cnt, recvstr[3])

                        elif trid0 == "HDFSASP1":  # 해외주식호가tr 일경우의 처리 단계
                            print("#### 해외주식호가 ####")
                            stockhoka_overseas(recvstr[3])
                            time.sleep(1)

                        elif trid0 == "HDFSCNT0":  # 주식체결 데이터 처리
                            print("#### 해외주식체결 ####")
                            data_cnt = int(recvstr[2])  # 체결데이터 개수
                            stockspurchase_overseas(data_cnt, recvstr[3])

                    elif data[0] == '1':
                        recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                        trid0 = recvstr[1]

                        if trid0 == "K0STCNI0" or trid0 == "K0STCNI9" or trid0 == "H0STCNI0" or trid0 == "H0STCNI9":  # 주실체결 통보 처리
                            print("#### 주식체결통보 ####")
                            stocksigningnotice_domestic(recvstr[3], aes_key, aes_iv)

                        elif trid0 == "H0GSCNI0" or trid0 == "H0GSCNI9" or trid0 == "H0GSCNI0" or trid0 == "H0GSCNI9":  # 해외주실체결 통보 처리
                            print("#### 해외주식체결통보 ####")
                            stocksigningnotice_overseas(recvstr[3], aes_key, aes_iv)

                    else:

                        jsonObject = json.loads(data)
                        trid = jsonObject["header"]["tr_id"]

                        if trid != "PINGPONG":
                            rt_cd = jsonObject["body"]["rt_cd"]

                            if rt_cd == '1':  # 에러일 경우 처리
                                if jsonObject["body"]["msg1"] != 'ALREADY IN SUBSCRIBE':
                                    print("### ERROR RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))
                                break

                            elif rt_cd == '0':  # 정상일 경우 처리
                                print("### RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))

                                # 체결통보 처리를 위한 AES256 KEY, IV 처리 단계
                                if trid == "K0STCNI0" or trid == "K0STCNI9" or trid == "H0STCNI0" or trid == "H0STCNI9":
                                    aes_key = jsonObject["body"]["output"]["key"]
                                    aes_iv = jsonObject["body"]["output"]["iv"]
                                    print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))

                                elif trid == "H0GSCNI0" or trid == "H0GSCNI9" or trid == "H0GSCNI0" or trid == "H0GSCNI9":
                                    aes_key = jsonObject["body"]["output"]["key"]
                                    aes_iv = jsonObject["body"]["output"]["iv"]
                                    print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))

                        elif trid == "PINGPONG":
                            print("### RECV [PINGPONG] [%s]" % (data))
                            print("### SEND [PINGPONG] [%s]" % (data))
                            
                except:
                    print('Reconnecting...')
                    for senddata in senddata_list:
                        await websocket.send(senddata)
                        time.sleep(0.5)
                    
                    
# 비동기로 서버에 접속한다.
asyncio.get_event_loop().run_until_complete(connect())
asyncio.get_event_loop().close()