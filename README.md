# jaPdfExtractor

Extract text from PDF using Japanese layout
===========================================

Japanese text will be read inside the bounding boxes of annotations, and then output in T2B, R2L order.

Add rectangular annotations to define the paragraph areas you wish to output. This script will parse them in the order in which the annotations were added to the page.

Usage
=====

python extract_text.py input.pdf output.txt

