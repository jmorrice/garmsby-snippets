from django.core.management.base import NoArgsCommand, CommandError
from designs.models import Design
from mailsnake import MailSnake
from datetime import datetime, timedelta
from pytz import timezone
from django_comments.models import Comment

class Command(NoArgsCommand):
	help = 'Exports current designs in voting to MailChimp segment'

	def handle_noargs(self, **options):
		try:
			ms = MailSnake('f92abfa01e0a9cecc885186de4e37106-us7')
			self.stdout.write('connected to mailchimp')
		except:
			raise CommandError("Can't connect to MailChimp")

		designs = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14))
		designers = []
		for design in designs:
			designers.append(design.designer)
		for designer in set(designers):
			user_designs = designs.filter(designer=designer)[:3]
			self.stdout.write('updating ' + user_designs[0].name + ' by ' + designer.first_name + ' ' + designer.last_name)
			ms.listUpdateMember(id='ed61191f4e', email_address=designer.email, merge_vars = { 
				'TITLE1':user_designs[0].name,
				'URL1':user_designs[0].tee_pic,
				'LIKES1':user_designs[0].likes,
				'COMMENTS1':Comment.objects.filter(object_pk=user_designs[0].id).count()
				})
			if len(user_designs) > 1:
				self.stdout.write('updating ' + user_designs[1].name + ' by ' + designer.first_name + ' ' + designer.last_name)
				ms.listUpdateMember(id='ed61191f4e', email_address=designer.email, merge_vars = { 
					'TITLE2':user_designs[1].name,
					'URL2':user_designs[1].tee_pic,
					'LIKES2':user_designs[1].likes,
					'COMMENTS2':Comment.objects.filter(object_pk=user_designs[1].id).count()
					})
			else:
				ms.listUpdateMember(id='ed61191f4e', email_address=designer.email, merge_vars = { 
					'TITLE2':'',
					'URL2':'',
					'LIKES2':'',
					'COMMENTS2':'',
					})

			if len(user_designs) > 2:
				self.stdout.write('updating ' + user_designs[2].name + ' by ' + designer.first_name + ' ' + designer.last_name)
				ms.listUpdateMember(id='ed61191f4e', email_address=designer.email, merge_vars = { 
					'TITLE3':user_designs[2].name,
					'URL3':user_designs[2].tee_pic,
					'LIKES3':user_designs[2].likes,
					'COMMENTS3':Comment.objects.filter(object_pk=user_designs[2].id).count()
					})
			else:
				ms.listUpdateMember(id='ed61191f4e', email_address=designer.email, merge_vars = { 
					'TITLE3':'',
					'URL3':'',
					'LIKES3':'',
					'COMMENTS3':'',
					})

		self.stdout.write('done.')