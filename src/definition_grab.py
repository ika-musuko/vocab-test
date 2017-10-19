from PyDictionary import PyDictionary
LEX = "lexwords/lex_words.txt"
DEF = "lexwords/lex_def.txt"

dictionary = PyDictionary()
with open(LEX,"r",encoding="utf-8") as lexf, open(DEF, "w",encoding="utf-8")  as deff:
	for row in lexf:
		word = row.split(',')[0]
		defz = dictionary.meaning(word)
		write = "%s|%s" % (word, defz)
		print(word)
		deff.write(write)