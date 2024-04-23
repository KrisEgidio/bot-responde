from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.pages.mission_page import MissionPage
import os


def kill_edge():
    os.system("taskkill /f /im msedge.exe >nul 2>&1")


def config_webdriver():
    kill_edge()
    options = Options()
    user_data_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Microsoft\\Edge\\User Data"
    options.add_argument(f"user-data-dir={user_data_dir}")
    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=options)


def main():
    driver = config_webdriver()

    try:
        # Inicializando Page Objects
        mission_page = MissionPage(driver)
        mission_page.wait_login()
        mission_page.go_to_available_mission()
        mission_page.solve_mission()

    except Exception as e:
        print(f"Ocorreu um erro durante a execução do bot: {e}")
    finally:
        # Encerrando o WebDriver
        driver.quit()


if __name__ == "__main__":
    main()
