from prev_answers import PREV_ANSWERS
from wordfreq import zipf_frequency
from english_words import english_words_lower_alpha_set
from wordle import get_N_letter_words
from collections import Counter
import matplotlib.pyplot as plt


def get_lowest_freq(words):
    """
    Returns a list of words that have the lowest frequency in the given list of words.
    """
    lowest_freq = float("inf")
    for word in words:
        freq = zipf_frequency(word, "en")
        if freq < lowest_freq:
            lowest_freq = freq
            print(word)
    return lowest_freq


def get_frequency_frequency(words):
    """
    Returns a dictionary of words and their respective frequencies.
    """
    freq_dist = Counter()
    for word in words:
        freq = zipf_frequency(word, "en")
        freq_dist[freq] += 1

    # sort the dictionary by frequency
    return dict(sorted(freq_dist.items()))


def get_letter_frequency(words):
    letter_frequency = Counter()
    for word in words:
        for letter in word:
            letter_frequency[letter] += 1
    # normalize dict
    total = sum(letter_frequency.values())
    for k in letter_frequency:
        letter_frequency[k] /= total
    return letter_frequency


def get_letter_frequency_score_of_word(word, letter_frequencies):
    score = 0
    for letter in word:
        score += letter_frequencies[letter]
    return score


if __name__ == "__main__":
    words = PREV_ANSWERS

    # print(get_lowest_freq(words))

    letter_frequency = get_letter_frequency(words)

    word_letter_scores = [
        get_letter_frequency_score_of_word(word, letter_frequency) for word in words
    ]

    # sort word_letter_scores
    word_letter_scores.sort()

    average = sum(word_letter_scores) / len(word_letter_scores)
    minimum = min(word_letter_scores)
    maximum = max(word_letter_scores)
    lower_quartile = word_letter_scores[len(word_letter_scores) // 4]
    upper_quartile = word_letter_scores[len(word_letter_scores) * 3 // 4]
    median = word_letter_scores[len(word_letter_scores) // 2]

    print(f"Average: {average:.2%}")
    print(f"Minimum: {minimum:.2%}")
    print(f"Maximum: {maximum:.2%}")
    print(f"Lower Quartile: {lower_quartile:.2%}")

    print(f"Upper Quartile: {upper_quartile:.2%}")
    print(f"Median: {median:.2%}")

    # for k, v in sorted(letter_frequency.items(), key=lambda x: x[1], reverse=True):
    #     print(k, f"{v:.2%}")

    # letter_frequency_2 = get_letter_frequency(get_N_letter_words(return_type=list))
    # for k, v in sorted(letter_frequency_2.items(), key=lambda x: x[1], reverse=True):
    #     print(k, f"{v:.2%}")

    # freq_freq = get_frequency_frequency(words)
    # # plot the frequency frequency
    # plt.bar(freq_freq.keys(), freq_freq.values())
    # plt.xlabel("Frequency")
    # plt.ylabel("Frequency of Frequency")
    # plt.title("Frequency Frequency of 5-letter words")
    # plt.show()
