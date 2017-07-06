def RC_score(bd):

	# Plan Irregularities	
	if bd.ir_plc is 1 and bd.re_crn is 1:
		bd.pl_irr = 2
	elif (bd.ir_plc is 1 and bd.re_crn is 0) or (bd.ir_plc is 0 and bd.re_crn is 1):
		bd.pl_irr = 1
	else:
		bd.pl_irr = 0

	# Soft Storey
	if bd.op_prk is 1 or bd.ab_prt is 1 or bd.st_shp is 1 or bd.tl_htg is 1:
		bd.soft_st = 1
	else:
		bd.soft_st = 0

	# Vertical Irregularity
	if bd.pr_stb is 1 or bd.bl_slp is 1:
		bd.vrt_irr = 1
	else:
		bd.vrt_irr = 0

	# Heavy Overhangs
	if bd.md_hrp is 1 or bd.sb_hrp is 1:
		bd.hvy_ovh = 1
	else:
		bd.hvy_ovh = 0

	# Apparent Quality
	if bd.ql_mat is 2 and bd.maintc is 2:
		bd.ap_qlt = 2
	elif bd.ql_mat is 0 and bd.maintc is 0:
		bd.ap_qlt = 0
	else:
		bd.ap_qlt = 1

	# Pounding
	if bd.un_flr is 1 or bd.pr_qlt is 1:
		bd.pnding = 1
	else:
		bd.pnding = 0

	buil_flr = int(bd.no_floor)

	if buil_flr is 2:
		flr = 1
	elif buil_flr > 5:
		flr = 6
	else:
		flr = buil_flr

	base_table = {
		 1: {1:150, 2:130, 3:100},
		 3: {1:140, 2:120, 3:90},
		 4: {1:120, 2:100, 3:75},
		 5: {1:100, 2:85, 3:65},
		 6: {1:90, 2:80, 3:60}
	}

	base_score = base_table[flr][bd.s_zone]

	soft_st_f = {1:0, 3:-15, 4:-20, 5:-25, 6:-30}
	hvy_ovh_f = {1:-5, 3:-10, 4:-10, 5:-15, 6:-15}
	ap_qlt_f = {1:-5, 3:-10, 4:-10, 5:-15, 6:-15}
	pnding_f = {1:0, 3:-2, 4:-3, 5:-5, 6:-5}
	bas_prsnt_f = {1:0, 3:3, 4:4, 5:5, 6:5}

	sft = bd.soft_st*soft_st_f[flr]
	vrt = bd.vrt_irr*(-10)
	plir = bd.pl_irr*(-5)
	hvyov = bd.hvy_ovh*hvy_ovh_f[flr]
	apqlty = bd.ap_qlt*ap_qlt_f[flr]
	shrt_clm = bd.shr_col*(-5)
	pound = bd.pnding*2*pnding_f[flr]
	soilcn = bd.soil_cn*10
	frmact = bd.frm_act*10
	bsmt = bd.bas_prsnt*bas_prsnt_f[flr]

	vs = sft + vrt + plir + hvyov + apqlty + shrt_clm + pound + soilcn + frmact + bsmt
	
	perf_sc = base_score + vs

	return perf_sc