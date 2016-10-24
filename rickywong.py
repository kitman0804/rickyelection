import os
import jieba
import jieba.analyse
from wordcloud import WordCloud
from PIL import Image, ImageDraw
import numpy as np
import re


# Font
font_path = "mingliu.ttc"


# Jieba dictionary
jieba.set_dictionary("dict/dict.txt.big.txt")
jieba.load_userdict("dict/dict_hk_places.txt")
jieba.load_userdict("dict/dict_hk_politics.txt")


# Read downloaded articles
def read_article(file):
    return {'topic': re.sub(".*\_(.*)\.txt", "\\1", file),
            'content': open(file, "rb").read().decode()}


# Extract words in the articles
punctuation = "（）「」，。"
unwanted_sym = "|".join([x for x in punctuation]) + "|\r|\n"

articles = [read_article("articles/" + x) for x in os.listdir("articles")]
words = [{'topic': x["topic"],
          'keywords': jieba.analyse.extract_tags(x["content"], 100),
          'words': jieba.cut(x["content"], cut_all=False)}
         for x in articles]
words = [{'topic': x["topic"],
          'keywords': x["keywords"],
          'words': " ".join([x_i for x_i in x["words"] if not re.match(unwanted_sym, x_i)])}
         for x in words]


# Create wordcloud for each topic
def create_circle_mask(img_size=(500, 500), radius=220):
    cx = img_size[0] / 2
    cy = img_size[1] / 2
    r = radius
    img = Image.new('RGB', img_size, "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(0,) * 3)
    return img


def create_wordcloud():
    for i in range(len(words)):
        mask = create_circle_mask()
        mask = np.asarray(mask)
        wc = WordCloud(font_path=font_path, mask=mask, mode="RGBA", background_color=None, relative_scaling=.5)
        wc = wc.generate(words[i]["words"])
        save_path = "wordclouds/wordcloud%02.0f_%s.png" % (i + 1, words[i]["topic"])
        wc.to_file(save_path)
        print("Wordcloud is stored in %s" % save_path)


create_wordcloud()

