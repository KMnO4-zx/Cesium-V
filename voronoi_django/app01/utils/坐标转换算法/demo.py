from 坐标转换算法.run import Solution
import json
import pprint

if __name__ == '__main__':
    json_data = []
    s = Solution(9, 50)
    s.deal()
    for i in range(s.size - 1):
        for j in range(s.size - 1):
            json_data.append(
                s.coordinate_table[i][j] + s.coordinate_table[i][j + 1] + s.coordinate_table[i + 1][j + 1] +
                s.coordinate_table[i + 1][j])
    data_ = json.dumps(json_data)
    with open('9-50.json', mode='w', encoding='utf-8') as f:
        f.write(data_)
