import json
from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Entry


class BaseLeaderboardView(LoginRequiredMixin):
	model = Entry
	navigation = 'leaderboard'

class LeaderboardListView(BaseLeaderboardView, ListView):
	pass

class LeaderboardDetailView(BaseLeaderboardView, DetailView):

	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		with open(self.get_object().file.path, 'r', encoding='utf-8') as f:
			a = json.loads(f.read())
		kwargs.update({
			'data_list': a
		})
		return super().get_context_data(**kwargs)