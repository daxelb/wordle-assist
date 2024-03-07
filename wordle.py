from english_words import english_words_lower_alpha_set
from wordfreq import zipf_frequency
from enum import Enum
from collections import Counter

from itertools import product
from tqdm import tqdm

from functools import partial
import multiprocessing as mp

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
N = 5


class Wordle:
    def __init__(self, min_frequency=1):
        self.cant_include = set()
        self.known = set()
        self.must_include = set()
        self.letter_options = [list(ALPHABET) for _ in range(N)]
        self.N_letter_words = get_N_letter_words_with_min_frequency(min_frequency)

    def add_guess(self, guess):
        assert len(guess) == N, f"Guess '{guess}' must be of length {N}."

        for i, letter_status_tuple in enumerate(guess):
            letter, status = letter_status_tuple

            if status == 0:
                self.cant_include.add(letter)
                for word_letter in self.letter_options:
                    if letter in word_letter:
                        word_letter.remove(letter)

            if status == 1:
                self.must_include.add(letter)
                if letter in self.letter_options[i]:
                    self.letter_options[i].remove(letter)

            if status == 2:
                self.must_include.add(letter)
                self.known.add(letter)
                self.letter_options[i] = [letter]

    def good_guess(self, win=False):
        letter_frequency = Counter()

        for word in self.guess_by_freq(0):
            for letter in word:
                letter_frequency[letter] += 1

        for letter in sorted(letter_frequency, key=letter_frequency.get, reverse=True):
            print(letter, letter_frequency[letter])

        word_scores = dict()
        for word in self.N_letter_words:
            score = 0
            for letter in set(word):
                score += letter_frequency[letter]

            word_scores[word] = score

        for i, word in enumerate(
            sorted(word_scores, key=word_scores.get, reverse=True)
        ):
            if i > 10:
                break
            print(word, word_scores[word])

    def guess_by_freq(self, lim):
        """
        Returns guesses filtered by their Zipf frequency, above a specified limit.
        """
        guesses = {}
        for word in self.N_letter_words:
            if not self.is_valid_guess(word):
                continue

            # Otherwise, check the Zipf frequency of the word
            freq = zipf_frequency(word, "en")
            if freq > lim:
                guesses[word] = freq

        return guesses

    def is_valid_guess(self, guess):
        # Check if all must_include letters are in the word
        if not self.must_include.issubset(set(guess)):
            return False
        # Check if word can be formed from self.letter_options
        if not all(
            letter in options for letter, options in zip(guess, self.letter_options)
        ):
            return False
        return True

    def print_guesses(self, freq):
        guesses = self.guess_by_freq(freq)
        for guess in sorted(guesses, key=guesses.get, reverse=True):
            print(guess, guesses[guess])


def get_N_letter_words(return_type=set):
    """
    Returns a set of five letter english words
    """
    assert return_type in (set, list)
    res = [word for word in english_words_lower_alpha_set if len(word) == N]
    if return_type == list:
        return res
    elif return_type == set:
        return set(res)
    else:
        raise ValueError("return_type must be set or list")


def get_N_letter_words_with_min_frequency(min_frequency, return_type=set):
    """
    Returns five-letter English words with a Zipf frequency greater than `min_frequency`.
    """
    five_letter_words = get_N_letter_words(return_type=list)
    res = [
        word for word in five_letter_words if zipf_frequency(word, "en") > min_frequency
    ]
    if return_type == list:
        return res
    elif return_type == set:
        return set(res)
    else:
        raise ValueError("return_type must be set or list")


def make_guess(guess, answer):
    word_score = list()
    for i in range(N):

        if guess[i] == answer[i]:
            score = 2
        elif guess[i] in answer:
            score = 1
        else:
            score = 0

        word_score.append((guess[i], score))
    return word_score


if __name__ == "__main__":
    wordle = Wordle()
    wordle.add_guess([("s", 0), ("n", 1), ("o", 2), ("r", 0), ("t", 0)])
    wordle.add_guess([("a", 0), ("l", 2), ("o", 2), ("n", 2), ("e", 2)])
    # wordle.add_guess({"a": 0, "l": 2, "o": 2, "n": 2, "e": 2})
    wordle.print_guesses(0)
    wordle.good_guess()
    # print(make_guess('later', 'ultra'))
