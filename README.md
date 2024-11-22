# Histogram generator

This program generates a histogram from frequency of each letter on the input.
The default input file is `/var/lib/words/dict`, this can be overridden with `--dictionary` argument

## Parameters:
```
$ ./histogram.py --help
Usage: histogram.py [OPTIONS]

  Main function of the CLI.

Options:
  --dictionary FILENAME           Location of input dictionary to parse
  --debug / --no-debug            Turn on debug log levels
  --latin-only / --count-non-latin
                                  Whether to restrict to latin alphabet
  --sort-by-letter / --sort-by-frequency
                                  Whether to display results sorted
                                  alphabetically or by occurance
  --help                          Show this message and exit.
```
## Usage

Prepare environment:
```
$ python3 -mvenv .venv
$ . .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

Run the program:
```
python3 ./histogram.py
```

With custom dictionary location:
```
python3 ./histogram.py --dictionary=/usr/share/dict/american-english-insane
```

With stdin:
```
cat /usr/share/dict/american-english-huge | python3 ./histogram.py --dictionary=-
```

With stdin:
```
cat /usr/share/dict/american-english-huge | python3 ./histogram.py --dictionary=-
```

With more options:
```
$ ./histogram.py --sort-by-frequency --dictionary=/usr/share/dict/american-english-huge --count-non-latin --debug
```

## Example output:
```
$ ./histogram.py --sort-by-frequency --dictionary=/usr/share/dict/american-english-huge 
Q: (5323)   | +
J: (6035)   | +
X: (8639)   | ++
Z: (15369)  | +++
W: (26196)  | ++++++
V: (30847)  | +++++++
K: (31001)  | +++++++
F: (36231)  | ++++++++
Y: (51569)  | ++++++++++++
B: (60151)  | ++++++++++++++
G: (80026)  | ++++++++++++++++++
H: (80670)  | +++++++++++++++++++
P: (89453)  | +++++++++++++++++++++
M: (92094)  | +++++++++++++++++++++
D: (98891)  | +++++++++++++++++++++++
U: (100937) | +++++++++++++++++++++++
C: (125036) | +++++++++++++++++++++++++++++
L: (168537) | +++++++++++++++++++++++++++++++++++++++
T: (199576) | +++++++++++++++++++++++++++++++++++++++++++++++
O: (208220) | +++++++++++++++++++++++++++++++++++++++++++++++++
N: (215214) | +++++++++++++++++++++++++++++++++++++++++++++++++++
R: (217035) | +++++++++++++++++++++++++++++++++++++++++++++++++++
A: (256469) | ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
I: (268534) | +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
S: (329258) | ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
E: (337288) | ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```