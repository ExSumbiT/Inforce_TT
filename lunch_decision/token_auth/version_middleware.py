class VersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the build version from the request headers, or use a default value
        build_version = request.META.get("HTTP_BUILD_VERSION", "1.0")

        # Set the build version as an attribute in the request object
        request.build_version = build_version

        response = self.get_response(request)
        return response
