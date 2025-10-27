from .entities import Treatmentinput
from ..utils.services import token_classification_service
from ..utils.utils import clean_string

def similarity_filter(input : Treatmentinput) -> Treatmentinput:
    print(f"similarity {input.value}")
    value = input.value
    words = value.split(' ')
    words = list(filter(lambda x: x != '', words))

    fragment_short = ' ' + input.user_input[input.user_input.find(input.key) + len(input.key):] + ' '
    fragment_short = clean_string(fragment_short)
    fragment_short = ' ' + fragment_short.strip() + ' '
    answer_list = []

    for word in words: # assembling the answer
        if len(word)>0 and word != '=':
            
            clean_word = ' ' + word[1:-1].replace('\n', '') + ' '
            single_word = ' ' + word.replace('\n', '') + ' '
            reduced_word = ' ' + word[1:-1] + ' '
            dry_word = ' ' + clean_string(word) + ' '
            candidates = [clean_word, single_word, reduced_word, ' ' + word + ' ', dry_word]    

            for candidate in candidates:
                if candidate.lower() in fragment_short.lower():
                    if candidate.strip() not in answer_list:
                        answer_list.append(candidate.strip())
                        break
    final_answer = ''
    if len(answer_list)>0:
        final_answer = ' '.join(answer_list)
    input.value = final_answer.strip()
    return input


def clean_aux(input : Treatmentinput) -> Treatmentinput:
    print(f"clean aux1 {input.value}")
    if input.current_intent.lower() == 'update':
        value = input.value.strip()
        tokens = token_classification_service(value)
        print(f"tokens {tokens}")
        for t in tokens:
            if t['entity'] == 'AUX':
                word = t['word'] + ' '
                value = value.replace(word, '')
        input.value = value.strip()
    print(f"clean aux2 {input.value}")
    return input

'''
def request_new_answer(input : Treatmentinput) -> Treatmentinput:

    fragment_short_idx = input.user_input.find(input.key)
    fragment_short = input.user_input[fragment_short_idx+len(input.key)]

    response = qa_service(variables={"entity" : input.current_entity, 
                                                "user_msg" : input.user_input,
                                                "attribute_key" : input.key,
                                                "fragment_short" : fragment_short,
                                                "user_intent" : input.current_intent}, 
                                 model_name=input.model_name,
                                 prompt_type='attribute')
    input.value = response['data']['response']
    return input
'''
def entity_filter(input : Treatmentinput) -> Treatmentinput:

    words = input.value.split(' ')
    words = list(filter(lambda x: x != '', words))
    candidates = []
    for word in words:
        word = clean_string(word)
        single_word = ' ' + word.lower() + ' '
        if single_word in input.user_input:
            candidates.append(single_word.strip())

    if not candidates:
        for word in words:
            if word.lower() in input.user_input:
                candidates.append(word.strip())
    candidates_str = ' '.join(candidates)
    tokens = token_classification_service(candidates_str)
    print(f"entity tokens: {tokens}")

    for token in tokens:
        if token['entity'] == 'NOUN':
            input.value = token['word']
    
    return input
        
        

def extract_entity(input : Treatmentinput) -> Treatmentinput:
    tokens = token_classification_service(input.user_input)
    for token in tokens:
        if token['entity'] == 'NOUN':
            input.value = token['word']
            break
    return input
        
def intent_filter(input : Treatmentinput) -> Treatmentinput:
    value = input.value.lower()

    keywords = ['READ', 'CREATE', 'DELETE', 'UPDATE', ' Yes ', ' No ']
    for keyword in keywords:
        if keyword.lower() in value:
            input.value = keyword
    return input

def extract_attribute(input : Treatmentinput) -> Treatmentinput:
    msg = input.user_input
    attribute_index = msg.find(input.key) + len(input.key)
    value = msg[attribute_index:]
    if ' and ' in msg:
        value_fragment = value.split(' and ')[0]
    elif ', ' in msg:
        value_fragment = value.split(', ')[0]
    else:
        input.value = value
        return input
    
    answer = []
    value_list = value_fragment.split(' ')

    for word in value_list:
        if word in value:
            answer.append(word)

    if len(answer)>0:
        input.value = ' '.join(answer)
        return input

def find_filter(input : Treatmentinput) -> Treatmentinput:
    new_answer = []
    msg = input.user_input.lower()
    keywords  = [' where ', ' when ', ' whenever ', ' since ', ' with ']
    addition_marks = ['and', ',']
    idx = -1
    for k in keywords:
        idx = msg.find(k)
        if idx > -1:
            idx = idx+len(k)
            msg = msg[idx:]
            tokens = token_classification_service(msg)
            for t in tokens:
                if t['entity'] == 'NOUN':
                    if len(new_answer)>1:
                        break
                    new_answer.append(t['word'])
                elif t['word'] not in addition_marks:
                    new_answer.append(t['word'])
                else:
                    break
            new_value = ' '.join(new_answer)
            input.value = new_value   
            break
    
    return input