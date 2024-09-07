# importing regular expressions module
import re


def convert_to_normalized_case(str_to_normalize: str) -> str:
    """This function accepts new_string and returns normalized from the case perspective string:"""
    # convert the source text to lowercase
    lower_source = str_to_normalize.lower()
    # define a regex pattern to split the text into sentences ('.','?' or '!' at the end of sentece,
    # followed whitespaces or new_line, followed by new word. i.e. end of every sentence
    pattern = r'([\.\?!]\s*)(\w+)'
    sentences = re.split(pattern, lower_source)
    # initialize a variable to store the normalized source text
    result = ""
    # capitalize the first letter of each sentence and append to normalized_source
    for sentence in sentences:
        result += sentence.capitalize()

    return result


def create_sentence_from_last_words(source_text: str) -> str:
    """This function accepts string text and returns new sentence from the last words of each sentence:"""
    # define a regex pattern to find the last word in each sentence
    pattern_last_word = r'(\s(\w+)[\.\?!])'

    # find the last words in each sentence and store them in new_words
    new_words = re.findall(pattern_last_word, source_text)

    # create a new line by joining the last words and capitalize it
    new_line = ''.join(word[1] + ' ' for word in new_words)
    new_line_cap = new_line.capitalize()

    return new_line_cap


def insert_text_into_text(source_text: str, pattern: str, new_line: str) -> str:
    """This function accepts source_text, new_line to input in the text and \n
     pattern of text  after which new_line should be added"""
    # find the index to insert the new line
    insert_index = source_text.find(pattern) + len(pattern)

    # split the text before and after the insertion point
    text_before_insert = source_text[:insert_index]
    text_after_insert = source_text[insert_index:]

    # insert the new line after the specified pattern
    new_text = text_before_insert + f' {new_line}' + text_after_insert

    return new_text


def str_find_replace(source_text: str, old_value: str, new_value: str) -> str:
    """This function accepts source_text the following parameters: \n
    - source_text: new text string where value will be changed from old_value to new_value
    - old_value: word that should be changed
    - new_value: word that will be inserted"""
    # replacing old_value to a new value in source_text
    new_text_replaced = re.sub(r"\b" + re.escape(old_value) + r"\b", new_value, source_text)
    return new_text_replaced


def calculate_spaces(source_text: str) -> int:
    """This function accepts text string  and returns number of all whitespace characters"""
    # calculate the number of all whitespace characters in the source_text
    space_count = len(re.findall(r'\s', source_text))
    return space_count


