## matchseq

Memory safe nucleotide subsequence search tool.
It will search a stream of nucleotides and print every occurrence of a specified subsequence
with optional left and right context. 

### Install

```bash
git clone https://github.com/jperelshteyn/dna_searcher.git
cd dna_searcher
python setup.py install
```

### Command Line Arguments

* `-T` target subsequence
* `-x` length of left context
* `-y` length of right context

### Usage

```bash
echo "ACACGTCAε" | matchseq -T:ACGT -x:1 -y:2
...
C ACGT CA
```

