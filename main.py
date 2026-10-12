student =[]
name = input("Enter student name:")
roll_no = input("Enter student roll number:")
branch = input("Enter student branch:")
marks = float(input("Enter student marks:"))
student = {
  "name":name,
  "roll_no":roll_no,
  "branch":branch,
  "marks":marks
}
students.append(student)
print("\n---Student Details---")
print("Name:",student["name"])
print("Roll Number:",student["roll_no"])
print("Branch:",student["branch"])
print("Marks:",student["marks"])
