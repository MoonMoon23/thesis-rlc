from django.urls import path
from . import views

#these are the urls for the project
urlpatterns = [
	path('', views.index, name='index'),
	path('applications/', views.ApplicationsListView, name="applications"),
	path('applications/add', views.ApplicationsCreate.as_view(), name="add-application"),
	path('applications/extend/<int:pk>', views.ApplicationsExtend, name="extend-application"),
	path('applications/edit/<int:pk>', views.ApplicationUpdateView.as_view(), name="edit-application"),
	path('applications/evaluate/<int:pk>', views.Evaluate.as_view(), name="evaluate"),
	path('applications/addproject', views.ProjectCreate.as_view(), name="create-project"),
	path('applications/delete/<int:pk>', views.ApplicationDelete.as_view(), name="delete-application"),
	path('applications/<int:pk>', views.ApplicationsDetailView, name="application-detail"),
	path('applications/projects/<int:pk>', views.ProjectDetailView, name="project-detail"),
	path('applications/projects/progress-report/add', views.ProgressCreate.as_view(), name="add-progress-report"),
	path('applications/projects/progress-report/addremarks/<int:pk>', views.ProgressReportAddRemarks.as_view(), name="add-remarks-progress-report"),
	path('applications/projects/update/<int:pk>', views.ProjectUpdateView.as_view(), name="edit-project"),
	path('faculty/', views.FacultyDetailView, name="faculty-detail"),
	path('faculty/update-faculty/<int:pk>', views.FacultyUpdateSelf.as_view(), name="update-faculty"),
	path('adminfaculty/', views.AdminFacultyView, name="admin-faculty"),
	path('adminfaculty/<int:pk>', views.AdminFacultyDetailView, name="admin-faculty-detail"),
	path('adminfaculty/add-faculty', views.FacultyCreate.as_view(), name="add-faculty"),
	path('adminfaculty/admin-update-faculty/<int:pk>', views.FacultyUpdate.as_view(), name="admin-update-faculty"),
	path('adminfaculty/delete-faculty/<int:pk>', views.FacultyDelete.as_view(), name="delete-faculty"),
	path('adminapplications/', views.AdminApplicationsListView, name="admin-applications"),
	path('check/pending', views.PendingListView, name="check-pending-rlc"),
	path('check/approved', views.ApprovedListView, name="check-approved-rlc"),
]
