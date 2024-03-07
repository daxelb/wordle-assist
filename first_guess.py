import multiprocessing as mp
from tqdm import tqdm
from functools import partial

from wordle import (
    get_N_letter_words_with_min_frequency,
    Wordle,
    make_guess,
)
from prev_answers import PREV_ANSWERS
from analyze_prev_words import get_letter_frequency, get_letter_frequency_score_of_word

UNCOMMON_LETTERS = {"k", "v", "x", "z", "j", "q"}
LETTER_FREQUENCIES = get_letter_frequency(PREV_ANSWERS)
LETTER_FREQUENCY_SCORE_THRESHOLD = 0.28
LETTER_FREQUENCY_SCORE_THRESHOLD_WITH_DUPLICATES = 0.35


def score_first_guess(guess, answers, frequency=0):
    score = 0

    for answer in answers:
        wordle = Wordle()
        wordle.add_guess(make_guess(guess, answer))
        score += len(wordle.guess_by_freq(frequency))
    return 1 / score if score else 0


def get_answers_guesses(answers_freq, guesses_freq):
    prev_answers = set(PREV_ANSWERS)
    answers = [
        answer
        for answer in get_N_letter_words_with_min_frequency(answers_freq)
        if answer not in prev_answers
    ]
    guesses = [
        guess
        for guess in get_N_letter_words_with_min_frequency(guesses_freq)
        if not has_uncommon_letters(guess)
        and (
            not has_duplicate_letters(guess)
            and get_letter_frequency_score_of_word(guess, LETTER_FREQUENCIES)
            >= LETTER_FREQUENCY_SCORE_THRESHOLD
        )
        or (
            get_letter_frequency_score_of_word(guess, LETTER_FREQUENCIES)
            >= LETTER_FREQUENCY_SCORE_THRESHOLD_WITH_DUPLICATES
        )
    ]
    return answers, guesses


def best_first_guess(answers_frequency, guesses_frequency):
    """
    Calculates and returns the best first guess based on scores derived from possible answers and guesses.
    """
    answers, guesses = get_answers_guesses(answers_frequency, guesses_frequency)
    return best_first_guess_helper(guesses, answers)


def best_first_guess_helper(guesses, answers):
    guess_scores = dict()
    for guess in tqdm(guesses):
        guess_scores[guess] = score_first_guess(guess, answers)
    return guess_scores


def best_first_guess_parallel(answers_frequency, guesses_frequency):
    answers, guesses = get_answers_guesses(answers_frequency, guesses_frequency)

    num_processes = mp.cpu_count()
    chunk_size = len(guesses) // num_processes + (len(guesses) % num_processes > 0)
    chunks = [guesses[i : i + chunk_size] for i in range(0, len(guesses), chunk_size)]

    partial_best_first_guess_helper = partial(best_first_guess_helper, answers=answers)

    try:
        with mp.Pool(processes=num_processes) as pool:
            results = pool.map(partial_best_first_guess_helper, chunks)
            pool.close()
            pool.join()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers.")
        pool.terminate()
        pool.join()  # This is necessary to stop the program and ensure no orphaned processes.
        return {}  # Or any other way you'd like to signify an early termination.

    # Combine the resultant guess_scores into a single dict
    guess_scores = {}
    for result in results:
        guess_scores.update(result)

    return guess_scores


def has_uncommon_letters(word):
    return any(letter in UNCOMMON_LETTERS for letter in word)


def has_duplicate_letters(word):
    """
    Returns True if the word has duplicate letters, otherwise False.
    """
    return len(set(list(word))) < len(word)


def is_prev_word(word):
    return word.upper() in PREV_ANSWERS


if __name__ == "__main__":
    answer_frequency = 4.5  # 1.18
    guess_frequency = 4.5

    try:
        g = best_first_guess_parallel(answer_frequency, guess_frequency)
        with open("wordle.txt", "w") as f:
            for guess in sorted(g, key=g.get, reverse=True):
                f.write(f"{guess} {g[guess]:.3e}\n")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
