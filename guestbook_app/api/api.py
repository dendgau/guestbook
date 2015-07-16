# -*- coding: utf-8 -*-
import restful as generic


class GreetingView(generic.GreetingView):

	def get(self, request, *args, **kwargs):
		return super(GreetingView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return super(GreetingView, self).post(request, *args, **kwargs)


class GreetingDetailView(generic.GreetingDetailView):

	def get(self, request, *args, **kwargs):
		return super(GreetingDetailView, self).get(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return super(GreetingDetailView, self).put(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return super(GreetingDetailView, self).delete(request, *args, **kwargs)