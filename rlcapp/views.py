from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Faculty, Office, Applications, Projects, Progress_Reports
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from .forms import ExtendApplication, CreateApplicationForm
from .filters import FacultyFilter, ApplicationsFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from datetime import datetime
import io
# Create your views here.

@login_required
def index(request):
	"""view function for the homepage"""

	#filters applications based on user
	rlc_applications = Applications.objects.filter(applicant=request.user).order_by('-id')

	context = {
		'rlc_applications' : rlc_applications,
	}

	return render(request, 'index.html', context=context)

#list view for applications for regular users
@login_required
def ApplicationsListView(request):
	
	rlc_applications = Applications.objects.filter(applicant=request.user).order_by('-id')
	app_filter = ApplicationsFilter(request.GET, queryset=rlc_applications)

	#this it to check if user has unfinished rlc projects
	excludes = ['EXTENDED', 'COMPLETED']
	counter = rlc_applications.exclude(status__in=excludes).count()
	
	paginator = Paginator(app_filter.qs, 5) #Show 5 applications per page.
	page = request.GET.get('page')
	
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	context = {
		'filter' : app_filter,
		'page' : response,
		'count' : counter
	}

	return render(request, 'rlcapp/rlc_list.html', context=context)

#detail view for applications for regular users
@login_required
def ApplicationsDetailView(request, pk):
	
	rlc_application = Applications.objects.get(id=pk)
	semester = Applications.get_current_semester()
	schoolyear = Applications.get_current_schoolyear()
	projects = Projects.objects.filter(application=rlc_application)
	
	if semester != rlc_application.semester_applicable:
		semester_different = True
	else:
		semester_different = False

	if schoolyear != rlc_application.schoolyear:
		schoolyear_different = True
	else:
		schoolyear_different = False

	can_extend = semester_different or schoolyear_different

	context = {
		'application' : rlc_application,
		'projects' : projects,
		'semester'  : semester,
		'schoolyear' : schoolyear,
		'extend'  : can_extend,
	}

	#these methods are for the submission of RLC Applications
	if request.method == "POST":
		if rlc_application.status == 'DRAFT' or rlc_application.status == 'FOR REVISION':
			if rlc_application.prev_status == 'PENDING COLLEGE APPROVAL':
				rlc_application.prev_status = rlc_application.status
				rlc_application.status = 'PENDING COLLEGE APPROVAL'
			else:
				rlc_application.prev_status = rlc_application.status
				rlc_application.status = 'PENDING DEPARTMENT APPROVAL'
		
		elif rlc_application.status =='PENDING DEPARTMENT APPROVAL':
			if rlc_application.prev_status == 'DRAFT':
				rlc_application.prev_status = rlc_application.status
				rlc_application.status = 'DRAFT'
			elif rlc_application.prev_status == 'FOR REVISION':
				rlc_application.prev_status = rlc_application.status
				rlc_application.status = 'FOR REVISION'

		elif rlc_application.status == 'PENDING COLLEGE APPROVAL':
			rlc_application.prev_status = rlc_application.status
			rlc_application.status = 'FOR REVISION'
		rlc_application.save()
		return render(request, 'rlcapp/applications_detail.html', context=context)

	return render(request, 'rlcapp/applications_detail.html', context=context)

#view for updating applications for regular users
@method_decorator(login_required, name='dispatch')
class ApplicationUpdateView(UpdateView):
	model = Applications
	fields = [
		'applicant',
		'units',
		'semester_applicable',
		'schoolyear',
		'status',
	]

#view for deleting applications
@method_decorator(login_required, name='dispatch')
class ApplicationDelete(DeleteView):
	model = Applications
	success_url = reverse_lazy('applications')

#view for Faculty Member page for regular users
@login_required
def FacultyDetailView(request):

	faculty = Faculty.objects.get(faculty_id=request.user.faculty_id)

	context = {
		'faculty' : faculty
	}

	return render(request, 'rlcapp/faculty_detail.html', context=context)

#view for updating faculty profile for regular users
@method_decorator(login_required, name='dispatch')
class FacultyUpdateSelf(UpdateView):
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
		]
	success_url = reverse_lazy('faculty-detail')

#view for Faculty Member List for administrators
@login_required
def AdminFacultyView(request):

	faculty = Faculty.objects.all()
	faculty_filter = FacultyFilter(request.GET, queryset=faculty)
	
	paginator = Paginator(faculty_filter.qs, 5) #Show 5 faculty members per page.
	page = request.GET.get('page')
	
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	context = {
		'filter' : faculty_filter,
		'page' : response
	}

	return render(request, 'rlcapp/admin_faculty.html', context=context)

#view for Faculty Member page for administrators
@login_required
def AdminFacultyDetailView(request, pk):

	faculty = Faculty.objects.get(id=pk)

	context = {
		'faculty' : faculty
	}

	return render(request, 'rlcapp/faculty_detail.html', context=context)

#view for creating faculty members for administrators
@method_decorator(login_required, name='dispatch')
class FacultyCreate(CreateView):
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

#view for updating faculty members for administrators
@method_decorator(login_required, name='dispatch')
class FacultyUpdate(UpdateView):
	template_name = 'rlcapp/admin_update_faculty_form.html'
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

#view for deleting faculty members for administrators
@method_decorator(login_required, name='dispatch')
class FacultyDelete(DeleteView):
	model = Faculty
	success_url = reverse_lazy('admin-faculty')

#view for creating projects
@method_decorator(login_required, name='dispatch')
class ProjectCreate(CreateView):
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

#view for updating projects
@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
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

#view to get a list of applications for administrators
@login_required
def AdminApplicationsListView(request):
	
	rlc_applications = Applications.objects.all().order_by('-id')
	app_filter = ApplicationsFilter(request.GET, queryset=rlc_applications)
	
	paginator = Paginator(app_filter.qs, 5) #Show 5 applications per page.
	page = request.GET.get('page')
	
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	context = {
		'filter' : app_filter,
		'page' : response
	}

	#this block of code is for generating the statistics report
	if request.method == "POST":
		
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=reports.pdf'

		buff = io.BytesIO()
		c = SimpleDocTemplate(buff, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

		elements = []

		data = [["Applicant","Units","Semester","Schoolyear","Status","Department"]]

		for apps in app_filter.qs:
			lines = []
			lines.append(str(apps.applicant))
			lines.append(str(apps.units))
			lines.append(str(apps.semester_applicable))
			lines.append(str(apps.schoolyear))
			lines.append(str(apps.status))
			lines.append(str(apps.associated_department))
			data.append(lines)

		t = Table(data)
		t.setStyle(TableStyle([
			('BACKGROUND',(0,0),(5,0),colors.black),
			('TEXTCOLOR',(0,0),(5,0),colors.white),
			('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black),
		]))

		elements.append(t)
		c.build(elements)
		response.write(buff.getvalue())
		buff.close
		
		return response
	

	return render(request, 'rlcapp/admin_rlc_list.html', context=context)

#view to create initial application
@method_decorator(login_required, name='dispatch')
class ApplicationsCreate(CreateView):

	model = Applications
	fields = [
		'applicant',
		'units',
		'semester_applicable',
		'schoolyear',
		'associated_department',
		'associated_college',
	]

	def get_initial(self):
		return {
			'applicant' : self.request.user,
			'associated_department' : self.request.user.department,
			'associated_college' : self.request.user.college,
		}

	
#view for viewing project details	
@login_required
def ProjectDetailView(request, pk):

	projects = Projects.objects.get(id=pk)
	progress_reports = Progress_Reports.objects.filter(associated_project=pk).order_by('-id')

	context = {
		'projects' : projects,
		'progress_reports' : progress_reports,
	}

	return render(request, 'rlcapp/project_detail.html', context=context)

#view for getting a list of applications that are pending for approving bodies
@login_required
def PendingListView(request):

	if request.user.department == None:
		rlc_applications = Applications.objects.filter(status='PENDING COLLEGE APPROVAL')
	else:
		rlc_applications = Applications.objects.filter(status='PENDING DEPARTMENT APPROVAL').filter(associated_department=request.user.department)

	app_filter = ApplicationsFilter(request.GET, queryset=rlc_applications)
	
	paginator = Paginator(app_filter.qs, 5) #Show 5 applications per page.
	page = request.GET.get('page')
	
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	context = {
		'filter' : app_filter,
		'page' : response
	}

	return render(request, 'rlcapp/pending_rlc_list.html', context=context)

#view for getting a list of approved applications for approving bodies
@login_required
def ApprovedListView(request):

	if request.user.department == None:
		rlc_applications = Applications.objects.filter(status='APPROVED' or 'COMPLETED')
	else:
		rlc_applications = Applications.objects.filter(status='APPROVED' or 'COMPLETED').filter(associated_department=request.user.department)

	app_filter = ApplicationsFilter(request.GET, queryset=rlc_applications)
	paginator = Paginator(app_filter.qs, 5) #Show 5 applications per page.
	page = request.GET.get('page')
	
	try:
		response = paginator.page(page)
	except PageNotAnInteger:
		response = paginator.page(1)
	except EmptyPage:
		response = paginator.page(paginator.num_pages)
	
	context = {
		'filter' : app_filter,
		'page' : response
	}

	return render(request, 'rlcapp/approved_rlc_list.html', context=context)

#view for evalutaing applications for approving bodies
@method_decorator(login_required, name='dispatch')
class Evaluate(UpdateView):
	model = Applications
	fields = ['remarks','status',]

#view for creating progress reports
@method_decorator(login_required, name='dispatch')
class ProgressCreate(CreateView):
	model = Progress_Reports
	fields = [
		'date_submitted',
		'associated_project',
		'progress_report_file',
	]
	success_url = reverse_lazy('project-detail')

#view for extending rlc applications
@login_required
def ApplicationsExtend(request, pk):

	rlc_application = Applications.objects.get(id=pk)
	semester = Applications.get_current_semester()
	schoolyear = Applications.get_current_schoolyear()
	projects = Projects.objects.filter(application=rlc_application)

	if request.method == "POST":
		newappform = ExtendApplication(request.POST)
		app = newappform.save(commit=False)
		app.applicant = rlc_application.applicant
		app.associated_department = rlc_application.applicant.department
		app.associated_college = rlc_application.applicant.college
		app.previous_application = rlc_application


		if rlc_application.semester_applicable == 'FIRST':
			app.semester_applicable = 'SECOND'
			app.schoolyear = schoolyear
		
		elif rlc_application.semester_applicable == 'SECOND':
			app.semester_applicable = "MIDYEAR"
			app.schoolyear = schoolyear

		elif rlc_application.semester_applicable == 'MIDYEAR':
			app.semester_applicable = "FIRST"
			sy = int(schoolyear) + 1
			app.schoolyear = sy
			
		app = newappform.save()

		rlc_application.prev_status = rlc_application.status
		rlc_application.status = 'EXTENDED'
		rlc_application.save()
		
		newapp = Applications.objects.get(id=app.id)
		newprojects = Projects.objects.filter(application=newapp)

		context = {
			'application' : newapp,
			'projects' : newprojects,
			'semester'  : semester,
			'schoolyear' : schoolyear,
		}
		
		return render(request, 'rlcapp/applications_detail.html', context=context)

	else:
		newappform = ExtendApplication()


	return render(request, 'rlcapp/extend_application_form.html', {'form' : newappform})

#view for adding remarks to progress reports for approving bodies
@method_decorator(login_required, name='dispatch')
class ProgressReportAddRemarks(UpdateView):
	model = Progress_Reports
	fields = ['remarks',]
	template_name_suffix = '_add_remarks'