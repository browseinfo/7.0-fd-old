<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>

<table style="width:750px">
<tr>
  <td><h5>PT. FD INDUSTRI INDONESIA<br>SMALL PETTY CASH</h5></td>
</tr>
</table>

<body>
        <table border="1" class="list_table" width="100%">
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Date")}</th>
                    <th style="text-align:left;">${_("V/CHR")}</th>
                    <th style="text-align:left;">${_("PARTICULAR")}</th>
                    <th style="text-align:left;">${_("DETAILS")}</th>
                    <th style="text-align:left;">${_("ACC. NO.")}</th>
                    <th style="text-align:left;">${_("DEBET")}</th>
                    <th style="text-align:left;">${_("DEBET")}</th>
                    <th style="text-align:left;">${_("DEBET")}</th>
                    <th style="text-align:left;">${_("CREDIT")}</th>
                    <th style="text-align:left;">${_("CREDIT")}</th>
                    <th style="text-align:left;">${_("BALANCE")}</th>
                    <th style="text-align:left;">${_("BALANCE")}</th>
                    <th style="text-align:left;">${_("RATE")}</th>
                </tr>
                <tr>
                	<th style="text-align:left;">${_(" ")}</th>
                    <th style="text-align:left;">${_(" ")}</th>
                    <th style="text-align:left;">${_(" ")}</th>
                    <th style="text-align:left;">${_(" ")}</th>
                    <th style="text-align:left;">${_(" ")}</th>
                    <th style="text-align:left;">${_("YEN")}</th>
                    <th style="text-align:left;">${_("USD")}</th>
                    <th style="text-align:left;">${_("IDR")}</th>
                    <th style="text-align:left;">${_("USD")}</th>
                    <th style="text-align:left;">${_("IDR")}</th>
                    <th style="text-align:left;">${_("USD")}</th>
                    <th style="text-align:left;">${_("IDR")}</th>
                    <th style="text-align:left;">${_("#N/A")}</th>
                </tr>
            </thead>

            %for begin in (get_begining_balance(o)):
	            <tbody>
	                <tr>
	                    <th style="text-align:left;"></th>
	                </tr>
	            </tbody>
	            <tbody>
	             %for val in begin['values']:
	             %endfor
	                <tr>
	                    <td style="text-align:left;">
	                       ${val.get('date') or ''}
	                     </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;"">
	                    </td>
	                    <td style="text-align:left;">
	                    <b>Begining</b>
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('debit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                      ${val.get('credit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                      ${begin['opening'] or ' '}
	                    </td>
	                    <td style="text-align:left;">
	                      ${val.get('new_balance') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                      ${val.get('rateof') or 0.0}
	                    </td>
	                </tr>
	                </tbody>
	           </tbody>
	            
	            <tbody>
	            %for val in begin['values']:
	                <tr>
	                    <td style="text-align:left;">
	                        ${val.get('date') or ''}
	                     </td>
	                    <td style="text-align:left;">
	                        ${val.get('ref') or ''}
	                    </td>
	                    <td style="text-align:left;"">
	                         ${val.get('partner') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                    	${val.get('name') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('account') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('jpy_debit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('debit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('idr_debit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('credit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('idr_credit') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                    	${val.get('opening_balance') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                    	${val.get('new_balance') or 0.0}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('rateof') or 0.0}
	                    </td>
	                </tr>
	                </tbody>
    		 %endfor
	                <tr>
	                    <td style="text-align:left;">
	                     </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;"">
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                      Total
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                        ${sum_debit()}
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                        ${sum_credit()}
	                    </td>
	                    <td style="text-align:left;">
	                        Closing Balance:
	                    </td>
	                    <td style="text-align:left;">
	                    	${sum_closing()}
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
				    </tr>



%endfor
     </table>
</body>
</html>
