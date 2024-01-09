import filelib

#读取
with open('firework.py',"r",encoding="utf-8") as f1 , open('Fireword.py',"r",encoding="utf-8") as f2:
    lines1 = f1.read()
    lines2 = f2.read()

diff = difflib.unified_diff(lines1,lines2)

for line in diff:
    print(line)