import joblib
import re
import underthesea
import streamlit as st

def lower_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    tokens = underthesea.word_tokenize(text)
    return tokens

def remove_stopword(tokens):
    with open("Model/vietnamese-stopwords.txt","r",encoding="utf-8") as file:
        stopwords = file.readlines()
    stopwords = [word.strip() for word in stopwords]
    final_tokens = [token for token in tokens if token not in stopwords]
    final_text = ' '.join(final_tokens)
    return final_text

def run():
    tfidf_vectorizer,MultiNB,encoder=joblib.load('Model/model.joblib')
    st.set_page_config(page_title="Hệ thống phân loại văn bản")

    st.write("# Hệ thống phân loại văn bản")
    
    sentence = st.text_area('Nhập văn bản:')
    if st.button('Submit', type='primary') and sentence:
        sentence=remove_stopword(lower_tokenize(sentence))
        vector_sentence = tfidf_vectorizer.transform([sentence])
        final_sentence=MultiNB.predict(vector_sentence)[0]
        final_sentence=encoder.inverse_transform([final_sentence])[0]
        st.title(f'Với văn bản trên, thể loại của văn bản sẽ thuộc: {final_sentence}')


if __name__ == "__main__":
    run()