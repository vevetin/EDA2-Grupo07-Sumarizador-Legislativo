import re

# Sufixos conjugados → sufixo do infinitivo
_REGRAS_VERBAIS = [
    # Gerúndio
    (r"ando$", "ar"),
    (r"endo$", "er"),
    (r"indo$", "ir"),
    # Particípio passado
    (r"ado$",  "ar"),
    (r"ido$",  "ir"),
    # Futuro do subjuntivo
    (r"armos$", "ar"), (r"ardes$", "ar"), (r"arem$", "ar"),
    (r"ermos$", "er"), (r"erdes$", "er"), (r"erem$", "er"),
    (r"irmos$", "ir"), (r"irdes$", "ir"), (r"irem$", "ir"),
    # Imperfeito do subjuntivo
    (r"assemos$", "ar"), (r"assem$", "ar"), (r"asse$", "ar"),
    (r"essemos$", "er"), (r"essem$", "er"), (r"esse$", "er"),
    (r"issemos$", "ir"), (r"issem$", "ir"), (r"isse$", "ir"),
    # Pretérito perfeito / 1ª pessoa do plural
    (r"amos$", "ar"),
    (r"aram$", "ar"), (r"ou$",  "ar"),
    (r"eram$", "er"), (r"eu$",  "er"),
    (r"iram$", "ir"), (r"iu$",  "ir"),
    # Imperfeito do indicativo (1ª conjugação)
    (r"avamos$", "ar"), (r"avas$", "ar"), (r"avam$", "ar"), (r"ava$", "ar"),
]

# Verbos irregulares: forma sem acento → infinitivo
VERBOS_IRREGULARES = {
    # ver
    "vejo": "ver",  "ves": "ver",   "vemos": "ver", "veem": "ver",
    "via":  "ver",  "vias": "ver",  "viamos": "ver", "viam": "ver",
    "vi":   "ver",  "viste": "ver", "viu": "ver",   "viram": "ver",
    "veja": "ver",  "vejas": "ver", "vejamos": "ver", "vejam": "ver",
    # dizer
    "digo": "dizer",  "dizes": "dizer",   "diz": "dizer",
    "dizemos": "dizer", "dizem": "dizer",
    "dizia": "dizer", "disse": "dizer",
    "dissemos": "dizer", "disseram": "dizer",
    "diga": "dizer",  "digas": "dizer",   "digamos": "dizer", "digam": "dizer",
    # fazer
    "faco": "fazer",  "faz": "fazer",    "fazemos": "fazer", "fazem": "fazer",
    "fazia": "fazer", "fiz": "fazer",    "fez": "fazer",
    "fizemos": "fazer", "fizeram": "fazer",
    "faca": "fazer",  "facam": "fazer",
    # ir  (fui/foi/fomos/foram também pertencem a 'ser', mas mapeamos para 'ir';
    #      o spaCy resolve o contexto antes deste fallback na maioria dos casos)
    "vou": "ir",  "vai": "ir",  "vao": "ir",
    "ia":  "ir",  "ias": "ir",  "iamos": "ir", "iam": "ir",
    "fui": "ir",  "foi": "ir",  "fomos": "ir", "foram": "ir",
    "va":  "ir",  "vas": "ir",
    # ser  (era/eram já são tratadas pelo spaCy; mantidas aqui como segurança)
    "sou": "ser",  "somos": "ser", "sao": "ser",
    "era": "ser",  "eras": "ser",  "eramos": "ser", "eram": "ser",
    "seja": "ser", "sejam": "ser",
    # estar
    "estou": "estar",   "esta": "estar",   "estamos": "estar", "estao": "estar",
    "estava": "estar",  "estavam": "estar",
    "esteve": "estar",  "estiveram": "estar",
    "esteja": "estar",  "estejam": "estar",
    # ter
    "tenho": "ter",  "tens": "ter",   "tem": "ter",    "temos": "ter",
    "tinha": "ter",  "tinhas": "ter", "tinhamos": "ter", "tinham": "ter",
    "tive":  "ter",  "teve": "ter",   "tivemos": "ter", "tiveram": "ter",
    "tenha": "ter",  "tenham": "ter",
    # poder
    "posso": "poder",  "podes": "poder", "pode": "poder",
    "podemos": "poder", "podem": "poder",
    "podia": "poder",   "puderam": "poder",
    "possa": "poder",   "possam": "poder",
    # querer
    "quero": "querer",   "queres": "querer", "quer": "querer",
    "queremos": "querer", "querem": "querer",
    "queria": "querer",  "quis": "querer",
    "quisemos": "querer", "quiseram": "querer",
    "queira": "querer",  "queiram": "querer",
    # vir
    "venho": "vir",  "vens": "vir",   "vem": "vir",    "viemos": "vir",
    "vinha": "vir",  "vim": "vir",    "veio": "vir",   "vieram": "vir",
    "venha": "vir",  "venham": "vir",
}