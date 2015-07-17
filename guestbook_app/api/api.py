# -*- coding: utf-8 -*-
import restful as generic


class CollectionResourceView(generic.CollectionResourceView):

	def get(self, request, *args, **kwargs):
		return super(CollectionResourceView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return super(CollectionResourceView, self).post(request, *args, **kwargs)


class SingleResourceView(generic.SingleResourceView):

	def get(self, request, *args, **kwargs):
		return super(SingleResourceView, self).get(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return super(SingleResourceView, self).put(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return super(SingleResourceView, self).delete(request, *args, **kwargs)