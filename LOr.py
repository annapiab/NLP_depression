import argparse
import csv
import math
from collections import Counter

def word_frequency_dict(file):
    """
    Creates a word frequency dictionary from a tab-separated values (TSV) file.

    Args:
        str: The path to the TSV file containing words and their frequencies.

    Returns:
        Dict: Keys are words, and values are the frequencies.
    """
    wordfrequency_dict = Counter()

    with open(file, "r", newline="", encoding="utf-8") as sink:
        file_reader = csv.reader(sink, delimiter="\t")

        # Skip the header row
        next(file_reader)

        for row in file_reader:
            if len(row) >= 2:
                word = row[0]
                frequency = int(row[1])

                wordfrequency_dict[word] += frequency

    return wordfrequency_dict


def compute_log_O(c, N):
    """
    Computes the log-odds from the frequencies c (values in the dictionary) and the total tokens N.

    Args:
        c: Frequencies values of the dictionary.
        N: The total number of tokens.

    Returns:
        A dictionary of log-odds.
    """
    log_odds = {}

    for word in c:
        log_odds[word] = math.log(c[word]) - math.log(N - c[word])

    return log_odds


def compute_ratio(c1, c2, N1, N2):
    """
    Computes the ratio of log-odds between the two corpora.

    Args:
        c1: A dictionary of frequencies for the first corpus.
        c2: A dictionary of frequencies for the second corpus.
        N1: The total number of tokens in the first corpus.
        N2: The total number of tokens in the second corpus.

    Returns:
        A dictionary of ratios of log-odds.
    """
    log_odds1= compute_log_O(c1, N1)
    log_odds2 = compute_log_O(c2, N2)

    ratio = {}

    for word in log_odds1:
        if word in log_odds2:
            ratio[word] = log_odds1[word] - log_odds2[word]

    return ratio


def main(args):
    """
    Computes the previous functions and prints the output in the 
    desired format.

    """
    wordfreq1 = word_frequency_dict(args.tsv1)
    wordfreq2 = word_frequency_dict(args.tsv2)

    total_tokens_kjv = sum(wordfreq1.values())
    total_tokens_yahoo = sum(wordfreq2.values())

    Log_ORatio = compute_ratio(wordfreq1, wordfreq2, total_tokens_kjv, total_tokens_yahoo)

    sorted_ratio = sorted(Log_ORatio.items(), key=lambda x: x[1])       

    highest_10 = sorted_ratio[:20]
    lowest_10 = sorted_ratio[-20:][::-1]

    print("Highest 15 log-odds ratio:")
    for word, ratio in highest_10:
        print(f"{word}: {ratio:.4f}")

    print("\nLowest 15 log-odds ratio:")
    for word, ratio in lowest_10:
        print(f"{word}: {ratio:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Computes log-odds ratio between two TSV files")
    parser.add_argument("tsv1", help="Path to the first TSV file")
    parser.add_argument("tsv2", help="Path to the second TSV file")
    args = parser.parse_args()

    main(args)
