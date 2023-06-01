import streamlit as st
import openai
import pandas as pd
import numpy as np
import altair as alt
import requests
import json

st.title("LawChat")
api_key = st.secrets['api_key']
openai.api_key = ''

with st.form("form"):
    lawchat_id= st.text_input("LawChat ID를 입력하세요")
    user_input = st.text_input ("질문을 입력하세요")
    submit = st.form_submit_button("gpt-4에게 임베딩 기반 질문하기")
    gpt3submit = st.form_submit_button("gpt-3.5에게 질문하기")
    gpt4submit = st.form_submit_button("gpt-4에게 질문하기")
    searchSubmit = st.form_submit_button("Semantic search검색")

if searchSubmit and user_input:
    with st.spinner('유사 문서 검색 중...'):
        gpt_response = requests.get(
            "http://localhost:8000/embedding-search",
            json={'prompt' : user_input, 'top_k' : 5}
        )

    if gpt_response.status_code == 200:
        response_data = gpt_response.json()  # Assuming the response is in JSON format
        for i, meta in enumerate(response_data['meta_data']):
            st.write(f"Semantic search score #{i+1} {meta['score']}\n---\n[{meta['제목']}]({meta['url']})\n\n[질문]{meta['질문']}\n\n[답변]{meta['답변']}")
    else:
        st.error("Failed to retrieve code. Please try again.")

if gpt3submit and user_input :
    openai.api_key = api_key
    gpt_prompt =[{
        'role':'system',
        'content': '당신은 대한민국 법을 학습한 유능한 AI이다'
        }, {
            'role':'user',
            'content':user_input
        }
    ]

    with st.spinner('gpt-3.5 답변 준비중...'):
        gpt_response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=gpt_prompt
        )

    prompt = gpt_response['choices'][0]['message']['content']
    st.write({prompt})


if gpt4submit and user_input :
    openai.api_key = api_key
    gpt_prompt =[{
        'role':'system',
        'content': '당신은 대한민국 법을 학습한 유능한 AI이다'
        }, {
            'role':'user',
            'content':user_input
        }
    ]

    with st.spinner('gpt-4 답변 준비중...'):
        gpt_response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=gpt_prompt
        )

    prompt = gpt_response['choices'][0]['message']['content']
    st.write({prompt})


if submit and lawchat_id=='n' and user_input :
    # with st.spinner('법률 질문 여부 준비중...'):

    with st.spinner('답변 준비중...'):
        gpt_response = requests.post(
            "http://localhost:8000/generate",
            json={'prompt' : user_input, "based_on_semantic_search" : True, 'top_k' : 5}
        )

    if gpt_response.status_code == 200:
        response_data = gpt_response.json()  # Assuming the response is in JSON format
        st.write(response_data['code'])
        for i, meta in enumerate(response_data['meta_data']):
            st.write(f"Semantic search score #{i+1} {meta['score']}\n---\n[{meta['제목']}]({meta['url']})")
    else:
        st.error("Failed to retrieve code. Please try again.")



    st.write(1234)
    data_frame = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40],
    })

    st.write('1 + 1 = ', 2)
    st.write('Below is a DataFrame:', data_frame, 'Above is a dataframe.')

    df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

    c = alt.Chart(df).mark_circle().encode(
        x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

    st.write(c)

else :
    st.write('ID와 질문을 확인하세요')