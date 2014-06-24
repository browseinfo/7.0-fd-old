<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for o in objects :
        <table class="list_table" border="1" width="100%">
        <center><h4>GUDANG BERIKAT PT FD INDUSTRI INDONESIA</h4>
        <h4>${get_branch(o)}</h4>
        <h4>PERIODE:  ${ date_format(data['form']['startdtae']) } SD ${ date_format(data['form']['enddtae']) }<h4></center>
            <thead>
                <tr>
                   <th style="text-align:left;">${_("KODE BARANG")}</th>
                    <th style="text-align:left;">${_("NAMA BARANG")}</th>
                    <th style="text-align:left;">${_("SATUAN")}</th>
                    <th style="text-align:left;">${_("SALDO AWAL01-SEPT-2013")}</th>
                    <th style="text-align:left;">${_("PEMASUKAN")}</th>
                    <th style="text-align:left;">${_("PENGELUARAN")}</th>
                    <th style="text-align:left;">${_("PENYESUAIAN(ADJUSTMENT)")}</th>
                    <th style="text-align:left;">${_("SALDO AKHIR 31-DECEMBER")}</th>
                    <th style="text-align:left;">${_("STOCK OPNAME31")}</th>
                    <th style="text-align:left;">${_("SELISIH")}</th>
                    <th style="text-align:left;">${_("KETERANGAN")}</th>
                </tr>
            </thead>
            %for line in (get_all_lines(o)):
                <tbody >
                <tr>
                    <td style="text-align:left;">
                        ${line.get('code') or ''}
                     </td>
                    <td style="text-align:left;">
                        ${line.get('product') or ''}
                     </td>
                    <td style="text-align:left;">
                        ${line.get('uom') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('totalqty') or ''}
                    </td>
                    <td style="text-align:left;"">
                        ${line.get('in_qty') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('out_qty') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('inv_qty') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('last_qty') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('ope_qty') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('selish') or ''}
                    </td>
                    <td style="text-align:left;">
                        ${line.get('katering') or ''}
                    </td>
                </tr>
                </tbody>
            %endfor
        </table>
        <table width="90%">
          <tbody>
	        <tr align="Right">
		          <td style="text-align:Right;"><h5>Kami bertanggung jawab<br>
		          atas kebenaran laporan ini<br>
		          Purwakarta,06 Februari 2014<br>
			      Kawasan Berikat<br>
		          KEIICHIRO SAKATA</h5></td>
	        </tr>
	      </tbody>
        </table>
    %endfor
</body>
</html>
