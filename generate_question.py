from pathlib import Path
from botok.tokenizers.wordtokenizer import WordTokenizer


def get_word_token(sentence, wt):
    word_tokens = wt.tokenize(sentence)
    return word_tokens

def is_valid_option(word_token):
    if len(word_token.text) > 3 and (word_token.pos == "VERB" or word_token.pos == "NOUN"):
        return True
    else:
        return False
        
def get_question(sentence, wt):
    word_tokens = get_word_token(sentence, wt)
    question = ''
    possible_options = ''
    for token_idx, word_token in enumerate(word_tokens):
        question += f'{word_token.text} '
        if is_valid_option(word_token):
            possible_options += f'{str(token_idx)},'
    if possible_options:
        return question, possible_options
    else:
        return "", ""

def get_last_id(level):
    question_files = list(Path(f'./sentences/{level}').iterdir())
    return len(question_files)-1

def set_questions(sample_text, level, last_id):
    sentences = sample_text.splitlines()
    word_tokenizer = WordTokenizer()
    if last_id == 0:
        last_id = 1
    for sentence in sentences:
        question, possible_option = get_question(sentence, word_tokenizer)
        if question:
            Path(f'./sentences/{level}/{last_id}.txt').write_text(f'{question}\n{possible_option}', encoding='utf-8')
            last_id += 1
    return last_id

if __name__ == "__main__":
    sample_text = Path('./sample.txt').read_text(encoding='utf-8')
    level = "C1"
    last_id = get_last_id(level)
    last_id = set_questions(sample_text, level, last_id)
    Path(f'./sentences/{level}/last_id').write_text(str(last_id-1))