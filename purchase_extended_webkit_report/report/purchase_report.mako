<html>
<head>
    <style type="text/css">
       ${css}
       
		hr.vertical
		{
		   border-right: thick solid #ff0000;
		} 
		th
		{
			font-family:helvetica; 
			font-size:10; 
		}
		tr
		{
			font-family:helvetica; 
			font-size:10; 
		}
   </style>
   
</head>
<header>
	%for o in objects :
	<table>
		<tr>
			<td style="font-face:Helvetica;font-size:18px;"><b>Total Purchase Amount Report - </b></td>
			<td><font color="white">.......</font></td>
			<td style="font-face:Helvetica; font-size:12px;"><b>Receive Date</b></td>
			<td><font color="white">.</font></td>
			<td>
				<table width="100%">
					<tr>
						<td style="font-size:12px;">${get_date_form()}</td>
					</tr>
				</table>
			</td>
			<td style="font-size:12px;"><b>To</b></td>
			<td><table width="100%">
				<tr>
					<td style="font-size:12px;">${get_date_to()}</td>
				</tr>
			</table></td>
		</tr>
		<tr>
			<td style="font-face:Helvetica;font-size:18px;"><b>By Supplier</b></td>
		</tr>
	</table>
</header>
<body>
        <table  width="50%">
            <thead>
                <tr>
                    <th style="text-align:left; font-size:10px; "><b>${_("Supplier Code")}</b></th>
                    <th style="text-align:left; font-size:10px;"><b>${_("Supplier Name")}</b></th>
                </tr>
            </thead>
            
        </table>
        <table width="100%" align="right" >
            <thead>
                <tr >
                    <th style="text-align:right; border-bottom: 1px solid black; font-size:10px; "><b>${_("Family Code")}</b></th>
                    <th style="text-align:right; border-bottom: 1px solid black; font-size:10px; "><b>${_("Total Qty")}</b></th>
                    <th style="text-align:right; border-bottom: 1px solid black; font-size:10px;"><b>${_("Total Amount")}</b></th>
                    <th style="text-align:right; border-bottom: 1px solid black; font-size:10px;"><b>${_("Currency")}</b></th>
                    <th style="text-align:right; border-bottom: 1px solid black; font-size:10px;"><b>${_("Total US Amount")}</b></th>
                 </tr>
            </thead>
        %for line in (get_order_lines(o)):
            <tbody>
                <tr>
                    <td style="text-align:left; font-size:10px;"> ${line.get('ref') or ' '} </td>
                    <td style="text-align:center; font-size:10px;"> ${ get_partner_name(line) } </td>
                </tr>
            </tbody>
        	%for li in line['values']:
					<tbody>
						<tr>
						    <td style="text-align:right; font-size:10px;">${li.get('code') or ''}</td>
						    <td style="text-align:right; font-size:10px;" >${li.get('qty') or ''}</td>
						    <td style="text-align:right; font-size:10px;" >${li.get('amount') or ''}</td>
						    <td style="text-align:right; font-size:10px;" >${li.get('currency') or ''}</td>
						    <td style="text-align:right; font-size:10px;" >${li.get('us_total_amount') or ''}</td>
						</tr> 
        	%endfor
						<tr>
							<td style="text-align:right; border-top: 1px solid #e0e0e0; font-size:10px;"><b>${_("Supplier Total")}</b></td>
						    <td style="text-align:right; border-top: 1px solid #e0e0e0; font-size:10px;" >${line.get('total') or ' '}</td>
						    <td style="text-align:right; border-top: 1px solid #e0e0e0; " > </td>
						    <td style="text-align:right; border-top: 1px solid #e0e0e0; " > </td>
						    <td style="text-align:right; border-top: 1px solid #e0e0e0; font-size:10px;" >${line.get('sum_total') or ' '}</td>
					    </tr>
						
					</tbody>
		%endfor
					<tbody>
						<tr>
							 <th style="text-align:right; font-size:10px; border-top: 1px solid black; ">${_("Grand Total")}</th>
						    <th style="text-align:right; font-size:10px; border-top: 1px solid black; " >${ get_total_qty() }</th>
						    <th style="text-align:right; font-size:10px; border-top: 1px solid black; " > </th>
						    <th style="text-align:right; font-size:10px; border-top: 1px solid black; " > </th>
						    <th style="text-align:right; font-size:10px; border-top: 1px solid black; " >${ get_total_amount() }</th>
					    </tr>
						
					</tbody>
				</table>
    %endfor
</body>
</html>
