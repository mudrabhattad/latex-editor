import re
import tkinter as tk
from tkinter import Text, Scrollbar, Button, INSERT

def process_latex():
    latex_code = input_text.get("1.0", "end-1c")

    # Regular expressions to detect LaTeX commands
    title_pattern = re.compile(r'\\title\{(.+?)\}')
    author_pattern = re.compile(r'\\author\{(.+?)\}')
    date_pattern = re.compile(r'\\date\{(.+?)\}')
    itemize_pattern = re.compile(r'\\begin{itemize}')
    enumerate_pattern = re.compile(r'\\begin{enumerate')
    document_begin_pattern = re.compile(r'\\begin{document}')
    document_end_pattern = re.compile(r'\\end{document')
    textbf_pattern = re.compile(r'\\textbf\{(.+?)\}')
    textit_pattern = re.compile(r'\\textit\{(.+?)\}')
    underline_pattern = re.compile(r'\\underline\{(.+?)\}')
    border_pattern = re.compile(r'\\BORDER{(.*?)}')
    paragraph_pattern = re.compile(r'\\p\s')
    paragraph_replacement = '\n\n'  # Replacing \p with double line breaks for paragraphs

    # Flags to indicate if we are inside the document environment
    inside_document = False
    detected_commands = []
    current_bullet_point = []
    current_numbered_item = 1
    bullet_flag = False

    for line in latex_code.split('\n'):
        if document_begin_pattern.search(line):
            inside_document = True
        elif document_end_pattern.search(line):
            break

        if inside_document:
            title_match = title_pattern.search(line)
            author_match = author_pattern.search(line)
            date_match = date_pattern.search(line)
            itemize_match = itemize_pattern.search(line)
            enumerate_match = enumerate_pattern.search(line)
            textbf_match = textbf_pattern.search(line)
            textit_match = textit_pattern.search(line)
            underline_match = underline_pattern.search(line)
            paragraph_match = paragraph_pattern.search(line)
            if paragraph_pattern.search(line):
                detected_commands.append(" <paragraph> ")
                
            if border_pattern.search(line):  # Detect the border command
                border_match = border_pattern.search(line)
                border_text = border_match.group(1)
                detected_commands.append(f"<border>{border_text}</border>")  # Replace with a placeholder for border

            if title_match:
                title_text = title_match.group(1)
                detected_commands.append(f"{title_text}")
                result_text.tag_configure("title", justify="center", font=("Arial", 20))
                result_text.insert("end", title_text, "title")
                result_text.insert("end", "\n\n")

            if author_match:
                detected_commands.append(f"{author_match.group(1)}")

            if date_match:
                detected_commands.append(f"{date_match.group(1)}")

            if textbf_match:
                plain_text = textbf_match.group(1)
                bold_text = re.sub(r'\\textbf\{(.+?)\}', r'\1', plain_text)  # Remove the LaTeX command
                detected_commands.append(f"{bold_text}")

                # Insert plain text without \textbf{} and apply the bold style
                result_text.insert(INSERT, bold_text + "\n")
                result_text.tag_add("bold", "end-1l", "end")
                result_text.tag_config("bold", font=("Arial", 12, "bold"))
                
            if textit_match:
                italic_text = textit_match.group(1)
                detected_commands.append(f"{italic_text}")
                result_text.insert(INSERT, italic_text + "\n")
                result_text.tag_add("italic", "end-2l", "end")
                result_text.tag_config("italic", font=("Arial", 12, "italic"))

            if underline_match:
                underline_text = underline_match.group(1)
                detected_commands.append(f"{underline_text}")
                result_text.insert(INSERT, underline_text + "\n")
                result_text.tag_add("underline", "end-2l", "end")
                result_text.tag_config("underline", underline=True)
                result_text.tag_config("underline", font=("Arial", 12, "underline"))
                

            
                
            if itemize_match:
                bullet_flag = True
                current_bullet_point = []
            elif "\\item" in line and bullet_flag:
                item_text = line.split("\\item", 1)[1].strip()
                current_bullet_point.append("• " + item_text)

            if enumerate_match:
                bullet_flag = False
                current_numbered_item = 1
            elif "\\item" in line and not bullet_flag:
                item_text = line.split("\\item", 1)[1].strip()
                current_bullet_point.append(f"{current_numbered_item}. {item_text}")
                current_numbered_item += 1

    detected_commands.extend(current_bullet_point)

    if detected_commands:
        result_text.delete("1.0", "end")
        for command in detected_commands:
            # Replace placeholder with RTF border representation
            command = command.replace("<border>", "{\\b\\i\\ul\\b0\\i0\\ulnone ") + "}"
            result_text.insert(INSERT, command + "\n\n")

def clear_input():
    input_text.delete("1.0", "end")

def clear_result():
    result_text.delete("1.0", "end")

# Create the main window
root = tk.Tk()
root.title("LaTeX Command Detector")

# Create a frame for the input text
input_frame = tk.Frame(root)
input_frame.pack(side="left", padx=10, pady=10)

# Create a frame for the result text
result_frame = tk.Frame(root)
result_frame.pack(side="right", padx=10, pady=10)

# Create and configure the input text widget
input_text = Text(input_frame, height=20, width=60)
input_text.pack()

# Create a scroll bar for the input text widget
scrollbar = Scrollbar(input_frame)
scrollbar.pack(side="right", fill="y")
input_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=input_text.yview)

# Create "Clear Input" button
clear_input_button = Button(input_frame, text="Clear Input", command=clear_input)
clear_input_button.pack()

# Create "Process" button to trigger LaTeX processing
process_button = Button(input_frame, text="Process LaTeX", command=process_latex)
process_button.pack()

# Create and configure the result text widget
result_text = Text(result_frame, height=20, width=60)
result_text.pack()

# Create "Clear Result" button
clear_result_button = Button(result_frame, text="Clear Result", command=clear_result)
clear_result_button.pack()

# Start the GUI main loop
root.mainloop()
