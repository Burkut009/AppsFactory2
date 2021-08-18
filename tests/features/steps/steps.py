import time
import unittest
from selenium import webdriver
from behave import *
import unittest as ut

from tests.features.steps.pages import BasePage, DashBoardPage, ProductDetailPage, SearchedProductPage, \
    ShoppingBasketPage


@given(u'user is on the Amazon home page')
def go_to_home_page(context):
    print("This is step 1")

    time.sleep(3)
    context.driver = webdriver.Chrome(
        executable_path=r"D:\javascriptpractice\AppsFactory1\tests\utilities\chromedriver.exe")
    context.driver.maximize_window()
    context.driver.get(context.config.userdata['url'])

    basePage = BasePage(context.driver)
    global dashBoardPage
    dashBoardPage = DashBoardPage(context.driver)
    global productDetailPage
    productDetailPage = ProductDetailPage(context.driver)
    global searchProductPage
    searchProductPage = SearchedProductPage(context.driver)
    global shoppingBasketPage
    shoppingBasketPage = ShoppingBasketPage(context.driver)

    # context.driver.switch_to_alert().accept()
    basePage.accept_cookies_click()
    print("This is end of step 1")


@given(u'user selects English language')
def select_english(context):
    print("This is step 2")
    dashBoardPage.selectLanguage()


@when(u'user enters "{user_input}" in the searchBox')
def search_a_word(context, user_input):
    print("This is step 3")
    global global_productName
    global_productName = user_input
    dashBoardPage.input_to_search(user_input)


@when(u'user clicks search icon')
def click_search_icon(context):
    print("This is step 4")
    dashBoardPage.click_search_icon()


@then(u'user is on the searched product result page')
def searched_result_page(context):
    print("This is step 5")

    assert True, global_productName in context.driver.title
    # assert global_productName in context.driver.title is True


@when(u'user clicks Sort by dropDown')
def click_sort(context):
    print("This is step 6")

    searchProductPage.sort_by_dropdown_click()


@when(u'user selects Price: Low to High option')
def low_to_high(context):
    print("This is step 7")
    searchProductPage.click_option()


@when(u'user selects the searched product with lowest price')
def select_with_lowest_price(context):
    print("This is step 8")
    global searched_product
    searched_product = searchProductPage.lowestPrice(global_productName)
    context.driver.implicitly_wait(4)


@then(u'user is on the searched product detail page')
def searched_product_page(context):
    print("This is step 8")
    product_name = searched_product["name"]

    assert True, product_name.lower() in context.driver.title.lower()


@then(u'user should see the correct searched product details')
def correct_searched_product(context):
    print("This is step 9")
    time.sleep(2)
    ActualPageSubtitle = productDetailPage.get_page_subtile().text
    ExpectedPageSubtitle = searched_product["name"]

    assert ExpectedPageSubtitle == ActualPageSubtitle

    time.sleep(2)
    price = productDetailPage.get_price().text

    ExpectedPrice = "€" + searched_product["price"]
    print("actuial price : " + price)
    print("Expected price : " + ExpectedPrice)
    assert ExpectedPrice == price


@when(u'user clicks add to basket button')
def add_to_basket(context):
    print("This is step 10")
    productDetailPage.add_to_basket_btn_click()


@when(u'user clicks basket button')
def click_basket_btn(context):
    print("This is step 11")
    shoppingBasketPage.basket_btn_click()


@then(u'user is on the Shopping Basket page')
def shopping_basket_page(context):
    print("This is step 12")
    actualPageSubTitle = shoppingBasketPage.get_subtitle().text
    expectedPageSubTitle = "Shopping Basket"
    assert expectedPageSubTitle == actualPageSubTitle
    assert True, "Basket" in context.driver.title


@then(u'user should see the searched products')
def searched_products(context):
    print("This is step 13")
    productName = searched_product["name"]

    price = context.searched_product["price"]

    assert True, productName.lower() in context.driver.page_source.lower()
    assert True, price in context.driver.page_source.lower()


@then(u'user checks if the basket calculates the result correctly')
def check_basket_correct(context):
    print("This is step 14")
    assert True, shoppingBasketPage.check_total_price()


@when(u'clicks  checkout button')
def click_checkout_btn(context):
    print("This is step 15")
    global pageTitleBeforeCheckout
    pageTitleBeforeCheckout = context.driver.title
    shoppingBasketPage.checkout_btn_click()
    context.driver.implicitly_wait(4)


@then(u'the user gets redirected to the registration page')
def redirectio_to_registeration(context):
    print("This is step 16")
    pageTitleAfterCheckout = context.driver.title

    assert pageTitleBeforeCheckout != pageTitleAfterCheckout
    assert True, "signin" in context.driver.current_url.lower()
