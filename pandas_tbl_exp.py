def qty_combined_years(previous_built_data, built_data, previous_year, current_year, cur_month):
    prev_manf_qty = previous_built_data[['Manufacturer', 'Date', 'Qty']].copy()
    prev_qty_month = prev_manf_qty.loc[(prev_manf_qty['Date'].dt.month <= cur_month)]
    prev_manf_qty['Date'] = prev_manf_qty['Date'].dt.year
    prev_manf_qty['Qty'] = prev_manf_qty['Qty'].fillna(0)
    prev_manf_qty = prev_manf_qty.groupby(['Manufacturer', 'Date'])['Qty'].sum().reset_index()
    prev_manf_qty['Date'] = prev_manf_qty['Date'].astype('string')
    prev_manf_qty = prev_manf_qty.pivot_table(index=['Manufacturer'], columns='Date').reset_index()
    
    prev_qty_month['Date'] = prev_qty_month['Date'].dt.year
    prev_qty_month['Date'] = 'm'+prev_qty_month['Date'].astype('string')
    prev_qty_month['Qty'] = prev_qty_month['Qty'].fillna(0)
    prev_qty_month = prev_qty_month.groupby(['Manufacturer', 'Date'])['Qty'].sum().reset_index()
    prev_qty_month['Date'] = prev_qty_month['Date'].astype('string')
    prev_qty_month = prev_qty_month.pivot_table(index=['Manufacturer'], columns='Date').reset_index()
    
    curr_manf_qty = built_data[['Manufacturer', 'Date', 'Qty']].copy()
    curr_manf_qty['Date'] = curr_manf_qty['Date'].dt.year
    curr_manf_qty['Qty'] = curr_manf_qty['Qty'].fillna(0)
    curr_manf_qty = curr_manf_qty.groupby(['Manufacturer', 'Date'])['Qty'].sum().reset_index()
    curr_manf_qty['Date'] = curr_manf_qty['Date'].astype('string')
    curr_manf_qty = curr_manf_qty.pivot_table(index=['Manufacturer'], columns='Date').reset_index()

    combined_yearsQ_nomonth = pd.merge(prev_manf_qty, prev_qty_month, on='Manufacturer', how='outer')
    combined_years_qty = pd.merge(combined_yearsQ_nomonth, curr_manf_qty, on='Manufacturer', how='outer')

    combined_years_qty['Qty',str(current_year)] = combined_years_qty['Qty',str(current_year)].fillna(0)
    combined_years_qty['Qty',str(previous_year)] = combined_years_qty['Qty',str(previous_year)].fillna(0)
    combined_years_qty['Qty','m'+str(previous_year)] = combined_years_qty['Qty','m'+str(previous_year)].fillna(0)
    combined_years_qty.loc['Total',:] = combined_years_qty[['Qty']].sum(axis=0, numeric_only=True)
    combined_years_qty.iloc[-1, combined_years_qty.columns.get_loc('Manufacturer')] = 'Total'
    combined_years_qty['Growth'] = ((combined_years_qty['Qty',str(current_year)]/combined_years_qty['Qty','m'+str(previous_year)])-1)
    combined_years_qty.loc[~numpy.isfinite(combined_years_qty['Growth']), 'Growth'] = 0
    combined_years_qty['Growth'] = (combined_years_qty['Growth']*100).round(1).astype('string')+' %'
    combined_years_qty['Qty'] = combined_years_qty['Qty'].apply(lambda x: x.apply(lambda y:'{:,.0f}'.format(y)))
    
    return combined_years_qty
