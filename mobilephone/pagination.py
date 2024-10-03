from rest_framework import pagination



class PhonePagination(pagination.PageNumberPagination):
    page_size = 1  # You can adjust this value
    page_size_query_param = 'page_size'
    max_page_size = 1