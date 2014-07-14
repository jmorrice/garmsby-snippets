from django.core.management.base import NoArgsCommand, CommandError
from designs.models import Design
from mailsnake import MailSnake
from datetime import datetime, timedelta
from pytz import timezone
from optparse import make_option

class Command(NoArgsCommand):
	help = 'Exports current designs in voting to MailChimp segment'
	option_list = NoArgsCommand.option_list + (
		make_option('--all',
			action='store_true',
			dest='all',
			help='Exports all designers to "Designer" segment'
			),
		)

	def handle_noargs(self, **options):
		try:
			ms = MailSnake('f92abfa01e0a9cecc885186de4e37106-us7')
			self.stdout.write('connected to mailchimp')
		except:
			raise CommandError("Can't connect to MailChimp")

		#check if segment already exists
		seg_id = None
		if options['all']:
			seg_name = 'Designers'
		else:
			seg_name = 'Week ' + datetime.today().strftime('%W-%Y')

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

		#query all or only current designs
		if options['all']:
			designs = Design.objects.all()
		else:
			designs = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14))
		try: 
			for design in designs:
				ms.listStaticSegmentMembersAdd(id='ed61191f4e', seg_id=seg_id,batch=[design.designer.email])
				self.stdout.write('added: ' + design.designer.email)
		except:
			raise CommandError("Error adding users")
		self.stdout.write('done.')