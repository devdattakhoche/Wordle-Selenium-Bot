import io
from collections import Counter

import pandas as pd
import requests

CONSTANTS = {
    "wordle_url": "https://www.nytimes.com/games/wordle/index.html",
    "words_csv": "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words",
    "word_list": ["adieu", "glops", "crwth"],
}


incorrect_letters = set()
correct_letters = set()
previous_correct_letter = set()
counts = {}
ans_list = [".", ".", ".", ".", "."]


def wordle_game(word, guess):

    resp = ["a", "a", "a", "a", "a"]
    visited = [0, 0, 0, 0, 0]
    word_freq = Counter(word)
    freq = dict()

    for idx, letter in enumerate(guess):
        if word[idx] == letter:
            resp[idx] = "c"
            freq[letter] = freq.get(letter, 0) + 1
            visited[idx] = 1

    for idx, letter in enumerate(guess):
        if not visited[idx] and letter in word:
            if freq.get(letter, 0) < word_freq[letter]:
                resp[idx] = "p"
                freq[letter] = freq.get(letter, 0) + 1

    return "".join(resp)


###########################################Utility Functions###############################################


def get_words_df():
    s = requests.get(CONSTANTS["words_csv"]).content
    df = pd.read_csv(io.StringIO(s.decode("utf-8")), names=["Words"], header=None)
    df["Words"] = pd.Series(df["Words"], dtype="string")
    return df["Words"]


def play_wordle(original_word, Words):

    idx = 0
    word_to_send = CONSTANTS["word_list"][idx]
    for attempt in range(1, 7):
        Words = send_word_and_update_list(
            word=word_to_send, Words=Words, original_word=original_word
        )
        ans = get_current_ans()
        if len(ans) == 5:
            return {"result": "success", "word": ans, "attempts": attempt}
        idx += 1
        if idx <= len(CONSTANTS["word_list"]) - 1:
            word_to_send = CONSTANTS["word_list"][idx]
        else:
            word_to_send = get_word_for_guess(Words)

    return {"result": "failure", "attempts": attempt}


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


def get_current_ans():
    ans = "".join(ans_list)
    ans = ans.replace(".", "")
    return ans


def send_word_and_update_list(word, Words, original_word):

    resp = wordle_game(word=original_word, guess=word)

    for _, letter in enumerate(word):
        Words = update_words(Words, resp, _, letter)

    return Words


def update_words(Words, resp, _, letter):
    if resp[_] == "c":
        data_state = "correct"
    elif resp[_] == "p":
        data_state = "present"
    else:
        data_state = "absent"

    counts = {}

    if data_state == "correct" or data_state == "present":
        previous_correct_letter.add(letter)
        correct_letters.add(letter)
        counts[letter] = counts.get(letter, 0) + 1
        if data_state == "correct":
            ans_list[_] = letter
        else:
            temp = ["." for _ in range(0, 5)]
            temp[_] = letter
            Words = Words[Words.str.match(r"^{}$".format("".join(temp))) == False]
    elif data_state == "absent" and (
        letter in ans_list or letter in previous_correct_letter
    ):
        temp = ["." for _ in range(0, 5)]
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

    df = get_words_df()
    total_attempts = 0
    success = 0
    failure = 0
    count = 100
    for idx, word in enumerate(df):
        if idx == count:
            break
        resp = play_wordle(word, df)
        if resp["result"] == "success":
            total_attempts += resp["attempts"]
            success += 1
        else:
            failure += 1

        ans_list = [".", ".", ".", ".", "."]
        incorrect_letters.clear()
        correct_letters.clear()
        counts = {}

    print("Success Percentage : ", (success / count) * 100)
    print("Failure Percentage : ", (failure / count) * 100)
    print("Average Attempts : ", total_attempts / success)
