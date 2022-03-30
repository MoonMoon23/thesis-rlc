from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from .managers import FacultyManager
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import datetime

#overrides django group class
class Office(models.Model):
	
	office_name = models.CharField(max_length=200, verbose_name="Office Name", default="")
	parent_office = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, default="")

	#checks if inputted office is department or college
	is_department = models.BooleanField(default=True, verbose_name="Is Department?")
	
	def __str__(self):
		return self.office_name


#overrides django user class
class Faculty(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=200, verbose_name="First Name", blank=True)
	middle_name = models.CharField(max_length=200, verbose_name="Middle Name", blank=True)
	last_name = models.CharField(max_length=200, verbose_name="Last Name", blank=True)
	faculty_id = models.CharField(max_length=10, verbose_name="Faculty ID", default="0000000000", unique=True)
	email = models.EmailField(verbose_name="Email Address")
	department = models.ForeignKey('Office', on_delete=models.PROTECT, limit_choices_to={'is_department':True}, related_name='+', null=True, blank=True)
	college = models.ForeignKey('Office', on_delete=models.PROTECT, limit_choices_to={'is_department':False}, null=True, blank=True)

	
	DESIGNATION_TITLES = (
			('Instructor', 'Instructor'),
			('Associate Professor', 'Associate Professor'),
			('Assistant Professor', 'Assistant Professor'),
			('Professor', 'Professor',)
		)

	designation = models.CharField(
			max_length=20,
			choices = DESIGNATION_TITLES,
			default = 'Instructor',
		)

	RANK_OPTIONS =(
			('1','1'),
			('2','2'),
			('3','3'),
			('4','4'),
			('5','5'),
			('6','6'),
			('7','7'),
		)

	rank = models.CharField(max_length = 1,choices = RANK_OPTIONS, default ='1')

	STATUS_OPTIONS = (
			('Active', 'Active'),
			('Inactive', 'Inactive'),
		)

	status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='Active', verbose_name="Faculty Status")

	username = None
	USERNAME_FIELD = 'faculty_id'
	REQUIRED_FIELDS = []

	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	access_level = models.ForeignKey('auth.Group',on_delete=models.PROTECT, null=True, blank=True, verbose_name="Access Level")
	remarks = models.TextField(default="", blank=True, verbose_name="Remarks")

	objects = FacultyManager()

	def __str__(self):
		return '{0} {1}'.format(self.first_name,self.last_name)

	def get_absolute_url(self):
		return reverse('admin-faculty-detail',args=[str(self.id)])

	def get_name(self):
		split_name = self.first_name.split()
		name = split_name[0]
		return '%s'% (name)

	def get_access_level(self):
		level = self.access_level
		return '%s'% (level)

	'''
	def admin_detail_view(self):
		return reverse('admin-faculty-detail',kwargs = {'pk' : self.id})
	'''
	
	class Meta:
		verbose_name_plural = "Faculty Members"


''' these functions are to calculate the schoolyear'''
def get_current_year():
	return datetime.date.today().year

def get_next_year():
	return datetime.date.today().year+1

def year_choices():
	return [(r,r) for r in range(2020, get_next_year()+1)]

class Applications(models.Model):
	applicant = models.ForeignKey('Faculty', on_delete=models.PROTECT, default="", verbose_name="Applicant")
	units = models.CharField(max_length=1, verbose_name="Number of Units", blank=True)
	previous_application = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, default="")

	SEMESTER_CHOICES = (
			('FIRST','FIRST'),
			('SECOND','SECOND'),
			('MIDYEAR','MIDYEAR'),
		)

	semester_applicable = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='FIRST', verbose_name="Applicable Semester")
	schoolyear = models.IntegerField(choices=year_choices(), default=get_current_year(), verbose_name="Schoolyear")

	STATUS_OPTIONS = (
			('DRAFT', 'DRAFT'),
			('PENDING DEPARTMENT APPROVAL', 'PENDING DEPARTMENT APPROVAL'),
			('FOR REVISION', 'FOR REVISION'),
			('PENDING COLLEGE APPROVAL', 'PENDING COLLEGE APPROVAL'),
			('APPROVED', 'APPROVED'),
			('EXTENDED', 'EXTENDED'),
			('COMPLETED', 'COMPLETED'),
		)

	status = models.CharField(max_length=90, choices=STATUS_OPTIONS, default='DRAFT')
	prev_status = models.CharField(max_length=30, default="", blank=True)
	associated_department = models.ForeignKey('Office', on_delete=models.PROTECT, limit_choices_to={'is_department':True}, related_name='+', null=True, blank=True, verbose_name="Department")
	associated_college = models.ForeignKey('Office', on_delete=models.PROTECT, limit_choices_to={'is_department':False}, null=True, blank=True, verbose_name="College")
	remarks = models.TextField(default="", blank=True, verbose_name="Remarks")
	checked_by = models.CharField(max_length=500, blank=True)
	approved_by = models.CharField(max_length=500, blank=True)

	def __str__(self):
		return '{0}, {1} SEMESTER AY {2} - {3}'.format(self.applicant,self.semester_applicable,self.schoolyear,self.schoolyear+1)

	def get_absolute_url(self):
		return reverse('application-detail',args=[str(self.id)])

	def get_current_semester():
		month = datetime.date.today().month
		if(month <= 5):
			return 'SECOND'
		elif(month >= 8):
			return 'FIRST'
		else:
			return 'MIDYEAR'

	def get_current_schoolyear():
		year = get_current_year()
		month = datetime.date.today().month
		if(month < 8):
			year = year - 1
			return str(year)
		elif(month >= 8):
			return str(year)
		


	class Meta:
		verbose_name_plural = "Applications"
		permissions = [('can_approve_reject','Can Approve or Reject RLC')]


#application project class
class Projects(models.Model):
	application = models.ForeignKey('Applications', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Associated Application")
	title = models.CharField(max_length=500, verbose_name="Project Name", blank=True)
	original_name = models.CharField(max_length=500, verbose_name="Original Name", blank=True)
	date_started = models.DateField(default=now(), verbose_name="Date Started")
	date_completed = models.DateField(verbose_name = "Date Completed", null=True, blank=True)
	percent_completed = models.DecimalField(max_digits = 5, decimal_places = 2, default=00.00, verbose_name="Percent Completed", validators=[MinValueValidator(0.00),MaxValueValidator(100.00)])
	authors = models.ManyToManyField('Faculty', null=True, blank=True, verbose_name="Faculty Involved")
	project_file = models.FileField(upload_to='RLC Applications', blank=True, verbose_name="Project File")
	remarks = models.TextField(default="", blank=True, verbose_name="Remarks")
	
	def get_absolute_url(self):
		return reverse('project-detail',args=[str(self.id)])

	class Meta:
		verbose_name_plural = "Projects"
		permissions = [('can_check_projects','Can check projects')]

	def __str__(self):
		return self.title

#RLC Progress Report class
class Progress_Reports(models.Model):
	date_submitted = models.DateField(default=now(), verbose_name="Date Submitted")
	associated_project = models.ForeignKey('Projects', on_delete=models.PROTECT, verbose_name="Associated Project", default="", null=True, blank=True)
	progress_report_file = models.FileField(upload_to='RLC Applications/Progress Reports', verbose_name="Progress Report")
	remarks = models.TextField(default="", blank=True, verbose_name="Remarks")

	'''accomplishments_file = models.FileField(upload_to='RLC Applications/Progress Reports/Accomplishments', verbose_name="Accomplishments")
	fund_utilization_file = models.FileField(upload_to='RLC Applications/Progress Reports/Fund Utilization', verbose_name="Fund Utilization")
	problems_and_constraints_file = models.FileField(upload_to='RLC Applications/Progress Reports/Problems and Constraints', verbose_name="Problems and Constraints")
	'''
	
	class Meta:
		verbose_name_plural = "Progress Reports"
		permissions = [('can_check_progress_reports','Can check progress reports')]

	def __str__(self):
		return '{0}, {1}'.format(self.associated_project, self.date_submitted)

	def get_absolute_url(self):
		return reverse('project-detail',kwargs = {'pk' : self.associated_project_id})

#involvement table
class Involvement(models.Model):
	project_id = models.ManyToManyField('Projects', default="", verbose_name="Project ID")
	faculty_id = models.ManyToManyField('Faculty', default="", verbose_name="Faculty ID")
	involvement = models.CharField(max_length=500, default="", verbose_name="Involvement")

	class Meta:
		verbose_name_plural = "Involvement"

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.project_id, self.faculty_id, self.involvement)
			