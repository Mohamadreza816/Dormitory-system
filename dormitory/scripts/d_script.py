from dormitory.models import dormitory
from room.signals import *
def run():
    d_name_gender = [('Ghadir',"M"),('Dabagh',"F")]
    for d in d_name_gender:
        if d[1] == 'M':
            obj = dormitory.objects.create(name=d[0], Gender=d[1],rooms=100)

        elif d[1] == 'F':
            obj = dormitory.objects.create(name=d[0], Gender=d[1],rooms=100)


