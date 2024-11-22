#!/usr/bin/env python3
import click
import logging
import os

from typing import Dict, IO
from collections import Counter
from functools import reduce, partial
from math import log10

LOGGER = logging.getLogger(__name__)
# This is only for "traditional" english letters. Pretty arbitrary, e.g.: "fiancé"
LATIN_CHARS = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}


# Currently this function is made thread-safe by making copies of the `letter_count` dict, which slows down
# execution, but otherwise allows for distributed compute in the future
def count_letters(letter_count: Dict[str, int], word: str, latin_only: bool) -> Counter:
    """
    Reduce function: count the letters.

    Args:
        letter_count (Counter): initial letter count
        word (str): input word to count letters in
        latin_only (bool): If True, only latin characters are counted

    Returns:
        Counter: The result of the reduce
    """
    return_dict = Counter(dict(letter_count))
    for letter in word:
        if not letter.isalnum():
            continue
        upper_letter = letter.upper()
        if latin_only and upper_letter not in LATIN_CHARS:
            continue
        return_dict[upper_letter] += 1
    return return_dict
    
@click.command
@click.option("--dictionary", default="/var/lib/words/dict", type=click.File("r"), help="Location of input dictionary to parse")
@click.option("--debug/--no-debug", default=False, help="Turn on debug log levels")
@click.option("--latin-only/--count-non-latin", default=True, help="Whether to restrict to latin alphabet")
@click.option("--sort-by-letter/--sort-by-frequency", default=True, help="Whether to display results sorted alphabetically or by occurance")
def cli(dictionary: IO, debug: bool, latin_only: bool, sort_by_letter: bool) -> None:
    """
    Main function of the CLI.
    """

    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)
    
    word_count = Counter()
    letter_counter_fun = partial(count_letters, latin_only=latin_only)
    line_count = 0
    for line in dictionary:
        line_count += 1
        if (line_count % 10_000) == 0:
            LOGGER.debug(f"Processed {line_count} words")
        word_count = reduce(letter_counter_fun, line, word_count)
    
    if not word_count:
        LOGGER.debug("Nothing to count")
        return
    
    sorted_by_occurence = sorted(word_count.items(), key=lambda kv: kv[1], reverse=True)
    LOGGER.debug(f"Result sorted by occurence: {sorted_by_occurence}")
    most_frequent = next(iter(sorted_by_occurence))
    LOGGER.debug(f"Most frequent letter: {most_frequent[0]}: {most_frequent[1]}")
    
    display_columns = int(os.environ.get("COLUMNS", "80"))
    LOGGER.debug(f"Columns: {display_columns}")

    # 3 or padding for ()s
    width = int(log10(most_frequent[1])) + 3
    display_columns, _ = os.get_terminal_size()
    # 10 for some padding for initial column and right margin    
    ratio = (display_columns - width - 10 )/ most_frequent[1]
    
    for char, count in sorted(word_count.items(), key=lambda kv: kv[0 if sort_by_letter else 1]):
        count_str = f"({count})"
        click.echo(f"{char}: {f'%-{width}s' % count_str} | {'+' * int(count * ratio)}")
        

if __name__ == '__main__':
    cli()