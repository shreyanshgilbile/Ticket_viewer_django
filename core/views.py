import numpy
import requests

from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class tickets(APIView):
	def get(self, request):
		# list_items
		session = requests.Session()
		session.auth = (settings.USERNAME, settings.PASSWORD)
		page_size = settings.PAGE_SIZE
		total_page = 1
		page = int(request.GET.get('page', 1))

		try:

			url = 'https://zccticketviewer98.zendesk.com/api/v2/tickets.json'
			# url + = '?page='+str(page)+'&per_page='+str(page_size)
			response = session.get(url = url, timeout=5)
			if response.status_code != 200:
				raise ValidationError("status_code " + str(response.status_code) + " returned")
			resp = response.json()
			# print(resp)
			resp = resp['tickets']
			data = {}

			total_page = int(len(resp)/page_size) if int(len(resp)/page_size) == len(resp)/page_size else int(len(resp)/page_size) + 1
			page = 1 if page<1 else page
			page = total_page if page>total_page else page
			startt = (page-1) * page_size
			endd = page * page_size if page * page_size < len(resp) + 1 else len(resp) + 1
			
			for item in resp[startt:endd]:
				data[str(item['id']) + ' - ' + item['subject']] = item

		except ValidationError as e:
			data = {"error": str(e)}
		except Exception as e:
			data = {"error": str(e)}
			print("--------------" + str(e))

		return render(request, 'index.html', {'list_items':data, 'page':page, 'total_page':total_page, 'next_page': "http://localhost:8000/?page=" + str(page + 1 if page + 1 <total_page else total_page), 'prev_page': "http://localhost:8000/?page=" + str(page - 1 if page -1 > 0 else 1)})
		# return Response({'Lauda': 'Lasoon'}, status=status.HTTP_200_OK)