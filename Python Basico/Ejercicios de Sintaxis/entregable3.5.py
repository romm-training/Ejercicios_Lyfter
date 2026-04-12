flow_controller = 1
grade = 0
count = 0
passing_grade = 70
passed_sum = 0
passed_count = 0
failed_sum = 0
failed_count = 0

while (flow_controller == 1):
    grade = int(input("Ingrese la nota del curso: "))
    if (grade >= passing_grade):
        passed_sum += grade
        passed_count += 1
    else:
        failed_sum += grade
        failed_count += 1

    flow_controller = int(input("Desea continuar? 1-SI 0-NO: "))

total_grades_count = passed_count + failed_count
total_grades_sum = passed_sum + failed_sum

total_average = total_grades_sum // total_grades_count if total_grades_count != 0 else 0
passed_average = passed_sum // passed_count if passed_count != 0 else 0
failed_average = failed_sum // failed_count if failed_count != 0 else 0

print(f"Cantidad de notas ingresadas: {total_grades_count}")
print(f"Cantidad de notas aprobadas: {passed_count}")
print(f"Cantidad de notas reprobadas: {failed_count}")
print(f"Promedio total: {total_average}")
print(f"Promedio Aprobadas: {passed_average}")
print(f"Promedio Reprobadas: {failed_average}")