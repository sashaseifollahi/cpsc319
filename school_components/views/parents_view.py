from django.views import generic
from school_components.models import Parent, Payment, Student, School, Period
from school_components.forms.parents_form import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db.models import Q
import json


def parent_list(request, parent_id=None):
	parent_list = Parent.objects.filter(
		school = request.user.userprofile.school,
		student__enrolled_student__period = request.user.userprofile.period
	).annotate().order_by('last_name')

	search_name = request.GET.get('name', None)
	search_receipt = request.GET.get('receipt_no', None)    

	if search_name:
			parent_list = parent_list.filter(
        		Q(first_name__icontains=search_name) | 
        		Q(last_name__icontains=search_name))

	if search_receipt:
		parent_list = parent_list.filter(
		payment__receipt_no__icontains=search_receipt)

	context_dictionary = {
		'parent_list': parent_list,
		'parent_filter': ParentFilter()
	}

	if parent_id:
		context_dictionary['parent'] = Parent.objects.get(pk=parent_id)
		context_dictionary['payment_form'] = PaymentForm()

	return render_to_response("parents/parent_list.html",
		context_dictionary,
		RequestContext(request))


def parent_get(request):
	if request.method == 'GET':
		parent_id = request.GET['parent_id']
		parent = Parent.objects.get(pk=parent_id)
		parent_json = serializers.serialize("json", [parent])
		# extract the fields we want
		parent_json = json.dumps(json.loads(parent_json)[0]['fields'])
		return HttpResponse(parent_json, content_type="application/json")


def parent_create(request):
	p = ParentForm(request.POST)
	context_dictionary = { 'parent_form': ParentForm() }
	if request.method == 'POST':

		if p.is_valid():
			new = p.save(commit=False)
			new.school = request.user.userprofile.school
			new.period = request.user.userprofile.period
			new.save()

			return HttpResponseRedirect(
				reverse('school:parentlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = p.errors 

	return render_to_response('parents/parent_form.html',
		context_dictionary,
		RequestContext(request))


def parent_form(request):
	parent_list = Parent.objects.all()
	context_dictionary = {'parent_list': parent_list,
						'parent_form': ParentForm() }

	return render_to_response('parents/parent_form.html',
		context_dictionary,
		RequestContext(request))

def payment_create(request, parent_id):
	if request.method == 'POST':
		pay = Payment(parent=Parent.objects.get(pk=parent_id))
		pf = PaymentForm(request.POST, instance=pay)
		
		if pf.is_valid():
			pf.save()
			
			if request.is_ajax():
				return HttpResponse("Payment added successfully.")
			else:
				return HttpResponseRedirect(
					reverse('school:parentlist', args=(parent_id,)))
		else:
			if request.is_ajax():
				return HttpResponse("An error occurred. Payment was not made.")
			return render_to_response('parents/parent_form.html',
				{'errors': pf.errors },
				RequestContext(request))
