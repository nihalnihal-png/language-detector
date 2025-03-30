import string
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox

# ---------------------------
# Stop words lists
# ---------------------------
english_stopwords = [
    'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are',
    'with', 'as', 'i', 'his', 'they', 'be', 'at', 'one', 'have', 'this', 'from', 'or', 'had', 'by',
    'not', 'word', 'but', 'what', 'some', 'we', 'can', 'out', 'other', 'were', 'all', 'there', 'when',
    'up', 'use', 'your', 'how', 'said', 'an', 'each', 'she'
]

spanish_stopwords = [
    'a', 'al', 'algo', 'algunas', 'algunos', 'algún', 'alguna', 'alli', 'allí', 'ambos', 'ante', 'antes', 'aquel',
    'aquella', 'aquellas', 'aquello', 'aquellos', 'aqui', 'aquí', 'asi', 'así', 'aunque', 'bajo', 'bastante', 'bien',
    'cada', 'casi', 'como', 'cómo', 'con', 'cual', 'cuál', 'cuales', 'cuáles', 'cualquier', 'cualquiera',
    'cualquieras', 'cuando', 'cuándo', 'cuanto', 'cuánto', 'cuanta', 'cuánta', 'cuantos', 'cuántos', 'cuantas',
    'cuántas', 'de', 'del', 'demás', 'demasiado', 'demasiada', 'demasiados', 'demasiadas', 'dentro', 'desde',
    'donde', 'dónde', 'dos', 'el', 'él', 'ella', 'ellas', 'ellos', 'en', 'entonces', 'entre', 'era', 'eras', 'eres',
    'es', 'esa', 'esas', 'ese', 'eso', 'esos', 'esta', 'está', 'están', 'estado', 'estamos', 'estando', 'estar',
    'estará', 'estas', 'este', 'esto', 'estos', 'estoy', 'etc', 'fin', 'fue', 'fueron', 'fui', 'fuimos', 'gueno',
    'ha', 'hace', 'haces', 'haciendo', 'han', 'hasta', 'hay', 'haya', 'he', 'hemos', 'hube', 'hubiera', 'hubieran',
    'hubiese', 'hubo', 'incluso', 'intenta', 'intentais', 'intentamos', 'intentan', 'intentar', 'intentas',
    'intento', 'ir', 'la', 'las', 'le', 'les', 'lo', 'los', 'mientras', 'muy', 'más', 'me', 'mi', 'mis', 'mucho',
    'mucha', 'muchos', 'muchas', 'nada', 'ni', 'ningún', 'ninguna', 'ningunas', 'ninguno', 'ningunos', 'no',
    'nos', 'nosotras', 'nosotros', 'nuestra', 'nuestras', 'nuestro', 'nuestros', 'nunca', 'otra', 'otro',
    'otros', 'para', 'parece', 'pero', 'poca', 'poco', 'por', 'porque', 'primero', 'puede', 'pueden', 'puedo',
    'pues', 'que', 'qué', 'quien', 'quién', 'quienes', 'quiénes', 'se', 'sea', 'sean', 'según', 'ser', 'si', 'sí',
    'siempre', 'siendo', 'sin', 'sino', 'sobre', 'solamente', 'solo', 'sólo', 'son', 'su', 'sus', 'tal', 'también',
    'tampoco', 'tan', 'tanta', 'tantas', 'tanto', 'tantos', 'te', 'tenéis', 'tenemos', 'tener', 'tengo', 'tiempo',
    'tiene', 'tienen', 'todo', 'todos', 'tomar', 'trabajar', 'trabajé', 'trabajó', 'tuyo', 'tuyos', 'último',
    'un', 'una', 'unas', 'uno', 'unos', 'usted', 'ustedes', 'va', 'vais', 'valor', 'vamos', 'van', 'varias',
    'varios', 'vaya', 'verdad', 'verdadero', 'vosotras', 'vosotros', 'voy', 'y', 'ya', 'yo'
]

french_stopwords = [
    'alors', 'alr', 'alr.', 'ainsi', 'ainsi que', 'ainsiqu', 'après', 'apres', 'aprè', 'ap.', 'au', 'aux', 'aucun', 
    'aucune', 'auc1', 'auc.', 'aujourd\'hui', 'auj', 'aujourdhui', 'auj.', 'auquel', 'auxquels', 'auxquelles', 
    'avant', 'avan', 'avant.', 'avec', 'avc', 'avec.', 'beaucoup', 'bcp', 'bien', 'bn', 'b1', 'b1n', 'car', 
    'c\'est', 'cest', 'c.', 'ce', 'ceci', 'cela', 'celui', 'celle', 'ceux', 'ces', 'cet', 'cette', 'ci', 'comme', 
    'cmme', 'comme.', 'comment', 'cmt', 'comt', 'concernant', 'conc.', 'contre', 'c0ntre', 'd\'abord', 'dabord', 
    'd\'accord', 'dacc', 'd\'ailleurs', 'dailleurs', 'de', 'du', 'des', 'dans', 'ds', 'dedans', 'dehors', 'depuis', 
    'dps', 'dèq', 'dès', 'dès que', 'desq', 'donc', 'dc', 'donc.', 'dos', 'déjà', 'deja', 'dèja', 'elle', 'elles', 
    'en', 'encore', 'enc.', 'entre', 'env.', 'et', 'et.', 'étaient', 'etaient', 'étais', 'etais', 'était', 'etait', 
    'être', 'etre', 'eu', 'eû', 'eurent', 'eut', 'eux', 'faire', 'fait', 'faites', 'font', 'furent', 'ici', 'il', 
    'ils', 'je', 'j\'ai', 'jai', 'j\'étais', 'jetais', 'j\'étaient', 'jetaient', 'la', 'là', 'la.', 'le', 'lequel', 
    'les', 'lesquels', 'lesquelles', 'leur', 'leurs', 'lors', 'lorsque', 'lq', 'lorsq', 'mais', 'ms', 'même', 
    'meme', 'mêmes', 'memes', 'moi', 'moins', 'mon', 'notre', 'nous', 'notre.', 'où', 'ou', 'on', 'ont', 'ou', 
    'par', 'parce que', 'pq', 'parq', 'parfois', 'parf.', 'pas', 'pcq', 'pendant', 'pendt', 'pour', 'pr', 'près', 
    'pres', 'puis', 'puissent', 'quand', 'qd', 'quant', 'que', 'qu\'', 'qui', 'quoi', 'sauf', 'sauf.', 'seulement', 
    'slm', 'si', 'sinon', 'sans', 'serait', 'sera', 'seront', 'ses', 'son', 'sont', 'sous', 'souvent', 'soyez', 
    'suis', 'suit', 'sur', 'tandis', 'tant', 'tellement', 'tel', 'telle', 'tels', 'toutes', 'tout', 'toute', 'trop', 
    'très', 'tres', 'tu', 't\'es', 'tes', 'un', 'une', 'voici', 'voilà', 'votre', 'vos', 'vous', 'vu'
]

manglish_stopwords = [
    'aanu', 'aannu', 'anu', 'aanuu', 'an', 'aayirunnu', 'ayirunnu', 'airunnu', 'ayirnu', 'adhava', 'adava',
    'athava', 'adhuva', 'adhe', 'athe', 'athae', 'atheyo', 'athentha', 'athenthae', 'athenthaaa', 'athinu',
    'athnu', 'athin', 'athinuu', 'athnk', 'athu', 'athokke', 'athokkeum', 'ayi', 'ai', 'ayiye', 'ayii',
    'enkil', 'enkilum', 'enkilaanu', 'enkilaa', 'ennal', 'ennaal', 'enn', 'ennn', 'ennum', 'ennuu', 'ennu',
    'enu', 'enuu', 'ennu paranja', 'ente', 'entea', 'entha', 'enthaanu', 'enthaayirunnu', 'enth', 'enthanu',
    'ethu', 'eth', 'ethanu', 'ethum', 'ethokke', 'ivide', 'ivid', 'ividu', 'ivd', 'ivdil', 'ividano', 'ividekku',
    'ivdekku', 'ividkku', 'ividil', 'njan', 'njaan', 'nj', 'njaa', 'njaan', 'nangal', 'njangal', 'njangale',
    'njngl', 'ningal', 'ningale', 'ningl', 'ningalu', 'ningalude', 'ningalkku', 'ningalkk', 'ningudae', 'ithu',
    'ith', 'ithinte', 'ithil', 'ithokke', 'ithuvare', 'ithuvareyum', 'ithum', 'ithivide', 'oru', 'or', 'oronn',
    'oridathu', 'orid', 'oru mathram', 'oru pole', 'oru nj', 'pakshe', 'paksh', 'pakshay', 'paksa', 'pinna',
    'pinne', 'pin', 'pinchu', 'poy', 'poi', 'poyi', 'poyyi', 'poi poyi', 'randu', 'rand', 'rendu', 'randum',
    'thanne', 'tanne', 'thannee', 'thannne', 'tan', 'valiya', 'valya', 'vella', 'vellam', 'velam', 'vellathinu',
    'vellathokke', 'vere', 'ver', 'verae', 'verum', 'verumm', 'verumbol', 'veronnumilla', 'vitt', 'vittum',
    'vittu', 'vittu poyi', 'yathoru', 'yethoru', 'yathre', 'yathrayum', 'yatre', 'yaathrayum', 'yaathram', 'yaath'
]

hinglish_stopwords = [
    'hai', 'kya', 'nahi', 'acha', 'thik', 'yaar', 'bhai', 'didi', 'maa', 'papa',
    'kar', 'raha', 'rahi', 'rahe', 'gaya', 'aaya', 'ja', 'aa', 'mein', 'mera', 'teri',
    'uska', 'iski', 'uski', 'hamara', 'tumhara', 'unka', 'inka', 'karke', 'hoke',
    'toh', 'hi', 'na', 're', 'ji', 'han', 'nahin', 'kyun', 'kyon', 'kaise',
    'kab', 'kidhar', 'kaisa', 'kaisi', 'sab', 'kuch', 'bahut', 'thora', 'ek', 'do',
    'teen', 'char', 'paanch', 'bas', 'fir', 'phir', 'abhi', 'tabhi', 'jab', 'tab',
    'yahaan', 'vahaan', 'idhar', 'udhar', 'andar', 'bahar', 'upar', 'neeche',
    'kyaa', 'kia', 'kyu', 'kyon', 'kese', 'kub', 'kider', 'sub', 'kutch', 'bohut',
    'thoda', 'yak', 'du', 'tin', 'chaar', 'panch', 'bass', 'avi', 'tabee', 'jah',
    'tub', 'yahan', 'vahan', 'idar', 'udar', 'ander', 'baahar', 'uper', 'niche'
]


def process_text(text):
    """Convert text to lowercase, remove punctuation, and split into words."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()

def count_stopwords(words, stopwords):
    """Count how many words match the stop words list."""
    return sum(word in stopwords for word in words)

def detect_script(text):
    """Detect the script based on Unicode ranges."""
    if re.search(r'[\u0D00-\u0D7F]', text):  # Malayalam
        return 'Malayalam'
    elif re.search(r'[\u0900-\u097F]', text):  # Hindi (Devanagari)
        return 'Hindi'
    elif re.search(r'[\u0400-\u04FF]', text):  # Russian (Cyrillic)
        return 'Russian'
    elif re.search(r'[\u0600-\u06FF]', text):  # Arabic
        return 'Arabic'
    elif re.search(r'[\u0C80-\u0CFF]', text):  # Kannada
        return 'Kannada'
    elif re.search(r'[\u0C00-\u0C7F]', text):  # Telugu
        return 'Telugu'
    return 'Latin'  # Default for English, Spanish, French, Manglish, Hinglish

def identify_language(text):
    """Identify the language using script detection and stop word analysis."""
    script = detect_script(text)
    if script == 'Malayalam':
        return 'Malayalam'
    elif script == 'Hindi':
        return 'Hindi'
    elif script == 'Russian':
        return 'Russian'
    elif script == 'Arabic':
        return 'Arabic'
    elif script == 'Kannada':
        return 'Kannada'
    elif script == 'Telugu':
        return 'Telugu'
    else:  # Latin script
        words = process_text(text)
        if count_stopwords(words, manglish_stopwords) > 0:
            return 'Manglish'
        elif count_stopwords(words, hinglish_stopwords) > 0:
            return 'Hinglish'
        else:
            counts = {
                'English': count_stopwords(words, english_stopwords),
                'Spanish': count_stopwords(words, spanish_stopwords),
                'French': count_stopwords(words, french_stopwords)
            }
            return max(counts, key=counts.get)



# UI using Tkinter

def detect_language_ui():
    user_text = text_input.get("1.0", tk.END).strip()
    if not user_text:
        messagebox.showwarning("Input Error", "Please enter some text!")
        return
    lang = identify_language(user_text)
    result_label.config(text=f"Detected Language: {lang}")

# Create main window
root = tk.Tk()
root.title("Nihal's Simple Yet Powerful Language Detector")
root.geometry("600x400")

# Create a text widget for input
text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10)
text_input.pack(pady=20)

# Create a button to trigger detection
detect_button = tk.Button(root, text="Detect Language", command=detect_language_ui)
detect_button.pack(pady=10)

# Create a label to display results
result_label = tk.Label(root, text="Detected Language: ", font=("Arial", 14))
result_label.pack(pady=10)

# Run the main event loop
root.mainloop()