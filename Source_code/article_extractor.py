#importing important libraries
import os
import re

#function which opens the files and extracts the articles using <Text> tags
def get_articles(sgm_file_path):
    sgmfile = open(sgm_file_path)
    sgmdata = sgmfile.read()
    #[14]
    articles = re.findall(r"<TEXT>(.*?)</TEXT>", sgmdata, re.DOTALL)

    return articles

#function which makes separate folders writes the extracted articles
def save_articles(articles, folder_name):
    os.mkdir(folder_name)
    cnt = 0
    for article in articles:
        cnt = cnt + 1
        new_file_path = folder_name + '//' + 'article_' + str(cnt) + '.txt'

        with open(new_file_path, 'w') as new_file:
            new_file.write(article)

#function for calling function for geeitng articles from source file and calling save function
def extract_and_save(source_file, folder_name):
    articles = get_articles(source_file)
    save_articles(articles, folder_name)


if __name__ == '__main__':
    #------------------------------------------------------
    # For File "reut2-020.sgm"
    #------------------------------------------------------
    source_file = 'reut2-020.sgm'
    folder_name = '020'


    extract_and_save(source_file, folder_name)
    #-------------------------------------------------------

    #------------------------------------------------------
    # For File "reut2-021.sgm"
    #------------------------------------------------------
    source_file = 'reut2-021.sgm'
    folder_name = '021'
    #function calling
    extract_and_save(source_file, folder_name)
    #-------------------------------------------------------
