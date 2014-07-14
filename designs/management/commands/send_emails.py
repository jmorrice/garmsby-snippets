from django.core.management.base import NoArgsCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from designs.models import Design, Like
from datetime import timedelta
from datetime import datetime
from pytz import timezone

class Command(NoArgsCommand):
	help = 'Send out updates to designers currently in voting.'

	def handle_noargs(self, **options):
		#	-this task runs twice a day through heroku scheduler at 1pm and 6am.
		#	-the only emails sent at 6am are regarding designs that finish voting on the same day before 3pm.
		#	-all other emails are sent through the 1pm task

		#determine time of task
		timezone_gb = timezone('Europe/London')
		am_update, pm_update = False, False

		if datetime.now(timezone_gb).hour > 10:
			pm_update = True
			print 'performing PM update...'
		else:
			am_update = True
			print 'performing AM update...'

		#loop through all designs in voting
		all_list = Design.objects.filter(created__gt=datetime.now(timezone_gb) - timedelta(days=14)) #db query

		for design in all_list:
			#determine time left between now and 2 weeks after submission date
			remaining = design.created.astimezone(timezone_gb) + timedelta(weeks=2) - datetime.now(timezone_gb)
			print design.name + ': ' + str(remaining.days) + ' days remaining'

			if am_update and remaining.days < 1 and design.created.hour < 15: #last day + submitted before 3pm - send email at 6am
				self.send_update(design, remaining)
			elif pm_update and remaining.days < 1 and design.created.hour >= 15: #last day + submitted after 3pm - send email at 1pm
				self.send_update(design, remaining)
			elif pm_update and remaining.days > 0: #not last day - send email at 1pm
				self.send_update(design, remaining)

		self.stdout.write('done.')

	def send_update(self, design, remaining):
		#choose subject and template by days remaining
		templates = {
			13 : 'initial_update',
			12 : 'regular_update',
			 9 : 'regular_update',
			 6 : 'regular_update',
			 3 : 'regular_update',
			 1 : 'prefinal_update',
			 0 : 'final_update',
		}

		subjects = {
			13 : "how's your design doing?",
			12 : 'quick note from garmsby',
			 9 : 'quick note from garmsby',
			 6 : 'quick note from garmsby',
			 3 : 'quick note from garmsby',
			 1 : "24 hours to go",
			 0 : "it's almost over",
		}

		if remaining.days in templates:
			timezone_gb = timezone('Europe/London')

			#determine days/hours/minutes left
			if remaining.days == 0 and remaining.seconds < 3600:
				TIME_LEFT = remaining.seconds / 60
				UNIT_LEFT = 'minutes'
			elif remaining.days == 0:
				TIME_LEFT = remaining.seconds / 3600
				UNIT_LEFT = 'hours'
			else:
				TIME_LEFT = remaining.days
				UNIT_LEFT = 'days'

			#determine recent likes
			RECENT_LIKES = Like.objects.filter(design__exact=design).filter(created__gte=datetime.now(timezone_gb) - timedelta(days=3)).count()

			d = Context({
				'SUBJECT' : subjects[remaining.days],
				'FNAME' : design.designer.first_name,
				'design_list' : [design],
				'TIME_LEFT' : TIME_LEFT,
				'UNIT_LEFT' : UNIT_LEFT,
				'LIKES_LEFT' : 110 - design.likes,
				'RECENT_LIKES' : RECENT_LIKES,
				})

			subject = subjects[remaining.days]
			text_content = get_template('email/' + templates[remaining.days] + '.txt').render(d)
			html_content = get_template('email/' + templates[remaining.days] + '.html').render(d)
			from_email, to = 'garmsby<accounts@garmsby.co.uk>', design.designer.email
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to, 'info@garmsby.co.uk'])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			self.stdout.write('email sent.')

		else:
			self.stdout.write('no update to send.')
