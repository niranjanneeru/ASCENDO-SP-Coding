def evaluate(code):
    try:
        code = cleanup(list(code))
        bracemap = buildbracemap(code)

        cells, codeptr, cellptr = [0], 0, 0

        result = ''

        while codeptr < len(code):
            command = code[codeptr]

            if command == ">":
                cellptr += 1
                if cellptr == len(cells): cells.append(0)

            if command == "<":
                cellptr = 0 if cellptr <= 0 else cellptr - 1

            if command == "+":
                cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

            if command == "-":
                cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

            if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
            if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
            if command == ".": result += (chr(cells[cellptr]))
            if command == ",": return "There was an Input Statement Hence Invalid", -1

            codeptr += 1

        return result, 0
    except:
        return "Compilation Error", 1


def cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[": temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap
