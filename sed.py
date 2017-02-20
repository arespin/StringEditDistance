import math
import sys
sys.stdout = open("sed_string1_string2.txt", "w")

def main():
    s1 = '#' + sys.argv[1]
    s2 = '#' + sys.argv[2]

    vals, row_entries, stars = sed(s1, s2)
    print(vals[-1][-1])
    #backpath = []
    # for l1, l2 in list(zip(vals, row_entries)):
    #      backpath.append(list(zip(l1, l2)))
    printTables(s1,s2, vals, row_entries, stars)




def sed(s1, s2):
    if len(s1) < len(s2):
        return sed(s2, s1)
    if len(s2) == 0:
        return len(s1)

    traces = []
    vals = [[2*i for i in range(len(s1))] for j in range(len(s2))]
    backtrace = [[2*i for i in range(len(s1))] for j in range(len(s2))]
    vowels = set("aeoiu")
    consonants = set("qwrtypsdfghjklzxcvbnm")
    stars = []
    for i, c1 in enumerate(s2):
        if c1 == '#':
            continue
        for j, c2 in enumerate(s1):
            insertion = vals[i-1][j] + 2
            deletion = vals[i][j-1] + 2
            substitution = vals[i-1][j-1]
            if c1 != c2:
                if (c1 in vowels) and (c2 in vowels):
                    substitution += 0.5
                elif c1 in consonants and c2 in consonants:
                    substitution += 0.6
                elif (c1 in vowels and c2 in consonants) or (c2 in vowels and c1 in consonants):
                    substitution += 3
            m = min(insertion, deletion, substitution)
            if m == deletion and m != substitution:
                stars.append((i,j))
            vals[i][j] = m
            if vals[i][j] == insertion:
                 backtrace[i][j] =  (i-1, j)
            elif vals[i][j] == substitution:
                backtrace[i][j] = (i-1, j-1)
            elif vals[i][j] == deletion:
                backtrace[i][j] = (i , j-1)


    return vals, backtrace, stars

def printTables(s1, s2, vals, row_entries, stars):
    cur = (len(s2) - 1, len(s1) - 1)
    path = [cur]

    while (cur[0], cur[1]) > (0, 0):
        cur = row_entries[cur[0]][cur[1]]
        path.append( cur)

    path = path[::-1]
    # PRINT THE LETTER CORRESPONDENCE
    print('-' * (5 * len(s1)) + '--')
    print('    ' + "    ".join(s1))
    print('-' * (5 * len(s1)) + '--')
    for e1, c1 in enumerate(s2):
        line = c1 + '  '
        for e2, c2 in enumerate(s1):
            if (e1, e2) in path:
                if (e1, e2) in stars:
                    line +=  '*:' + c2 + " " * 2
                else:
                    line +=  c1 + ':' + c2 + " "*2

            else:
                line += " "*5
        print(line)

    print('\n\n')
    print('-' * (5 * len(s1)) + '--')
    print('    ' + "    ".join(s1))
    print('-' * (5 * len(s1)) + '--')

    for e1, c1 in enumerate(s2):
        line = c1 + '  '
        for e2, c2 in enumerate(s1):
            if (e1, e2) in path:
                line +=  "{0:.1f}".format(vals[e1][e2]) + " "*2

            else:
                line += " "*5
        print(line)

if __name__ == '__main__':
    main()
