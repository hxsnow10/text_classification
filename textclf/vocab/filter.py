#encoding=utf-8

class Vocabulary_filter():

    def __init__(self,vocabulary,white_list={},black_list={},black_flag={'n'}):
        self.vocabulary=vocabulary
        self.white_list=white_list
        self.black_list=black_list#TODO:是否可以不需要黑名单？
        self.black_flag=black_flag
        self.check()
        self.filtered_words=[]

    def check(self):
        s=set(self.black_list) & set(self.white_list)
        if s!=set([]):
            print 'white_list & black_list == ', s

    def filter_word(self, word, flag):
        if word in self.white_list:
            return True
        if word in self.black_list:
            return False
        
        if flag[0] in self.black_flag:
            return False
        else:
            return True 

    def filter(self):
        new_words=[]
        for word in self.vocabulary.words:
            flag=self.vocabulary.word_flag[word]
            if self.filter_word(word,flag):
                new_words.append(word)
        self.vocabulary.update_words(new_words,mode='replace')

