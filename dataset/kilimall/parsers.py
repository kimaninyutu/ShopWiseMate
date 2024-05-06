import category_locators


class Parser:
    def __init__(self, soup):
        self.soup = soup

    def get_shoes(self):
        print(self.soup.find_all(category_locators.SHOES))




