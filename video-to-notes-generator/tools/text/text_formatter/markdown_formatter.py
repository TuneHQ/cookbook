import os

import mistune


class MarkdownFormatter:
    def __init__(self, text, save_folder):
        self.text = text
        self.save_folder = save_folder

    def fix_formatting(self):
        # Use mistune to parse and reformat the markdown text
        markdown = mistune.create_markdown()
        self.text = markdown(self.text)

    def save_file(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        file_path = os.path.join(self.save_folder, "formatted_markdown.md")
        with open(file_path, "w") as file:
            file.write(self.text)
        return file_path


# Example usage:
# formatter = MarkdownFormatter("#Header\n##Subheader\nContent", "output_folder")
# formatter.fix_formatting()
# file_path = formatter.save_file()
# print(f"File saved at: {file_path}")
