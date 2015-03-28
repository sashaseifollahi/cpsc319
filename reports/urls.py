from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
   
    #reports
    url(r'^view_reports/','reports.views.view_reports',name='view_reports'),

    url(r'^create_new_report_page/','reports.views.create_new_report_page',name='create_new_report_page'),

    url(r'^reportcard_teacher_page/$','reports.views.reportcard_teacher',name='reportcardteacher'),
    url(r'^reportcard_teacher_page/(?P<class_id>\d+)/$', 
		'reports.views.reportcard_teacher', 
		name='reportcardteacher'),
    url(r'^reportcard_teacher_page/(?P<class_id>\d+)/(?P<student_id>\d+)/$', 
		'reports.views.reportcard_teacher', 
		name='reportcardteacher'),
 
    url(r'^reportcard_adm_page/$','reports.views.reportcard_adm',name='reportcardadm'),
    url(r'^reportcard_adm_page/(?P<student_id>\d+)/$', 
		'reports.views.reportcard_adm', 
		name='reportcardadm'),

    url(r'^student_phone_page/$','reports.views.studentphone',name='studentphone'),
    url(r'^student_phone_page/(?P<class_id>\d+)/$', 
		'reports.views.studentphone', 
		name='studentphone'),

    url(r'^export/','reports.views.export_data',name='export'),

)
