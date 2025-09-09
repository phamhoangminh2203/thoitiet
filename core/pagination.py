from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class OptionalLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            "data": data,
            "offset": self.offset + 1,
            "total": len(data)
        })
