import language_tool_python

def fix_grammar(text: str) -> str:
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    return tool.correct(text)

if __name__ == "__main__":
    with open("article.txt", "r", encoding="utf-8") as f:
        original_text = f.read()

    corrected_text = fix_grammar(original_text)

    with open("corrected_document.txt", "w", encoding="utf-8") as f:
        f.write(corrected_text)

    print("Grammar correction complete!")
