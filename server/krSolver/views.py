from django.shortcuts import render
from django.http import HttpResponse
from lib import krSolver

# Create your views here.

def solve(request, cookie, captchaUrl):
	#captchaUrl = request.GET.get('url', '')
	return HttpResponse(str(krSolver.solve(cookie, captchaUrl)))