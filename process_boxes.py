import re

# Read the original .tex file
with open("algebra.tex", "r", encoding="utf-8") as file:
    t = file.read()

# Modify the content change brackets
t = re.sub(r'\\begin{definition}\[(.*?)\]', r'\\begin{definition}{\1}', t)
t = re.sub(r'\\begin{satz}\[(.*?)\]', r'\\begin{satz}{\1}', t)
t = re.sub(r'\\begin{lemma}\[(.*?)\]', r'\\begin{lemma}{\1}', t)
t = re.sub(r'\\begin{beispiel}\[(.*?)\]', r'\\begin{beispiel}{\1}', t)
t = re.sub(r'\\begin{folgerung}\[(.*?)\]', r'\\begin{folgerung}{\1}', t)
t = re.sub(r'\\begin{proposition}\[(.*?)\]', r'\\begin{proposition}{\1}', t)

# Change Comma
t = re.sub(r'\\begin{definition}{(.*?)}', lambda m: f'\\begin{{definition}}' + '{' + m.group(1).replace(',', ';') + '}', t)
t = re.sub(r'\\begin{satz}{(.*?)}', lambda m: f'\\begin{{satz}}' + '{' + m.group(1).replace(',', ';') + '}', t)
t = re.sub(r'\\begin{folgerung}{(.*?)}', lambda m: f'\\begin{{folgerung}}' + '{' + m.group(1).replace(',', ';') + '}', t)
t = re.sub(r'\\begin{proposition}{(.*?)}', lambda m: f'\\begin{{proposition}}' + '{' + m.group(1).replace(',', ';') + '}', t)
t = re.sub(r'\\begin{lemma}{(.*?)}', lambda m: f'\\begin{{lemma}}' + '{' + m.group(1).replace(',', ';') + '}', t)
t = re.sub(r'\\begin{beispiel}{(.*?)}', lambda m: f'\\begin{{beispiel}}' + '{' + m.group(1).replace(',', ';') + '}', t)

# Save the modified content to a new .tex file
with open("new_algebra.tex", "w", encoding="utf-8") as file:
    file.write(t)

print("Conversion complete. Saved as output.tex")
