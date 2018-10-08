import sys
import logging
#sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'BT', 'BL', 'BD', 'BCONJ', 'BCOR', 'BE', 'ET', 'EL', 'ED', 'ECONJ', 'ECOR', 'EE', 'SEC', 'SSEC', 'SSSEC', 'ES', 'TEXT','ITEXT','BIBS','MT',
)

states = (('ig', 'exclusive'), ('sec', 'exclusive'))

# Set up three logging objects
logging.basicConfig(
    level = logging.DEBUG,
    filename = "lexlog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Tokens

def t_ig_BT(t):
    r'\\begin\{theorem\}'
    t.lexer.begin('INITIAL')
    return t

def t_ig_BL(t):
    r'\\begin\{lemma\}'
    t.lexer.begin('INITIAL')
    return t

def t_ig_BD(t):
    r'\\begin\{definition\}'
    t.lexer.begin('INITIAL')
    return t

def t_ig_BCONJ(t):
    r'\\begin\{conjecture\}'
    t.lexer.begin('INITIAL')
    return t

def t_ig_BCOR(t):
    r'\\begin\{corollary\}'
    t.lexer.begin('INITIAL')
    return t

def t_ig_BE(t):
    r'\\begin\{example\}'
    t.lexer.begin('INITIAL')
    return t

def t_ET(t):
    r'\\end\{theorem\}'
    t.lexer.begin('ig')
    return t

def t_EL(t):
    r'\\end\{lemma\}'
    t.lexer.begin('ig')
    return t

def t_ED(t):
    r'\\end\{definition\}'
    t.lexer.begin('ig')
    return t

def t_ECONJ(t):
    r'\\end\{conjecture\}'
    t.lexer.begin('ig')
    return t

def t_ECOR(t):
    r'\\end\{corollary\}'
    t.lexer.begin('ig')
    return t

def t_EE(t):
    r'\\end\{example\}'
    t.lexer.begin('ig')
    return t

def t_INITIAL_ig_SEC(t):
    r'\\section\{'
    t.lexer.begin('sec')
    return t

def t_ig_SSEC(t):
    r'\\subsection\{'
    t.lexer.begin('sec')
    return t

def t_ig_SSSEC(t):
    r'\\subsubsection\{'
    t.lexer.begin('sec')
    return t

def t_sec_ES(t):
    r'\}'
    t.lexer.begin('ig')
    return t

def t_ig_BIBS(t):
    r'\\bibliographystyle'
    t.lexer.begin('INITIAL')
    return t

def t_INITIAL_MT(t):
    r'\\maketitle'
    t.lexer.begin('ig')
    return t

def t_INITIAL_sec_TEXT(t):
    r'[\s\S]'
    return t

def t_ig_ITEXT(t):
    r'[\s\S]'
    pass

##def t_newline(t):
##    r'\n+'
##    t.lexer.lineno += t.value.count("\n")

##def t_ANY_eof(t):
##    return None

def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex(debug=True, debuglog = log)

# Parsing rules

def p_statement_text(p):
    'statement : text'
    p[0] = p[1]

def p_text_text(p):
    'text : text text'
    p[0] = p[1] + p[2]

def p_ptext_text(p):
    'ptext : TEXT'
    p[0] = p[1]

def p_ptext_ptext_text(p):
    'ptext : ptext TEXT'
    p[0] = p[1] + p[2]

def p_text_theorem(p):
    'text : BT ptext ET'
    p[0] = p[1] + p[2] + p[3]

def p_text_lemma(p):
    'text : BL ptext EL'
    p[0] = p[1] + p[2] + p[3]

def p_text_corollary(p):
    'text : BCOR ptext ECOR'
    p[0] = p[1] + p[2] + p[3]

def p_text_conjecture(p):
    'text : BCONJ ptext ECONJ'
    p[0] = p[1] + p[2] + p[3]

def p_text_example(p):
    'text : BE ptext EE'
    p[0] = p[1] + p[2] + p[3]

def p_text_definition(p):
    'text : BD ptext ED'
    p[0] = p[1] + p[2] + p[3]

def p_text_sec(p):
    'text : SEC ptext ES'
    p[0] = p[1] + p[2] + p[3]

def p_text_ssec(p):
    'text : SSEC ptext ES'
    p[0] = p[1] + p[2] + p[3]

def p_text_sssec(p):
    'text : SSSEC ptext ES'
    p[0] = p[1] + p[2] + p[3]

def p_text_mtbeg(p):
    'text : ptext MT'
    p[0] = p[1] + p[2]

def p_text_bibend(p):
    'text : BIBS ptext'
    p[0] = p[1] + p[2]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc(debug = True, debuglog = log)
