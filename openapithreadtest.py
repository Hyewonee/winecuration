from dotenv import load_dotenv
import os
import openai
import httpx

# Load environment variables
load_dotenv()
API_KEY = os.environ.get('OPEN_API_KEY')
# Create a custom httpx client with SSL verification disabled
httpx_client = httpx.Client(verify=False)
client = openai.OpenAI(api_key=API_KEY, http_client=httpx_client)

def createThread():
    # Create the OpenAI client with the custom httpx client
    empty_thread = client.beta.threads.create()
    print(empty_thread)
    # id='thread_E6eVIAPvsJJmEyPGErcoAPfV'

def createAssistant():
    my_assistant = client.beta.assistants.create(
        instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        name="Math Tutor",
        tools=[],
        model="gpt-4-turbo",
    )
    print(my_assistant)
    # id='asst_FfGnTTxgONacIvmkQ9VDAris'

def createMessege():
    thread_message = client.beta.threads.messages.create(
        "thread_E6eVIAPvsJJmEyPGErcoAPfV",
        role="assistant",
        content='''밑의 규칙에 따라
            [AY) 캔달잭슨 그랑리저브 카베르네쇼비뇽]에 대한 소개 멘트를 생성해줘. 규칙에 따라 차례로 서술해줘.\n        0. 맨 윗줄은 와인 이름을 표기한다.\n        1. 와인이 생산 된 국가를 표기한다.\n        2. 와인 소개 멘트는 와인에 어울리는 음식 페어링을 포함한다. 음식 종류는 3가지를 넘지 않도록 한다.\n        ex) 와인에 알맞는 음식 : 치즈, 김치, 김\n        3. 와인의 산미를 Start rating으로 표시한다. 최대 별점은 별 3개로 표시한다. 별은 반개단위로도 제공한다. ☆는 별 반개를 의미한다. ex) 산미 : ★★\n        4. 와인의 당도를 Start rating으로 표시한다. 최대 별점은 별 3개로
            표시한다. 별은 반개단위로도 제공한다.\n        ex) 당도 : ★★☆\n        5. 1 ~ 3 밑에 와인의 상세 정보를 시적인 느낌을 담아 표시한다. 상세 정보는 맛에 대한 생생한 느낌을 담는다. 와인의 역사
            나 특징을 담아도 좋다.\n        ex) 미네랄 베이스의 생생한 산도, 감미로운 이스트 풍미, 깨끗하면서도 과일 향 여운이 남는 피니쉬\n\n        최종 예시 : \n        꼬끼예뜨 레 끌레 브뤼 그랑 크
            뤼\n        원산지 : 일본\n        와인에 알맞는 음식 : 치즈, 김치, 김\n        산미 : ★★☆\n        당도 : ★★\n        크리미하고 피노누와의 순수함이 잘 느껴지는 입안을 감싸는 풍미, 긴장감 
            을 바탕으로 하는 롱피니쉬'''
    )
    print(thread_message)
    # id='msg_4SSRfnacDzDMtI7Pe6of3HTE'

def createRun():
    run = client.beta.threads.runs.create(
        thread_id="thread_E6eVIAPvsJJmEyPGErcoAPfV",
        assistant_id="asst_FfGnTTxgONacIvmkQ9VDAris"
    )
    print(run)
    # id='run_UQf2eMOSd6wnhas6mGY2GL1u'

def checkMessege():
    messege = client.beta.threads.messages.list(
        thread_id='thread_E6eVIAPvsJJmEyPGErcoAPfV'
    )
    for i in messege:
        print(i)

# createAssistant()
# createThread()
# createMessege()
# createRun()
checkMessege()
