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
	<h3>TOTAL PT SALES AS AT ${ data['form']['period_id'][1] }</h3>
    %for o in objects :
        <table border="1" width="100%">
                <tr>
                    <th style="text-align:center;">  ${_("NO")}</th>
                    <th style="text-align:center;"> ${_("CUSTOMER")}</th>
                    <th style="text-align:center;"> ${_("TOTAL (USD)")}</th>
					%for cat in get_categ():
						<th > ${ cat.name } </th>
					%endfor
					<font color="white"> ${ total_dict() } </font>
                </tr>
            </thead>
            %for line in (get_payslip_lines(o)):
                <tbody >
                <tr>
					<td style="text-align:center;"> ${ get_index() } </td>
					<td style="text-align:center;white-space: pre;"> ${ line.keys()[0] } </td>
					<td style="text-align:center;"> ${ line[line.keys()[0] ]['total'] } </td>
					<font color="white"> ${ set_grand_total( line[line.keys()[0]]['total'] ) }</font>
					%for cat in get_categ():
						<td style="text-align:center;"> ${ line[line.keys()[0] ].get(cat.name) or '-' } </td>
					%endfor					
                </tr>
                </tbody>
            %endfor
				<tr>
					<td></td>
					<td style="text-align:right;font-weight:bold;"> TOTAL</td>
					<td style="text-align:center;font-weight:bold;"> ${ get_grand_total() } </td>
					%for cat in get_categ():
						<td style="text-align:center;font-weight:bold;"> ${ get_grand_total_categ(cat.name) or '-' } </td>
					%endfor									
				</tr>
        </table>
 
    %endfor
	<h3>REMARK:FOR THE FOREIGN CURRENCY ACCOUNT,STANDARD RATES ARE AS BELOW:</h3>
	<h3>FOR   RP=</h3>
	<h3><font color="white">......</font>YEN=</h3>
</body>
</html>
