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
	<h3>TOTAL PURCHASE PT AS AT ${ data['form']['period_id'][1] }</h3>
    %for o in objects :
        <table width="100%">
                <tr>
                    <th style="text-align:left;border:1px solid black;">  ${_("NO")}</th>
                    <th style="text-align:left;border:1px solid black;"> ${_("SUPPLIER")}</th>
                    <th style="text-align:left;border:1px solid black;"> ${_("TOTAL (USD)")}</th>
					%for cat in get_categ():
						<th style="border:1px solid black;"> ${ cat.name } </th>
					%endfor
					<font color="white"> ${ total_dict() } </font>
                </tr>
            </thead>
            %for line in (get_payslip_lines(o)):
                <tbody>
                <tr>
					<td style="text-align:center; border: 1px solid #e0e0e0;"> ${ get_index() } </td>
					<td style="text-align:center;white-space: pre; border: 1px solid #e0e0e0;"> ${ line.keys()[0] } </td>
					<td style="text-align:center; border: 1px solid #e0e0e0;"> ${ line[line.keys()[0] ]['total'] } </td>
					<font color="white"> ${ set_grand_total( line[line.keys()[0]]['total'] ) }</font>
					%for cat in get_categ():
						<td style="text-align:center; border: 1px solid #e0e0e0;"> ${ line[line.keys()[0] ].get(cat.name) or '-' } </td>
					%endfor					
                </tr>
                </tbody>
            %endfor
				<tr>
					<td style="border:1px solid black;"></td>
					<td style="text-align:center;font-weight:bold; border:1px solid black;"> TOTAL</td>
					<td style="text-align:center;font-weight:bold; border:1px solid black;"> ${ get_grand_total() } </td>
					%for cat in get_categ():
						<td style="text-align:center;font-weight:bold; border:1px solid black;"> ${ get_grand_total_categ(cat.name) or '-' } </td>
					%endfor									
				</tr>
        </table>
 
    %endfor
</body>
</html>
