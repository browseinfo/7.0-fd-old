<html>
<head>
    <style type="text/css">
        ${css}
        body
        {
			font-family:helvetica;
			font-size:7;
		}
		h4
		{
			font-family:helvetica;
			font-size:12;
		}
		th
		{
			font-family:helvetica;
			font-size:7;
			border:1px solid black;
		}
		td
		{
			font-family:helvetica;
			font-size:9;
			border-top:1px solid black;
			border-left:1px solid black;
			border-bottom:1px solid black;
		}
    </style>
</head>
<body>
    <table  width="220%" >
	<h2>PT Sales Day Book as at ${ get_month(data['form']['start_date']) } </h2>
	</br>
		<table width="220%">
			<th width="8%">DATE</th><th width="10%">INVOICE NUMBER</th><th width="10%">AREA</th>
			<th width="14%">CUSTOMER</th><th width="20%">DESCRIPTION</th><th width="6%">CURRENCY</th><th width="7%">TOTAL</th>
			<th width="7%">RATE</th><th width="8%">DPP PPN</th><th width="10%">NO SERI FAKTUR PAJAK</th>
			%for o in get_invoice_ids(data['form']):
				%for line in o.invoice_line:
					<tr>
						<td style="text-align:center;" > ${ get_formate_date(o.date_invoice) } </td>
						<td style="text-align:center;"> ${ o.number or '' } </td>
						<td style="text-align:center;"> ${ o.branch_id.name or '' } </td>
						<td style="text-align:left;"> ${ o.partner_id.name or '' } </td>
						<td style="text-align:left;"> ${ line.name or '' } </td>
						<td style="text-align:center;"> ${ o.currency_id.name or '' }  
							<font color="white">${ set_currency_data(o.currency_id.name,line.price_subtotal) } </font> 
						</td>
						<td style="text-align:right;"> ${ line.price_subtotal or '0.0' } </td>
						<td style="text-align:right;">
							<font color="white">${ set_exchange_rate(o) } </font> 
							${ o.exchange_rate or '0.0' }						 	
						</td>
						<td style="text-align:right;"> ${ (line.price_subtotal) * (o.exchange_rate) } </td>
						<td style="text-align:right; border-right:1px solid gray;"> ${ o.nomor_seri or '' } </td>
					</tr>
				%endfor
			%endfor
		</table>
		<table width="220%">
			%for key in get_currency_data():
				<tr>
					<td width="8%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;"><font color="white"></font></td>
					<td width="14%" style="border:none;"><font color="white"></font></td>
					<td width="20%" style="text-align:center; border:none;"><b>${ get_string() }</b></td>
					<td width="6%" style="border:none;">${ key }</td>
					<td width="7%" style="text-align:right; border:none;">${ get_currency_total(key) }</td>
					<td width="7%" style="border:none;"><font color="white"></font></td>
					<td width="8%" style="text-align:right; border:none;" >${ get_dpp_total(data['form']) }</td>
					<td width="10%" style="text-align:right; border:none;"><font color="white"></font></td>
				</tr>
			%endfor
		</table>
		</br>
		</br>
		</br>
		<table width="220%">
			<th width="8%" style="border:none;"><font color="white"></font></th>
			<th width="10%" style="border:none; text-align:left">Name</th>
			%for key in get_currency_data():
				<th width="6%" style="border:none; text-align:right">${ key }</th>
			%endfor
			<th width="14%" style="border:none;"><font color="white"></font></th>
			<th width="20%" style="border:none;"><font color="white"></font></th>
			<th width="6%" style="border:none;"><font color="white"></font></th>
			<th width="7%" style="border:none;"><font color="white"></font></th>
			<th width="7%" style="border:none;"><font color="white"></font></th>
			<th width="8%" style="border:none;"><font color="white"></font></th>
			<th width="10%" style="border:none;"><font color="white"></font></th>
			%for k in get_customer_name(data['form']):
				<tr>
					<td width="8%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;">${ k }</td>
					%for key in get_currency_data():
						<td width="6%" style="border:none; text-align:right">${ check_currency_total(key,k) }</td>
					%endfor
					<td width="14%" style="border:none;"><font color="white"></font></td>
					<td width="20%" style="border:none;"><font color="white"></font></td>
					<td width="6%" style="border:none;"><font color="white"></font></td>
					<td width="7%" style="text-align:right; border:none;" >
						<font color="white">${ set_dpp( (get_exchange_rate(k)) * get_keys(k) ) }</font>
						${ (get_exchange_rate(k)) * get_keys(k) }
					</td>
					<td width="7%" style="border:none;"><font color="white"></font></td>
					<td width="8%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;"><font color="white"></font></td>
				</tr>
			%endfor
				<tr>
					<td width="8%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;"><font color="white"></font></td>
					%for key in get_currency_data():
						<td width="10%" style="border-top:1px solid black; border-left:none;border-bottom:none; text-align:right">
							${ get_currency_total(key) }
						</td>
					%endfor
					<td width="14%" style="border:none;"><font color="white"></font></td>
					<td width="20%" style="border:none;"><font color="white"></font></td>
					<td width="6%" style="border:none;"><font color="white"></font></td>
					<td width="7%" style="text-align:right; border-top:1px solid black; border-left:none;border-bottom:none;" >
						${ get_dpp() }
					</td>
					<td width="7%" style="border:none;"><font color="white"></font></td>
					<td width="8%" style="border:none;"><font color="white"></font></td>
					<td width="10%" style="border:none;"><font color="white"></font></td>
				</tr>
		</table>
	</table>
</body>
</html>