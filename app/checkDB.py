from models import *
from debug import *

for c in Channel.objects():
    print(c.comments)