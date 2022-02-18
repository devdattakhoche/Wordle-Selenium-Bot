import io
import random
import time

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

incorrect_letters = set()
correct_letters = set()
counts = {}
ans_list = [".", ".", ".", ".", "."]


def init_driver():

    wordle_url = "https://www.nytimes.com/games/wordle/index.html"
    s = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=option)
    driver.get(wordle_url)
    time.sleep(1)
    return driver


def get_words_df():
    url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode("utf-8")), names=["Words"], header=None)
    df["Words"] = pd.Series(df["Words"], dtype="string")
    return df["Words"]


def goaway_popup(driver_instance):
    driver_instance.find_element(By.TAG_NAME, "body").click()


def update_df(Words):
    if len(incorrect_letters):
        for letter in incorrect_letters:
            Words = Words[Words.str.contains(letter) == False]
    if len(correct_letters):
        for letter in correct_letters:
            Words = Words[Words.str.contains(letter) == True]
    if "".join(ans_list) != ".....":
        Words = Words[Words.str.match(r"{}".format("".join(ans_list))) == True]

    incorrect_letters.clear()
    correct_letters.clear()

    for key, value in counts.items():
        if value >= 2:
            Words = Words[Words.str.count(key) == value]

    return Words


def play_wordle():

    Words = get_words_df()
    word_list = ["golps", "crwth","adieu"]
    idx = 0
    word_to_send = word_list[idx]
    driver = init_driver()
    goaway_popup(driver)

    for attempt in range(1, 7):

        Words = send_word_and_update_list(
            driver_instance=driver, word=word_to_send, Words=Words
        )
        Words = update_df(Words)
        ans = "".join(ans_list)
        ans = ans.replace(".", "")
        if len(ans) == 5:
            return {"result": "success", "word": ans, "attempts": attempt}
        idx += 1
        if idx <= len(word_list) - 1:
            word_to_send = word_list[idx]
        else:
            word_to_send = Words.iloc[random.randint(0, len(Words) - 1)]

        time.sleep(2)

    return {"result": "error"}


def get_keys(driver_instance):
    game_app = driver_instance.find_element(By.TAG_NAME, "game-app")
    game = driver_instance.execute_script(
        "return arguments[0].shadowRoot.getElementById('game')", game_app
    )
    keyboard = game.find_element(By.TAG_NAME, "game-keyboard")
    keys = driver_instance.execute_script(
        "return arguments[0].shadowRoot.getElementById('keyboard')", keyboard
    )
    return keys


def get_board_grid(driver_instance, word):
    game_app = driver_instance.find_element(By.TAG_NAME, "game-app")
    game = driver_instance.execute_script(
        "return arguments[0].shadowRoot.getElementById('game')", game_app
    )
    grid_row = game.find_element(By.CSS_SELECTOR, f"game-row[letters='{word}']")
    return grid_row


def send_word_and_update_list(driver_instance, word, Words):

    keys = get_keys(driver_instance)
    for letter in word:
        keys.find_element(By.CSS_SELECTOR, f'button[data-key="{letter}"]').click()
        time.sleep(0.1)

    keys.find_element(By.CSS_SELECTOR, 'button[data-key="↵"]').click()
    time.sleep(2)
    grid = get_board_grid(driver_instance, word)
    for _, letter in enumerate(word):

        state = driver_instance.execute_script(
            "return arguments[0].shadowRoot.querySelector('div > game-tile:nth-child({})')".format(
                _ + 1
            ),
            grid,
        )
        data_state = state.get_attribute("evaluation")
        letter = state.get_attribute("letter")
        counts = {}
        if data_state == "correct" or data_state == "present":
            correct_letters.add(letter)
            counts[letter] = counts.get(letter, 0) + 1
            if data_state == "correct":
                ans_list[_] = letter
            else:
                temp = [".", ".", ".", ".", "."]
                temp[_] = letter
                Words = Words[Words.str.match(r"^{}$".format("".join(temp))) == False]
        elif data_state == "absent" and letter in ans_list:
            temp = [".", ".", ".", ".", "."]
            temp[_] = letter
            Words = Words[Words.str.match(r"^{}$".format("".join(temp))) == False]
        elif data_state == "absent":
            incorrect_letters.add(letter)
    return Words


print(play_wordle())
