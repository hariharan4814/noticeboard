from django.test import TestCase
from apps.accounts.models import CustomUser
from apps.students.models import Student
from apps.students.forms import StudentForm


class StudentFormTests(TestCase):

    def test_student_form_creates_user(self):
        form_data = {
            "name": "Jane Doe",
            "roll_number": "ROLL123",
            "department": "Computer Science",
            "year": "2",
            "email": "jane@example.com",
            "phone": "1234567890",
            "username": "janedoe",
            "password": "SecretPassword123"
        }

        form = StudentForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        student = form.save()

        # Check that student was saved
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student.name, "Jane Doe")

        # Check that corresponding user was saved
        self.assertIsNotNone(student.user)
        self.assertEqual(student.user.username, "janedoe")
        self.assertEqual(student.user.email, "jane@example.com")
        self.assertEqual(student.user.role, CustomUser.Role.STUDENT)
        self.assertTrue(student.user.check_password("SecretPassword123"))

    def test_student_delete_cascades_to_user_via_signal(self):
        student = Student.objects.create(
            name="Bob Smith",
            roll_number="ROLL456",
            department="Electrical Engineering",
            year="3",
            email="bob@example.com",
        )
        user = CustomUser.objects.create_user(
            username="bobsmith",
            password="Password123",
            email="bob@example.com",
            role=CustomUser.Role.STUDENT
        )
        student.user = user
        student.save()

        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 1)

        # Delete student, which should trigger signal to delete user
        student.delete()

        self.assertEqual(Student.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 0)

