from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

'''
class DefaultPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100
'''
class DefaultPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_objects": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # پارامتری که کاربر وارد می‌کند
    max_page_size = 100  # حداکثر تعداد آیتم‌های هر صفحه