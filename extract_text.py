# Japanese PDF Text Extractor (JaPdfExtractor)
# Extract_text.py
# Simple app that uses PyMuPDF to extract Japanese text from specified zones on each page of a PDF file
# First parameter is the PDF input, and second is the UTF-8 encoded text file output

import fitz  # PyMuPDF
import argparse

def text_in_rect(page_text, bounding_rect):
    # Return sorted text blocks that are contained within a Rect
    rect_blocks = [b for b in page_text if fitz.Rect(b[:4]) in bounding_rect]

    # Reverse-sort the blocks of text (into R2L Japanese reading order)
    rect_blocks.sort(key=lambda b: b[0], reverse=True)  # sort by horizontal coordinate

    return rect_blocks

def line_leading(blocks):
    # Identify the default line spacing in a paragraph; use the last two lines of the list
    if len(blocks) < 3:  # skip if there are less than 3 blocks
        return 0
    last = blocks[-1]
    penultimate = blocks[-2]
    # Get distance between x coords of successive blocks
    leading = penultimate[0] - last[0]
    # Increase value by 5% to cover slight variations
    leading = leading + (leading * 0.05)
    return leading

def get_annot_rects(page):
    # Return a list of rects for annotations on the specifed page
    # First, get page annotations as a list
    annotations = list(page.annots())

    # List to hold the rectangles of the annotations
    annotation_rects = []

    # Iterate through each annotation, if any
    if annotations:
        for annot in annotations:
            # Get the rectangle of the annotation
            rect = annot.rect
            # Append the rectangle to the list
            annotation_rects.append(rect)
    return annotation_rects

def write_blocks(output_file, zone, zone_blocks, line_leading):
    # Write blocks to the file
    # To determine paragraph breaks, get starting xPos of all the blocks
    first_block = zone_blocks[0]
    x_pos = first_block[0]

    for block in zone_blocks:
        # Add paragraph break, as necessary
        current_x_pos = block[0]
        current_spacing = x_pos - current_x_pos
        # Debugging
        # output_file.write(f"{current_x_pos} {current_spacing}\n\n")

        # Emit newline if line spacing is more than leading
        if current_spacing > line_leading:
            output_file.write(f"\n\n")

        # Save current block xPos
        x_pos = current_x_pos

        # Get text line block
        line = block[4]
        # Strip newlines (why are they there, anyway?)
        clean_line = line.replace("\n", "")
        # Write the extracted text to the output file
        output_file.write(f"{clean_line}")

        # Add newline if current line ends with a period
        if clean_line[-1] == "。":
            output_file.write(f"\n")

    # Emit newline if this zone looks like a title (i.e., vertical orientation)
    if zone.height > zone.width:
        output_file.write(f"\n\n")

def extract_text_from_pdf(pdf_path, output_path):
    # Extract the text, page by page
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Default page zones
    zones = []

    # Default leading for this document
    leading = 0

    # Open the output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Loop through each page
        for page_num in range(pdf_document.page_count):
            # Get the page
            page = pdf_document.load_page(page_num)

            # Debugging - Output page break header
            output_file.write(f"\n***Page {page_num + 1}:\n")

            # Get page zones (annotation rectangles)
            new_zones = get_annot_rects(page)
            if new_zones and len(new_zones) > 1:
                zones = new_zones
            
            # Extract text blocks from the page
            page_blocks = page.get_text("blocks")

            # Enumerate zones and write text within each one
            for zone in zones:
                # Debugging - output the blocks
                # output_file.write(f"\n\nPage zone: {zone}\nBlocks: {rect_blocks}\n\n")

                # Get blocks that are contained within a zone rect
                rect_blocks = text_in_rect(page_blocks, zone)

                # Get line leading
                if not leading:
                    leading = line_leading(rect_blocks)
 
                # Write blocks with line and paragraph breaks
                write_blocks(output_file, zone, rect_blocks, leading)

    # Close the PDF document
    pdf_document.close()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Extract text from a Japanese PDF without using OCR.")
    parser.add_argument('pdf_path', help="The path to the PDF file.")
    parser.add_argument('output_path', help="The path to the output text file.")
    
    args = parser.parse_args()
    
    # Extract text from the PDF
    extract_text_from_pdf(args.pdf_path, args.output_path)

if __name__ == '__main__':
    main()

