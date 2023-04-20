from rest_framework import status
from rest_framework.response import Response


class ApiBaseView:
    def _create_response_for_invalid_serializers(self, *serializers):
        errors = {field: error for serializer in serializers for field, error in serializer.errors.items()}
        return Response(
            {"errors": errors},
            status=status.HTTP_400_BAD_REQUEST)

    def _create_response_for_exception(self, exception):
        return Response(
            {"error": str(exception.message)},
            status=status.HTTP_400_BAD_REQUEST)

    def _create_response_not_found(self, exception):
        return Response(
            {"error": str(exception.message)},
            status=status.HTTP_404_NOT_FOUND)
