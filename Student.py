#Mỗi đối tượng học sinh có các thuộc tính sau: id, tên, giới tính, tuổi, điểm toán, 
#điểm lý, điểm hóa, điểm trung bình và học lực.

class Student:
    def __init__(self, StudentId, Name, Gender, DoB, Math, Physic, Chem):
        self._StudentId = StudentId
        self._Name = Name
        self._Gender = Gender
        self._DoB = DoB
        self._Math = Math
        self._Physic = Physic
        self._Chem = Chem
        self._Gpa = 0
        self._Rank = " "