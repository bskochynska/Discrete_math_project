@property
def students(self):
    return self.__students
@property
def activity_groups(self):
    return self.__activity_groups
@property
def grades(self):
    return self.__grades
def course_grade(self) -> list[tuple[Student, str]]:
    """Return each student's total grade converted to a letter (A-E)."""
    result = []
    for el in self.students:
        score = 0
        for group in self.activity_groups:
            for activity in group.activities:
                grade = self.grades.get((el.name, activity.name))
                if self.grades.get((el.name, activity.name)) is not None:
                    score += grade
        letter = 0
        if score >= 90:
            letter = 'A'
        elif score >= 82:
            letter = 'B'
        elif score >= 74:
            letter = 'C'
        elif score >= 64:
            letter = 'D'
        elif score >= 60:
            letter = 'E'
        elif score >= 35:
            letter = 'FX'
        else:
            letter = 'F'

        result.append((el, letter))
    return result
