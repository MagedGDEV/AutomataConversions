python regexToNFA.py convert "(1|0)*1" in NFA1.json NFA1
python regexToNFA.py convert "(a|b)*abb" in NFA2.json NFA2
python regexToNFA.py convert "(a|b)*[A-Z]+(a|b)*" in NFA3.json NFA3

pause 

python NFAtoDFA.py convert NFA1.json in DFA1.json DFA1
python NFAtoDFA.py convert NFA2.json in DFA2.json DFA2
python NFAtoDFA.py convert NFA3.json in DFA3.json DFA3

pause 

python minimizeDFA.py minimize DFA1.json in minDFA1.json minDFA1
python minimizeDFA.py minimize DFA2.json in minDFA2.json minDFA2
python minimizeDFA.py minimize DFA3.json in minDFA3.json minDFA3

pause