import spacy
from textblob import TextBlob



sp = spacy.load("en_core_web_sm")



file = open("./test/article_1.txt")
file_full = file.read()

file_text_start = "<text>"
file_text_end = "</text>"

file_text_start_index = file_full.find(file_text_start) + len(file_text_start)
file_text_end_index = file_full.find(file_text_end)

file_text = file_full[file_text_start_index:file_text_end_index]