from django.conf.urls import patterns, url
from school_components import views
from school_components.views.register_view import CourseRegisterWizard, FORMS

urlpatterns = patterns('',
	# # registration
	url(r'^register1/$', 
		CourseRegisterWizard.as_view(FORMS),
		name='courseregister'),

	url(r'^register/$', 
		'school_components.views.register_view.course_register', 
		name='courseregister'),
	url(r'^register/(?P<page_no>\d+)/$', 
		'school_components.views.register_view.course_register', 
		name='courseregister'),
	url(r'^registerlkc/$', 
		'school_components.views.register_view.lkccourse_register', 
		name='lkccourseregister'),
	url(r'^registerlkc/(?P<page_no>\d+)/$', 
		'school_components.views.register_view.lkccourse_register', 
		name='lkccourseregister'),


	# students
	url(r'^students/$', 
		'school_components.views.students_view.student_list', 
		name='studentlist'),
	url(r'^students/(?P<student_id>\d+)/$', 
		'school_components.views.students_view.student_list', 
		name='studentlist'),
	url(r'^students/create/$', 
		'school_components.views.students_view.student_create', 
		name='studentcreate'),
	url(r'^students/form/$', 
		'school_components.views.students_view.student_form', 
		name='studentform'),
	url(r'^students/upload/$', 
		'school_components.views.students_view.student_upload', 
		name='studentupload'),
	url(r'^students/export/$', 
		'school_components.views.students_view.student_export', 
		name='studentexport'),
    
	# parents
	url(r'^parents/$', 
		'school_components.views.parents_view.parent_list', 
		name='parentlist'),
	url(r'^parents/(?P<parent_id>\d+)/$', 
		'school_components.views.parents_view.parent_list', 
		name='parentlist'),
	url(r'^parents/create/$', 
		'school_components.views.parents_view.parent_create', 
		name='parentcreate'),
	url(r'^parents/form/$', 
		'school_components.views.parents_view.parent_form', 
		name='parentform'),

	# payment
	url(r'^payment/(?P<parent_id>\d+)/$', 
		'school_components.views.parents_view.payment_create', 
		name='paymentcreate'),

	# courses
	url(r'^courses/$', 
		'school_components.views.courses_view.course_list', 
		name='courselist'),
	url(r'^courses/(?P<course_id>\d+)/$', 
		'school_components.views.courses_view.course_list', 
		name='courselist'),
	url(r'^courses/create/$', 
		'school_components.views.courses_view.course_create', 
		name='coursecreate'),
	url(r'^courses/assignments/$', 
		'school_components.views.courses_view.course_assignment', 
		name='courseassignment'),

	# departments
	url(r'^departments/create/$', 
		'school_components.views.courses_view.dept_create', 
		name='deptcreate'),

	# classes
	url(r'^classes/$', 
		'school_components.views.classes_view.class_list', 
		name='classlist'),
	url(r'^classes/(?P<class_id>\d+)/$', 
		'school_components.views.classes_view.class_list', 
		name='classlist'),
	url(r'^classes/create/$', 
		'school_components.views.classes_view.class_create', 
		name='classcreate'),
	url(r'^classes/register/$', 
		'school_components.views.classes_view.class_registration', 
		name='classregistration'),
    url(r'^classes/attendance/$',
        'school_components.views.classes_view.class_attendance',
        name='classattendance'),
    url(r'^classes/performance/$',
        'school_components.views.classes_view.class_performance',
        name='classperformance'),
    url(r'^classes/assignment/$',
        'school_components.views.classes_view.class_assignment',
        name='classassignment'),
    url(r'^classes/reportcard/$',
        'school_components.views.classes_view.class_reportcard',
        name='classreportcard'),
                       
    # schools
    url(r'^schools/$',
        'school_components.views.schools_view.school_list',
        name='schoollist'),
    url(r'^schools/(?P<school_id>\d+)/$',
        'school_components.views.schools_view.school_list',
        name='schoollist'),
    url(r'^schools/create/$',
        'school_components.views.schools_view.school_create',
        name='schoolcreate'),

    # periods
    url(r'^periods/$',
        'school_components.views.periods_view.period_list',
        name='periodlist'),
    url(r'^periods/(?P<period_id>\d+)/$',
        'school_components.views.periods_view.period_list',
        name='periodlist'),
    url(r'^periods/create/$',
        'school_components.views.periods_view.period_create',
        name='periodcreate'),
                       
)