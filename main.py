from etaxarchivemessagebox import MessageBoxArchiver
from seleniumlibraries.browser import Browser

if __name__ == "__main__":
    with Browser() as browser:
        message_box_archiver = MessageBoxArchiver(browser)
        message_box_archiver.archive()
