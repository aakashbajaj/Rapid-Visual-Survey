def ms_mbt(p):
	
	nflr = p.no_floor + p.bas_prsnt

	if p.yr_constr is None:
		if nflr == 1:
			return "MC3L1"
		elif nflr == 2:
			return "MC3L2"
		else:
			return "MC3M"

	elif p.yr_constr > 2001 and p.hrz_bnd is 1:
		if nflr == 1:
			return "ME1L1"
		elif nflr == 2:
			return "ME2L2"
		else:
			return "ME1M"

	else:
		if nflr == 1:
			return "MC3L1"
		elif nflr == 2:
			return "MC3L2"
		else:
			return "MC3M"


def rc_mbt(p):

	nflr = p.no_floor + p.bas_prsnt

	if p.yr_constr is None:
		if nflr == 1 or nflr == 2 or nflr == 3:
			return "RC1L"
		else:
			return "RC1M"

	if p.yr_constr < 2001:
		if nflr == 1 or nflr == 2 or nflr == 3:
			return "RC1L"
		else:
			return "RC1M"

	else:
		if nflr == 1 or nflr == 2 or nflr == 3:
			return "RC2L(LC)"
		elif nflr == 4 or nflr == 6 or nflr == 7:
			return "RC2M(LC)"
		else:
			return "RC2H(LC)"