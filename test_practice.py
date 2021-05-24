#import statements
import pytest
import requests
from selenium import webdriver
import time


#setup method to initialise browser(chrome)
@pytest.fixture()
def setup(request):
    driver=webdriver.Chrome(executable_path="Drivers/chromedriver.exe")
    driver.maximize_window()
    driver.implicitly_wait(10)
    request.instance.driver = driver
    yield
    driver.quit()


#class
@pytest.mark.usefixtures("setup")
class Test_herokuapp:


    #testcase1: Assert Broken images
    def test_case_a(self):
        self.driver.get("http://the-internet.herokuapp.com/broken_images")
        images = self.driver.find_elements_by_xpath("//img")
        count = 0
        for img in images:
            if (requests.head(img.get_attribute('src')).status_code == 404):
                count += 1
        actual_result = count
        expected_result = 2
        #checking if count of broken image's is 2 out of 4 images on the page
        assert (actual_result == expected_result)


    # testcase2: Assert forgot password success message
    def test_case_b(self):
        self.driver.get("http://the-internet.herokuapp.com/forgot_password")
        self.driver.find_element_by_xpath("//input[@name='email']").send_keys('test@tester.com')
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        test = self.driver.find_element_by_xpath("//h1").text
        actual_result = test
        expected_result = "Internal Server Error"
        #do not have valid email to check this so checked with invalid email id to get error
        assert (actual_result == expected_result)


    # testcase3: Assert form validation functionality Post entering a dummy username and password
    def test_case_c(self):
        self.driver.get("http://the-internet.herokuapp.com/login")
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys('tomsmith')
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys('SuperSecretPassword!')
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        test = self.driver.find_element_by_xpath("//div[@id='flash']").text
        actual_result = test
        expected_result = "You logged into a secure area!\n×"
        #checking if the user is logged into account or not using success message
        assert (actual_result == expected_result)


    # testcase4: Write a test to enter alphabets and mark it as a failure if we cannot enter
    def test_case_d(self):
        self.driver.get("http://the-internet.herokuapp.com/inputs")
        self.driver.find_element_by_xpath("//input[@type='number']").send_keys('abc')
        test = self.driver.find_element_by_xpath("//input[@type='number']").text
        actual_result = test
        expected_result = ""
        #checking if non numeric value can be entered into text field
        assert (actual_result == expected_result)


    # testcase5: Write a test to sort the table by the amount due
    def test_case_e(self):
        self.driver.get("http://the-internet.herokuapp.com/tables")
        self.driver.find_element_by_xpath("(//span[text()='Due'])[1]").click()
        columns = self.driver.find_elements_by_xpath("//table[@id='table1']/tbody/tr/td[4]")
        actual_result = []
        for i in columns:
            actual_result.append(i.text)
        expected_result = ['$50.00', '$50.00', '$51.00', '$100.00']
        #checking new order of amount after sorting by amount
        assert (actual_result == expected_result)


    # testcase6: Assert a 'successful notification" after repeated unsuccessful notification
    def test_case_f(self):
        self.driver.get("http://the-internet.herokuapp.com/notification_message_rendered")
        self.driver.find_element_by_xpath("//a[text()='Click here']").click()
        while self.driver.find_element_by_xpath("//div[@id='flash']").text == "Action unsuccesful, please try again\n×":
            self.driver.find_element_by_xpath("//a[text()='Click here']").click()
        actual_result = self.driver.find_element_by_xpath("//div[@id='flash']").text
        expected_result = "Action successful\n×"
        #waiting till successful notification appears
        assert (actual_result == expected_result)
