<html>
<head>
    <style type="text/css">
        ${css}
		th,td
		{


		}
    </style>
</head>
<body>
    <table  width="100%">
	<h2>${ branch_code(data['form']['branch_id'][0]) } Purchase Day Book ${ date_format(data['form']['start_date']) } To ${ date_format(data['form']['end_date']) } </h2>
	<th style="border-bottom: 1px solid black;">ETA DATE</th>
	<th style="border-bottom: 1px solid black;">INVOICE NUMBER</th>
	<th style="border-bottom: 1px solid black;">DATE INVOICE</th>
	<th style="border-bottom: 1px solid black;">ACCOUNT CODE</th>
	<th style="border-bottom: 1px solid black;">SUPPLIER</th>
	<th style="border-bottom: 1px solid black;">DESCRIPTION</th>
	<th style="border-bottom: 1px solid black;">FREIGN CURRENCY</th>
	<th style="border-bottom: 1px solid black;">TOTAL (USD)</th>
	%for cat in get_categ():
        <th style="border-bottom: 1px solid black;"> ${ cat.name } </th>
	 %endfor
	 <font color="white"> ${ total_dict() } </font>
	<th style="border-bottom: 1px solid black;">ACC TOTAL</th>
	%for o in purchase_details(data['form']):
		<tr style="border-bottom: 1px solid #e0e0e0;">
			<td style="white-space: pre; border-bottom: 1px solid #e0e0e0;"> ${ date_format(o.date_due) or '' } </td>
			<td style="border-bottom: 1px solid #e0e0e0;"> ${ o.number or '' } </td>
			<td style="white-space: pre; border-bottom: 1px solid #e0e0e0;"> ${ date_format(o.date_invoice) or '' } </td>
			<td style="border-bottom: 1px solid #e0e0e0;"> ${ o.account_id.code or '' } </td>
			<td style="white-space: pre; border-bottom: 1px solid #e0e0e0;"> ${ o.partner_id.name or '' } </td>
			<td style="white-space: pre; border-bottom: 1px solid #e0e0e0;"> ${ str(get_product_code(o.invoice_line)).replace('[','').replace(']','').replace("u'",'').replace("'",'') or '' } </td>
			<td style="border-bottom: 1px solid #e0e0e0;"> ${ o.currency_id.name or '' } </td>
			<td style="border-bottom: 1px solid #e0e0e0;"> ${ get_currency_subtotal(o) }
			</td>
			%for cat in get_categ():
				<td style="border-bottom: 1px solid #e0e0e0;"> ${ categ_price(o.invoice_line,cat) } </td>
			%endfor
			<td style="font-weight:bold; border-bottom: 1px solid #e0e0e0;"> ${ get_total() } </td>
		</tr>
	%endfor
		<tr>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td></td>
			<td style="font-weight:bold;"> ${ get_total() } </td>
			%for cat in get_categ():
				<td style="font-weight:bold;"> ${ get_grand_total(cat.id) } </td>
			%endfor
			<td style="font-weight:bold;"> ${ get_total() } </td>
		</tr>
	</table>
</body>
</html>
