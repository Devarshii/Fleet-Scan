import io
import pytesseract
from pdf2image import convert_from_path
import cv2
import string
from PIL import Image,ImageChops,ImageFilter
from gtts import gTTS
import os
from translate import Translator
import pandas
import tabula 

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def draw_boxes_on_character(img):
    
    img = cv2.imread("download.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    texts = pytesseract.image_to_string(img)
    print(texts)

    conf = r'-c tessedit_char_whitelist='+string.digits
    img_width = img.shape[1]
    img_height = img.shape[0]


    boxes = pytesseract.image_to_boxes(img, config =conf)

    print(boxes)
    for box in boxes.splitlines():
        box = box.split(" ")
        character = box[0]
        x = int(box[1])
        y = int(box[2])
        x2 = int(box[3])
        y2 = int(box[4])
        cv2.rectangle(img, (x, img_height - y), (x2, img_height - y2), (0, 255, 0), 1)
        cv2.putText(img, character, (x, img_height -y2), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255) , 1)
    return img

def draw_boxes_on_text(img):
   
    texts = pytesseract.image_to_string(img)
    print(texts)

    conf = r'-c tessedit_char_whitelist='+string.digits
    img_width = img.shape[1]
    img_height = img.shape[0]
    raw_data = pytesseract.image_to_data(img)

    #print(raw_data)
    for count, data in enumerate(raw_data.splitlines()):
        if count > 0:
            data = data.split()
            if len(data) == 12:
                x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
                cv2.putText(img, content, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255) , 1)
                
    return img,texts

def extract_text_from_pdf(pdf_path):
    # Convert PDF to image
    pages = convert_from_path(pdf_path, 500, poppler_path=r'C:\Users\drago\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin')
     
    # Extract text from each page using Tesseract OCR
    text_data = ''
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + '\n'
     
    # Return the text data
    return text_data

print("Select \n1. For Image to text \n2. Pdf to text")
value=int(input("Enter the digit"))
print(value)


if value == 1:
    img = cv2.imread("download.jpg")
    #img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thr = cv2.adaptiveThreshold(gry, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 15, 22)
    
    img,texts = draw_boxes_on_text(img)
    cv2.imshow("Output", img)
    cv2.waitKey(0)
    
    textfile = open('file.txt', 'w')
    textfile.write(texts)
    print("Text is written in file!")
    textfile.close()

    with open('file.txt','r') as f:
        lines = f.readlines()
        
    lines = [line.replace(' ','') for line in lines]
    
    with open('file.txt', 'w') as f:
        f.writelines(lines)
    
    textfile = open('file.txt')
    text = textfile.read()

    lang = 'en'

    object = gTTS(text=text, lang=lang, slow=False)
    object.save("speech.mp3")

    os.system("speech.mp3")
    
    print("Choose \n1.Hindi \n2.German \n3.French \n4.Chinese \n5.English")
    lan=int(input("\nSelect the number for language"))
    
    if(lan==1):
        translator= Translator(to_lang="hindi")
        translation = translator.translate(texts)
        print(translation)
        translation.encode('utf-8')
        textfile = open('file.txt', 'w',encoding='utf-8')
        textfile.write(translation)
        print("Text is written in file!")
        textfile.close()

        textfile = open('file.txt' , encoding='utf-8')
        text = textfile.read()

        lang = 'hi'

        object = gTTS(text=text, lang=lang, slow=False)
        object.save("speech.mp3")

        os.system("speech.mp3")
        
    if(lan==2):
        translator= Translator(to_lang="German")
        translation = translator.translate(texts)
        print(translation)
        textfile = open('file.txt', 'w')
        textfile.write(translation)
        print("Text is written in file!")
        textfile.close()

        textfile = open('file.txt')
        text = textfile.read()

        lang = 'de'

        object = gTTS(text=text, lang=lang, slow=False)
        object.save("speech.mp3")

        os.system("speech.mp3")
    if(lan==3):
        translator= Translator(to_lang="French")
        translation = translator.translate(texts)
        
        print(translation.encode('utf-8'))
        textfile = open('file.txt', 'w')
        textfile.write(translation)
        print("Text is written in file!")
        textfile.close()

        textfile = open('file.txt')
        text = textfile.read()

        lang = 'fr'

        object = gTTS(text=text, lang=lang, slow=False)
        object.save("speech.mp3")

        os.system("speech.mp3")
    if(lan==4):
        translator= Translator(to_lang="Chinese")
        translation = translator.translate(texts,)
        print(translation)
        translation.encode('utf-8')
        textfile = open('file.txt', 'w',encoding='utf-8')
        textfile.write(translation)
        print("Text is written in file!")
        textfile.close()

        textfile = open('file.txt', encoding='utf-8')
        text = textfile.read()

        lang = 'zh-cn'

        object = gTTS(text=text, lang=lang, slow=False)
        object.save("speech.mp3")

        os.system("speech.mp3")
    if(lan==5):
        translator= Translator(to_lang="english")
        translation = translator.translate(texts)
        print(translation)
        textfile = open('file.txt', 'w')
        textfile.write(translation)
        print("Text is written in file!")
        textfile.close()

        textfile = open('file.txt')
        text = textfile.read()

        lang = 'en'

        object = gTTS(text=text, lang=lang, slow=False)
        object.save("speech.mp3")

        os.system("speech.mp3")
    
    
    
    #textfile = open('file.txt', 'w')
    #textfile.write(texts)
    #print("Text is written in file!")
    #textfile.close()

    #textfile = open('file.txt')
    #text = textfile.read()

    #lang = 'en'

    #object = gTTS(text=text, lang=lang, slow=False)
    #object.save("speech.mp3")

    #os.system("speech.mp3")
    
elif value == 2: 
    text = extract_text_from_pdf('table.pdf')
    print(text)

    textfile = open('file2.txt', 'w')
    textfile.write(text)
    print("Text is written in file!")
    textfile.close()
    df=tabula.read_pdf('table.pdf' , pages= 'all')
    tabula.convert_into("table.pdf",'table.csv',output_format='csv',pages='all')
    
else:
    print("Enter valid value")
