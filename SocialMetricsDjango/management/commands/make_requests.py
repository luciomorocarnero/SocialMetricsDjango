from django.core.management.base import BaseCommand, CommandError
from SocialMetricsDjango.API import *
from SocialMetricsDjango.settings import *
class Command(BaseCommand):
    help =  """
    Make request for all APIs like
    --instagram str
    --tiktok str
    --youtube_id str
    --youtube_username str 
    --twitter str 
    """

    def add_arguments(self, parser):
        parser.add_argument("--instagram", type=str)
        parser.add_argument("--tiktok", type=str)
        parser.add_argument("--youtube_id", type=str)
        parser.add_argument("--youtube_username", type=str)
        parser.add_argument("--twitter", type=str)

    def handle(self, *args, **options):
        if options['instagram']:
            self.stdout.write(f"making instagram requests for {options['instagram']}")
            try:
                APIIntagram(options['instagram']).get(cache=False)
            except Exception as e:
                raise CommandError(e)
        
        if options['tiktok']:
            self.stdout.write(f"making tiktok requests for {options['tiktok']}")
            try:
                APITiktok(options['tiktok']).get(cache=False)
            except Exception as e:
                raise CommandError(e)
        
        if options['youtube_id']:
            if options['youtube_username']:
                raise CommandError("Must be youtube_id or youtube_username not both")
            
            self.stdout.write(f"making youtube requests for {options['youtube_id']}")
            try:
                APIYoutube(options['youtube_id'],api_key=YoutubeConfig.KEY).get(cache=False)
            except Exception as e:
                raise CommandError(e)
        
        if options['youtube_username']:
            if options['youtube_id']:
                raise CommandError("Must be youtube_username or youtube_id not both")
            
            self.stdout.write(f"making youtube requests for {options['youtube_username']}")
            try:
                APIYoutube.by_userName(options['youtube_username'], api_key=YoutubeConfig.KEY).get(cache=False)
            except Exception as e:
                raise CommandError(e)
        
        if options['twitter']:
            self.stdout.write(f"making twitter requests for {options['twitter']}")
            try:
                APITwitter(options['twitter']).get(cache=False)
            except Exception as e:
                raise CommandError(e)
        
