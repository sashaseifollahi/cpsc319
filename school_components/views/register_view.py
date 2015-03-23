from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from school_components.forms.parents_form import PaymentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from school_components.forms.registration_form import *
from school_components.models import *
from django.core.exceptions import ObjectDoesNotExist
import json


FORMS = [	
	('parent_form', ParentContactRegistrationForm),
	('student_form', StudentRegistrationForm),
	('summary_form', SummaryRegistrationForm),
	('payment_form', PaymentRegistrationForm)
]

TEMPLATES = {
	'parent_form': "registration/course_registration_parent.html",
	'student_form': "registration/course_registration_student.html",
	'summary_form': "registration/course_registration_summary.html",
	'payment_form': "registration/course_registration_payment.html",
}

class CourseRegisterWizard(SessionWizardView):

	#  TODO: school/period
	# put current school/period in kwargs to render courses dropdown
	def get_form_kwargs(self, step=None):
		kwargs = {}
		if step == 'student_form':
			kwargs = {
				'school_id': self.request.user.userprofile.school,
				'period_id': self.request.user.userprofile.period,
			}
		return kwargs

	def get_template_names(self):
			return [TEMPLATES[self.steps.current]]
 
 	# do fancy stuff in between forms
	def render(self, form=None, **kwargs):
		context_dictionary = self.get_context_data(form=form, **kwargs)
		#  get parent/students for autocomplete
		if self.steps.current == 'parent_form':
			context_dictionary['parent_list'] = Parent.objects.all().values('id', 'first_name', 'last_name')
		
		elif self.steps.current == 'student_form':
			context_dictionary['student_list'] = Student.objects.all().values('id', 'first_name', 'last_name')
		
		elif self.steps.current == 'summary_form':
			#  save parent/student before rendering summary form
			form_keys = ['parent_form', 'student_form']
			forms = {}
			for key in form_keys:
				forms[key] = self.get_form(
					step=key, 
					data=self.storage.get_step_data(key),
					files=self.storage.get_step_files(key)
				)

			parent, context_dictionary['parent_message'] = self.create_parent(forms['parent_form'])
			student, context_dictionary['student_message'] = self.create_student(parent, forms)

			# save parent to session for payment form
			self.request.session['parent_id'] = parent.id

		elif self.steps.current == 'payment_form':
			parent_id = self.request.session['parent_id']
			context_dictionary['payment_parent'] = Parent.objects.get(pk=parent_id)

	 	return self.render_to_response(context_dictionary)

	# based on parent first and last names
	def create_parent(self, form):
		#  TODO: school/period
		school_id = self.request.session['school_id']
		period_id = self.request.session['period_id']

		school = School.objects.get(pk=school_id)
		period = Period.objects.get(pk=period_id)

		if form.is_valid():
			form_data = form.cleaned_data
			defaults = {
				'cell_phone': form_data['cell_phone'],
				'email' : form_data['email'],
				'school' : school,
				'period': period, 
				'comments': form_data['parent_comments']
			}

			parent, created = Parent.objects.get_or_create(
				first_name=form_data['first_name'], 
				last_name=form_data['last_name'],
				defaults=defaults)

			if not created:
				# update existing parent with new values
				for attr, value in defaults.iteritems():
					setattr(parent, attr, value)
				parent.save()

			return parent, "%s %s was saved successfully. " % (parent.first_name, parent.last_name)
		else:
			return None, "%s %s could not be updated. " % (parent.first_name, parent.last_name)

	def create_student(self, parent, forms):
		# TODO: school/period		
		school_id = self.request.session['school_id']
		period_id = self.request.session['period_id']

		school = School.objects.get(pk=school_id)
		period = Period.objects.get(pk=period_id)

		parent_form = forms['parent_form']
		student_form = forms['student_form']

		#  TODO: emergency cell/home phone, emergency comments
		if student_form.is_valid():
			form_data = student_form.cleaned_data
			parent_data = parent_form.cleaned_data

			emergency_name = "{0} {1}".format(
				parent_data['emergency_first_name'],
			 	parent_data['emergency_last_name'])

			defaults = {
				'home_phone': form_data['home_phone'],
				'birthdate': form_data['birthdate'],
				'address': form_data['address'],
				'email': form_data['email'],
				'allergies': form_data['allergies'],
				'comments': form_data['comments'],
				'emergency_contact_name' : emergency_name,
				'emergency_contact_phone' : parent_data['emergency_cell_phone'],
				'relation' : parent_data['emergency_relation'],
				'parent': parent,
				'school': school,
				'period': period
			}

			student, created = Student.objects.get_or_create(
				first_name=form_data['first_name'], 
				last_name=form_data['last_name'],
				defaults=defaults)

			if not created:
				# update existing student with new values
				for attr, value in defaults.iteritems():
					setattr(student, attr, value)
				student.save()

			return student, "%s %s was saved successfully." % (student.first_name, student.last_name)
		else:
			return None, "Student could not be updated."

	# THINK OF SOMETHING BETTER 
	def register_classes(self, student, form):
		course_status = {}

		form_data = form.cleaned_data
		for field, value in form_data.iteritems():
			if type(value) is str and "id_" in value:
				class_id = int(value.split('id_')[-1])
				classs = Class.objects.get(pk=class_id)

				current_size = ClassRegistration.objects.filter(reg_class=classs).count()
				registered = current_size + 1 <= classs.class_size

				course_status['%s %s' % (classs.course.name, classs.section)] = registered

				reg = ClassRegistration(reg_class=classs, student=student, 
					registration_status=registered)
				reg.save()


	# process the data from the parent and student forms
	def done(self, form_list, **kwargs):
		del self.request.session['parent_id']
		return render_to_response(
			"registration/course_registration_parent.html", 
			context_dictionary)


# TODO: School/Period
#  should have some way to use the model form...
def payment_create(request, parent_id):
	message = {}
	if request.method == 'POST':
		pay = Payment(parent=Parent.objects.get(pk=parent_id))
		pf = PaymentRegistrationForm(request.POST, instance=pay, prefix='payment_form')
		
		if pf.is_valid():
			payment = pf.save()
			message['success'] = "Receipt %s was saved successfully." % payment.receipt_no
			del request.session['parent_id']
			return HttpResponse(json.dumps(message), content_type="application/json")
		else:
			message['errors'] =  pf.errors 
			return HttpResponseBadRequest(json.dumps(message), content_type="application/json")

def lkccourse_register(request, page_no=None):
	if page_no is None or page_no == "1" :
		html = "registration/lkc_course_registration_parent.html"
	elif page_no == "2":
		html = "registration/lkc_course_registration_student.html"
	elif page_no == "3":
		html = "registration/lkc_course_registration_summary.html"
	elif page_no == "4":
		html = "registration/lkc_course_registration_payment.html"

	return render_to_response(html, {}, RequestContext(request))