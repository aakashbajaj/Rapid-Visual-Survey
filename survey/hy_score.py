def HY_Score(bd):

	# Structural Irregularity
	if bd.lck_wll is 1 or bd.hvy_ovh is 1 or bd.re_crn is 1 or bd.crn_bld is 1:
		bd.str_irr = 1
	else:
		bd.str_irr = 0

	# Apparent Quality
	if bd.ql_mat is 2 and bd.maintc is 2:
		bd.ap_qlt = 2
	elif bd.ql_mat is 0 and bd.maintc is 0:
		bd.ap_qlt = 0
	else:
		bd.ap_qlt = 1

	# Diaphragm Action
	if bd.ab_diap is 1 or bd.lrg_cut is 1:
		bd.diap_ab = 1
	else:
		bd.diap_ab = 0

	# Horizontal Bands
	if bd.plnt_lvl is 1 or bd.lntl_lvl is 1 or bd.sill_lvl is 1 or bd.roof_lvl is 1:
		bd.hrz_bnd = 1
	else:
		bd.hrz_bnd = 0

	# Arches
	if bd.arches is 1 or bd.jck_roof is 1:
		bd.arch = 1
	else:
		bd.arch = 0

	# Pounding
	if bd.cnt_bld is 0:
		bd.pnding = 0
	elif bd.pr_qlt is 1:
		bd.pnding = 2
	else:
		bd.pnding = 1

	# Rubble Wall Masonary
	if bd.thk_wll is 1 or bd.rnd_stn is 1 or bd.hvy_roof is 1:
		bd.rub_wll = 1
	else:
		bd.rub_wll = 0


	buil_flr = int(bd.no_floor)

	if buil_flr is 2:
		flr = 1
	elif buil_flr > 5:
		flr = 5
	else:
		flr = buil_flr

	base_table = {
		 1: {1:150, 2:130, 3:100},
		 3: {1:125, 2:110, 3:85},
		 4: {1:110, 2:90, 3:70},
		 5: {1:70, 2:60, 3:50}
	}

	base_score = base_table[flr][bd.s_zone]

	orn_opn_f = {1:-2, 3:-5, 4:-5, 5:-5}
	pnding_f = {1:0, 3:-3, 4:-5, 5:-5}
	diap_ac_f = {1:-10, 3:-15, 4:-15, 5:-15}
	bas_prsnt_f = {1:0, 3:3, 4:4, 5:5}

	strirr = bd.str_irr * (-10)
	apqlty = bd.ap_qlt * (-10)
	soilcn = bd.soil_cn * (10)
	pound = bd.pnding * pnding_f[flr]
	wlopng = bd.prt_opn * (-5)
	irropn = bd.irr_opn * orn_opn_f[flr]
	diapac = bd.diap_ab * diap_ac_f[flr]
	hrzbnd = bd.hrz_bnd * (20)
	archf = bd.arch * (-10)
	rublwl = bd.rub_wll * (-15)
	bsmnt = bd.bas_prsnt * bas_prsnt_f[flr]

	vs = strirr + apqlty + soilcn + pound + wlopng + irropn + diapac + hrzbnd + archf + rublwl + bsmnt

	perf_sc = base_score + vs

	return perf_sc