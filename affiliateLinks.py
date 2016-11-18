import json

from boto.s3.connection import S3Connection
from boto.s3.key import Key



# create connection to bucket 
c = S3Connection('AKIAIQQ36BOSTXH3YEBA','cXNBbLttQnB9NB3wiEzOWLF13Xw8jKujvoFxmv3L')
# create connection to bucket 
b = c.get_bucket('public.tenthtee')



affiliate_links = {}

affiliate_links['Draftkings'] = 'http://partners.draftkings.com/aff_c?offer_id=124&aff_id=316114'
affiliate_links['Draftday'] = 'https://www.draftday.com/?affiliateRefCode=homefieldlabs'
affiliate_links['Victiv'] = 'https://www.victiv.com/r/etnq5voo4r'
affiliate_links['Fantasyfeud'] = 'https://www.fantasyfeud.com'


affiliate_links = json.dumps(affiliate_links)


k = Key(b)
k.key = 'affiliateLinks'
k.set_contents_from_string(affiliate_links)
k.make_public()