from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.translation import ugettext as _

from chunked_upload.settings import EXPIRATION_DELTA
from chunked_upload.constants import UPLOADING, COMPLETE
from datastore.models import MyChunkedUpload
from datastore.models import VNF

prompt_msg = _(u'Do you want to delete {obj}?')


class Command(BaseCommand):

    model = MyChunkedUpload
    vnf = VNF

    help = 'Deletes chunked uploads that have already expired.'

    option_list = BaseCommand.option_list + (
        make_option('--interactive',
                    action='store_true',
                    dest='interactive',
                    default=False,
                    help='Prompt confirmation before each deletion.'),
    )

    def handle(self, *args, **options):
        interactive = options.get('interactive')

        count = {UPLOADING: 0, COMPLETE: 0}
        qs = self.model.objects.all()
        qs = qs.filter(created_on__lt=(timezone.now() - EXPIRATION_DELTA))

        for chunked_upload in qs:
            if interactive:
                prompt = prompt_msg.format(obj=chunked_upload) + u' (y/n): '
                answer = raw_input(prompt).lower()
                while answer not in ('y', 'n'):
                    answer = raw_input(prompt).lower()
                if answer == 'n':
                    continue

            # Deleting NF Template associated to uncompleted NF Image upload
            uncomplete_vnf = self.vnf.objects.filter(vnf_id=chunked_upload.vnf_id)
            if len(uncomplete_vnf) != 0:
                if uncomplete_vnf[0].image_upload_status == VNF.IN_PROGRESS:
                    uncomplete_vnf[0].delete()

            count[chunked_upload.status] += 1
            # Deleting uncompleted NF Image upload both from DB and from disk
            chunked_upload.delete()

        print('%i complete uploads were deleted.' % count[COMPLETE])
        print('%i incomplete uploads were deleted.' % count[UPLOADING])
