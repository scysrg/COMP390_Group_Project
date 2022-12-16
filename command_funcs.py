import scrapping_funcs


def scrap_6_keywords():
    scrap_command('Over Ear Headphones', 20)
    scrap_command('USB Microphones',7)
    scrap_command('1080p Webcams', 20)
    scrap_command('Capture Cards', 20)
    scrap_command('8-channel Audio Mixers', 7)
    scrap_command('Gaming Laptops', 20)


def scrap_command(keywords: str, pages: int):
    # data_out_file = open('data_output.txt', 'w', encoding='UTF-8')

    for i in range(1, pages+1):
        print(i)
        search_url = scrapping_funcs.get_target_url(i, keywords)
        search_results = scrapping_funcs.get_one_page(search_url)
        scrapping_funcs.get_data_from_results(search_results)



# Over Ear Headphones
# USB Microphones
# 1080p Webcams
# Capture Cards
# 8-channel Audio Mixers
# Gaming Laptops
