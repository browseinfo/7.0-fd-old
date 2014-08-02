<html>
<head>
    <style type="text/css">
        ${css}
		th,td
		{
			border:1px solid black;
		}
    </style>
</head>
<body>
    <table  width="100%">
	<h1>${ branch_code(data['form']['branch_id'][0]) }  Sale Day Book between ${ date_format(data['form']['start_date']) } and ${ date_format(data['form']['end_date']) } </h1>
	<th>DATE</th><th>INVOICE NUMBER</th><th>ACCOUNT CODE</th><th>CUSTOMER</th><th>DESCRIPTION</th><th>FOREIGN CURRENCY</th><th>TOTAL (USD)</th>
	%for cat in get_categ():
        <th> ${ cat.name } </th>
	 %endfor
	 <font color="white"> ${ total_dict() } </font>
	<th>ACC TOTAL</th>
	%for o in sale_details(data['form']):
		<tr>
			<td style="white-space: pre;"> ${ date_format(o.date_invoice) or '' } </td>
			<td> ${ o.number or '' } </td>
			<td> ${ o.account_id.code or '' } </td>
			<td style="white-space: pre;"> ${ o.partner_id.name or '' } </td>
			<td> ${ str(get_product_code(o.invoice_line)).replace('[','').replace(']','').replace("u'",'').replace("'",'') or '' } </td>
			<td> ${ o.currency_id.name or '' } </td>
			<td> ${ get_currency_subtotal(o) } </font></td>
			%for cat in get_categ():
				<td> ${ categ_price(o.invoice_line,cat) } </td>
			%endfor
			<td style="font-weight:bold;"> ${ get_total() } </td>
		</tr>
	%endfor
		<tr>
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
