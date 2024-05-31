class ProductsLocators:
    SEARCH_RESULTS = "div[class*='-paxs row _no-g _4cl-3cm-shs']"
    PRODUCT_LOCATOR = "article[class*='prd _fb col c-prd']"
    PRODUCT_NAME = "h3[class*='name']"
    PRODUCT_PRICE = "div[class*='prc']"
    PRODUCT_OLD_PRICE = "div[class*='old']"  # CSS selector for old price
    PRODUCT_LINK = "a.core"
    PRODUCT_IMAGE = "img"
    PRODUCT_RATING = "div[class*='bdg _glb _xs']"  # Adjust this if the rating locator is different
