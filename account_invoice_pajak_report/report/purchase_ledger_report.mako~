<html>
<head>
    <style type="text/css">
       ${css}
   </style>
</head>
<header>
</header>

<table style="width:750px">
<tr>
  <td><h2>Purchase Amount Report (Invoice)</h2></td>
  <td>Issue Date</td>		
  <td>
   <table style="width:150px" border='1'>
      <td>${get_start_date()}</td>
   </table>
  </td>
  <td>To</td>
  <td>
  <table style="width:150px" border='1'>
     <td>${get_end_date()}</td>
   </table>
 </tr>
<tr>
</table>

<table style="width:200px">
<tr>
  <td><b>Customer Code</b></td>
  <td>  </td>		
 </tr>
<tr>
</table>

<table>
<table style="width:200px">
<tr>
  <td><b>Customer Code</b></td>
  <td>  </td>		
 </tr>
<tr>
</table>
       %for o in objects :
        <center></center>
        <table width="100%">
                	
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Issue Date")}</th>
                    <th style="text-align:left;">${_("SO")}</th>
                    <th style="text-align:left;">${_("Cust PO No")}</th>
                    <th style="text-align:left;">${_("Part No")}</th>
                    <th style="text-align:left;" >${_("Part Name")}</th>
                    <th style="text-align:left;" >${_("Order Qty")}</th>
                    <th style="text-align:left;" >${_("Unit Price")}</th>
                    <th style="text-align:left;" >${_("Amount")}</th>
                    <th style="text-align:left;" >${_("Amount(US)")}</th>
                    <th style="text-align:left;" >${_("Profit(US)")}</th>
                    <th style="text-align:left;" >${_("Profit%")}</th>
                </tr>
            </thead>
			<b><hr color="black"></b>              
            %for line in (get_data(o)):
	            <tbody>
	                <tr>
	                    <th style="text-align:left;">${line.get('partner_id') or ' '}</th>
	                </tr>
	            </tbody>
	                	%for val in line['values']:
	                <tr>
	                    <td style="text-align:left;">
	                        ${val.get('date_invoice') or ''}
	                     </td>
	                    <td style="text-align:left;">
	                        ${val.get('number') or ''}
	                    </td>
	                    <td style="text-align:left;"">
	                        ${val.get('origin') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('default_code') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('product_id') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('quantity') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('price_unit') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                        ${val.get('price_subtotal') or ''}
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                    <td style="text-align:left;">
	                    </td>
	                </tr>
	                </tbody>
					               
	             %endfor
	             <tr>
					<td style="text-align:right;"></td>
				    <td style="text-align:right;" ></td>
				    <td style="text-align:right;" ></td>
				    <td style="text-align:right;" > </td>
				    <td style="text-align:right;" >${_("SubTotal")} </td>
				    <td style="text-align:left;" >${line['total'] or ' '}</td>
				    <td style="text-align:right;" ></td>
				    <td style="text-align:left;" >${line['sum_total'] or ' '}</td>
			    </tr>
            %endfor
             			         
            %endfor
            
        </table>
   
</body>
</html>
