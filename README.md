## matchseq

Memory-safe nucleotide subsequence search tool.
It will search a stream of nucleotides and print every occurrence of a specified subsequence
with optional left and right context. 

### Install

```bash
git clone https://github.com/jperelshteyn/nucl-finder.git
cd nucl-finder
python setup.py install
```

### Command Line Arguments

* `-T` target subsequence (required)
* `-x` length of left context (optional)
* `-y` length of right context (optional)

### Requirements

Input nucleotide sequence as well as the target subsequence must only consist of base values:
`A`, `C`, `G`, `T`
The end of sequence character is `ε` - nothing will be search after it. 

### Usage

```bash
echo "ACACGTCAε" | matchseq -T:ACGT -x:1 -y:2
...
C ACGT CA
```

