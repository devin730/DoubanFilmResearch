#!/usr/bin/python
# coding: utf-8

#! 这个代码并未投入生产环境


from selenium import webdriver
from time import sleep


def search(word):
    co = webdriver.ChromeOptions()
    co.headless = False
    browser = webdriver.Chrome(options=co)
    url = 'https://movie.douban.com'
    browser.get(url)
    sleep(0.5)
    browser.find_element_by_id('inp-query').send_keys(word)
    browser.find_element_by_xpath('//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input').click()
    sleep(0.5)
    rs = browser.find_elements_by_class_name('item-root')
    for r in rs:
        print("item:——————————————————————————————————————————")
        print(r.find_element_by_xpath('div[1]/div[1]/a').text)
        print(r.find_element_by_xpath('div[1]/div[2]/span[2]').text)
        print(r.find_element_by_xpath('div[1]/div[2]/span[3]').text)
        print(r.find_element_by_xpath('div[1]/div[3]').text)
        print(r.find_element_by_xpath('div[1]/div[4]').text)
        


if __name__ == '__main__':
    search('行尸走肉')

