# jaPdfExtractor

Extract text from PDF using Japanese layout
===========================================

Japanese text will be read inside the bounding boxes of annotations, and then output in T2B, R2L order.

To define the regions of the page that you wish to parse for Japanese text, add rectangular annotations to the PDF. 

This script will parse the annotations in the order they were added to the page, and then use those rectangles to parse all subsequent pages. I.e., you can draw one set of rectangles on the title page, and then another set on the first body page, which will then be used for all subsequent pages.

At this time, the script attempts to detect paragraph breaks, inserting newlines in the text output, but it does not detect furigana characters.

Usage
=====

`python extract_text.py input.pdf output.txt`



