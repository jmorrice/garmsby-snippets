from django.core.management.base import BaseCommand, CommandError
from designs.models import Design, Like, ReadyNotification
from mailsnake import MailSnake
from datetime import datetime

class Command(BaseCommand):
	help = 'Exports current designs in voting to MailChimp segment'

	def handle(self, *args, **options):
		for design_name in args:
			#check if design with that name exists
			try:
				design_name = design_name.replace('_',' ')
				design = Design.objects.get(name=design_name)
			except:
				raise CommandError("Design with that name doesn't exist.")

			#connect to mailchimp	
			try:
				ms = MailSnake('f92abfa01e0a9cecc885186de4e37106-us7')
				self.stdout.write('connected to mailchimp')
			except:
				raise CommandError("Can't connect to MailChimp")

			#check if segment already exists
			seg_id = None
			seg_name = 'Design Followers: ' + design.name
			for segment in ms.listStaticSegments(id='ed61191f4e'):
				if segment['name'] == seg_name:
					seg_id = segment['id']
					self.stdout.write('Segment already exists with id ' + str(seg_id))

			#otherwise create segment	
			try:
				if seg_id == None:
					seg_id = ms.listStaticSegmentAdd(id='ed61191f4e', name=seg_name)
					self.stdout.write('created segment with id: ' + str(seg_id))
			except:
				raise CommandError("Error creating segment")

			#add users who liked the design to mailchimp segment
			likes = Like.objects.filter(design=design.id)
			self.stdout.write(design.name + ' has ' + str(likes.count()) + ' likes in total. Adding users to mailchimp segment...')

			try:
				for like in likes:
					if like.user.email:
						ms.listStaticSegmentMembersAdd(id='ed61191f4e', seg_id=seg_id,batch=[like.user.email])
						self.stdout.write('added: ' + like.user.email)
					else:
						self.stdout.write('no email for: ' + like.user.first_name + ' ' + like.user.last_name)
			except:
				raise CommandError("Error adding users")

			#add users who requested a shop notification to mailchimp segment
			alerts = ReadyNotification.objects.filter(design=design.id)
			self.stdout.write(str(alerts.count()) + ' notifications were requested for ' + design.name + ' in total. Adding users to mailchimp segment...')

			try:
				for alert in alerts:
					if alert.user.email:
						ms.listStaticSegmentMembersAdd(id='ed61191f4e', seg_id=seg_id,batch=[alert.user.email])
						self.stdout.write('added: ' + alert.user.email)
					else:
						self.stdout.write('no email for: ' + alert.user.first_name + ' ' + alert.user.last_name)
			except:
				raise CommandError("Error adding users")

			self.stdout.write('done.')