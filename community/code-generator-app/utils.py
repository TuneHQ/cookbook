language_to_extensions_map = {
  "Python": "py",
  "JavaScript": 'js',
  "Java": "java",
  "C++": "cpp",
  "Haskell": "hs"
}

def get_supported_languages():
    return ["Python", "JavaScript", "Java", "C++", "Haskell"]

def get_file_extension(programming_language):
    if programming_language in language_to_extensions_map:
        return language_to_extensions_map[programming_language]
    else: 
        return "txt"
    
def extract_between_backticks(text):
    lines = text.split('```')
    code_snippet = lines[1]
    code_snippet_clean = code_snippet[code_snippet.find("\n"):]
    return code_snippet_clean