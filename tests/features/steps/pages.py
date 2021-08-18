import time
from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    search_box_id = "twotabsearchtextbox"
    search_icon_id = "nav-search-submit-button"
    user_name_id = "user-menu > a"
    accept_cookies_id = "sp-cc-accept"
    accept_cookies_name = "accept"
    language_dropdown_xpath = "//span[@class='icp-nav-flag icp-nav-flag-de']"
    english_button_xpath = "(//*[@class='a-label a-radio-label'])[2]"
    english_radio_btn_xpath = "//*[@value='en_GB']"
    save_btn_name = "a-button-input"

    def __init__(self, driver):
        self.driver = driver

    def input_to_search(self, user_input):

        self.driver.find_element_by_id(self.search_box_id).send_keys(user_input)

    def click_search_icon(self):
        self.driver.find_element_by_id(self.search_icon_id).click()

    def click_language_dropdown(self):
        self.driver.find_element_by_xpath("//span[@class='icp-nav-flag icp-nav-flag-de']").click()

    def get_english_radio_btn(self):
        return self.driver.find_element_by_xpath(self.english_radio_btn_xpath)

    def click_english_btn(self):
        self.driver.find_element_by_xpath("(//*[@class='a-label a-radio-label'])[2]").click()

    def accept_cookies_click(self):
        # wait = WebDriverWait(self.driver, 10)
        # accept = wait.until(EC.element_to_be_clickable((By.NAME, "accept")))
        self.driver.find_element_by_id(BasePage.accept_cookies_id).click()

    def save_btn_click(self):
        self.driver.find_element_by_class_name("a-button-input").click()

    def selectLanguage(self):
        time.sleep(3)
        self.click_language_dropdown()

        english_selected = self.get_english_radio_btn().is_selected()
        print(english_selected)
        if english_selected:
            self.save_btn_click()
        else:
            self.click_english_btn()
            time.sleep(1)
            english_selected = self.get_english_radio_btn().is_selected()
            print(english_selected)
            self.save_btn_click()
            time.sleep(1)


class DashBoardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


class ProductDetailPage(BasePage):
    subtitle_id = "productTitle"
    price_block_id = "priceblock_ourprice"
    add_to_basket_btn_id = "add-to-cart-button"

    def __init__(self, driver):
        super().__init__(driver)

    def get_page_subtile(self):
        subtitle = self.driver.find_element_by_id(self.subtitle_id)
        return subtitle.subtile

    def get_price(self):
        return self.driver.find_element_by_id(self.price_block_id)

    def add_to_basket_btn_click(self):
        self.driver.find_element_by_id(self.add_to_basket_btn_id).click()


class SearchedProductPage(BasePage):
    sort_by_dropdown_xpath = "//*[@class='a-button-text a-declarative']"
    products_class_name = "[class='a-section a-spacing-none']"
    low_to_high_option_xpath = "(//*[text()='Price: Low to High'])[2]"

    def __init__(self, driver):
        super().__init__(driver)

    def sort_by_dropdown_click(self):
        self.driver.find_element_by_xpath(self.sort_by_dropdown_xpath).click()

    def get_products(self):
        self.driver.implicitly_wait(10)
        return self.driver.find_elements_by_css_selector(self.products_class_name)

    def low_to_high_option_click(self):
        self.driver.find_element_by_xpath(self.low_to_high_option_xpath).click()

    def click_option(self):
        self.driver.implicitly_wait(2)
        self.low_to_high_option_click()
        self.driver.implicitly_wait(4)

    def lowestPrice(self, product_name):
        product_with_lowest_price = {}
        valid_product_index = []
        products = self.get_products()

        for i in products:
            print(i.text)

        print(product_name)
        for i in range(len(products)):
            if "€" in products[i].text and "prime" not in products[i].text.lower() and product_name.lower() in products[
                i].text.lower():
                valid_product_index.append(i)

        print(valid_product_index)

        lowest_product_name = self.driver.find_element_by_xpath(
            "(//div[@class='a-section a-spacing-none'])[" + str((valid_product_index[0] + 1)) + "]//h2//span")
        lowest_product_price = self.driver.find_element_by_xpath("(//div[@class='a-section a-spacing-none'])[" + str(
            (valid_product_index[1] + 1)) + "]//span[@class='a-price-whole']")
        print(lowest_product_name.text)
        print(lowest_product_price.text)
        product_with_lowest_price["name"] = lowest_product_name.text
        product_with_lowest_price["price"] = lowest_product_price.text
        lowest_product_price.click()
        return product_with_lowest_price


class ShoppingBasketPage(BasePage):
    basket_btn_id = "hlb-view-cart-announce"
    subtitle_xpath = " //h1"
    product_prices_xpath = "//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap sc-product-price " \
                           "a-text-bold'] "
    total_product_prices_xpath = "//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap']"
    checkout_btn_name = "proceedToRetailCheckout"

    def __init__(self, driver):
        super().__init__(driver)

    def basket_btn_click(self):
        self.driver.find_element_by_id(self.basket_btn_id).click()

    def get_subtitle(self):
        return self.driver.find_element_by_xpath(self.subtitle_xpath)

    def get_product_prices(self):
        return self.driver.find_element_by_xpath(self.product_prices_xpath)

    def checkout_btn_click(self):
        self.driver.find_element_by_name(self.checkout_btn_name)

    def get_total_prices(self):
        return self.driver.find_element_by_xpath(self.total_product_prices_xpath)

    # /**
    #  * check if expected total price equals to actual total price
    #  *
    #  * @return boolean
    #  */

    def check_total_price(self):
        # prices_string = []
        prices_string = self.get_element_text(self.get_product_prices())
        total_price = 0
        for price in prices_string:
            # //when we calculate,we do not need "€" sign,hence we start from first index to exclude €
            price_in_double = Decimal(price[1:])
            total_price += price_in_double

        expected_price = self.total_product_prices[0].text
        expected_total_price = Decimal(expected_price[1:])
        if total_price == expected_total_price:
            return True
        else:
            return False

    @staticmethod
    def get_element_text(product_prices):
        product_prices_text = []

        for pp in product_prices:
            product_prices_text.append(pp.text)

        return product_prices_text
