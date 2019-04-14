# 生成随机数模块
import random
# 数学运算
import math
# import tkinter
from tkinter import *
import time
# 设置目标状态（0表示空位）
_goal_state = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]


# 寻找列表中是否存在
def index(item, seq:'List[]'):
    if item in seq:
        return seq.index(item)
    else:
        return -1


# 八数码问题
class EightPuzzle:
    def __init__(self):
        # h(n)
        self._hval = 0
        # g(n)
        self._depth = 0
        # 搜索树中的双亲结点
        self._parent = None
        self.adj_matrix = []
        # 从目标状态出发随机构造，确保一定有解
        for i in range(3):
            self.adj_matrix.append(_goal_state[i][:])

    # 相等
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    # 打印形式
    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    # 复制自身
    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    # 生成合法移动
    def _get_legal_moves(self) -> 'List[(int,int)]':
        # 寻找空位
        row, col = self.find(0)
        free = []
        
        # 判断合法移动
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    # 生成移动
    def _generate_moves(self) -> 'List[EightPuzzle]':
        # 合法移动
        free = self._get_legal_moves()
        # 找空位
        zero = self.find(0)

        # 执行移动
        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a,b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        # 尝试每个合法移动
        return map(lambda pair: swap_and_clone(zero, pair), free)

    # 生成解决路径
    def _generate_solution_path(self, path):
        # 搜索到根节点
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    # 解决问题主函数
    def solve(self, h:'function'):
        # 目标测试函数
        def is_solved(puzzle:'EightPuzzle') -> 'bool':
            return puzzle.adj_matrix == _goal_state

        open_list = [self]
        closed_list = []
        move_count = 0
        while len(open_list) > 0:
            x = open_list.pop(0)
            move_count += 1
            # 目标测试
            if (is_solved(x)):
                if len(closed_list) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()
            index_open = index_closed = -1
            for move in succ:
                # 是否已经遇见这种状态
                index_open = index(move, open_list)
                index_closed = index(move, closed_list)
                # 计算距离目标状态的距离h(n)
                h_n = h(move)
                # 评价函数
                # f(n) = h(n) + g(n)
                f_n = h_n + move._depth

                # 没遇到过这个状态
                if index_closed == -1 and index_open == -1:
                    move._hval = h_n
                    open_list.append(move)
                # 在open列表中
                elif index_open > -1:
                    copy = open_list[index_open]
                    if f_n < copy._hval + copy._depth:
                        # 符合条件直接复制
                        copy._hval = h_n
                        copy._parent = move._parent
                        copy._depth = move._depth
                # 在closed列表中
                elif index_closed > -1:
                    copy = closed_list[index_closed]
                    if f_n < copy._hval + copy._depth:
                        move._hval = h_n
                        closed_list.remove(copy)
                        open_list.append(move)

            closed_list.append(x)
            # 根据f(n)进行排序
            open_list = sorted(open_list, key=lambda p: p._hval + p._depth)

        return [], 0

    # 随机生成初始状态
    def random_shuffle(self, step_count):
        # 从目标状态出发随即构造，确保一定有解
        for i in range(step_count):
            row, col = self.find(0)
            free = self._get_legal_moves()
            target = random.choice(free)
            self.swap((row, col), target)            
            row, col = target

    # 根据数字确定坐标
    def find(self, value: 'int') -> '(int,int)':
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    # 获取指定坐标的数字
    def peek(self, row:'int', col:'int'):
        return self.adj_matrix[row][col]

    # 给某个指定坐标赋值
    def poke(self, row:'int', col:'int', value:'int'):
        self.adj_matrix[row][col] = value

    # 根据坐标交换两个数字
    def swap(self, pos_a:'int', pos_b:'int'):
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)

# 启发式搜索
def heur(puzzle, item_total_calc:'func(current row:int, target roe:int, current col:int, target col:int)->int', total_calc:'func(t:int)->int') -> 'int':
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # account for 0 as blank
            if target_row < 0: 
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)


# 计算h值
def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)


# GUI shows 简单GUI动画展示
def GUI_shows(numberss, root):
    
    couter_row = 0
 
    # def on_closing():text=number, bg ='red',
    #     root.destroy()
    colors = ['#ffffff', '#CD5555', '#EE7621', '#4169E1', '#6A5ACD', '#FFA500', '#48D1CC', '#00CD66', '#66CD00' ]
    for numbers in numberss:
        couter_line = 0
        for number in numbers:
            if number == 0:
                Label(width=10, height=5).grid(row=couter_row, column=couter_line)
            else:
                Label(text=number, bg=colors[number], fg='white', width=10, height=5).grid(row=couter_row, column=couter_line)
            couter_line = couter_line + 1
        couter_row = couter_row + 1 
    root.update()
   

# 主函数 运行，调用其他函数
def main():
    p = EightPuzzle()
    # 简化问题，演示方便，设置步数为20
    p.random_shuffle(18)
    # 打印初始状态
    
    root = Tk()
    root.title("八数码问题")
    path, count = p.solve(h_manhattan)
    path.reverse()
    
    
    print(p)
    for i in path:
        print(i)
        GUI_shows(i.adj_matrix, root)
        time.sleep(2)
    
    # print ("Solved with Manhattan distance exploring", count, "states")
    root.mainloop()

if __name__ == "__main__":\
    main()
    