import streamlit as st

from textblob import TextBlob

#import pdftotext

import spacy
from spacy import displacy

#import pt_core_news_sm


from PIL import Image

import pandas as pd

# Audio
from gtts import gTTS

from bokeh.models.widgets import Div

def get_value( my_key, my_dicts):
    for key, value in my_dicts.items():
        if my_key == key:
            return value

def get_key( my_value, my_dicts):
    for key, value in my_dicts.items():
        if my_value == value:
            return key

@st.cache
def lista_idiomas(idioma_original):
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        if idioma_original != df_idiomas.iloc[i,1]:
            key = df_idiomas.iloc[i,0] # sigla 'pt'
            value = df_idiomas.iloc[i,1] # valor 'Portuguese'
            dict_idiomas[key] = value
    return dict_idiomas

@st.cache
def lista_idiomas_full():
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    dict_idiomas = {}
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        key = df_idiomas.iloc[i,0] # sigla 'pt'
        value = df_idiomas.iloc[i,1] # valor 'Portuguese'
        dict_idiomas[key] = value
    return dict_idiomas

def play(raw_text, idioma_key):
    tts = gTTS(text=raw_text, lang=idioma_key)
    tts.save("audio.mp3")
    audio_file = open("audio.mp3","rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

    

def carregar_texto(type):
        file = st.file_uploader("Carregue um arquivo de texto", type=[type])
        #st.write("Arquivos de demonstração")
        #if st.button("Camoes.txt"):
        #    file = DEFAULT_TEXT
        #    Flag_button = True        
        if file is not None:
       	    #st.success("Arquivo carregado.")
            doc = file.getvalue()
            flag = 'upload'
        else:
            st.write("Um arquivo tipo de 3kB, por favor.")
        st.markdown("### Arquivos de demonstração")
        if st.button("Camoes.txt"):
            doc = camoes
            flag = 'demo'
        if st.button("Armstrong.txt"):
            doc = armstrong
            flag = 'demo'  
        return doc, flag  


def convert(dict_idioma,blob):
    try:
        dict_idioma_full = lista_idiomas_full()
      
        #st.write(dict_idioma)
                    
        #st.success("Original Language"+":  "+ idioma_original + " ("+original_key+")")
        #play(file.getvalue(),original_key)
            
        #dict_idioma = lista_idiomas(idioma_original)
        options = st.radio("Choose a language", tuple(dict_idioma.values()))
                    
        #idioma_final = get_key(idioma_original, dict_idioma)
        #st.subheader(options)               
        value = options
        idioma_final_key = get_key(value, dict_idioma)
        #st.subheader(idioma_final_key)
        try:
            texto_convertido = str(blob.translate(to=idioma_final_key))
            st.success("Language"+": "+ value + " ("+idioma_final_key+")")
            st.write(texto_convertido)
                                #st.text(idioma_final_key)
            play(texto_convertido,idioma_final_key)
                        
        except:
            st.error("ERROR: some languages will fail to play the sound.")
    except:
        st.error("ERROR: some languages will fail to play the sound.")


@st.cache(allow_output_mutation=True)
def load_model(name):
    return spacy.load(name)


@st.cache(allow_output_mutation=True)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)

SPACY_MODEL_NAMES = ["pt_core_news_sm"]
camoes = "Amor é fogo que arde sem se ver. Poema escrito por Luís Vaz de Camões. Começa assim. Amor é um fogo que arde sem se ver. É ferida que dói, e não se sente. É um contentamento descontente. É dor que desatina sem doer. É um não querer mais que bem querer. É um andar solitário entre a gente. É nunca contentar-se e contente. É um cuidar que ganha em se perder. É querer estar preso por vontade. É servir a quem vence, o vencedor. É ter com quem nos mata, lealdade. Mas como causar pode seu favor. Nos corações humanos amizade. Se tão contrário a si é o mesmo Amor?"

armstrong = "What A Wonderful World, Louis Armstrong. The Louis Armstrong Songbook Listening. I see trees of green, Red roses too, I see them bloom, For me and you, And I think to myself, What a wonderful world. I see skies of blue and clouds of white, The bright blessed day, The dark sacred night, And I think to myself, What a wonderful world. The colors of the rainbow, So pretty in the sky, Are also on the faces, Of people going by, I see friends shaking hands, Saying: How do you do? They're really saying, I love you."


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""

def main():
    
    """Ouça e Fale App """
    
    #st.title("Reader & Voice")


    html_page = """
    <div style="background-color:tomato;padding=50px">
        <p style='text-align:center;font-size:50px;font-weight:bold'>Reader & Voice</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)

    image = Image.open("reader.png")
    st.sidebar.image(image,caption="", use_column_width=True)

    image1 = Image.open("bandeiras.png")
    st.image(image1,caption="",use_column_width=True)
   
    activities = ["Home","Reader", 'Spacy',"About"]
    choice = st.sidebar.radio("Home",activities)
    dict_idioma_full = lista_idiomas_full()
    flag = 'carregar'
    warning = "Carregue um arquivo ou clique num arquivo da demonstração."
    warning_spacy = "Textos em Português."
    carregado = "Arquivo demonstraçao carregado..."
    uploaded = "Arquivo uploaded"

    if choice == 'Home':
        #st.write("Files:")
        st.markdown("### Files -> .txt")
        st.write("After uploading you can convert to 8 languages")
        st.write("#### Portuguese, Chinese, Spanish, French, Italian, Japanese, Russian and English")
        
    if choice == 'Spacy':
        try:
            doc, flag = carregar_texto('txt')
            if flag == "demo":
                st.success(carregado)
            if flag == 'upload':
                st.success(uploaded)
            blob = TextBlob(doc)
            idioma_original = get_value(blob.detect_language(),dict_idioma_full)   
            st.markdown("### Texto")
            st.write(doc)
            if idioma_original == "Portuguese":
                doc = process_text('pt_core_news_sm',doc)
                nlp = spacy.load('pt_core_news_sm')
                st.text([(word, word.ent_type_) for word in doc if word.ent_type_])
                displacy.render(doc, style='ent', jupyter=True)
        
                if "parser" in nlp.pipe_names:
                    st.header("Dependency Parse & Part-of-speech tags")
                    st.sidebar.header("Dependency Parse")
                    split_sents = st.sidebar.checkbox("Split sentences", value=True)
                    collapse_punct = st.sidebar.checkbox("Collapse punctuation", value=True)
                    collapse_phrases = st.sidebar.checkbox("Collapse phrases")
                    compact = st.sidebar.checkbox("Compact mode")
                    options = {
                       "collapse_punct": collapse_punct,
                       "collapse_phrases": collapse_phrases,
                       "compact": compact,
                       }
                    docs = [span.as_doc() for span in doc.sents] if split_sents else [doc]
                    for sent in docs:
                        html = displacy.render(sent, options=options)
                        # Double newlines seem to mess with the rendering
                        html = html.replace("\n\n", "\n")
                        if split_sents and len(docs) > 1:
                            st.markdown(f"> {sent.text}")
                        st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

                if "ner" in nlp.pipe_names:
                    st.header("Named Entities")
                    st.sidebar.header("Named Entities")
                    default_labels = ["PER", "LOC", "ORG", "MISC"]
                    labels = st.sidebar.multiselect("Entity labels", nlp.get_pipe("ner").labels, default_labels)
                    html = displacy.render(doc, style="ent", options={"ents": labels})

                    # Newlines seem to mess with the rendering
                    html = html.replace("\n", " ")
                    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
                    attrs = ["text", "label_", "start", "end", "start_char", "end_char"]
                    if "entity_linker" in nlp.pipe_names:
                        attrs.append("kb_id_")
                    data = [[str(getattr(ent, attr)) for attr in attrs]
                    for ent in doc.ents
                    if ent.label_ in labels]
                    df = pd.DataFrame(data, columns=attrs)
                    st.dataframe(df)
    
                if "textcat" in nlp.pipe_names:
                    st.header("Text Classification")
                    st.markdown(f"> {text}")
                    df = pd.DataFrame(doc.cats.items(), columns=("Label", "Score"))
                    st.dataframe(df)
            
                vector_size = nlp.meta.get("vectors", {}).get("width", 0)
                if vector_size:
                    st.header("Vectors & Similarity")
                    st.code(nlp.meta["vectors"])
                    text1 = st.text_input("Text or word 1", "apple")
                    text2 = st.text_input("Text or word 2", "orange")
                    doc1 = process_text(spacy_model, text1)
                    doc2 = process_text(spacy_model, text2)
                    similarity = doc1.similarity(doc2)
                    if similarity > 0.5:
                        st.success(similarity)
                    else:
                        st.error(similarity)

                st.header("Token attributes")

                if st.button("Show token attributes"):
                    attrs = [
        "idx",
        "text",
        "lemma_",
        "pos_",
        "tag_",
        "dep_",
        "head",
        "ent_type_",
        "ent_iob_",
        "shape_",
        "is_alpha",
        "is_ascii",
        "is_digit",
        "is_punct",
        "like_num",
    ]
                    data = [[str(getattr(token, attr)) for attr in attrs] for token in doc]
                    df = pd.DataFrame(data, columns=attrs)
                    st.dataframe(df)


                st.header("JSON Doc")
                if st.button("Show JSON Doc"):
                    st.json(doc.to_json())

                st.header("JSON model meta")
                if st.button("Show JSON model meta"):
                    st.json(nlp.meta)

            if idioma_original != "Portuguese":
                st.erro("Apenas textos em Portugues, por favor")


        except:
                st.info(choice + " --> "+warning_spacy)
                st.warning(choice + " --> "+warning)
        

        
    if choice == 'Reader':
        try:
            doc, flag = carregar_texto('txt')
            if flag == "demo":
                st.success(carregado)
            if flag == 'upload':
                st.success(uploaded)
            blob = TextBlob(doc)
            idioma_original = get_value(blob.detect_language(),dict_idioma_full)   
            
            st.markdown("### Texto")
            st.markdown(blob)
         
            original_key = get_key(idioma_original, dict_idioma_full)
            dict_idioma = lista_idiomas(idioma_original)
            st.success("Original Language"+":  "+ idioma_original + "  ("+original_key+")")
            #st.markdown(original_key)
            play(doc,original_key)
         
            convert(dict_idioma, blob)
                          
        except:
            st.warning(choice + " --> "+warning)

    if choice == 'About':
        st.subheader("I hope you enjoy it and use to learn something")
        st.subheader("For while only txt files")
        st.subheader("Built with Streamlit, Textblob and Spacy")
        st.write("Obs: Spacy loaded with model pt_core_news_sm")
        st.write("Problems/bugs:")
        st.write(" - sometimes the original language can't be correctly detected")
        st.write(" - sometimes the sound will fail.")
        st.subheader("Powerful example of Spacy code analyse")
        st.write("Thanks Ines Montani : https://gist.github.com/ines/b320cb8441b590eedf19137599ce6685")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)



if __name__ == '__main__':
    main()
