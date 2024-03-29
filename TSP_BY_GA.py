import random
import copy
import numpy as np

class Node:
    def __init__(self, Cycle = None, Distance = -1):
        self.Cycle = Cycle
        self.Distance = Distance

class Genetic_Algorithm:
    def __init__(self):
        self.Matrix = None
        self.Number = None
        self.Init_Solution = None
        self.Best_Solution = None
        self.Population = []
        self.Number_Individual = 5000
        self.Mutation_Rate = 0.3
        self.Crossover_Rate = 0.7
        self.Number_Sample = 10
        self.Number_Generation = 500
        self.Log = []

    def Import_Matrix(self, Path):

        def Is_Float(Number):
            try:
                float(Number)
                return True
            except ValueError:
                return False

        def Is_Symmetric():
            Temp = copy.deepcopy(self.Matrix)
            Temp = np.array(Temp)
            return np.array_equal(Temp,Temp.T)

        File = open(Path, 'r')
        Lines = File.readlines()
        self.Number = len(Lines)
        self.Matrix = [[0]*self.Number for _ in range(self.Number)]
        for Row in range(self.Number):
            Line = Lines[Row].split()
            if len(Line) != self.Number:
                print(f"Số phần tử hàng {Row} khác {self.Number} phần tử")
                exit(0)
            elif Is_Float(Line[Row]) == False or float(Line[Row]) != 0:
                print(f"Phần tử ở đường chéo chính hàng {Row} khác 0")
                exit(0)
            else:
                for Col in range(len(Line)):
                    if Is_Float(Line[Col]):
                        self.Matrix[Row][Col] = float(Line[Col])
                    else:
                        print(f"Phần tử '{Line[Col]}'(Row:{Row}, Col{Col}) không thể chuyển sang số thực")
                        exit(0)
        if Is_Symmetric() == False:
            print("Không phải ma trận đối xứng")
            exit(0)
        self.Initial_Population()
        File.close()

    def Export_Result(self, Path):
        File = open(Path, 'w')
        File.write("Kết quả tiến hóa di truyền\n\n".upper())
        File.write(f"{'':<30}{'Khoảng cách:':<30}{'Chu trình:'}\n")
        File.write(f"{'Chu trình khởi đầu:':<30}{self.Init_Solution.Distance:<30}{self.Init_Solution.Cycle}\n")
        File.write(f"{'Chu trình tốt nhất:':<30}{self.Best_Solution.Distance:<30}{self.Best_Solution.Cycle}\n")
        File.write("Danh sách cung:\n")
        File.write(f"{'':<30}{'Ban đầu:':<30}{'Tốt nhất:':<30}\n")
        for i in range(self.Number-1):
            uf = self.Init_Solution.Cycle[i+0]
            vf = self.Init_Solution.Cycle[i+1]
            wf = self.Matrix[uf][vf]
            uo = self.Best_Solution.Cycle[i+0]
            vo = self.Best_Solution.Cycle[i+1]
            wo = self.Matrix[uo][vo]
            Linef = f"{uf} <-- {wf} --> {vf}"
            Lineo = f"{uo} <-- {wo} --> {vo}"
            File.write(f"{'':<30}{Linef:<30}{Lineo:<30}\n")
        uf = self.Init_Solution.Cycle[-1]
        vf = self.Init_Solution.Cycle[0]
        wf = self.Matrix[uf][vf]
        uo = self.Best_Solution.Cycle[-1]
        vo = self.Best_Solution.Cycle[0]
        wo = self.Matrix[uo][vo]
        Linef = f"{uf} <-- {wf} --> {vf}"
        Lineo = f"{uo} <-- {wo} --> {vo}"
        File.write(f"{'':<30}{Linef:<30}{Lineo:<30}\n")
        File.close()
        print("Dữ liệu kết quả được ghi hoàn tất")

    def Export_Log(self, Path):
        File = open(Path, 'w')
        File.write("Quá trình tiến hóa di truyền\n\n".upper())
        for i in range(len(self.Log)):
            File.write(f"Thế hệ thứ {i}:\n")
            if i == 0 or i % 10 == 0:
                for Individual in self.Log[i]:
                    File.write(f"    Khoảng cách: {Individual.Distance:<30} Chu trình: {Individual.Cycle}\n")
            else:
                File.write("    Dữ liệu về thế hệ này đã được lượt bớt nhằm tiết kiệm tài nguyên\n")
            File.write("\n")
        File.close()
        print("Dữ liệu nhật ký được ghi hoàn tất")

    def Get_Distance(self, Array):
        Distance = 0
        Distance += self.Matrix[Array[-1]][Array[0]]
        for i in range(self.Number-1):
            Distance += self.Matrix[Array[i]][Array[i+1]]
        return Distance

    def Initial_Population(self):
        for each in range(self.Number_Individual):
            Individual = Node()
            Individual.Cycle = list(range(self.Number))
            random.shuffle(Individual.Cycle)
            Individual.Distance = self.Get_Distance(Individual.Cycle)
            self.Population.append(Individual)
        self.Init_Solution = min(self.Population, key=lambda x:x.Distance)

    def Evolution_Process(self):
        self.Log.append(sorted(self.Population, key=lambda x:x.Distance))
        print(f"Thế hệ đầu tiên(khởi tạo), khoảng cách tốt nhất {self.Init_Solution.Distance}")
        for i in range(self.Number_Generation):
            New_Population = []
            New_Population.append(sorted(self.Population, key=lambda x:x.Distance)[0])
            New_Population.append(sorted(self.Population, key=lambda x:x.Distance)[1])
            for each in range((self.Number_Individual-2)//2):
                if random.random() < self.Crossover_Rate:
                    Dad_Gene = min(random.sample(self.Population, k=self.Number_Sample), key=lambda x:x.Distance).Cycle
                    Mom_Gene = min(random.sample(self.Population, k=self.Number_Sample), key=lambda x:x.Distance).Cycle
                    Crossover_Point = random.randint(0,self.Number-1)
                    Child_Gene_F = Dad_Gene[:Crossover_Point] + [Cell for Cell in Mom_Gene if Cell not in Dad_Gene[:Crossover_Point]]
                    Child_Gene_S = Mom_Gene[:Crossover_Point] + [Cell for Cell in Dad_Gene if Cell not in Mom_Gene[:Crossover_Point]]
                else:
                    Child_Gene_F = random.choice(self.Population).Cycle
                    Child_Gene_S = random.choice(self.Population).Cycle
                if random.random() < self.Mutation_Rate:
                    Start, End = sorted(random.sample(range(self.Number), 2))
                    Child_Gene_F[Start:End+1] = reversed(Child_Gene_F[Start:End+1])
                    Start, End = sorted(random.sample(range(self.Number), 2))
                    Child_Gene_S[Start:End+1] = reversed(Child_Gene_S[Start:End+1])

                New_Population.append(Node(Cycle=Child_Gene_F,Distance=self.Get_Distance(Child_Gene_F)))
                New_Population.append(Node(Cycle=Child_Gene_S,Distance=self.Get_Distance(Child_Gene_S)))
            self.Population = New_Population
            self.Log.append(sorted(New_Population, key=lambda x:x.Distance))
            self.Best_Solution = min(New_Population, key=lambda x:x.Distance)
            if (i+1) % 10 == 0:
                print(f"Thế hệ thứ {i+1}, khoảng cách tốt nhất {self.Best_Solution.Distance}")

    def Main(self):
        self.Import_Matrix("100_Cities.txt")
        self.Evolution_Process()
        #self.Export_Result("Result.txt")
        #self.Export_Log("Log.txt")
        print("Chương trình thực thi hoàn tất")

GA = Genetic_Algorithm()
GA.Main()