from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import Faculty, Office, Applications, Projects, Progress_Reports
from django.contrib.auth.models import Group
from django import forms

class FacultyCreationForm(UserCreationForm):

    class Meta:
        model = Faculty
        fields = ('faculty_id',)


class FacultyChangeForm(UserChangeForm):

    class Meta:
        model = Faculty
        fields = ('faculty_id',)

class CreateFacultyForm(ModelForm):

	class Meta:
		model = Faculty
		fields = [
		'faculty_id',
		'first_name',
		'middle_name',
		'last_name',
		'password',
		'email',
		'department',
		'college',
		'designation',
		'rank',
		'access_level',
		'is_staff',
		'is_superuser',
		]

class AdminUpdateFacultyForm(ModelForm):

	class Meta:
		model = Faculty
		fields = [
		'faculty_id',
		'first_name',
		'middle_name',
		'last_name',
		'password',
		'email',
		'department',
		'college',
		'designation',
		'rank',
		'status',
		'remarks',
		'access_level',
		'is_staff',
		'is_superuser',
		]

class CreateRLCForm(ModelForm):

	class Meta:
		model = Projects
		fields = [
		'application',
		'title',
		'original_name',
		'date_started',
		'date_completed',
		'percent_completed',
		'authors',
		'project_file',
		]

class CreateApplicationForm(ModelForm):

	class Meta:
		model = Applications
		fields = [
		'applicant',
		'units',
		'semester_applicable',
		'schoolyear',
		'associated_department',
		'associated_college',
		]

class ExtendApplication(ModelForm):

	#need to add department and college
	class Meta:
		model = Applications
		fields = [
		'units',
		]
