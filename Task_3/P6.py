def analyze_grades(grade_list):
    print("Avarage: " + str(sum(grade_list) / len(grade_list) if grade_list else 0))
    print("Highst: " + str(max(grade_list)))
    print("Lowest: " + str(min(grade_list)))

analyze_grades([10, 15, 30, 25])