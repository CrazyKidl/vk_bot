main = open('text.py', 'r', encoding='utf-8')
test_main = open('test_main.py', 'w', encoding='windows-1251')
word = '[club192674616|@dapizdabot] '
word_ = '[club192674616|да (бот)] '
word__ = '.object'
doc = main.read().splitlines()
for line in doc:
    if word in line:
        line = line.replace(word, '')
    if word_ in line:
        line = line.replace(word_, '')
    if word__ in line:
        line = line.replace(word__, '')
    test_main.write(line + '\n')
test_main.close()
main.close()
