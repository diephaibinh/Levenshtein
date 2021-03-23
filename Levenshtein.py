
#----------------Thêm, xóa, thay thế chữ----------------#

def String_insert(string, text, position):
    return string[:position] + text + string[position:]


def String_delete(string, position):
    return string[:position] + string[(position + 1):]


def String_substitute(string, new_text, position):
    return string[:position] + new_text + string[(position + 1):]


#---------------Thuật toán tính khoảng cách Levenshtein----------------#

def Create_Matrix(str1, str2):
    matrix = []
    
    # Create matrix
    row = []
    for i in range(len(str2) + 1):
        row = []
        if i == 0:
          for j in range(len(str1) + 1):
            row.append(j)
        else:
            row.append(i)
    
        matrix.append(row)

    # Find minimum edit distance
    previous_row = 0
    for i, c1 in enumerate(str2):
        row = []
        current_row = previous_row + 1
        for j, c2 in enumerate(str1):
            value = 0
        
            if c2 == c1:
                value = matrix[previous_row][j]
            else:
                substitutions = matrix[previous_row][j]
                deletions = matrix[previous_row + 1][j]
                insertions = matrix[previous_row][j + 1]
                value = min(substitutions, deletions, insertions) + 1
        
            matrix[current_row].append(value)

        previous_row += 1

    return matrix


def Create_Backtrace_List(str1, str2, matrix):
    backtrace_list = []

    case_1 = 'insertion'
    case_2 = 'deletion'
    case_3 = 'substitution'
    case_4 = '0'

    rows = len(matrix)
    cols = len(matrix[0])

    c_NextCell = cols - 1
    r_NextCell = rows - 1

    while r_NextCell > 0:
        str1_char_index = c_NextCell - 1
        str2_char_index = r_NextCell - 1

        if str1[str1_char_index] == str2[str2_char_index]:
            backtrace_list.append(case_4)
            c_NextCell = c_NextCell - 1
            r_NextCell = r_NextCell - 1

        else:
            substitutions = matrix[r_NextCell - 1][c_NextCell - 1]
            deletions = matrix[r_NextCell][c_NextCell - 1]
            insertions = matrix[r_NextCell - 1][c_NextCell]

            value = min(substitutions, deletions, insertions)
        
            if value == insertions:
                backtrace_list.append(case_1 + '_' + str2[str2_char_index])
                r_NextCell = r_NextCell - 1
            else:         
                if value == deletions:
                    backtrace_list.append(case_2 + '_' + str1[str1_char_index])
                    c_NextCell = c_NextCell - 1
                else:
                    if value == substitutions:
                        backtrace_list.append(case_3 + '_' + str2[str2_char_index])
                        c_NextCell = c_NextCell - 1
                        r_NextCell = r_NextCell - 1
    
    return backtrace_list

# --------------------------------Phần trên là thuật toán, bắt đầu từ đây thôi-----------------------------------------#    

# Khoảng cách Levenshtein giữa 2 chuỗi
# Input: 2 chuỗi (String)
#    + Str1 (String)
#    + Str2 (String)
# Output: Khoảng cách Levenshtein (kiểu Int)
def Levenshtein_distance(str1, str2):
    matrix = Create_Matrix(str1, str2)
    rows = len(matrix)
    cols = len(matrix[0])
    return matrix[rows - 1][cols - 1]



# Source: https://stackoverflow.com/questions/14260126/how-python-levenshtein-ratio-is-computed
# Tính tỉ lệ tương đồng giữa 2 chuỗi
# Input: 2 chuỗi (String)
#    + Str1 (String)
#    + Str2 (String)
# Output: Tỉ lệ tương đồng bao nhiêu % (Float)
def Matching_ratio(str1, str2):
    l = Levenshtein_distance(str1, str2)
    m = len(str1)
    if m < len(str2):
        m = len(str2)
    ratio = (1 - l/m) * 100

    return ratio



# Tính tỉ lệ tương đồng của từng câu trong mảng 1 với từng câu trong mảng 2
# Input: 
#    + List_1 (String)
#    + List_2 (String)
# Output: List của các dictionary. Với mỗi dictionary có format:
#    + 'senA': <câu A>
#    + 'senB': <câu B>
#    + 'ratio': <tỉ lệ tương đồng (ratio)> [kiểu float]
def Matching_ratio_dict(lst_1, lst_2):
    result = []

    key_1 = "senA"
    key_2 = "senB"
    key_3 = "ratio"

    for str1 in lst_1:
        for str2 in lst_2:
            dic = {}
            dic[key_1] = str1
            dic[key_2] = str2
            dic[key_3] = Matching_ratio(str1, str2)
            result.append(dic)

    return result



def main():   
    lst1 = ['Không có kính không phải vì xe không có kính', 'Bom giật bom run kính vỡ đi rồi', 'Ung dung buồng lái ta ngồi']
    lst2 = ['Nhìn đất nhìn trời nhìn thẳng', 'Nhìn thấy gió vào xoa mắt đắng', 'Nhìn thấy con đường chạy thẳng vào tim']

    result = Matching_ratio_dict(lst1, lst2)
    for dic in result:
        values = list(dic.values())
        string = values[0] + ' - ' + values[1] + ': ' + str(values[2]) + " %"
        print(string)




if __name__ == "__main__":
    main()
