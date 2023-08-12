# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
from spacy.matcher import PhraseMatcher
from spellchecker import SpellChecker

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

codes = {
    '01': ['fair', 'okay', 'alright', 'ok', 'decent'],
    '02': ['good', 'great', 'awesome', 'cool', 'fun', 'rocks', 'excellent',
           'amazing', 'fantastic', 'wonderful', 'incredible', 'superb', 'perfect'],
    '03': ['bad', 'terrible', 'crap', 'sucks', 'awful', 'dreadful', 'horrible'],
    '04': ['expensive', 'pricey', 'costly', 'overpriced', 'high priced', 'high cost',
                  'high price', 'high cost', 'over priced', 'over cost', 'over priced'],
    '05': ['cheap', 'inexpensive', 'low cost', 'low priced', 'low price', 'low cost',
                        'affordable', 'low budget', 'low cost', 'low budget', 'low priced', 'low price'],
    '06': ['fast', 'quick', 'speedy', 'rapid', 'swift', 'speed', 'quickly', 'rapidly', 'swiftly'],
    '07': ['slow', 'sluggish', 'leisurely', 'unhurried', 'slowly', 'sluggishly', 'leisurely', 'unhurriedly', 'wait']
}
           
nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)

for code, keywords in codes.items():
    patterns = [nlp(keyword) for keyword in keywords]
    matcher.add(code, None, *patterns)

def autocode(text: str) -> list[str]:
    doc = nlp(text)
    matches = matcher(doc)

    output = []
    
    for match_id, _, _ in matches:
        rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
        output.append(rule_id)

    # Remove duplicates while preserving order
    output = list(dict.fromkeys(output))

    return output

def correct_spelling(text: str) -> str:
    spell = SpellChecker()
    words = text.split()
    corrected_words = []

    for word in words:
        # Get the most likely correct spelling
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)

    corrected_text = ' '.join(corrected_words)
    return corrected_text

data = ""
while True:
    data = input("Enter text to autocode or press enter to quit:\n")
    if data == "":
        break
    # Lowercase and trim to prepare for processing
    data = data.lower().strip()
    # Spell check it
    corrected_data = correct_spelling(data)
    print(corrected_data)
    print(autocode(data))
