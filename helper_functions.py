def remove_empty_lines(text):
    "\n".join([s for s in text.split("\n") if s])
    text = "".join([s for s in text.splitlines(True) if s.strip("\r\n")])
    return text
