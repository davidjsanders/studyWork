# Import base library modules - From Bluetooth symbolic link to /base_lib
from v3_00_Phone_Screen \
    import v3_00_Phone_Screen

#
# SuperClass.
# ----------------------------------------------------------------------------
class Phone_Screen(v3_00_Phone_Screen):
    def __init__(self):
        super(Phone_Screen, self).__init__()


phone_screen = Phone_Screen()
phone_screen.run()
