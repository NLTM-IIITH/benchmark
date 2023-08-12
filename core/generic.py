from django.views import generic


class DeleteView(generic.DeleteView):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)
