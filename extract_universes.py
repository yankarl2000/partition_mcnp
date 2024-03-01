'''
extract_universes.py filename.i
сохраняет файлы типа u123.i в папку filename_universes по тому же пути

'''
import sys, os

def extract_universes(file_name):
    name = os.path.splitext(os.path.basename(file_name))[0]
    path = os.path.dirname(file_name)
    surf_name = os.path.join(path, name+'_universes', 'surf.i')
    try:  
        os.mkdir(os.path.join(path, name+'_universes'))
    except OSError as error:  
        print(error)   
    # задача цикла получить массивы номеров строк
    u_list = [] # номера universe
    begin_u = [] # - начала блоков universe начало первого cell
    end_u = [] # - номера строчек перед cell не из блока
    old_u, u = -1, -1 # предыдущий и текущий номер universe (-1 ~ нет universe)
    begin_cell = 0 # номер первой строки текущего cell
    universe = False # флаг - принадлежал ли предыдущий cell universe
    with open(file_name, 'r') as source, open(surf_name, 'w') as surf:
        c = 0 # счётчик номеров строк
        card = False
        for line in source:
            if card: # сохраняет поверхности и материалы
                surf.write(line)
                continue
            if line[0].isdigit(): # первая строка новой ячейки
                if universe: old_u = u
                else:
                    if old_u != -1:
                        end_u.append(begin_cell-1)
                    old_u = -1
                begin_cell = c
                universe = False
            else:
                if ' U=' in line:
                    universe = True
                    u = get_u(line)
                    if (u != old_u):
                        begin_u.append(begin_cell)
                        u_list.append(u)
                        print(f'get u{u}')
                        if old_u != -1:
                            end_u.append(begin_cell-1)
            if line == '\n':
                if universe: end_u.append(c-1)
                card = True
            c += 1
    if len(u_list)<1:print('no universes in file'); exit()
    # задача цикла сохранить файлы типа '_universes/u123.i'
    with open(file_name, 'r') as file:
        c = 0
        i = 0
        universe = False
        for line in file:
            if c == begin_u[i]:
                universe = True
                u_file_name = os.path.join(path, name+'_universes', f'u{u_list[i]}.i')
                u_file = open(u_file_name, 'w')
            if universe: u_file.write(line.replace('U=', '$U='))
            if c == end_u[i]:
                universe = False
                with open(surf_name, 'r') as surf:
                    u_file.write('\n')
                    for l in surf:
                        u_file.write(l)
                u_file.close()
                print(f'write u{u_list[i]}.i')
                i += 1
            if len(u_list) <= i: break
            c += 1
    os.remove(surf_name) 

def get_u(s):
    l = s.partition('U=')
    return int(l[2].split()[0])

if __name__ == "__main__":
    if len(sys.argv)<2:
        filename = input("enter filename: ")
    else:
        filename = sys.argv[1]
    extract_universes(filename)