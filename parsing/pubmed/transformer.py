import re

def ace_substitutor(sentences, token = 'ACEI'):
    '''Substitutes token in place of different spellings of ACE inhibitor'''
    
    ace_options = r'^(\bangiotensin converting enzyme (ace) inhibitor+?)(s\b|\b)|(\bangiotensin-converting enzyme (ace) inhibitor+?)(s\b|\b)|(\bace inhibitor+?)(s\b|\b)|(\bace\b)|(\bacei\b)|(\bangiotensin-converting enzyme inhibitor+?)(s\b|\b) \(acei+?(s\b|\b)\)|(\bangiotensin converting enzyme inhibitor+?)(s\b|\b) \(acei+?(s\b|\b)\)|(\bangiotensin-converting enzyme inhibitor+?)(s\b|\b)|(\bangiotensin-converting enzyme+?)(s\b|\b)|(\bangiotensin converting enzyme inhibitor+?)(s\b|\b)|(\bangiotensin converting enzyme+?)(s\b|\b)'
    sentences = map(lambda sent: re.sub(ace_options,'ACEI', sent.lower()), sentences)
    return sentences

