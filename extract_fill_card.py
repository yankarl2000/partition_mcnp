'''
extract_fill_card.py filename.i
создает файл filename_fill_card.i
'''
import sys, os

def extract_fill_card(file_name, log=True):
    name = os.path.splitext(os.path.basename(file_name))[0]
    path = os.path.dirname(file_name)
    surf_name = os.path.join(path, name+'_surf.i')
    fill_name = os.path.join(path, name+'_fill_card.i')
    begin_f = [] # - начало первого cell (fill)
    end_f = [] # - номера строчек перед cell не из блока fill
    begin_cell = 0 # номер первой строки текущего cell
    with open(file_name, 'r') as file, open(surf_name, 'w') as surf:
        c = 0 # счётчик номеров строк
        card = False
        for line in file:
            if card: # сохраняет поверхности и материалы
                surf.write(line)
                continue
            if line[0].isdigit(): # первая строка новой ячейки
                begin_cell = c
            else:
                if ' FILL=' in line:
                    if log: print(f'get FILL={line.partition("FILL=")[2]}')
                    begin_f.append(begin_cell)
                    end_f.append(c-1)
            if line == '\n':
                if card: break
                card = True
            c += 1
    if len(begin_f)<1:
        os.remove(surf_name)
        return 'no fill card in file'
    # задача цикла сохранить файл filename_fill_card.i
    with open(file_name, 'r') as file, open(fill_name, 'w') as fill:
        c = 0
        i = 0
        for line in file:
            if begin_f[i] <= c <= end_f[i]:
                fill.write(line)
            if c == end_f[i]:
                i += 1
            if len(begin_f) <= i: break
            c += 1
        with open(surf_name, 'r') as surf:
                    fill.write('\n')
                    for l in surf:
                        fill.write(l)
    os.remove(surf_name)
    return f'the "{name}_fill_card.i" file was created successfully'

if __name__ == "__main__":
    if len(sys.argv)<2:
        filename = input("enter filename: ")
    else:
        filename = sys.argv[1]
    message = extract_fill_card(filename)
    print(message)