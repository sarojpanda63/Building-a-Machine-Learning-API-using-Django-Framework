from django.shortcuts import HttpResponse, render
import json
from .models import approval
import joblib
import pandas as pd

def mySite(request):
	return render(request, 'MyAPI/mySite.html')
def status(request):
	status='YOu entered wrong entry'
	if request.method=="POST":
		firstname=request.POST.get('firstname')
		lastname=request.POST.get('lastname')
		dependants=int(request.POST.get('dependants'))
		applicantincome=int(request.POST.get('applicantincome'))
		coapplicantincome=int(request.POST.get('coapplicantincome'))
		loanamount=int(request.POST.get('loanamount'))
		loanterm=int(request.POST.get('loanterm'))
		credithistory=int(request.POST.get('credithistory'))
		gender=request.POST.get('gender')
		married=request.POST.get('married')
		graduatededucation=request.POST.get('graduatededucation')
		selfemployed=request.POST.get('selfemployed')
		area=request.POST.get('area')
		data=pd.DataFrame({
			'dependants':[dependants],
			'applicantincome':[applicantincome],
			'coapplicantincome':[coapplicantincome],
			'loanamt':[loanamount],
			'loanterm':[loanterm],
			'credithistory':[credithistory], 
			'gender_female':[0],
			'gender_male':[0],
			'married_no':[0],
			'married_yes':[0],
			'education_graduate':[0],
			'education_not_graduate':[0],
			'selfemployed_no':[0],
			'selfemployed_yes':[0],
			'area_rural':[0],
			'area_semiurban':[0],
			'area_urban':[0]})
		if gender=='Female':
			data['gender_female']=1
		if gender=='Male':
			data['gender_male']=1
		if married=='No':
			data['married_no']=1
		if married=='Yes':
			data['married_yes']=1
		if graduatededucation=='Graduate':
			data['education_graduate']=1
		if graduatededucation=='Not_Graduate':
			data['education_not_graduate']=1
		if selfemployed=='No':
			data['selfemployed_no']=1
		if selfemployed=='Yes':
			data['selfemployed_yes']=1
		if area=='Rural':
			data['area_rural']=1
		if area=='Semiurban':
			data['area_semiurban']=1
		if area=='Urban':
			data['area_urban']=1
		X_min=pd.DataFrame({
			'dependants':[0],
			'applicantincome':[150],
			'coapplicantincome':[0],
			'loanamt':[9000],
			'loanterm':[36],
			'credithistory':[0], 
			'gender_female':[0],
			'gender_male':[0],
			'married_no':[0],
			'married_yes':[0],
			'education_graduate':[0],
			'education_not_graduate':[0],
			'selfemployed_no':[0],
			'selfemployed_yes':[0],
			'area_rural':[0],
			'area_semiurban':[0],
			'area_urban':[0]})
		X_max=pd.DataFrame({
			'dependants':[3],
			'applicantincome':[81000],
			'coapplicantincome':[33837],
			'loanamt':[600000],
			'loanterm':[480],
			'credithistory':[1], 
			'gender_female':[1],
			'gender_male':[1],
			'married_no':[1],
			'married_yes':[1],
			'education_graduate':[1],
			'education_not_graduate':[1],
			'selfemployed_no':[1],
			'selfemployed_yes':[1],
			'area_rural':[1],
			'area_semiurban':[1],
			'area_urban':[1]})
		X_std = (data - X_min) / (X_max - X_min)
		data = X_std * (1 - 0) + 0
		mdl=joblib.load('loan_model.pkl')
		ypred=mdl.predict(data)
		ypred=(ypred>0.58)
		if ypred==True:
			status="Loan Approved"
		if ypred==False:
			status="Loan Rejected"
		approve=approval(
			firstname=firstname, lastname=lastname,
			dependants=dependants, applicantincome=applicantincome,
			coapplicantincome=coapplicantincome, loanamt=loanamount,
			loanterm=loanterm, credithistory=credithistory,
			gender=gender, married=married, graduatededucation=graduatededucation,
			selfemployed=selfemployed,area=area)
		approve.save()
		return render(request, 'MyAPI/status.html', {'dict_1':status})
def myForm(request):
	return render(request, 'MyAPI/myForm.html')
