import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    presence_of_all_elements_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.wait import WebDriverWait

from etaxarchivemessagebox.config import Config
from seleniumlibraries.browser import Browser
from seleniumlibraries.web_page import WebPage


class Form(WebPage):
    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)
        xpath = "//h1[contains(text(), '帳票の表示')]"
        self.browser.wait_for(By.XPATH, xpath)
        self.browser.wait.until(presence_of_all_elements_located)
        # # Since Javascript doesn't work so quickly.
        # time.sleep(1)

    def click_select_all(self) -> None:
        xpath = "//button[text()='すべて選択']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        # # Since Javascript doesn't work so quickly.
        # time.sleep(1)

    def click_create_form(self) -> None:
        xpath = "//button[text()='帳票作成']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        # Since Javascript doesn't work so quickly.
        time.sleep(1)

    def click_yes_link(self) -> None:
        xpath = "//a[text()='はい']"
        self.browser.scroll_and_click(By.XPATH, xpath)

    def click_show(self) -> None:
        xpath = "//button[text()='表示' and not(@disabled)]"
        # This takes long time to load after clicking yes link
        method = visibility_of_element_located((By.XPATH, xpath))
        WebDriverWait(self.browser.driver, 30).until(method)
        self.browser.scroll_and_click(By.XPATH, xpath)
        # # Since download doesn't start so quick.
        # time.sleep(1)

    def cancel(self) -> None:
        xpath = "//button[text()='キャンセル']"
        self.browser.scroll_and_click(By.XPATH, xpath)

    def click_yes_button(self) -> None:
        xpath = "//button[text()='はい']"
        self.browser.scroll_and_click(By.XPATH, xpath)

    def close(self) -> None:
        xpath = "//button[text()='閉じる']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        self.browser.wait_for_closing_tab(2, 10)
        window1 = self.browser.driver.window_handles[1]
        self.browser.driver.switch_to.window(window1)


class Notification(WebPage):
    XPATH_XML = "//button[contains(text(), '保存する（XML形式）')]"
    XPATH_FORM = "//button[contains(text(), '帳票を表示する')]"
    FILE_NAME_XML = "download"

    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)
        xpath = "//h2[contains(text(), '通知内容')]"
        self.browser.wait_for(By.XPATH, xpath)
        # body = self.browser.wait_for(By.TAG_NAME, "body")
        # print(body.get_attribute("outerHTML"))
        # self.browser.driver.save_screenshot("test.png")

    def has_xml(self) -> bool:
        return bool(self.browser.driver.find_elements(By.XPATH, self.XPATH_XML))

    def save_xml(self) -> None:
        self.browser.scroll_and_click(By.XPATH, self.XPATH_XML)

    def has_form(self) -> bool:
        return bool(self.browser.driver.find_elements(By.XPATH, self.XPATH_FORM))

    def click_form(self) -> Form:
        self.browser.scroll_and_click(By.XPATH, self.XPATH_FORM)
        window2 = self.browser.driver.window_handles[2]
        self.browser.driver.switch_to.window(window2)
        return Form(self.browser)

    def close(self) -> None:
        xpath = "//button[text()='閉じる']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        self.browser.wait_for_closing_tab(1, 10)
        window0 = self.browser.driver.window_handles[0]
        self.browser.driver.switch_to.window(window0)


class MessageElement:
    def __init__(self, element: WebElement) -> None:
        self.element = element
        self.label = element.find_element(By.XPATH, ".//*[@class='label']")
        self.date = element.find_element(By.XPATH, ".//*[@class='date']")
        self.title = element.find_element(By.XPATH, ".//*[@class='ttl']")

    def click(self, browser: Browser) -> None:
        button = self.element.find_element(By.XPATH, ".//*[@role='button']")
        chains = ActionChains(browser.driver)
        chains.move_to_element(button).click().perform()


class Receipt(WebPage):
    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)
        xpath = "//h1[contains(text(), 'お知らせ・受信通知')]"
        self.browser.wait_for(By.XPATH, xpath)
        self.list_messages = self.get_list_messages()

    def get_list_messages(self) -> list[MessageElement]:
        element_list_messages = self.browser.wait_for(By.ID, "folder-box--ls")
        xpath_message = "*[contains(@class, 'folder-box--ls--one')]"
        list_element_message = element_list_messages.find_elements(
            By.XPATH, xpath_message
        )
        list_message = [MessageElement(element) for element in list_element_message]
        for message in list_message:
            print(message.label.text)
            print(message.date.text)
            print(message.title.text)
            print("")
        return list_message

    def click_tab_before_120_days_or_earlier(self) -> None:
        xpath = "//a[text()='120日以前']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        self.list_messages = self.get_list_messages()

    def click_next(self) -> None:
        xpath = "//a[@id='lnk_next']"
        self.browser.scroll_and_click(By.XPATH, xpath)
        self.list_messages = self.get_list_messages()

    def click_message(self, index: int) -> Notification:
        print(f"index: {index}")
        if index < 0 or len(self.list_messages) <= index:
            raise IndexError("Index out of range.")
        self.list_messages[index].click(self.browser)
        window1 = self.browser.driver.window_handles[1]
        self.browser.driver.switch_to.window(window1)
        return Notification(self.browser)


class ETaxHome(WebPage):
    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)
        xpath_logging_in = "//*[@id='userName' and contains(text(), 'ログイン中')]"
        self.browser.wait_for(By.XPATH, xpath_logging_in)
        self.logger.debug("Login Success.")

    def go_to_receipt(self) -> Receipt:
        xpath = "//a[*//*[contains(text(), 'お知らせ・受信通知')]]"
        self.browser.scroll_and_click(By.XPATH, xpath)
        return Receipt(self.browser)


class ETaxLogin(WebPage):
    URL = "https://login.e-tax.nta.go.jp/login/reception/loginCorporate"

    def __init__(self, browser: Browser) -> None:
        super().__init__(browser)
        self.logger.debug("Start Chrome Driver.")
        self.browser.driver.get(self.URL)

    def login(self, user_id: str, password: str) -> ETaxHome:
        self.logger.debug("Login to e-tax.")
        self.browser.wait_for(By.ID, "oStUserId").send_keys(user_id)
        self.browser.wait_for(By.ID, "oStPassword").send_keys(password)
        self.click_login_button()
        dialog = self.browser.wait.until(
            visibility_of_element_located(
                (By.XPATH, "//*[p/text()='動作環境チェック']")
            )
        )
        dialog.find_element(By.XPATH, "//a[contains(text(), '次へ')]").click()
        self.click_login_button()
        return ETaxHome(self.browser)

    def click_login_button(self) -> None:
        # Since login button can't be clicked due to following error:
        #   selenium.common.exceptions.ElementNotInteractableException: Message: element not interactable: [object HTMLButtonElement] has no size and location
        #     (Session info: chrome=135.0.7049.95)
        element_password = self.browser.wait_for(By.ID, "oStPassword")
        # To prevent stale element reference: stale element not found:
        # https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#stale-element-reference-exception
        actions = ActionChains(self.browser.driver)
        actions = actions.move_to_element(element_password)
        actions = actions.send_keys(Keys.TAB + Keys.TAB)
        actions = actions.pause(0.25)
        actions = actions.send_keys(Keys.ENTER)
        actions.perform()


class MessageDirectory:
    def __init__(self, root_directory: Path, message: MessageElement) -> None:
        self.name = self.build_name(message)
        self.path = self.determine_path(root_directory)
        self.path.mkdir(parents=True, exist_ok=True)

    def build_name(self, message: MessageElement) -> str:
        date = message.date.text.replace("/", "-")
        label = message.label.text
        title = message.title.text
        return f"{date}-{label}-{title}"

    def determine_path(self, root_directory: Path) -> Path:
        path = root_directory / self.name
        index = 1
        while path.exists():
            index += 1
            path = root_directory / f"{self.name}-{str(index)}"
        return path

    def move_xml_to_message_directory(self) -> None:
        path_xml = self.path.parent / Notification.FILE_NAME_XML
        shutil.move(path_xml, self.destination_xml)

    def move_form_to_message_directory(self) -> None:
        list_pdf = list(self.path.parent.glob("*.pdf"))
        if len(list_pdf) == 0:
            return
        if len(list_pdf) > 1:
            raise RuntimeError("More than one PDF file found.")
        form = list_pdf[0]
        shutil.move(form, self.destination_form)

    @property
    def destination_xml(self) -> Path:
        return self.path / f"{self.name}-受信データ.xtx"

    @property
    def destination_pdf(self) -> Path:
        return self.path / f"{self.name}.pdf"

    @property
    def destination_form(self) -> Path:
        return self.path / f"{self.name}-帳票.pdf"


class DownloadDirectory:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.resolve()
        self.path.mkdir(parents=True, exist_ok=True)
        print(f"Download directory: {self.path}")

    def create_message_directory(self, message: MessageElement) -> MessageDirectory:
        message_directory = MessageDirectory(self.path, message)
        return message_directory


@dataclass
class Message:
    directory: MessageDirectory
    notification: Notification

    def archive(self) -> None:
        if self.notification.has_xml():
            print("XML file found.")
            self.save_xml()
        self.notification.browser.save_as_pdf(self.directory.destination_pdf)
        if self.notification.has_form():
            print("Form file found.")
            self.save_form()
        self.notification.close()

    def save_xml(self) -> None:
        self.notification.save_xml()
        self.notification.browser.wait_for_download(20)
        self.directory.move_xml_to_message_directory()

    def save_form(self) -> None:
        form = self.notification.click_form()
        form.click_select_all()
        form.click_create_form()
        form.click_yes_link()
        form.click_show()
        form.cancel()
        form.click_yes_button()
        form.close()
        self.directory.move_form_to_message_directory()


class MessageBoxArchiver:
    def __init__(self, browser: Browser) -> None:
        # browser.driver.get("https://google.com")
        login = ETaxLogin(browser)
        home = login.login(**Config().login)
        receipt = home.go_to_receipt()
        receipt.click_tab_before_120_days_or_earlier()
        receipt.click_next()
        self.receipt = receipt
        self.directory = DownloadDirectory(self.receipt.browser.DIRECTORY_DOWNLOAD)

    def archive(self) -> None:
        for index, message in enumerate(self.receipt.list_messages):
            directory = self.directory.create_message_directory(message)
            notification = self.receipt.click_message(index)
            Message(directory, notification).archive()
