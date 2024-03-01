'''
del_material.py filename N

идём с самого начала, 
проверяем на совпадение ^'число'+'пробелы'+'номер материала'+'пробелы', 
до следуюшей строки вида ^'число' или пустой строки ничего не сохраняем
после первой пустой строки сохраняем всё в первосданном виде
'''
import sys, os

def is_mat(N, line, del_line):
    l = line.split()
    if line[0].isdigit():
        return l[0].isdigit() and (l[1] == N)
    else:
        return del_line

def del_material(file_name, N):
    name = os.path.splitext(os.path.basename(file_name))[0]
    path = os.path.dirname(file_name)
    del_name = os.path.join(path, f'del_M{N}_'+name+'.i')
    with open(file_name, 'r') as file, open(del_name, 'w') as new_file:
        del_line = False
        cells = True
        for line in file:
            if line == '\n':
                cells = False
            if is_mat(N, line, del_line) and cells:
                del_line = True
            else:
                del_line = False
                new_file.write(line)

if __name__ == "__main__":
    if len(sys.argv)<2:
        filename = input("enter filename: ")
        N = input("enter material number: ")
    elif len(sys.argv)<3:
        filename = sys.argv[1]
        N = input("enter material number: ")
    else:
        filename = sys.argv[1]
        N = sys.argv[2]
    del_material(filename, N)