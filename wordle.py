from english_words import english_words_lower_alpha_set
from wordfreq import zipf_frequency

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class Wordle:
  def __init__(self):
    self.known = set()
    self.must_include = set()
    self.word = [list(ALPHABET) for _ in range(5)]

  def add_guess(self, guess):
    for i, letter in enumerate(guess):
      status = guess[letter]
      if status == 0:
        for word_letter in self.word:
          if letter in word_letter:
            word_letter.remove(letter)
      if status == 1:
        self.must_include.add(letter)
        if letter in self.word[i]:
          self.word[i].remove(letter)
      if status == 2:
        self.must_include.add(letter)
        self.known.add(letter)
        self.word[i] = [letter]

  def good_guess(self, win=False):
    freq = dict()
    for word in self.guess_by_freq(0):
      for letter in word:
        if letter not in freq:
          freq[letter] = 0
        freq[letter] += 1
    for lett in sorted(freq, key=freq.get, reverse=True):
      print(lett, freq[lett])
    word_scores = dict()
    for word in get_flw():
      if len(set(word)) != len(word):
        continue
      score = 0
      for lett in word:
        if lett not in freq or lett in self.must_include:
          continue
        score += freq[lett]
      word_scores[word] = score
    for lett in sorted(word_scores, key=word_scores.get, reverse=True):
      print(lett, word_scores[lett])

  def guess_by_freq(self, lim):
    guesses = dict()
    for l0 in self.word[0]:
      for l1 in self.word[1]:
        for l2 in self.word[2]:
          for l3 in self.word[3]:
            for l4 in self.word[4]:
              guess = [l0, l1, l2, l3, l4]
              bad_guess = False
              for e in self.must_include:
                if e not in guess:
                  bad_guess = True
                  break
              if not bad_guess:
                guess = ''.join(guess)
                if guess in english_words_lower_alpha_set:
                  freq = zipf_frequency(guess, 'en')
                  if freq > lim:
                    guesses[guess] = freq
    return guesses

  def print_guesses(self, freq):
    guesses = self.guess_by_freq(freq)
    for guess in sorted(guesses, key=guesses.get, reverse=True):
      print(guess, guesses[guess])


def get_flw():
  """
  Returns a set of five letter english words
  """
  return {word for word in english_words_lower_alpha_set if len(word) == 5}


def get_freq_flw(freq):
  return {word for word in get_flw() if zipf_frequency(word, 'en') > freq}


def best_first_guess():
  guess_scores = dict()
  answers = get_freq_flw(4)
  guesses = get_freq_flw(2)
  for i, g in enumerate(guesses):
    if 'x' in g or 'z' in g or 'q' in g or len(set(list(g))) < 5:
      continue
    score = 0
    for j, a in enumerate(answers):
      progress = 100*((i*len(answers) + j)/(len(guesses) * len(answers)))
      print(f'{progress:2f}%', end='\r')
      wordle = Wordle()
      wordle.add_guess(make_guess(g, a))
      score += len(wordle.guess_by_freq(4))
    guess_scores[g] = score
  return guess_scores


def make_guess(guess, answer):
  word_score = dict()
  for i in range(5):
    word_score[guess[i]] = get_score(guess, answer, i)
  return word_score


def get_score(guess, answer, i):
  if guess[i] == answer[i]:
    return 2
  if guess[i] in answer:
    return 1
  return 0


if __name__ == "__main__":
  wordle = Wordle()
  wordle.add_guess({'s': 2, 'a': 1, 'l': 0, 'e': 1, 't': 0})
  wordle.add_guess({'h': 1, 'e': 1, 'a': 2, 'r': 0, 'd': 0})
  # wordle.add_guess({'l': 1, 'a': 2, 'u': 2, 'g': 0, 'h': 0})
  # wordle.print_guesses(0)
  wordle.good_guess()
  # print(make_guess('later', 'ultra'))
  # g = best_first_guess()
  # with open('wordle.txt', 'a') as f:
  #   for guess in sorted(g, key=g.get):
  #     f.write(guess, g[guess])
