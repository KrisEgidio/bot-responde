from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


class MissionPage(BasePage):
    games = ['mpb', 'pop', 'sertanejo', 'trends', 'rock', 'nectar']

    ### XPATH ###
    btn_quiz_xpath = "//a[@href='/games/quiz/{}']"
    btn_option_xpath = "//p[contains(text(), '{}')]"

    ### URLS ###
    home_url = "https://www.tacaoplayumusic.com/"

    ### LOCATORS ###
    btn_login_locator = (By.XPATH, "//a[@href='/api/v1/spotify/login?to=redirect']")
    btn_games_locator = (By.XPATH, "//a[@href='/games']")
    question_locator = (By.XPATH, "//*[@id='__layout']/div/main/div/div[3]/div[1]/p")
    options_locator = (By.XPATH, "//p[@class='flex-1 ml-4 text-xs tracking-wide md:text-lg text-neutral-700']")
    btn_confirm_locator = (By.XPATH, "//button[contains(text(), 'confirmar')]")

    def __init__(self, webdriver):
        super().__init__(webdriver)

    def wait_login(self):
        try:
            self.webdriver.get(self.home_url)
            self.wait_clickable_element(5, self.btn_login_locator).click()
        except (TimeoutException, NoSuchElementException) as e:
            pass

    def go_to_available_mission(self):
        for game in self.games:
            self.wait_visible_element(5, self.btn_games_locator).click()
            btn_quiz = self.btn_quiz_xpath.format(game)
            self.wait_visible_element(5, (By.XPATH, btn_quiz)).click()
            break
            # TO DO: colocar aqui se a opção de missão completa apareceu

    def solve_mission(self):
        next_question_exists = True
        while next_question_exists:
            question = self.get_question_options()
            # TO DO: obter a resposta via api
            self.select_answer("Mudaram as estações, nada mudou")
            self.wait_clickable_element(3, self.btn_confirm_locator).click()
            # TO DO: validar se a próxima questão existe

    def get_question_options(self):
        question = self.wait_visible_element(10, self.question_locator).text
        options = '; '.join([option.text for option in self.find_elements(self.options_locator)])
        return f"Pergunta: {question}; Opções: {options}"

    def select_answer(self, answer):
        btn_option = self.btn_option_xpath.format(answer.strip())
        self.wait_visible_element(3, (By.XPATH, btn_option)).click()
