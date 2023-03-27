from Management import ManagementStudent
from Student import Student
 
# khởi tạo một đối tượng QuanLySinhVien để quản lý sinh viên
manage = ManagementStudent()
while True:
    print("\nManagement Student by Python")
    print("_______________________MENU____________________________")
    print("||  1. Add Student.                                  ||")
    print("||  2. Update Student information by ID.             ||")
    print("||  3. Delete Student by ID.                         ||")
    print("||  4. Find Student by ID.                           ||")
    print("||  5. Find Stunent By Name.                         ||")
    print("||  6. Sort From Student by GPA (A->Z).              ||")
    print("||  9. Show all Student.                             ||")
    print("||  0. Exit                                          ||")
    print("_______________________________________________________")
     
    key = int(input("Enter option: "))
    if (key == 1):
        print("\n1. Add Student.")
        manage.NewStudent()
        print("\nSucessfull!")
    elif (key == 2):
        if (manage.QuantStudent() > 0):
            print("\n2. Update Student information. ")
            print("\nEnter Student ID: ")
            ID = int(input())
            manage.updateStudent(ID)
        else:
            print("\nStudent list is empty!")
    elif (key == 3):
        if (manage.QuantStudent() > 0):
            print("\n3. Detele Student.")
            print("\nEnter ID: ")
            ID = int(input())
            if (manage.DeleteById(ID)):
                print(f"\nStudent with id = {ID} has been Deleted.")
            else:
                print(f"\nStudent with id = {ID} doesn't exits.")
        else:
            print("\nStudent list is empty!")
    elif (key == 4):
        if (manage.QuantStudent() > 0):
            print("\n4. Find Student by ID.")
            print("\nEnter Student ID to Find: ")
            ID = input()
            searchId = manage.FindById(ID)
            manage.ShowID(searchId)
        else:
            print("\nStudent list is empty!")
    elif (key == 5):
        if (manage.QuantStudent() > 0):
            print("\n5. Find Student by Name.")
            print("\nEnter Student Name to Find: ")
            Name = input()
            SearchName = manage.FindByName(Name)
            manage.ShowStudent(SearchName)
        else:
            print("\nStudent list is empty!")
    elif (key == 6):
        if (manage.QuantStudent() > 0):
            print("8. Sort Student by Gpa (A -> Z).")
            manage.SortByGpa()
            manage.ShowStudent(manage.GetListStudent())
        else:
            print("\nStudent list is empty!")
    elif (key == 9):
        if (manage.QuantStudent() > 0):
            print("\n9. Show All Student.")
            manage.ShowStudent(manage.GetListStudent())
        else:
            print("\nStudent list is empty!")
    elif (key == 0):
        print("\nGood bye!")
        break
    else:
        print("\nThis Funtion doesn't exits!")
        print("\nPlease Select Funtion in Menu.")