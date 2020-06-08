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


def lista_idiomas(idioma_original):
    df_idiomas = pd.read_csv('lista_idiomas.csv')
    #st.table(df_idiomas)
    dict_idiomas = {}
    
    linhas = len(df_idiomas)
    for i in range(0, linhas):
        if idioma_original != df_idiomas.iloc[i,1]:
            key = df_idiomas.iloc[i,0] # sigla 'pt'
            #st.write(key)
            value = df_idiomas.iloc[i,1] # valor 'Portuguese'
            #st.write(value)
            dict_idiomas[key] = value
    return dict_idiomas


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

    

def carregar_texto():
        file = None
        file = st.file_uploader("Carregue um arquivo de texto", type=['txt'])
        if file is not None:
            doc = file.getvalue()
            flag = 'upload'         
              
        return doc, flag


def carregar_files(tipo, choice):
        if tipo == "upload":
            doc, flag = carregar_texto()
        elif tipo == "demo":
            doc, flag = carregar_demo(choice)           
        
        return doc, flag

def carregar_demo(choice):
    st.markdown("### Arquivos de demonstração")
    if st.button("Amor é fogo que arde sem se ver.txt"):
        doc = camoes
        flag = 'demo'
    
    if choice != "Spacy":
        if st.button("What A Wonderful World.txt"):
            doc = armstrong
            flag = 'demo'

    #if choice != "Spacy":
    #    if st.button("Paint it Black.txt"):
    #        doc = black
    #        flag = 'demo'    

    if st.button("Strani Amori.txt"):
        doc = legiao
        flag = 'demo'

    if choice != "Spacy":
        if st.button("La Barca.txt"):
            doc = barca
            flag = 'demo'    
    
    
    
    return doc, flag  


def convert(dict_idioma,blob, options):
    try:
                  
        value = options # idioma choosed at radio box
       
        idioma_final_key = get_key(value, dict_idioma)
       
        try:
            texto_convertido = str(blob.translate(to=idioma_final_key))
            st.success("Language"+": "+ value + " ("+idioma_final_key+")")
            st.write(texto_convertido)
            play(texto_convertido,idioma_final_key)
                        
        except:
            st.error("ERROR 1: some languages will fail to play the sound.")
    except:
        st.error("ERROR 2: some languages will fail to play the sound.")


@st.cache(allow_output_mutation=True)
def load_model(name):
    return spacy.load(name)


@st.cache(allow_output_mutation=True)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)


SPACY_MODEL_NAMES = ["pt_core_news_sm"]

camoes = "Amor é fogo que arde sem se ver. Poema escrito por Luís Vaz de Camões. Começa assim. Amor é um fogo que arde sem se ver. É ferida que dói, e não se sente. É um contentamento descontente. É dor que desatina sem doer. É um não querer mais que bem querer. É um andar solitário entre a gente. É nunca contentar-se e contente. É um cuidar que ganha em se perder. É querer estar preso por vontade. É servir a quem vence, o vencedor. É ter com quem nos mata, lealdade. Mas como causar pode seu favor. Nos corações humanos amizade. Se tão contrário a si é o mesmo Amor?"

armstrong = "What A Wonderful World, Louis Armstrong. The Louis Armstrong Songbook. Lets Listening. I see trees of green, Red roses too, I see them bloom, For me and you, And I think to myself, What a wonderful world. I see skies of blue and clouds of white, The bright blessed day, The dark sacred night, And I think to myself, What a wonderful world. The colors of the rainbow, So pretty in the sky, Are also on the faces, Of people going by, I see friends shaking hands, Saying: How do you do? They're really saying, I love you."

legiao = "Strani amori. Renato Russo. Mi dispiace devo andare via. Ma sapevo che era una bugia. Quanto tempo perso dietro a lui. Che promette e poi non cambia mai. Strani amori mettono nei guai. Ma, in realtà, siamo noi. E lo aspetti ad un telefono. Litigando che sia libero. Con il cuore nello stomaco. Un gomitolo nell'angolo. Lì da solo, dentro un brivido. Ma perchè lui non c'è. E sono strani amori che fanno crescere. E sorridere tra le lacrime. Quante pagine lì da scrivere. Sogni e lividi da dividere. Sono amori che spesso a questa età. Si confondono dentro a quest'anima. Che si interroga senza decidere. Se è un amore che fa per noi. E quante notti perse a piangere. Rileggendo quelle lettere. Che non riesci più a buttare via. Dal labirinto della nostalgia. Grandi amori che finiscono. Ma perchè restano nel cuore. Strani amori che vanno e vengono. Nei pensieri che lì nascondono. Storie vere che ci appartengono. Ma si lasciano come noi. Strani amori fragili. Prigionieri liberi. Strani amori mettono nei guai. Ma, in realtà, siamo noi. Strani amori fragili. Prigionieri liberi. Strani amori che non sanno vivere. E si perdono dentro noi. Mi dispiace devo andare via. Questa volta l'ho promesso a me. Perchè ho voglia di un amore vero. Senza te." 


barca = "La Barca. Luis Miguel. Dicen que la distancia es el olvido. Pero yo no concibo esta razón. Porque yo seguiré siendo el cautivo. De los caprichos de tu corazón. Supiste esclarecer mis pensamientos. Me diste la verdad que yo soñé. Ahuyentaste de mí los sufrimientos. En la primera noche que te amé. Hoy mi playa se viste de amargura. Porque tu barca tiene que partir. A cruzar otros mares de locura. Cuida que no naufrague en tu vivir. Cuando la luz del sol se esté apagando. Y te sientas cansada de vagar. Piensa que yo por ti estaré esperando. Hasta que tú decidas regresar. Supiste esclarecer mis pensamientos. Me diste la verdad que yo soñé. Ahuyentaste de mí los sufrimientos. En la primera noche que te amé. Hoy mi playa se viste de amargura. Porque tu barca tiene que partir. A cruzar otros mares de locura. Cuida que no naufrague en tu vivir. Cuando la luz del sol se esté apagando. Y te sientas cansada de vagar. Piensa que yo por ti estaré esperando. Hasta que tú decidas regresar."

black = "Paint it Black. Roling Stones. I see a red door and I want it painted black. No colors anymore. I want them to turn black. I see the girls walk by dressed. In their summer clothes. I have to turn my head. Until my darkness goes. I see a line of cars. And they're all painted black. With flowers and my love. Both never to come back. I see people turn their heads. And quickly look away. Like a new born baby. It just happens every day. I look inside myself. And see my heart is black. I see my red door. And must have it painted black. Maybe then I'll fade away. And not have to face the facts. It's not easy facin' up. When your whole world is black. No more will my green sea. Go turn a deeper blue. I could not foresee. This thing happening to you. If I look hard enough. Into the settin' Sun. My love will laugh with me. Before the mornin' comes. I see a red door and. I want it painted black. No colors anymore. I want them to turn black. I see the girls walk by dressed. In their summer clothes. I have to turn my head. Until my darkness goes. I want see your face. Painted black. Black as night. Black as coal. Don't wanna see the Sun. Flying high in the sky. I wanna see it painted, painted, painted. Painted black. Yeah!" 

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

    image1 = Image.open("bandeira6.png")
    st.image(image1,caption="",use_column_width=True)  
   
    menu1 = ["Home","Reader", 'Spacy',"About"]
    choice1 = st.sidebar.radio("Home",menu1)

    menu2 = ["Demo", "Upload"]
    choice2 = st.sidebar.selectbox("Ativity",menu2)
    
    dict_idioma_full = lista_idiomas_full()
   
    warning_demo = "Clique num arquivo da demonstração"
    warning_upload = "Carregue um arquivo txt, por favor"
    warning_spacy = "treinado apenas para textos em Português."
    file_test = "Arquivo demonstraçao carregado..."
    file_upload = "Arquivo uploaded carregado..."
    spacy_again = "------> Carregue novamente "

    if choice1 == 'Home':
        #st.write("Files:")
        st.markdown("### Files -> .txt")
        st.write("After uploading you can convert to 6 languages")
        st.write("#### Portuguese, Spanish, French, Italian, Japanese and English")
        
    if choice1 == 'Spacy':
        st.subheader(choice1 +" -> "+choice2)
        try:
            if choice2 == menu2[0]:  # "Demo"
                doc_demo, flag = carregar_files("demo", choice1)
                st.success(file_test)
                doc = doc_demo
                                  
            
            elif choice2 == menu2[1]: # "Upload"
                doc_upload, flag = carregar_files("upload", choice2)
                st.success(file_upload)
                doc = doc_upload

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
                st.info("Original Language "+":  "+ idioma_original)
                st.warning(choice2 + "--> "+ warning_spacy)
                st.info(spacy_again) 


        except:
            if choice1 == "Spacy" and choice2 == "Demo":
                st.warning(choice2 + " --> "+warning_demo)
            elif choice1 == "Spacy" and choice2 == "Upload":
                st.warning(choice2 + " --> "+warning_upload)
        

        
    if choice1 == 'Reader':
        st.subheader(choice1 +" -> "+choice2)
        
        try:
            if choice2 == menu2[0]:  # "Demo"
                doc_demo, flag = carregar_files("demo", choice1)
                st.success(file_test)
                doc = doc_demo
                                  
            
            elif choice2 == menu2[1]: # "Upload"
                doc_upload, flag = carregar_files("upload", choice2)
                st.success(file_upload)
                doc = doc_upload
       
                       
            blob = TextBlob(doc)
            dict_idioma_full = lista_idiomas_full()
            idioma_original = get_value(blob.detect_language(),dict_idioma_full)   
            
            st.markdown("### Texto")
            st.markdown(blob)
            
 
            original_key = get_key(idioma_original, dict_idioma_full)

            # dict_idioma recebe a lista sem o idioma original
            dict_idioma = lista_idiomas(idioma_original)        # Remove idioma original da lista
            
            st.success("Original Language"+":  "+ idioma_original + "  ("+original_key+")")
            #st.markdown(original_key)
            play(doc,original_key)
            
            if flag != "demo":
                options = st.radio("Choose a language", tuple(dict_idioma.values()))
                convert(dict_idioma, blob, options)
                        
        except:
           if choice1 == "Reader" and choice2 == "Demo":
                st.warning(choice2 + " --> "+warning_demo)
           elif choice1 == "Reader" and choice2 == "Upload":
                st.warning(choice2 + " --> "+warning_upload)

    if choice1 == 'About':
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
