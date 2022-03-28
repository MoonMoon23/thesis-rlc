from django.contrib.auth.models import Group
from .models import Faculty, Applications
from django import forms
import django_filters

class FacultyFilter(django_filters.FilterSet):

	#first_name = django_filters.CharFilter(lookup_expr='icontains')
	#last_name = django_filters.CharFilter(lookup_expr='icontains')
	faculty_id = django_filters.CharFilter(lookup_expr='exact', label="Faculty ID")

	
	class Meta:
		model = Faculty
		fields = [
			'faculty_id',
			'department',
			'college',
			'status',
			'access_level',
		]



class ApplicationsFilter(django_filters.FilterSet):
	
	SEMESTER_CHOICES = (
				('FIRST','FIRST'),
				('SECOND','SECOND'),
				('MIDYEAR','MIDYEAR'),
		)

	semester_applicable = django_filters.ChoiceFilter(label="Semester", choices=SEMESTER_CHOICES)

	class Meta:
		model = Applications
		fields = [
			'applicant',
			'semester_applicable',
			'schoolyear',
			'status',
			'associated_department',
		]