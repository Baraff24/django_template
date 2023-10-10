# STATUS_CHOICES VALUES
COMPLETE = 'COMPLETE'
PENDING_COMPLETE_DATA = 'PENDING_EXTRA_DATA'

# GENDER_CHOICES VALUES
MAN = 'MAN'
WOMAN = 'WOMAN'
NONE = 'NONE'

# TYPE_OF_USER_CHOICES VALUES
PATIENT = 'PATIENT'
PROFESSIONAL = 'PROFESSIONAL'


STATUS_CHOICES = (
    (COMPLETE, 'Complete'),
    (PENDING_COMPLETE_DATA, 'Pending Complete Data'),
)


GENDER_CHOICES = (
    (MAN, 'Man'),
    (WOMAN, 'Woman'),
    (NONE, 'None'),
)


TYPE_OF_USER_CHOICES = (
    (PATIENT, 'Patient'),
    (PROFESSIONAL, 'Professional'),
)
