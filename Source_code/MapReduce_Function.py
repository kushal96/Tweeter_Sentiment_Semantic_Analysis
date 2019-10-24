#for opening he folders and writing files
import os

#function for splitting data into rows and columns for word counting[15]
def get_word_count_list(file_path, words_list):#[19]
    words_found = []

    try:
        src = open(file_path)

        for tweet in src:#[17]
            column = tweet.split(",")
            for word in words_list:
                for cell in column:
                    for word in cell:
                        cnt = cell.count(word)
                        for i in range(cnt):
                            words_found.append(word)
        
    finally:
        src.close()

    return words_found


#function which is called for finding word frequency
def get_word_count(file_path, save_file_as):#[15]
    my_words_list = ["oil", "vehicle", "university", "dalhousie","expensive", "good school", "bad school","population", "bus", "agriculture","economy"]
    #[18]
    words_in_tweet = get_word_count_list(file_path, my_words_list)#[16]
    spk_prll = spark.sparkContext.parallelize(words_in_tweet)#[21][22]
    #for mapping the words which are found
    mapped_words = spk_prll.map(lambda x: (x, 1))#[20]
    #reduces the word count in given data
    reduced_word_cnt = mapped_words.reduceByKey(lambda x, y: x + y)#[20]
    reduced_word_cnt.collect()#[22]
    #stores the frequency counts of given words into text file[20]
    reduced_word_cnt.coalesce(1).saveAsTextFile(save_file_as)



if __name__ == '__main__':
    get_word_count("/home/ubuntu/Assignment_2_data/searchedtweets.csv", "searched_tweets_wordcount.txt")
    #opening 1 article folder
    src_folder = "/home/ubuntu/Assignment_2_data/020/"
    for article in os.listdir(src_folder):
        #storing the word count
        get_word_count(src_folder + article, "020" + article + "_wordCount.txt")

    # opening 1 article folder
    src_folder = "/home/ubuntu/Assignment_2_data/021/"
    for article in os.listdir(src_folder):
        #storing the word count
        get_word_count(src_folder + article, "021" + article + "_wordCount.txt")

    
##    get_word_count("/home/ubuntu/Assignment-2/reut2-020.sgm", "020SGM_WordCount.txt")
##    get_word_count("/home/ubuntu/Assignment-2/reut2-021.sgm", "021SGM_WordCount.txt")
    
