# Choices for all fields
ACCESS_CHOICES = (
	('FULL', 'FULL'),
	('PARTIAL', 'PARTIAL'),
	('NO', 'NO')
)

SEISMIC_ZONE = (
	( 1, 'II and III'),
	( 2, 'IV'),
	( 3, 'V')
)

BLD_USE = (
	('Residential','Residential'),
	('Commercial','Commercial'),
	('Mixed','Mixed'),
	('Others','Others')
)

FEAT_CHOICE = (
	(0, "Absent"),
	(1, "Present")
)

QUAL_CHOICE = (
	(0,"Good"),
	(1,"Moderate"),
	(2,"Poor")
)

SOIL_CHOICE = (
	(0, "Medium"),
	(1, "Hard"),
	(-1, "Soft")
)

FRM_CHOICE = (
	(-1, "Absent"),
	(1, "Present"),
	(0, "Not Sure")
)

IRR_CHOICE = (
	(0,"None"),
	(1,"Moderate"),
	(2,"Extreme")
)

TYP_CHOICE = (
	("Brick Masonary", "Brick Masonary"),
	("Composite", "Composite")
)

OPENING_CHOICE = (
	(0, "Small (<1/3)"),
	(1, "Moderate (1/3 to 2/3)"),
	(2, "Large (>2/3)")
)

BOOL_CHOICE = (
	(1, "Yes"),
	(0, "No")
)

PND_CHOICE = (
	(0, "Absent"),
	(1, "Normal Apparent Condition of Adjacent Building"),
	(2, "Poor Apparent Condition of Adjacent Building")
)