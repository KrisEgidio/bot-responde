from src.utils.logger import Logger
from src.pages.base_page import BasePage
from src.utils.api_requests import APIRequests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class MissionPage(BasePage):
    games = ['mpb', 'pop', 'sertanejo', 'trends', 'rock', 'nectar']

    ### XPATH ###
    btn_quiz_xpath = "//a[@href='/games/quiz/{}']"
    btn_option_xpath = "//p[contains(text(), '{}')]"

    ### URLS ###
    home_url = "https://www.tacaoplayumusic.com/"
    login_url = "https://www.tacaoplayumusic.com/api/v1/spotify/login?to=redirect"

    ### LOCATORS ###
    btn_login_locator = (By.XPATH, "//a[@href='/api/v1/spotify/login?to=redirect']")
    btn_games_locator = (By.XPATH, "//a[@href='/games']")
    question_locator = (By.XPATH, "//*[@id='__layout']/div/main/div/div[3]/div[1]/p")
    options_locator = (By.XPATH, "//p[@class='flex-1 ml-4 text-xs tracking-wide md:text-lg text-neutral-700']")
    btn_confirm_locator = (By.XPATH, "//button[contains(text(), 'confirmar')]")
    modal_mission_locator = (By.XPATH, "//p[contains(text(), 'Missão de hoje já foi feita!')]")
    total_coins_locator = (By.XPATH, "//a[@href='/perfil/resgates']//b")

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.logger = Logger()
        self.logger_decorated = Logger(decorated=True)

    def wait_login(self):
        try:
            self.webdriver.get(self.login_url)
            self.wait_clickable_element(5, self.btn_login_locator).click()
        except (TimeoutException, NoSuchElementException) as e:
            pass

    def go_to_available_mission(self):
        for game in self.games:
            self.wait_visible_element(5, self.btn_games_locator).click()
            btn_quiz = self.btn_quiz_xpath.format(game)
            self.wait_visible_element(5, (By.XPATH, btn_quiz)).click()
            self.logger_decorated.info("MISSÃO DISPONÍVEL")
            try:
                self.wait_visible_element(3, self.modal_mission_locator)
                self.logger.error("Ops! A missão de hoje já foi realizada! Tente novamente amanhã!")
                raise RuntimeError()
            except (TimeoutException, NoSuchElementException) as e:
                self.logger.info(game.upper())
                break

    def solve_mission(self):
        next_question_exists = True
        while next_question_exists:
            question = self.get_question_options()
            api_requests = APIRequests()
            answer = api_requests.send_question(question).get('response')
            self.select_answer(answer)
            try:
                self.wait_clickable_element(3, self.btn_confirm_locator).click()
            except (TimeoutException, NoSuchElementException) as e:
                next_question_exists = False

    def get_question_options(self):
        question = self.wait_visible_element(10, self.question_locator).text
        options = '; '.join([option.text for option in self.find_elements(self.options_locator)])
        self.logger_decorated.info("PERGUNTA")
        self.logger.info(question)
        self.logger_decorated.info("OPÇÕES")
        for option in self.find_elements(self.options_locator):
            self.logger.info(f"- {option.text}")
        return f"Pergunta: {question}; Opções: {options}"

    def select_answer(self, answer):
        btn_option = self.btn_option_xpath.format(answer.strip())
        self.wait_visible_element(3, (By.XPATH, btn_option)).click()
        self.logger_decorated.info("RESPOSTA")
        self.logger.info(f"- {answer}")

    def get_total_coins(self):
        coins = self.wait_presence_element(5, self.total_coins_locator).text
        self.logger_decorated.info("SALDO TOTAL")
        self.logger.info(coins)
