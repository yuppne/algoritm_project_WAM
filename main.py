import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import subway_resource.geoLine as line
import subway_resource.linkData as link
import subway_resource.nodeData as node
import os.path
from collections import defaultdict
import math
from heapq import heapify, heappush, heappop

INF = 99999999
File_path = "w2/output.txt"

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("mainUI.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class Main_WindowClass(QMainWindow, form_class):
    result = list()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        # self.qPixmapFileVar = QPixmap()
        # self.qPixmapFileVar.load("subway.png")
        # self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1286)
        # self.lbl_picture.setPixmap(self.qPixmapFileVar)

        self.hide_input_box()

        self.dist = load_graph_file()
        print("load complete")

        self.topbgcolor.setStyleSheet("background-color: #B00020")
        self.topbgcolor_2.setStyleSheet("background-color: #B00020")
        self.howmany.setStyleSheet("Color: white")
        self.people_group_1.setStyleSheet("Color: white")
        self.people_group_2.setStyleSheet("Color: white")
        self.people_group_3.setStyleSheet("Color: white")
        self.people_group_4.setStyleSheet("Color: white")

        self.run_button2.setPixmap(QPixmap("go_button.png"))
        self.p_start_lbl_1.setStyleSheet("Color: black")
        self.p_start_lbl_2.setStyleSheet("Color: black")
        self.p_start_lbl_3.setStyleSheet("Color: black")
        self.p_start_lbl_4.setStyleSheet("Color: black")
        # self.people_number_c_box.setStyleSheet("background-color: white;" "Color: black")
        self.people_number_c_box.setStyleSheet("QComboBox"
                                               "{"
                                               "border : 3px solid black"
                                               "}"
                                               "QComboBox::! on:pressed"
                                               "{"
                                               "border : 3px white;"
                                               "border-style : dotted;"
                                               "}"
                                               "QComboBox::! on:hover"
                                               "{"
                                               "border : 4px red;"
                                               "border-style : dotted;"
                                               "}")

        self.home.setPixmap(QPixmap("snow.png"))
        self.home.setStyleSheet("background-color: #B00020")

        self.people_number_c_box.currentIndexChanged.connect(self.p_num_Function)

        # set the title
        title = "Fine Middle Point"
        self.setWindowTitle(title)

    def hide_input_box(self):
        self.people_group_1.hide()
        self.people_group_2.hide()
        self.people_group_3.hide()
        self.people_group_4.hide()

    def clear_input_label(self):
        self.p_start_lbl_1.clear()
        self.p_start_lbl_2.clear()
        self.p_start_lbl_3.clear()
        self.p_start_lbl_4.clear()

    def p_num_Function(self):  # input box 숨기기
        self.p_num = self.people_number_c_box.currentIndex() + 2

        self.hide_input_box()
        self.clear_input_label()

        self.make_input_place()

    def make_input_place(self):  # 이용 인원수에 따라 input box 보여주기
        if self.p_num == 2:
            self.people_group_1.show()
            self.people_group_2.show()
        elif self.p_num == 3:
            self.people_group_1.show()
            self.people_group_2.show()
            self.people_group_3.show()
        elif self.p_num == 4:
            self.people_group_1.show()
            self.people_group_2.show()
            self.people_group_3.show()
            self.people_group_4.show()

    def get_start_pos(self):  # n명의 출발지점 가져온 후 길찾기 함수 호출
        p = list()

        if self.p_num >= 2:
            p.append(self.p_start_lbl_1.text())
            p.append(self.p_start_lbl_2.text())
        if self.p_num >= 3:
            p.append(self.p_start_lbl_3.text())
        if self.p_num >= 4:
            p.append(self.p_start_lbl_4.text())

        return p


def find_way(p, dist):  # 길찾기 함수 시작
    print("in find way")

    length = len(node.nodeDataRaw)

    min_dist = INF
    min_rate = 0.0
    min_dist_arr = list()  # 최소거리를 저장
    d_id = [-1]  # 목적지 ID
    p_id = get_id_from_name(p)  # 출발지 ID

    print("check wrong station name")
    if p_id[0] == -1:  # 잘못된 역 이름 Check
        d_id.append("")
        for i in range(len(p_id) - 1):
            d_id[0] += "\"" + p_id[i + 1] + "\"역은 잘못된 역 이름 입니다.\n"
        return d_id
    print("out check")

    cost_list = [0 for i in range(len(p_id))]
    for i in node.nodeDataRaw:  # 각 출발점으로부터 some station 까지의 거리의 총합이 가장 작은 station 구하기
        total_dist = 0
        avg_rate = 0.0
        for j in p_id:
            cost_list[p_id.index(j)] = int(dist[j][i["no"]])
            total_dist += int(dist[j][i["no"]])
        avg_dist = total_dist / len(p_id)
        for x in range(len(p_id)):  # 평균 비율 계산
            cost_list[x] -= avg_dist
            avg_rate += abs(cost_list[x])
        print(avg_rate)
        if total_dist == min_dist and min_rate > avg_rate:
            min_dist = total_dist
            min_rate = avg_rate
            d_id[0] = i["no"]
        elif total_dist < min_dist and avg_rate < 500:
            min_dist = total_dist
            min_rate = avg_rate
            d_id[0] = i["no"]

    print(get_name_from_id(d_id))
    print(min_dist_arr)

    return get_name_from_id(d_id)


def get_id_from_name(p):  # id list를 입력받아 name list로 바꿈
    print("in get_id")
    p_temp = p.copy()
    p_id = list()
    p_count = 0

    for i in node.nodeDataRaw:
        for j in p_temp:
            if j == node.nodeDataRaw[i['no']]['nm']:
                p_temp.pop(p_temp.index(j))
                p_id.append(i['no'])
                p_count += 1
        if p_count == len(p):
            break

    if len(p_temp) != 0:
        print("잘못된 역 찾기 :", end="")
        print(p_temp)
        p_temp.insert(0, -1)
        return p_temp

    return p_id


def get_name_from_id(p_id):  # name list를 입력받아 id list로 바꿈
    print("in get name")

    p = list()

    for i in p_id:
        for j in node.nodeDataRaw:
            if int(j['no']) == i:
                p.append(j['nm'])
    return p


def load_graph_file():  # 그래프 파일 있으면 불러오고 없으면 생성
    print("in load graph")

    dist = list()
    length = len(node.nodeDataRaw)
    if os.path.isfile(File_path):  # 16초    불러오기
        print("file exist")
        with open(File_path, 'r') as output:
            for i in range(length):
                dist.append(list())
                line = output.readline()
                for j in range(length):
                    dist[i].append(line.split(' ')[j])
    else:
        print("file not exist")  # 2분31초  생성
        dist = make_graph(length)
    return dist


def make_graph_file(graph, length):  # 그래프 파일 만들기
    print("in make graph file")

    with open(File_path, 'w') as output:
        for i in range(length):
            for j in range(length):
                output.write('{0} '.format(str(graph[i][j])))
            output.write("\n")


def make_graph(length):  # 그래프 만들기 (nodeData와 linkData로)
    print("in make graph")

    link_length = len(link.linkDataRaw)

    graph = list()
    count = 0

    for i in range(length):
        graph.append(list())
        for j in range(length):
            if i == j:
                graph[i].append(0)
            else:
                graph[i].append(INF)

    for i in range(length):

        while count < len(link.linkDataRaw):
            if link.linkDataRaw[count][0] == i:
                if link.linkDataRaw[count][0] < length and link.linkDataRaw[count][1] < length:  # 없는 역과의 링크 체크
                    graph[i][link.linkDataRaw[count][1]] = link.linkDataRaw[count][2]
                    count += 1
                else:
                    count += 1
            else:
                break

    dist = floyd_warshall(graph, length)
    make_graph_file(dist, length)
    return dist


def floyd_warshall(a, n):
    print("in floyd_warshall")

    dist = a.copy()

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# utility: priority queue
class Pq:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return str(self.queue)

    def insert(self, item):
        heappush(self.queue, item)

    def extract_min(self):
        return heappop(self.queue)[1]

    def update_priority(self, key, priority):
        for v in self.queue:
            if v[1] == key:
                v[0] = priority
        heapify(self.queue)

    def empty(self):
        return len(self.queue) == 0


# utility: Graph
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(lambda: [])

    def add_edge(self, link_info):
        v = link_info[0]
        u = link_info[1]
        w = link_info[2]
        self.graph[v].append((u, w))

    def __str__(self):
        result = ''
        for v in self.V:
            result += f'{v}: {str(self.graph[v])}, \n'
        return result


def dijkstra(graph, s, length):
    Q = Pq()  # priority queue of vertices
    # [ [distance, vertex], ... ]
    d = dict.fromkeys(graph.V, math.inf)  # distance pair
    # will have default value of Infinity
    pi = dict.fromkeys(graph.V, None)  # map of parent vertex
    # useful for finding shortest path

    # initialize
    d[s] = 0

    # update priority if prior path has larger distance
    def relax(u, v, w):
        if d[v] > d[u] + w:
            d[v] = d[u] + w
            Q.update_priority(v, d[v])
            pi[v] = u

    # initialize queue
    for v in graph.V:
        Q.insert([d[v], v])
    while not Q.empty():
        u = Q.extract_min()
        for v, w in graph.graph[u]:
            if u < length and v < length:
                relax(u, v, w)
    return d, pi


def shortest_path(s, t):  # 순서 출력 , 환승역 issue
    length = len(node.nodeDataRaw)

    print("1")
    p = [s, t]
    p_id = get_id_from_name(p)
    print("1.5")
    s_id = p_id[0]
    t_id = p_id[1]

    temp_list = list()
    for i in range(length):
        temp_list.append(i)

    g = Graph(temp_list)
    print("2")
    for i in link.linkDataRaw:
        if i[0] < length and i[1] < length:
            g.add_edge(i)
    print("in dijk")
    d, pi = dijkstra(g, s_id, length)
    print("out dijk")
    path = [t_id]
    current = t_id
    # if parent pointer is None,
    # then it's the source vertex

    while pi[current]:
        path.insert(0, pi[current])
        # set current to parent
        current = pi[current]

    result = get_name_from_id(path)
    for i in range(len(result) - 1):
        if len(result) > 1:
            if result[i] == result[i + 1]:
                result[i + 1] += "(환승)"

    return result


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = Main_WindowClass()

    myWindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
