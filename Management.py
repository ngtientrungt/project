from Student import Student

import os
import re

class ManagementStudent:
    #khởi tạo 1 list để chứa thông tin học sinh
    listStudent = []
    
    #Id là mã học sinh tự động tăng và bắt đầu từ số 1
    def generateId(self):
        maxId = 1
        if (self.QuantStudent() > 0):
            maxId = self.listStudent[0]._StudentId
            for Stu in self.listStudent:
                if (maxId < Stu._StudentId):
                    maxId = Stu._StudentId
            maxId += 1
        return maxId
            

    def QuantStudent(self):
        #__len__ giúp trả về độ dài của chuỗi, ở đây giúp trả vể số lượng học sinh
        return self.listStudent.__len__()
    
    def NewStudent(self):
        # Khởi tạo một học sinh mới
        StudentId = self.generateId()
        Name = input("Enter student's name: ")
        while True:
            Gender = input("Enter student's (Male/Female) gender: ").capitalize()
            if re.match(r"^Male$|^Female$", Gender): 
                break
            else:
                print("Error!, Please input agian!")

        DoB = input("Enter student Date of Birth - (dd/mm/yyyy): ")

        #Math, Physic, Chem sử dụng float 
        Math = float(input("Enter Math: "))
        Physic = float(input("Enter Physic: "))
        Chem = float(input("Enter Chem: "))

        Stu = Student(StudentId, Name, Gender, DoB, Math, Physic, Chem)
        self.ComputeGpa(Stu)
        self.FindRank(Stu)
        self.listStudent.append(Stu)
    
    def updateStudent(self, ID):
        # Tìm kiếm học sinh trong danh sách listStudent
        Stu:Student = self.FindById(ID)
        # Nếu học sinh tồn tại thì cập nhập thông tin học sinh
        if (Stu != None):
        # nhập thông tin học sinh
            Name = input("Enter student's name: ")
            while True:
                Gender = input("Enter student's (Male/Female) gender: ").capitalize()
                if re.match(r"^Male$|^Female$", Gender): 
                    break

            DoB = input("Enter student Date of Birth - (dd/mm/yyyy): ")

            Math = float(input("Enter Math: "))
            Physic = float(input("Enter Physic: "))
            Chem = float(input("Enter Chem: "))
            # cập nhật thông tin học sinh
            # ._ proteted atribute giúp truy cập ngoài packet bởi lớp con
            Stu._Name = Name
            Stu._Gender = Gender
            Stu._DoB = DoB
            Stu._Math = Math
            Stu._Physic = Physic
            Stu._Chem = Chem
            self.ComputeGpa(Stu)
            self.FindRank(Stu)
        else:
            print(f"Student with {ID} doesn't exits.")
            
    #Hàm tính điểm Gpa cho học sinh
    def ComputeGpa(self, Stu:Student):
        Gpa = (Stu._Math + Stu._Physic + Stu._Chem) / 3
        # làm tròn điểm trung binh với 2 chữ số thập phân
        Stu._Gpa = round(Gpa, 2)
        
    #Hàm xếp loại học lực cho nhân viên
    def FindRank(self, Stu:Student):
        if (Stu._Gpa >= 8):
            Stu._Rank = "Excellent"
        elif (Stu._Gpa >= 6.5):
            Stu._Rank = "Good"
        elif (Stu._Gpa >= 5):
            Stu._Rank = "Pass"
        else:
            Stu._Rank = "Fail"

    #Hàm sắp xếp danh sach học sinh theo điểm Gpa tăng dần
    def SortByGpa(self):
        self.listStudent.sort(key=lambda x: x._Gpa, reverse=False)

    # Hàm tìm kiếm học sinh theo Id
    # Trả về một học sinh
    def FindById(self, ID):
        ResultId = 0
        if (self.QuantStudent() > 0):
            for Stu in self.listStudent:
                if (Stu._StudentId == ID):
                    ResultId = Stu
        return Stu
        
    # Hàm tìm kiếm học sinh theo tên
    # Trả về một danh sách học sinh
    def FindByName(self, keyword):
        listShow = []
        if (self.QuantStudent() > 0):
            for Stu in self.listStudent:
                if (keyword.capitalize() in Stu._Name.capitalize()):
                    listShow.append(Stu)
        return listShow
        
    # Hàm xóa học sinh theo ID
    def DeleteById(self, ID):
        isDeleted = False
        # tìm kiếm học sinh theo ID
        Stu = self.FindById(ID)
        if (Stu != None):
            self.listStudent.remove(Stu)
            isDeleted = True
        return isDeleted

    def ShowStudent(self, listShow):
        # hien thi tieu de cot
        print("{:^8} {:<18} {:^8} {:^18} {:^8} {:^8} {:^8} {:^8} {:^8}"
            .format("ID", "Name", "Gender", "DoB", "Math", "Physic", "Chem", "Gpa", "Rank"))
        # hien thi danh sach học sinh
        if (listShow.__len__() > 0):
            for Stu in listShow:
                print("{:^8} {:<18} {:^8} {:^18} {:^8} {:^8} {:^8} {:^8} {:^8}"
                    .format(Stu._StudentId, Stu._Name, Stu._Gender, Stu._DoB, Stu._Math, Stu._Physic, Stu._Chem, 
                            Stu._Gpa, Stu._Rank))
        print("\n")

    def ShowID(self, Stu):
        # hien thi tieu de cot
        print("{:^8} {:<18} {:^8} {:^18} {:^8} {:^8} {:^8} {:^8} {:^8}"
            .format("ID", "Name", "Gender", "DoB", "Math", "Physic", "Chem", "Gpa", "Rank"))
        # hien thi danh sach học sinh
        if (Stu in self.listStudent):
            for Stu in self.listStudent:
                print("{:^8} {:<18} {:^8} {:^18} {:^8} {:^8} {:^8} {:^8} {:^8}"
                    .format(Stu._StudentId, Stu._Name, Stu._Gender, Stu._DoB, Stu._Math, Stu._Physic, Stu._Chem, 
                            Stu._Gpa, Stu._Rank))
        print("\n")

    # Hàm trả về danh sách học sinh hiện tại
    def GetListStudent(self):
        return self.listStudent




