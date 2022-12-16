import scrapping_funcs
from scrapping_funcs import get_last_page

key_words_list= ['Over Ear Headphones', 'USB Microphones', '1080p Webcams', 'Capture Cards', '8-channel Audio Mixers', 'Gaming Laptops']


def scrap_6_keywords():
    for key_words in key_words_list:
        scrap_command(key_words, get_last_page(key_words))


def scrap_command(keywords: str, pages: int):
    # data_out_file = open('data_output.txt', 'w', encoding='UTF-8')

    for i in range(1, pages+1):
        # print(i)
        search_url = scrapping_funcs.get_target_url(i, keywords)
        search_results = scrapping_funcs.get_one_page(search_url)
        scrapping_funcs.get_data_from_results(search_results)



# Over Ear Headphones
# USB Microphones
# 1080p Webcams
# Capture Cards
# 8-channel Audio Mixers
# Gaming Laptops
