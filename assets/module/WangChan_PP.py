from transformers import AutoTokenizer, AutoModelForSequenceClassification


def load_wangchan():
    # global WANGCHAN_TOKENIZER
    # WANGCHAN_TOKENIZER = AutoTokenizer.from_pretrained("CH0KUN/autotrain-TNC_Domain_WangchanBERTa-921730254")
    WANGCHAN_MODEL = AutoModelForSequenceClassification.from_pretrained("CH0KUN/autotrain-TNC_Domain_WangchanBERTa-921730254")
    return WANGCHAN_MODEL
    
def load_wangchan_tokenizer():
    global TOKENIZER
    TOKENIZER = AutoTokenizer.from_pretrained("CH0KUN/autotrain-TNC_Domain_WangchanBERTa-921730254")

def all_preprocessing(text,model):
    input =  TOKENIZER(text,return_tensors="pt")
    outputs =  model(**input)
    output_LST = outputs.logits.softmax(dim=-1).tolist()[0]
    domainProb = max(output_LST) 
    domainIndex = output_LST.index(domainProb)
    return domainIndex, domainProb

def is_tokenizer_ready():
    try: 
        TOKENIZER("สวัสดี",return_tensors="pt")
        return True
    except:
        return False
