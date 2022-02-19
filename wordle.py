import io
import time

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType



CONSTANTS = {
    "wordle_url": "https://www.nytimes.com/games/wordle/index.html",
    "words_csv": "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words",
    # "word_list": ["slate", "crwth"]
    "word_list": ["adieu", "golps", "crwth"]
    # "word_list":["arise","gumbo","chynd"]
    # "word_list" : ["crane","whims","fudgy","plotz"]
    # "word_list": [ "slate"],
}


incorrect_letters = set()
correct_letters = set()
counts = {}
previous_correct_letter = set()
ans_list = [".", ".", ".", ".", "."]


#####################Driver Functions#############################


def get_letter_data_state(driver_instance, grid, _):
    state = driver_instance.execute_script(
        "return arguments[0].shadowRoot.querySelector('div > game-tile:nth-child({})')".format(
            _ + 1
        ),
        grid,
    )
    data_state = state.get_attribute("evaluation")
    letter = state.get_attribute("letter")
    return letter, data_state


def get_keys(driver_instance):
    game = get_game(driver_instance)
    keyboard = game.find_element(By.TAG_NAME, "game-keyboard")
    keys = driver_instance.execute_script(
        "return arguments[0].shadowRoot.getElementById('keyboard')", keyboard
    )
    return keys


def get_board_grid(driver_instance, word):
    game = get_game(driver_instance)
    grid_row = game.find_element(By.CSS_SELECTOR, f"game-row[letters='{word}']")
    return grid_row


def get_game(driver_instance):
    game_app = driver_instance.find_element(By.TAG_NAME, "game-app")
    game = driver_instance.execute_script(
        "return arguments[0].shadowRoot.getElementById('game')", game_app
    )
    return game


def goaway_popup(driver_instance):
    driver_instance.find_element(By.TAG_NAME, "body").click()


def init_driver():
    s = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    # option.add_argument("-headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=s, options=option)
    driver.get(CONSTANTS["wordle_url"])
    time.sleep(1)
    return driver


def press_key(keys, letter):
    keys.find_element(By.CSS_SELECTOR, f'button[data-key="{letter}"]').click()


###########################################Utility Functions###############################################


def get_words_df():
    s = requests.get(CONSTANTS["words_csv"]).content
    df = pd.read_csv(io.StringIO(s.decode("utf-8")), names=["Words"], header=None)
    df["Words"] = pd.Series(df["Words"], dtype="string")
    return df["Words"]


def get_word_for_guess(Words):

    positions = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
    }

    for word in Words:
        for idx, ch in enumerate(word):
            positions[idx + 1][ch] = positions[idx + 1].get(ch, 0) + 1

    freq_distribution = 0
    word_to_send = ""
    for word in Words:
        for idx, ch in enumerate(word):
            freq_distribution += positions[idx + 1][ch]
        word_to_send = word
        break

    for word in Words:
        temp = 0
        for idx, ch in enumerate(word):
            temp += positions[idx + 1][ch]
        if temp > freq_distribution:
            freq_distribution = temp
            word_to_send = word
    return word_to_send


def play_wordle():

    Words = get_words_df()

    idx = 0
    word_to_send = CONSTANTS["word_list"][idx]
    driver = init_driver()
    goaway_popup(driver)

    for attempt in range(1, 7):

        Words = send_word_and_update_list(
            driver_instance=driver, word=word_to_send, Words=Words
        )
        ans = get_current_ans()
        if len(ans) == 5:
            time.sleep(10)
            return {"result": "success", "word": ans, "attempts": attempt}
        idx += 1
        if idx <= len(CONSTANTS["word_list"]) - 1:
            word_to_send = CONSTANTS["word_list"][idx]
        else:
            word_to_send = get_word_for_guess(Words)

        time.sleep(2)

    return {"result": "failure", "attempts": attempt}


def get_current_ans():
    ans = "".join(ans_list)
    ans = ans.replace(".", "")
    return ans


def send_word_and_update_list(driver_instance, word, Words):

    keys = get_keys(driver_instance)
    for letter in word:
        press_key(keys, letter)
        time.sleep(0.1)

    press_key(keys, "↵")
    time.sleep(2)

    grid = get_board_grid(driver_instance, word)

    for _, letter in enumerate(word):
        Words = update_words(driver_instance, Words, grid, _)

    return Words


def update_words(driver_instance, Words, grid, _):
    letter, data_state = get_letter_data_state(driver_instance, grid, _)
    counts = {}

    if data_state == "correct" or data_state == "present":
        correct_letters.add(letter)
        previous_correct_letter.add(letter)
        counts[letter] = counts.get(letter, 0) + 1
        if data_state == "correct":
            ans_list[_] = letter
        else:
            temp = [".", ".", ".", ".", "."]
            temp[_] = letter
            Words = Words[Words.str.match(r"^{}$".format("".join(temp))) == False]
    elif data_state == "absent" and (
        letter in ans_list or letter in previous_correct_letter
    ):
        temp = [".", ".", ".", ".", "."]
        temp[_] = letter
        Words = Words[Words.str.match(r"^{}$".format("".join(temp))) == False]
    elif data_state == "absent" and letter not in previous_correct_letter:
        incorrect_letters.add(letter)

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


if __name__ == "__main__":
    print(play_wordle())
