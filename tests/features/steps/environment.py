from selenium import webdriver


def before_all(context):
    web = context.config.userdata['browser']

    context.web = web
