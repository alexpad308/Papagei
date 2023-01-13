# -*- coding: utf-8 -*-

# doc: https://www.osgeo.cn/python-tutorial/pdf-pdfminer.htm

import re
import time
import string
from tqdm import trange
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams

from tts import TTSX


def open_pdf(filename):
    with open(filename, 'rb') as f:
        parse = PDFParser(f)  # 创建一个PDF文档分析器
        doc = PDFDocument()  # 创建一个PDF文档对象存储文档结构

        parse.set_document(doc)  # 连接分析器与文档对象
        doc.set_parser(parse)
        doc.initialize()  # 提供初始化密码，如果没有密码，就创建一个空的字符串

        resource = PDFResourceManager()  # 创建一个PDF资源管理器对象来存储共享资源
        laparams = LAParams()  # 创建一个PDF参数分析器
        device = PDFPageAggregator(resource, laparams=laparams)  # 创建一个PDF设备对象
        interpreter = PDFPageInterpreter(resource, device)  # 创建一个PDF解释器对象

    result = []
    for page in doc.get_pages():
        interpreter.process_page(page)
        page = device.get_result()

        page_result = []
        for section in page:
            if hasattr(section, "get_text"):
                sec = section.get_text()
                sec = sec.replace("\n", " ")
                sec = cut_sentences_zh(sec)
                page_result += sec

        result.append(page_result)

    return result


def cut_sentences_en(text):
    # split english text into sentences
    # https://stackoverflow.com/questions/4576077/python-split-text-on-sentences

    # define regex for sentence splitting
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")

    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    # print(sentences)

    return sentences


def cut_sentences_zh(text):
    # split chinese text into sentences
    # https://zhon.readthedocs.io/en/latest
    # return re.findall(zhon.hanzi.sentence, text)

    # define regex for sentence splitting
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"
    asians = "([\u2E80-\u9FFF])"

    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits + "[.]" + digits, "\\1<prd>\\2<prd>\\3", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "。。。" in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    text = re.sub(asians + " " + asians, "\\1\\2", text)  # remove space between asian characters
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "！" in text: text = text.replace("！\"", "\"！")
    if "?" in text: text = text.replace("?\"", "\"?")
    if "？" in text: text = text.replace("？\"", "\"？")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("。", "。<stop>")
    text = text.replace("？", "？<stop>")
    text = text.replace("！", "！<stop>")
    text = text.replace("<prd>", ".")

    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    # print(sentences)

    return sentences


def judge_language(sentence):
    # judge language type of sentence, support Chinese, Japanese, Korean, English

    # 去除标点符号和数字
    remove_nota = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    sentence = re.sub(remove_nota, '', sentence)
    sentence = sentence.translate(remove_punctuation_map)

    result = []

    # unicode digits
    re_words = re.compile(u"[0-9]")
    res = re.findall(re_words, sentence)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[0-9]", '', sentence).strip()
    if len(res) > 0:
        result.append('num')
    if len(res2) <= 0:
        return 'zh-cn'  # 考虑单数字的情况，按照中文处理

    # unicode english
    re_words = re.compile(u"[a-zA-Z]")
    res = re.findall(re_words, sentence)  # 查询出所有的匹配字符串
    res2 = re.sub('[a-zA-Z]', '', sentence).strip()
    if len(res) > 0:
        result.append('en')
    if len(res2) <= 0:
        return 'en'

    # unicode chinese
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    res = re.findall(re_words, sentence)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u4e00-\u9fa5]+", '', sentence).strip()
    if len(res) > 0:
        result.append('zh-cn')
    if len(res2) <= 0:
        return 'zh-cn'

    # unicode korean
    re_words = re.compile(u"[\uac00-\ud7ff]+")
    res = re.findall(re_words, sentence)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\uac00-\ud7ff]+", '', sentence).strip()
    if len(res) > 0:
        result.append('ko')
    if len(res2) <= 0:
        return 'ko'

    # unicode japanese katakana and unicode japanese hiragana
    re_words = re.compile(u"[\u30a0-\u30ff\u3040-\u309f]+")
    res = re.findall(re_words, sentence)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u30a0-\u30ff\u3040-\u309f]+", '', sentence).strip()
    if len(res) > 0:
        result.append('ja')
    if len(res2) <= 0:
        return 'ja'

    # 考虑存在日文汉字的情况，按照日文处理
    if result == ['ja', 'zh-cn'] or result == ['zh-cn', 'ja']:
        return 'ja'

    # 考虑存在文字+数字的情况，按照包含的文字类型判断
    if 'num' in result and len(result) > 1:
        result.remove('num')

    return result


def test_judge_languge():
    s1 = "汉语是世界上最优美的语言，正则表达式是一个很有用的工具"
    s2 = "正規表現は非常に役に立つツールテキストを操作することです"
    s3 = "あアいイうウえエおオ"
    s4 = "정규 표현식은 매우 유용한 도구 텍스트를 조작하는 것입니다"
    s5 = "Regular expression is a powerful tool for manipulating text."
    s6 = "Regular expression 正则表达式 あアいイうウえエおオ 정규 표현식은"
    print(judge_language(s1))
    print(judge_language(s2))
    print(judge_language(s3))
    print(judge_language(s4))
    print(judge_language(s5))
    print(judge_language(s6))


def test_PDF_Reader():
    pdf = PDF_Reader('../doc/harry_potter.pdf')
    pdf.read(40, 47)

    pdf = PDF_Reader('../doc/王小波选集.pdf')
    pdf.read(1690, 1692)


class PDF_Reader:
    def __init__(self, file_name):
        self.book = open_pdf(file_name)  # pdf file
        self.pages = len(self.book)  # pdf pages
        self.tts = TTSX()  # tts engine
        self.tts.set_speed(130)

    def read(self, start_page=None, end_page=None):
        # read range
        start = start_page - 1 if start_page else 0
        end = end_page if end_page else self.pages
        book = self.book[start:end]

        for page in book:
            if not page:
                continue

            for section in page:
                if not section:
                    continue

                # 根据段落语言，选择语句切分工具
                sentences = []
                section_lang = judge_language(section)
                if section_lang == 'en':
                    sentences = cut_sentences_en(section)
                if section_lang == 'zh-cn' or 'zh-cn' in section_lang:
                    sentences = cut_sentences_zh(section)

                for sentence in sentences:
                    print(sentence)
                    language = judge_language(sentence)
                    if type(language) == list:
                        language = language[0]  # 处理多语言情况

                    self.tts.set_voice(self.tts.lang[language])
                    self.tts.say(sentence)

            print('Page Turning ...')
            for i in trange(1 * 100):
                time.sleep(0.01)


if __name__ == '__main__':
    test_PDF_Reader()
