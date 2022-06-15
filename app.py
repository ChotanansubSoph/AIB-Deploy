from cgi import test
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time

import random 

import tensorflow as tf 
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import transformers


from io import StringIO

from assets.module import LSTM_PP
from assets.module import WangChan_PP

#Load Model and Tokenizer 
@st.cache(allow_output_mutation=True,show_spinner=False,ttl=1800,max_entries=10)
def load_model_lstm(): return LSTM_PP.load_LSTM()

@st.cache(allow_output_mutation=True,show_spinner=False,ttl=1800,max_entries=10)
def load_model_wangchan(): return WangChan_PP.load_wangchan()

@st.cache(hash_funcs={transformers.models.gpt2.tokenization_gpt2_fast.GPT2TokenizerFast: hash},
                    allow_output_mutation=True,
                    show_spinner=False,
                    ttl=1800,
                    max_entries=10)
def load_wangchan_tokenizer(): return WangChan_PP.load_wangchan_tokenizer()

#Set up 

samepleList = [
    'ประชาธิปไตย (อังกฤษ: democracy) เป็นระบอบการปกครองแบบหนึ่งซึ่งพลเมืองเป็นเจ้าของอำนาจอธิปไตยและเลือกผู้ปกครองซึ่งทำหน้าที่ออกกฎหมาย โดยพลเมืองอาจใช้อำนาจของตนด้วยตนเองหรือผ่านผู้แทนที่เลือกไปใช้อำนาจแทนก็ได้ การตัดสินว่าผู้ใดเป็นพลเมืองบ้างและการแบ่งปันอำนาจในหมู่พลเมืองเป็นอย่างไรนั้นมีการเปลี่ยนแปลงตามเวลาและแต่ละประเทศเปลี่ยนแปลงในอัตราไม่เท่ากัน นอกจากการเลือกตั้งแล้ว ความคิดที่เป็นรากฐานของประชาธิปไตย ได้แก่ เสรีภาพในการชุมนุมและการพูด การไม่แบ่งแยกและความเสมอภาค สิทธิพลเมือง ความยินยอม สิทธิในการมีชีวิตและสิทธิฝ่ายข้างน้อย นอกจากนี้ ประชาธิปไตยยังทำให้ทุกฝ่ายตระหนักถึงผลประโยชน์ของตนและแบ่งอำนาจจากกลุ่มคนมาเป็นชุดกฎเกณฑ์แทน',
    "ปอบเป็นอวิชชาตามตำนานเล่าว่า ผีปอบ คือ ผีสายยักษ์ อยู่ในสายการปกครอง ของท้าวเวสวัณ ที่เข้าสิงร่างมนุษย์ ก็เพื่ออาศัยร่างมนุษย์กินอาหาร โดยเฉพาะอาหารสดคาว หรือ สัตว์เป็นๆ เช่น ไปหักคอเป็ด ไก่ ในเล้ากิน หรืออาศัยร่าง เหมือนเป็นร่างทรง จะเข้าสิงร่างมนุษย์ที่มีวิบากกรรมทางนี้ คือ อดีตเคยนับถือผีเป็นที่พึ่ง ที่ระลึกยามมีทุกข์ จนเป็นประเพณีธรรมเนียมปฏิบัติสืบต่อกันมา มีจิตผูกพันกับผี และกรรมทำปาณาติบาต ฆ่าสัตว์เซ่นไหว้ผี บางทีก็ฆ่าสัตว์เล็ก เช่น เป็ด ไก่ บางทีก็ฆ่าสัตว์ใหญ่ เช่น วัว ควาย เป็นต้น ผู้ที่ถูกปอบเข้าสิง จะมีอาการเปลี่ยนไป เป็นดุร้าย รำพึงรำพันต่าง ๆ นานา จดจำบุคคลคุ้นเคยหรือคนในครอบครัว ไม่ได้หรือไม่กินก็อาหารดิบ ๆ สุก ๆ ที่เท่าไหร่ก็ไม่อิ่ม วิธีการปราบผีปอบต้องใช้หมอผีหรือวิธีทางไสยศาสตร์ ในภาคอีสาน จะมีการทำพิธีจับผีปอบเป็นพิธีใหญ่ โดยหมอผีจะไล่จับผีปอบตามที่ต่าง ๆ โดยใช้อุปกรณ์อย่างหนึ่ง ที่เป็นเครื่องสาน เรียก โมงข้อใช้สำหรับกักขังปอบ",
    "ผลผลิตทางเศรษฐกิจมหภาคมักถูกวัดโดยผลิตภัณฑ์มวลรวมภายในประเทศ (จีดีพี) หรือสิ่งใดสิ่งหนึ่งในบัญชีประชาชาติ เศรษฐกรผู้ที่สนใจในการเพิ่มขึ้นในระยะยาวศึกษาการเจริญเติบโตทางเศรษฐกิจ ความก้าวหน้าทางเทคโนโลยี การสะสมเครื่องจักรและทุนอื่นๆ และการมีการศึกษาและทุนมนุษย์ที่ดีขึ้นเป็นปัจจัยที่ทำให้เกิดการเพิ่มขึ้นในผลผลิตทางเศรษฐกิจตลอดช่วงเวลา อย่างไรก็ดี ผลผลิตไม่จำเป็นจะต้องเพิ่มขึ้นอย่างคนเส้นคนวาตลอดเวลา วัฏจักรธุรกิจสามารถก่อให้เกิดการลดลงในระยะสั้นที่เราเรียกว่าภาวะเศรษฐกิจถดถอย เศรษฐกรมองหานโยบายทางเศรษฐศาสตร์มหาภคที่ป้องกันเศรษฐกิจไม่ให้เข้าสู้ภาวะถดถอยและทำให้การเจริญเติบโตในระยะยาวเร็วมากขึ้น",
    "การกระเจิง (อังกฤษ: scattering) เป็นกระบวนการทางฟิสิกส์ทั่วไปอย่างหนึ่งที่บางรูปแบบของการฉายรังสี เช่น แสง เสียง หรืออนุภาคที่เคลื่อนที่ได้ ถูกบังคับให้เบี่ยงเบนไปจากวิถีทางตรงไปหนึ่งเส้นทางหรือมากกว่าหนึ่งเส้นทางเนื่องจากการไม่สม่ำเสมอ (non-uniformities) ในตัวกลางที่พวกมันเดินทางผ่านไป ในการใช้งานทั่วไป การกระเจิงนี้รวมถึงการเบี่ยงเบนของรังสีที่สะท้อนจากมุมที่คาดการณ์ไว้ตามกฎของการสะท้อน การสะท้อนที่มีการกระเจิงมักจะถูกเรียกว่าการสะท้อนกระเจิงและการสะท้อนที่ไม่กระเจิงจะถูกเรียกว่าการสะท้อนเหมือนกระจก"
    ]
placeholder = random.choice(samepleList)

AIBlogo_image = Image.open('assets/img/AIBlogo.png')
book_image = Image.open('assets/img/book.jpg')

DOMAIN_LIST = ['วิทยาศาสตร์ประยุกต์🔬',
               'ศิลปกรรม🖌️',
               'ความเชื่อ🙏🏼',
               'การเงิน และ พาณิชย์ 💵',
               'ประวัติศาสตร์🔎',
               'จินตนาการ🔮',
               'ธรรมชาติ และ วิทยาศาสตร์บริสุทธิ์🌱',
               'สังคมวิทยา📚', ]

with st.sidebar:
    st.image(AIBlogo_image,width=100)

    st.header("🖥️เกี่ยวกับโปรเจคนี้")
    st.write("โปรเจคนี้จัดทำขึ้นภายใต้กิจกรรมในโครงการ [AI Builder 2022](https://ai-builders.github.io/) โดยได้จักทำขึ้นเพื่อทำนายแวดวงของเอกสารบทความภาษาไทย สามารถต่อยอดในการจัดทำระบบกำกับแวดวงเอกสารแบบอัตนโนมัติได้ โดยแบบจำลองในโปรเจคนี้ ได้เลือกใช้แบบจำลอง [WangChanBERTa](https://airesearch.in.th/releases/wangchanberta-pre-trained-thai-language-model/) และ LSTM แบบจำลองถูกเทรนด้วยข้อมูลบทความจาก [Thai National Corpus](https://www.arts.chula.ac.th/ling/tnc/) จำนวน 49,153 บทความ ",unsafe_allow_html=True)
    
    st.header("🌐แหล่งอ้างอิง")
    st.write("ชุดข้อมูลบทความ จาก TNC : THAI NATIONAL CORPUS (Third Edition) ในพระราชูปถัมภ์สมเด็จพระเทพรัตนราชสุดาฯ สยามบรมราชกุมารี ภาควิชาภาษาศาสตร์ คณะอักษรศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย [ข้อมูลเพิ่มเติม](https://www.arts.chula.ac.th/ling/tnc/)")



st.header('ระบบจำแนกแวดวงเอกสารภาษาไทย📔🔍')


with open("assets/webfonts/font.txt") as f:
    st.markdown(f.read(),unsafe_allow_html=True)
with open("assets/css/style.css") as f:
    st.markdown(f"<style> {f.read()} </style>",unsafe_allow_html=True)
hide_table_index = """
            <style>         
            thead {display:none}  
            tbody th {display:none}
            .blank {display:none}
            </style>
            """ 
st.markdown(hide_table_index, unsafe_allow_html=True)





st.image(book_image)
#<a href='https://www.freepik.com/photos/library-books'>Library books photo created by jcomp - www.freepik.com</a>




left_col, right_col = st.columns(2)

with left_col:
    isDataComplete = False
    #Input Method Selection
    st.subheader("1. ปรับแต่งข้อมูลนำเข้า⚙️")
    input_option = st.selectbox(
                    "🔸 1.1 เลือกช่องทางการรับข้อความ📝",
                    ("พิมพ์ข้อความ⌨️","อัพโหลดไฟล์📤 "))

    st.info(f'🔹สถานะ: คุณได้เลือก {input_option}')

    if input_option == "พิมพ์ข้อความ⌨️":
        input_text = st.text_area("🔸 1.2 กรอกข้อความ⌨️",
                placeholder,
                max_chars=5000)

    else:
        input_text = None
        uploaded_file = st.file_uploader("🔸 1.2 อัพโหลดไฟล์ (นามสกุล txt.)")
        if uploaded_file != None:
            if uploaded_file.type == "text/plain":
                #st.write("yeh it's text file!")

                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                input_text = stringio.read()

            # elif uploaded_file.type == "text/csv":
            #     st.write("boom it's csv!") 
                

    #Model Selection     
    model_option = st.selectbox(
                    "🔸 1.3 เลือกแบบจำลอง(Model)🤖",
                    ("WangChanBERTa (แนะนำ🔥)","Long short-term memory (LSTM)"))
    if model_option == "WangChanBERTa (แนะนำ🔥)":
        selected_model = "WangChanBERTa"
    else:
        selected_model = "Long short-term memory (LSTM)"
    st.info(f'🔹สถานะ: คุณได้เลือกแบบจำลอง: {selected_model}')

    #Accept Button
    button = st.button('ตกลง')
    if button:
        if input_text == None:
            alert_left = "กรุณาอัพโหลดไฟล์⚠️"
        elif input_text == "":
            alert_left = "กรณุกรอกข้อความ⚠️"
        else:
            alert_left = "ข้อมูลพร้อมต่อการประมวลผล✅"
            isDataComplete = True
        if isDataComplete != True:
            st.warning(alert_left)
        st.info(f"🔹สถานะ: {alert_left}",)

        placeholder = input_text


with right_col: 
    st.subheader("2. ผลลัพธ์การประมวลผล 👩🏻‍💻")
    if button and isDataComplete:
        

        started_load_time = time.time()
        
        with st.spinner(text='กำลังจัดเตรียมแบบจำลอง⌛️ (อาจใช้เวลาในครั้งแรก ไม่เกิน30วินาที)'):
            progress_bar = st.progress(0)
            lstm_model = load_model_lstm()
            progress_bar.progress(30)
            wangchan_model = load_model_wangchan()
            progress_bar.progress(60)
            wangchan_tokenizer = load_wangchan_tokenizer()
            progress_bar.progress(100)

        finished_load_time = time.time()
        loadModelTime = finished_load_time - started_load_time
        st.info("จัดเตรียมแบบจำลอง✅ (เวลาที่ใช้ {:.2f} วินาที)".format(loadModelTime))


        with st.spinner(text='กำลังประมวลผล⌛️'):
            

            started_time = time.time()
            if selected_model == "Long short-term memory (LSTM)":
                domainIndex, domainProb = LSTM_PP.all_preprocessing(input_text[:1500],lstm_model)
                predicted_domain = DOMAIN_LIST[domainIndex]
            else:
                domainIndex, domainProb = WangChan_PP.all_preprocessing(input_text[:1500],wangchan_model,wangchan_tokenizer)
                predicted_domain = DOMAIN_LIST[domainIndex]

            finished_time = time.time()
            processingTime = finished_time - started_time

            st.info("ประมวลผลเสร็จสิ้น✅ (เวลาที่ใช้ {:.2f} วินาที)".format(processingTime))
            lst = [['แบบจำลอง(Model)🤖',selected_model],
                   ['เวลาที่ใช้ในการประมวลผล⌛️', "{:.2f} วินาที".format(processingTime)],
                   ['ข้อความ📃',input_text],
                   ['ผลการทำนายแวดวง📌', predicted_domain],
                   ['ความใกล้เคียง📊', "{:.2f}%".format(domainProb*100)]
                  ]
            vizDF = pd.DataFrame(lst)
            st.table(vizDF)
            st.balloons()
            placeholder = input_text
            
    else:
        st.write("กรุณาปรับแต่งข้อมูลนำเข้าเพื่อประมวลผล💡")