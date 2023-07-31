from datetime import date, datetime, timedelta

# Get the current date
today = date.today()
current_year = today.year



def convert_to_epoch_milliseconds(date_input, is_mtd):
    if is_mtd and isinstance(date_input, str):
         date_created = datetime.strptime(date_input, '%Y-%m-%d')

    elif is_mtd and isinstance(date_input, date):
        date_created = datetime(date_input.year, date_input.month, date_input.day)

    elif isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, '%Y-%m-%d')
        yesterday  = date_obj - timedelta(1)
        date_created = datetime(yesterday.year, yesterday.month, yesterday.day)

    elif isinstance(date_input, date):
        yesterday = date_input - timedelta(1)
        date_created = datetime(yesterday.year, yesterday.month, yesterday.day)

    else:
        raise ValueError("Invalid input format. Expected date object or date string in 'YYYY-MM-DD' format.")
    return int(date_created.timestamp()) * 1000

def convert_to_epoch_milliseconds_future(date_input):
    if isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, '%Y-%m-%d')
        yesterday  = date_obj - timedelta(1)
        yesterday_obj = datetime(yesterday.year, yesterday.month, yesterday.day) +timedelta(hours=23, minutes=59, seconds=59)
    elif isinstance(date_input, date):
        yesterday = date_input - timedelta(1)
        yesterday_obj = datetime(yesterday.year, yesterday.month, yesterday.day) + timedelta(hours=23, minutes=59, seconds=59)
    else:
        raise ValueError("Invalid input format. Expected date object or date string in 'YYYY-MM-DD' format.")
    return int(yesterday_obj.timestamp()) * 1000

def date_format(date_stmap):
    if isinstance(date_stmap, str):
        date_object = datetime.strftime(date_stmap, '%Y-%m-%d')
        yesterday = date_object- timedelta(1)
        return yesterday
    else:
        yesterday = date_stmap - timedelta(1)
        return yesterday
    

# Calculate the start and end dates for MTD and YTD
start_date_mtd = date(current_year, today.month, 1)
end_date_mtd = today
start_date_ytd = date(current_year, 1, 1)
end_date_ytd = today

# Format the dates as strings
start_date_mtd_str = start_date_mtd.strftime('%Y-%m-%d')
end_date_mtd_str = end_date_mtd.strftime('%Y-%m-%d')
start_date_ytd_str = start_date_ytd.strftime('%Y-%m-%d')
end_date_ytd_str = end_date_ytd.strftime('%Y-%m-%d')

# This is only used for the CURRENT
start_time_epoch = convert_to_epoch_milliseconds(today, False)

# This is used for YTD, MTD, CURRENT
end_time_epoch = convert_to_epoch_milliseconds_future(today)

# This is only used for the MTD epoch
start_time_epoch_mtd =convert_to_epoch_milliseconds(start_date_mtd, True)

# regular times
start_time_regular= date_format(today).strftime('%Y-%m-%d')
end_time_regular=  date_format(today).strftime('%Y-%m-%d')


print(f"start-epoch {start_time_epoch} end-time-epoch {end_time_epoch}")
print(f"epoch mtd {start_time_epoch_mtd}")
print(f"regular times {start_date_mtd_str}")
print(f"regular times {start_time_regular}, {end_time_regular}")


excel_references={
# --------------------Current_date----------------------

    #region DOMESTIC POS TRANSACTIONS FOR CURRENT DATE 
    'domestic_pos_txns_count_current_date': {
        'cell_reference': 'C3',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND  txn_type='POS') and (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    
     'domestic_pos_spends_in_lakhs_current_date': {
        'cell_reference': 'D3',
        'query': f'''
                    select 
                       Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                        SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)
                        AS POS_total 
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE iso_num_currency_code = 356 and (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch': True
    },

       'domestic_pos_unique_txns_count_current_date': {
        'cell_reference': 'E3',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    # endregion

    #region POS INTERNATIONAL TRANSACTIONS FOR CURRENT DATE
    'international_pos_txns_count_current_date':{
        'cell_reference':'C4',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    'international_pos_spends_in_lakhs_current_date':{
        'cell_reference':'D4',
        'query':f'''
            	SELECT 
                    Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) -
	                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
	                AS POS_total 
		        FROM cards.scapia_unbilled_card_txn_details
                WHERE  iso_num_currency_code <> 356  and (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
        ''',
        'is_epoch':True

    },
    'internationl_pos_unique_txns_count_current_date':{
        'cell_reference':'E4',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },
    # endregion

    # region DOMESTIC_ECOM_TRANSACTIONS_FOR_CURRENT_DATE
    'ecom_domestic_txns_count_current_date':{
        'cell_reference':'C6',
        'query': f'''SELECT COUNT(card_id) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
         'is_epoch':True
    },
    'ecom_doemstic_spends_in_lakhs_current_date':{
        'cell_reference':'D6',
        'query':f'''
                    SELECT 
                        round((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
	                    SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END ))/ 100000,2)
	                    AS ECOM_total 
		            FROM cards.scapia_unbilled_card_txn_details
                    WHERE  iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'ecom_domestic_txn_unique_count_current_date':{
        'cell_reference':'E6',
       'query': f'''SELECT COUNT(DISTINCT(card_id)) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
       'is_epoch':True
    },
    # endregion

    # region ECOM_INTERNATIONAL_TRANSACTIONS_FOR_CURRENT_DATE
    'ecom_international_txns_count_current_date':{
        'cell_reference':'C7',
        'query':f'''
                    SELECT 
                    COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details 
                    WHERE  (iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                    (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },

    'ecom_international_spends_in_lakhs_current_date':{
        'cell_reference':'D7',
        'query':f'''
	                SELECT 
                            round((SUM(CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                            SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
                            AS ECOM_total 
		                FROM cards.scapia_unbilled_card_txn_details
                            WHERE  iso_num_currency_code <> 356 AND 
                            (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },

    'ecom_international_txn_unique_count_current_date':{
        'cell_reference':'E7',
        'query':f'''
                    SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE(iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                        (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },
    # endregion

    

    # region ECOM_TOTAL_current_date
    'ECOM_total_current_date':{
        'cell_reference':'D8',
        'query':f'''  
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}'
            ''',
        'is_epoch':True
    },
    # endregion

    # region total_spends_current_date
    'total_spends_current_date':{
        'cell_reference':'D9',
        'query':f'''  
                WITH pos_tots AS (
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch}' and txn_time_epoch <= '{end_time_epoch}'
                ), ecom_tots AS (
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS ECOM_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch}' and  txn_time_epoch <= '{end_time_epoch}'
                )
                SELECT SUM(POS_TOTAL_DOMESTIC + ECOM_TOTAL_DOMESTIC) FROM pos_tots, ecom_tots
            ''',
        'is_epoch':True
    },
    # endregion

    # region cards_count
    
    'cards_count_current_date':{
        'cell_reference':'E9',
        'query':f''' 
                    select COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END )) +
                    COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) )+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END ))+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END ))
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE  txn_time_epoch >='{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}'
                ''',
          'is_epoch':True
    },
    # endregion

    # region rewards_inelgible
    'cards_count_for_reward_inelgible_current_date':{
        'cell_reference':'C10',
        'query':f'''
                        SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                        AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                        (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },

    'reward_inelgibile_current_date':{
        'cell_reference':'D10',
        'query':f'''
                        SELECT ROUND((SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) then txn_amount ELSE 0 END) - 
                        SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) AND txn_type='REFUND'
                        then txn_amount ELSE 0 END))/100000,2)
                        FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE(txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },

    'unique_cards_count_rewards_inelgible_current_date':{
        'cell_reference':'E10',
        'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region scapia_travels
    'cards_count_scapia_travel_spends_current_date':{
        'cell_reference':'C11',
         'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
               (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
        'is_epoch':True
    },
    'scapia_travel_spends_current_date':{
         'cell_reference':'D11',
         'query':f'''
                    SELECT ROUND((SUM(case when  txn_type <> 'ATM' AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) then txn_amount ELSE 0 END) - 
                    SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) AND txn_type='REFUND'
                    then txn_amount ELSE 0 END))/100000,2) AS total_amount
                    FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE(txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
     'unique_cards_count_scapia_travel_current_date':{
        'cell_reference':'E11',
         'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region ATM_TRANSACTIONS
    'cards_count_for_atm_txns_current_date':{
        'cell_reference':'C12',
        'query':f'''
                    SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'atm_spends_current_date':{
        'cell_reference':'D12',
        'query':F'''
                    SELECT ROUND(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'unique_cards_count_atm_current_date':{
        'cell_reference':'E12',
        'query':F'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region repayments
    'repayment_txns_count_current_date':{
        'cell_reference':'C13',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
      'repayment_amount_received_current_date':{
        'cell_reference':'D13',
        'query':f'''
                    SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },
      'repayment_unique_txns_count_current_date':{
        'cell_reference':'E13',
        'query':f''' SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },
    # endregion

    # region calculating surcharge
    'surcharge_txns_count_current_date':{
        'cell_reference': 'C14',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND  (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },

       'surcharge_amount_current_date':{
        'cell_reference': 'D14',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
       'surcharge_unique_txns_count_current_date':{
        'cell_reference': 'E14',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
    # endregion

    # region calculating fees
    'fees_txns_count_current_date':{
        'cell_reference':'C15',
        'query':f''' SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                    ''',
        'is_epoch':True
    },
        'fees_amount_current_date':{
        'cell_reference':'D15',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
        'fees_unique_txns_count_current_date':{
        'cell_reference':'E15',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
        'is_epoch':True
    },
    # endregion

    # region cards_issued_current_date 
    'cards_issued_current_date_current_date':{
        'cell_reference':'C16',
        'query':f'''SELECT  COUNT(t2.page_id) AS cards_count FROM card_customer_details t1
                        JOIN 
                        cards.loan_approval_workflow t2 ON
                        t1.scapia_customer_id = t2.internal_user_id 
                        WHERE DATE(t1.updated_at) ='{start_time_regular}' AND 
                        page_id IN ('ONBOARDING_COMPLETED','CIF_POLLING','VIRTUAL_CARD_ACTV','SIM_BINDING','PHYSICAL_CARD_ACTV')
                        ''',
        'is_epoch':False
    },
    # endregion

    # region ntb# for current_date [need to check]
    'ntb_percentage_current_date':{
        'cell_reference':'C17',
        'query':f'''
                    WITH cards_issued AS (
                        SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE DATE(t1.updated_at) ='{start_time_regular}' AND 
                        (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    ntb_data AS (
                        SELECT count(internal_user_id) AS ntb_count 
                        FROM cards.workflow_docs          
                        JOIN cards.card_customer_details ON card_customer_details.scapia_customer_id = workflow_docs.internal_user_id 
                        WHERE document_TYPE = 'CARD_INFO' AND (DATE(card_customer_details.updated_at) ='{start_time_regular}' AND JSON_EXTRACT(workflow_docs.document_details, '$.existingBankCustomerInfo.ddupeFlag') = "N")
                    )
                    SELECT  (ntb_count / cards_count) * 100 AS percentage
                    FROM cards_issued, ntb_data;
                ''',
         'is_epoch':False
    },
    # endregion
    
    # region average_credit_card_limit_current_date 
    'average_credit_card_limit_current_date':{
        'cell_reference':'C18',
        'query':f''' 
                    SELECT AVG(t2.card_limit) FROM cards.user_cards t1
                    JOIN cards.card_details t2 ON t1.scapia_customer_id = t2.scapia_customer_id
                    WHERE t1.card_status='ACTIVE' AND DATE(t1.created_at) ='{start_time_regular}'
                ''',
        'is_epoch':False

    },
    # endregion

    # region finding the count for the age 23-24_current_date
    'age_for_23_24_current_date':{
        'cell_reference':'C19',
        'query':f'''
                    SELECT
            SUM(
                IF(
                CASE 
                WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                ELSE YEAR(issued_date)-YEAR(dob)-1
                END in (23,24),1,0)) AS _count
            FROM
            (
            SELECT
                DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
            FROM workflow_docs as w 
            JOIN loan_approval_workflow as l 
            ON  l.workflow_type = 'card' AND 
                l.status = 'completed' AND 
                l.loan_approval_workflow_id = w.workflow_id 
                AND w.document_type = 'user_information'
            WHERE
                -- Add your WHERE condition for the issued date comparison here
                DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') = '{start_time_regular}'
            ) t;
       ''',
        'is_epoch':False
    },
    # endregion

    # region percentage of age2324_current_date
    'age_avg_23_24_current_date':{
        'cell_reference':'C20',
        'query':f'''
                    WITH cards_cout AS (
                    SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE DATE(t1.updated_at) ='{start_time_regular}' AND 
                        (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    cards_23_24 AS (
                    SELECT
                    SUM(
                        IF(
                        CASE 
                        WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                        ELSE YEAR(issued_date)-YEAR(dob)-1
                        END in (23,24),1,0)) AS _count
                    FROM
                    (
                    SELECT
                        DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                        l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
                    FROM workflow_docs as w 
                    JOIN loan_approval_workflow as l 
                    ON  l.workflow_type = 'card' AND 
                        l.status = 'completed' AND 
                        l.loan_approval_workflow_id = w.workflow_id 
                        AND w.document_type = 'user_information'
                    WHERE
                        -- Add your WHERE condition for the issued date comparison here
                        DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') = '{start_time_regular}'
                    ) t
                    )

                    SELECT  (_count/cards_count)*100 FROM cards_cout,cards_23_24
                '''  ,
                'is_epoch':False
    },
    # endregion

    # region active_cards_current_date
    'active_cards_for_current_date':{
         'cell_reference':'C21',
        'query':f''' 
                    SELECT COUNT(card_status) FROM cards.user_cards
                    WHERE DATE(updated_at) = '{start_time_regular}' AND card_status='ACTIVE'
                ''',
        'is_epoch':False
    },
    #endregion

# --------------------------------MTD-----------------------------------------------
    
    #region DOMESTIC POS TRANSACTIONS FOR MTD 
    'domestic_pos_txns_count_MTD': {
        'cell_reference': 'F3',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND  txn_type='POS') and (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    
     'domestic_pos_spends_in_lakhs_MTD': {
        'cell_reference': 'G3',
        'query': f'''
                    select 
                       Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                        SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)
                        AS POS_total 
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE iso_num_currency_code = 356 and (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch': True
    },

       'domestic_pos_unique_txns_count_MTD': {
        'cell_reference': 'H3',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    # endregion

    #region POS INTERNATIONAL TRANSACTIONS FOR MTD
    'international_pos_txns_count_MTD':{
        'cell_reference':'F4',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch': True
    },
    'international_pos_spends_in_lakhs_MTD':{
        'cell_reference':'G4',
        'query':f'''
            	SELECT 
                    Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) -
	                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
	                AS POS_total 
		        FROM cards.scapia_unbilled_card_txn_details
                WHERE  iso_num_currency_code <> 356  and (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
        ''',
        'is_epoch':True

    },
    'internationl_pos_unique_txns_count_MTD':{
        'cell_reference':'H4',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },
    # endregion

    # region DOMESTIC_ECOM_TRANSACTIONS_FOR_MTD
    'ecom_domestic_txns_count_MTD':{
        'cell_reference':'F6',
        'query': f'''SELECT COUNT(card_id) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and ( txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')''',
         'is_epoch':True
    },
    'ecom_doemstic_spends_in_lakhs_MTD':{
        'cell_reference':'G6',
        'query':f'''
                    SELECT 
                        round((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
	                    SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END ))/ 100000,2)
	                    AS ECOM_total 
		            FROM cards.scapia_unbilled_card_txn_details
                    WHERE  iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'ecom_domestic_txn_unique_count_MTD':{
        'cell_reference':'H6',
       'query': f'''SELECT COUNT(DISTINCT(card_id)) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and ( txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}')''',
       'is_epoch':True
    },
    # endregion

    # region ECOM_INTERNATIONAL_TRANSACTIONS_FOR_MTD
    'ecom_international_txns_count_MTD':{
        'cell_reference':'F7',
        'query':f'''
                    SELECT 
                    COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details 
                    WHERE  (iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                    (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },

    'ecom_international_spends_in_lakhs_MTD':{
        'cell_reference':'G7',
        'query':f'''
	                SELECT 
                            round((SUM(CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                            SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
                            AS ECOM_total 
		                FROM cards.scapia_unbilled_card_txn_details
                            WHERE  iso_num_currency_code <> 356 AND 
                            (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },

    'ecom_international_txn_unique_count_MTD':{
        'cell_reference':'H7',
        'query':f'''
                    SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE(iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                        (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')''',
        'is_epoch':True
    },
    # endregion

    # region POS_TOTAL_MTD
    'pos_total_MTD':{
        'cell_reference':'G5',
        'query':f''' 
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}'
            ''',
        'is_epoch':True
    },
    # endregion

    # region ECOM_TOTAL_MTD
    'pos_total_current_date':{
        'cell_reference':'G8',
        'query':f'''  
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}'
            ''',
        'is_epoch':True
    },
    # endregion
    
    # region cards_count_unique_MTD
    'cards_count_MTD':{
        'cell_reference':'H9',
        'query':f''' 
                    select COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END )) +
                    COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) )+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END ))+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END ))
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE  txn_time_epoch >='{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}'
                ''',
          'is_epoch':True
    },
    # endregion

    # region total_spends_MTD
    'total_spends_MTD':{
        'cell_reference':'G9',
        'query':f'''  
                WITH pos_tots AS (
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch_mtd}' and  txn_time_epoch <= '{end_time_epoch}'
                ), ecom_tots AS (
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS ECOM_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch_mtd}' and txn_time_epoch <= '{end_time_epoch}'
                )
                SELECT SUM(POS_TOTAL_DOMESTIC + ECOM_TOTAL_DOMESTIC) FROM pos_tots, ecom_tots
            ''',
        'is_epoch':True
    },
    # endregion

    # region rewards_inelgible MTD
    'cards_count_for_reward_inelgible_MTD':{
        'cell_reference':'F10',
        'query':f'''
                        SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                        AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                        (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },

    'reward_inelgibile_MTD':{
        'cell_reference':'G10',
        'query':f'''
                        SELECT ROUND((SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) then txn_amount ELSE 0 END) - 
                        SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) AND txn_type='REFUND'
                        then txn_amount ELSE 0 END))/100000,2)
                        FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE(txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },

    'unique_cards_count_rewards_inelgible_MTD':{
        'cell_reference':'H10',
        'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region scapia_travels MTD
    'cards_count_scapia_travel_spends_MTD':{
        'cell_reference':'F11',
         'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
               (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
        'is_epoch':True
    },
    'scapia_travel_spends_MTD':{
         'cell_reference':'G11',
         'query':f'''
                    SELECT ROUND((SUM(case when  txn_type <> 'ATM' AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) then txn_amount ELSE 0 END) - 
                    SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) AND txn_type='REFUND'
                    then txn_amount ELSE 0 END))/100000,2) AS total_amount
                    FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE(txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
     'unique_cards_count_scapia_travel_MTD':{
        'cell_reference':'H11',
         'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                    (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region ATM_TRANSACTIONS MTD
    'cards_count_for_atm_txns_MTD':{
        'cell_reference':'F12',
        'query':f'''
                    SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'atm_spends_MTD':{
        'cell_reference':'G12',
        'query':F'''
                    SELECT ROUND(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    'unique_cards_count_atm_MTD':{
        'cell_reference':'H12',
        'query':F'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
    # endregion

    # region repayments MTD
    'repayment_txns_count_MTD':{
        'cell_reference':'F13',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
      'repayment_amount_received_MTD':{
        'cell_reference':'G13',
        'query':f'''
                    SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },
      'repayment_unique_txns_count_MTD':{
        'cell_reference':'H13',
        'query':f''' SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE txn_type='REPAYMENT' AND  (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },
    # endregion

    # region calculating surcharge
    'surcharge_txns_count_MTD':{
        'cell_reference': 'F14',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND  (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
         'is_epoch':True
    },

       'surcharge_amount_MTD':{
        'cell_reference': 'G14',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
       'surcharge_unique_txns_count_MTD':{
        'cell_reference': 'H14',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
         'is_epoch':True
    },
    # endregion

    # region calculating fees MTD
    'fees_txns_count_MTD':{
        'cell_reference':'F15',
        'query':f''' SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                    ''',
        'is_epoch':True
    },
        'fees_amount_MTD':{
        'cell_reference':'G15',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
                ''',
        'is_epoch':True
    },
        'fees_unique_txns_count_MTD':{
        'cell_reference':'H15',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch >= '{start_time_epoch_mtd}' AND  txn_time_epoch <= '{end_time_epoch}')
            ''',
        'is_epoch':True
    },
    # endregion

    # region cards_issued_MTD
    'cards_issued_MTD':{
        'cell_reference':'F16',
        'query':f'''
                        SELECT  COUNT(t2.page_id) AS cards_count FROM card_customer_details t1
                        JOIN 
                        cards.loan_approval_workflow t2 ON
                        t1.scapia_customer_id = t2.internal_user_id 
                        WHERE (DATE(t1.updated_at) >='{start_date_mtd_str}' AND DATE(t1.updated_at) <='{end_time_regular}') AND 
                        page_id IN ('ONBOARDING_COMPLETED','CIF_POLLING','VIRTUAL_CARD_ACTV','SIM_BINDING','PHYSICAL_CARD_ACTV')
                    ''',
        'is_epoch':False
    },
    # endregion

    # region ntb# for MTD
    'ntb_percentage_MTD':{
        'cell_reference':'F17',
        'query':f'''
                        WITH cards_issued AS (
                        SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE (DATE(t1.updated_at) >='{start_date_mtd_str}' AND DATE(t1.updated_at) <='{end_time_regular}') AND 
                        (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    ntb_data AS (
                        SELECT count(internal_user_id) AS ntb_count 
                        FROM cards.workflow_docs t2
                        JOIN cards.card_customer_details ON card_customer_details.scapia_customer_id = t2.internal_user_id 
                        WHERE document_TYPE = 'CARD_INFO' AND (DATE(t2.updated_at) >='{start_date_mtd_str}' AND DATE(t2.updated_at) <='{end_time_regular}')AND JSON_EXTRACT(t2.document_details, '$.existingBankCustomerInfo.ddupeFlag') = "N"
                    )
                    SELECT  (ntb_count / cards_count) * 100 AS percentage
                    FROM cards_issued, ntb_data;
                ''',
                    'is_epoch':False
    },
    # endregion

   
    
    # region finding the count for the age 23-24_MTD
    'age_for_23_24_MTD':{
        'cell_reference':'F19',
        'query':f'''
                    SELECT
            SUM(
                IF(
                CASE 
                WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                ELSE YEAR(issued_date)-YEAR(dob)-1
                END in (23,24),1,0)) AS _count
            FROM
            (
            SELECT
                DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
            FROM workflow_docs as w 
            JOIN loan_approval_workflow as l 
            ON  l.workflow_type = 'card' AND 
                l.status = 'completed' AND 
                l.loan_approval_workflow_id = w.workflow_id 
                AND w.document_type = 'user_information'
            WHERE
                -- Add your WHERE condition for the issued date comparison here
                DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') >='{start_date_mtd_str}' and <='{end_time_regular}'
            ) t;
       ''',
        'is_epoch':False
    },
    # endregion
   
   
    
    # region active_cards_MTD
    'active_cards_for_MTD':{
         'cell_reference':'F21',
        'query':f''' 
                    SELECT COUNT(card_status) FROM cards.user_cards
                    WHERE (DATE(updated_at) >= '{start_date_mtd_str}' AND DATE(updated_at) <= '{end_time_regular}' ) AND card_status='ACTIVE'
                ''',
        'is_epoch':False
    },
    #endregion
    
# ------------------YTD-----------------------
    
    #region DOMESTIC POS TRANSACTIONS FOR YTD
    'domestic_pos_txns_count_YTD': {
        'cell_reference': 'I3',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND  txn_type='POS') and (txn_time_epoch <= '{end_time_epoch}') and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())''',
        'is_epoch': True
    },
    
     'domestic_pos_spends_in_lakhs_YTD': {
        'cell_reference': 'J3',
        'query': f'''
                    select 
                       Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                        SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)
                        AS POS_total 
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE iso_num_currency_code = 356 and  (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
         'is_epoch': True
    },

       'domestic_pos_unique_txns_count_YTD': {
        'cell_reference': 'K3',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='POS') and (txn_time_epoch <= '{end_time_epoch}' and YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
        'is_epoch': True
    },
    # endregion

    #region POS INTERNATIONAL TRANSACTIONS FOR YTD
    'international_pos_txns_count_YTD':{
        'cell_reference':'I4',
        'query':f'''SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
        'is_epoch': True
    },
    'international_pos_spends_in_lakhs_YTD':{
        'cell_reference':'J4',
        'query':f'''
            	SELECT 
                    Round((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) -
	                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
	                AS POS_total 
		        FROM cards.scapia_unbilled_card_txn_details
                WHERE  iso_num_currency_code <> 356  and (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
        ''',
        'is_epoch':True

    },
    'internationl_pos_unique_txns_count_YTD':{
        'cell_reference':'K4',
        'query':f'''SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code <> 356 AND txn_type='POS') and (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
        'is_epoch':True
    },
    # endregion

    # region DOMESTIC_ECOM_TRANSACTIONS_FOR_YTD
    'ecom_domestic_txns_count_YTD':{
        'cell_reference':'I6',
        'query': f'''SELECT COUNT(card_id) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
         'is_epoch':True
    },
    'ecom_doemstic_spends_in_lakhs_YTD':{
        'cell_reference':'J6',
        'query':f'''
                    SELECT 
                        round((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
	                    SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END ))/ 100000,2)
	                    AS ECOM_total 
		            FROM cards.scapia_unbilled_card_txn_details
                    WHERE  iso_num_currency_code = 356 AND 
                    (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    'ecom_domestic_txn_unique_count_YTD':{
        'cell_reference':'K6',
       'query': f'''SELECT COUNT(DISTINCT(card_id)) from cards.scapia_unbilled_card_txn_details WHERE (iso_num_currency_code = 356 AND txn_type='ECOM') and (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
       'is_epoch':True
    },
    # endregion

    # region ECOM_INTERNATIONAL_TRANSACTIONS_FOR_YTD
    'ecom_international_txns_count_YTD':{
        'cell_reference':'I7',
        'query':f'''
                    SELECT 
                    COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details 
                    WHERE  (iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
        'is_epoch':True
    },

    'ecom_international_spends_in_lakhs_YTD':{
        'cell_reference':'J7',
        'query':f'''
	                SELECT 
                            round((SUM(CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                            SUM(CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )) / 100000,2)
                            AS ECOM_total 
		                FROM cards.scapia_unbilled_card_txn_details
                            WHERE  iso_num_currency_code <> 356 AND 
                           (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },

    'ecom_international_txn_unique_count_YTD':{
        'cell_reference':'K7',
        'query':f'''
                    SELECT COUNT(DISTINCT(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE(iso_num_currency_code <> 356 AND  txn_type='ECOM') AND 
                       (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))''',
        'is_epoch':True
    },
    # endregion

    # region ECOM_TOTAL_YTD
    'pos_total_YTD':{
        'cell_reference':'J8',
        'query':f'''  
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE   txn_time_epoch <= '{end_time_epoch}' AND  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
            ''',
        'is_epoch':True
    },
    # endregion
      
    # region total_spends_current_date
        'total_spends_current_date':{
            'cell_reference':'J9',
            'query':f'''  
                    WITH pos_tots AS (
                    SELECT 
                    ROUND((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                    SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)  AS POS_TOTAL_DOMESTIC
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE   txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
                    ), ecom_tots AS (
                    SELECT 
                    ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                    (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                    SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS ECOM_TOTAL_DOMESTIC
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE   txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
                    )
                    SELECT SUM(POS_TOTAL_DOMESTIC + ECOM_TOTAL_DOMESTIC) FROM pos_tots, ecom_tots
                ''',
            'is_epoch':True
        },
        # endregion

    # region cards_count_unique_YTD
    'cards_count_YTD':{
        'cell_reference':'K9',
        'query':f''' 
                    select COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END )) +
                    COUNT(distinct( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) )+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END ))+
                    COUNT(distinct( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END ))
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE txn_time_epoch <= '{end_time_epoch}' and YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
                ''',
          'is_epoch':True
    },
    # endregion

    # region rewards_inelgible YTD
    'cards_count_for_reward_inelgible_YTD':{
        'cell_reference':'I10',
        'query':f'''
                        SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                        AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                        (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
         'is_epoch':True
    },

    'reward_inelgibile_YTD':{
        'cell_reference':'I11',
        'query':f'''
                        SELECT ROUND((SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) then txn_amount ELSE 0 END) - 
                        SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                        (iso_num_currency_code = 356 AND 
                        t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')) AND txn_type='REFUND'
                        then txn_amount ELSE 0 END))/100000,2)
                        FROM cards.scapia_unbilled_card_txn_details t1
                        WHERE(txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },

    'unique_cards_count_rewards_inelgible_YTD':{
        'cell_reference':'K11',
        'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE t1.mcc IN ('6513','6011','6540','8211','8220','8241','8244','8249','8299','8351','6051','6012','6011')  
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                    (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    # endregion

    # region scapia_travels YTD
    'cards_count_scapia_travel_spends_YTD':{
        'cell_reference':'I11',
         'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details t1
                WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
               (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
            ''',
        'is_epoch':True
    },
    'scapia_travel_spends_YTD':{
         'cell_reference':'J11',
         'query':f'''
                    SELECT ROUND((SUM(case when  txn_type <> 'ATM' AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) then txn_amount ELSE 0 END) - 
                    SUM(case when (txn_amount>20 AND txn_type <> 'ATM') AND 
                    (iso_num_currency_code = 356 AND 
                    (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')) AND txn_type='REFUND'
                    then txn_amount ELSE 0 END))/100000,2) AS total_amount
                    FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
     'unique_cards_count_scapia_travel_YTD':{
        'cell_reference':'K11',
         'query':f'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details t1
                    WHERE (t1.mid = '10000Qn8' OR t1.mid = '100000000000Qn8')
                    AND (txn_amount > 20 AND txn_type <> 'ATM' ) AND iso_num_currency_code = 356 AND 
                     (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    # endregion

    # region ATM_TRANSACTIONS YTD
    'cards_count_for_atm_txns_YTD':{
        'cell_reference':'I12',
        'query':f'''
                    SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    'atm_spends_YTD':{
        'cell_reference':'J12',
        'query':F'''
                    SELECT ROUND(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    'unique_cards_count_atm_YTD':{
        'cell_reference':'K12',
        'query':F'''
                    SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='ATM' AND (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
    # endregion

    # region repayments YTD
    'repayment_txns_count_YTD':{
        'cell_reference':'I13',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='REPAYMENT' AND  (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
            ''',
         'is_epoch':True
    },
      'repayment_amount_received_YTD':{
        'cell_reference':'J13',
        'query':f'''
                    SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='REPAYMENT' AND  (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
         'is_epoch':True
    },
      'repayment_unique_txns_count_YTD':{
        'cell_reference':'K13',
        'query':f''' SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                        WHERE txn_type='REPAYMENT' AND  (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
         'is_epoch':True
    },
    # endregion

    # region calculating surcharge
    'surcharge_txns_count_YTD':{
        'cell_reference': 'I14',
        'query':f'''
                SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND  (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
         'is_epoch':True
    },

       'surcharge_amount_YTD':{
        'cell_reference': 'J14',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
            ''',
         'is_epoch':True
    },
       'surcharge_unique_txns_count_YTD':{
        'cell_reference': 'K14',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='SURCHARGE' AND   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
            ''',
         'is_epoch':True
    },
    # endregion

    # region calculating fees YTD
    'fees_txns_count_YTD':{
        'cell_reference':'I15',
        'query':f''' SELECT COUNT(card_id) FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_type='FEES' AND   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                    ''',
        'is_epoch':True
    },
        'fees_amount_YTD':{
        'cell_reference':'J15',
        'query':f'''
                SELECT round(SUM(txn_amount)/100000,2) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
                ''',
        'is_epoch':True
    },
        'fees_unique_txns_count_YTD':{
        'cell_reference':'K15',
        'query':f'''
                SELECT COUNT(distinct(card_id)) FROM cards.scapia_unbilled_card_txn_details
                WHERE txn_type='FEES' AND   (txn_time_epoch <= '{end_time_epoch}' and  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW()))
            ''',
        'is_epoch':True
    },
    # endregion
    
    # region cards_issued_YTD
    'cards_issued_MTD_YTD':{
        'cell_reference':'I16',
        'query':f'''
                        SELECT  COUNT(t2.page_id) AS cards_count FROM card_customer_details t1
                        JOIN 
                        cards.loan_approval_workflow t2 ON
                        t1.scapia_customer_id = t2.internal_user_id 
                        WHERE (DATE(t1.updated_at)  <='{end_time_regular}' AND  YEAR(t1.updated_at)  = YEAR(NOW()))
                        and page_id IN ('ONBOARDING_COMPLETED','CIF_POLLING','VIRTUAL_CARD_ACTV','SIM_BINDING','PHYSICAL_CARD_ACTV')
                    ''',
        'is_epoch':False
    },
    # endregion

    # region ntb# for YTD
    'ntb_percentage_YTD':{
        'cell_reference':'I17',
        'query':f'''
                        WITH cards_issued AS (
                        SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE (DATE(t1.updated_at) <='{end_time_regular}' AND YEAR(t1.updated_at)  = YEAR(NOW()))
                       and (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    ntb_data AS (
                        SELECT count(internal_user_id) AS ntb_count 
                        FROM cards.workflow_docs t2
                        JOIN cards.card_customer_details ON card_customer_details.scapia_customer_id = t2.internal_user_id 
                         WHERE document_TYPE = 'CARD_INFO' AND  (DATE(t2.updated_at) <='{end_time_regular}' AND YEAR(t2.updated_at)  = YEAR(NOW())) AND JSON_EXTRACT(t2.document_details, '$.existingBankCustomerInfo.ddupeFlag') = "N"
                    )
                    SELECT  (ntb_count / cards_count) * 100 AS percentage
                    FROM cards_issued, ntb_data;   
                ''',
                    'is_epoch':False
    },
    # endregion
    
    # region avg_credit_Card_limit_YTD
     'average_credit_card_limit_YTD':{
        'cell_reference':'I18',
        'query':f''' 
                   SELECT AVG(t2.card_limit) FROM cards.user_cards t1
                    JOIN cards.card_details t2 ON t1.scapia_customer_id = t2.scapia_customer_id
                    WHERE t1.card_status='ACTIVE' AND (DATE(t1.created_at)<='{end_time_regular}' and YEAR(t1.created_at)  = YEAR(NOW()))
                ''',
        'is_epoch':False

    },
    # endregion

    # region finding the count for the age 23-24_YTD
    'age_for_23_24_MTD':{
        'cell_reference':'I19',
        'query':f'''
                    SELECT
            SUM(
                IF(
                CASE 
                WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                ELSE YEAR(issued_date)-YEAR(dob)-1
                END in (23,24),1,0)) AS _count
            FROM
            (
            SELECT
                DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
            FROM workflow_docs as w 
            JOIN loan_approval_workflow as l 
            ON  l.workflow_type = 'card' AND 
                l.status = 'completed' AND 
                l.loan_approval_workflow_id = w.workflow_id 
                AND w.document_type = 'user_information'
            WHERE
                -- Add your WHERE condition for the issued date comparison here
                DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') <='{end_time_regular}' and YEAR(l.updated_at)  = YEAR(NOW())
            ) t;
       ''',
        'is_epoch':False
    },
    # endregion

    # region percentage of age2324_MTD
    'age_avg_23_24_MTD':{
        'cell_reference':'I20',
        'query':f'''
                    WITH cards_cout AS (
                    SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE ( DATE(t1.updated_at) <='{end_time_regular}' AND YEAR(t1.updated_at)  = YEAR(NOW()) ) and
                        (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    cards_23_24 AS (
                    SELECT
                    SUM(
                        IF(
                        CASE 
                        WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                        ELSE YEAR(issued_date)-YEAR(dob)-1
                        END in (23,24),1,0)) AS _count
                    FROM
                    (
                    SELECT
                        DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                        l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
                    FROM workflow_docs as w 
                    JOIN loan_approval_workflow as l 
                    ON  l.workflow_type = 'card' AND 
                        l.status = 'completed' AND 
                        l.loan_approval_workflow_id = w.workflow_id 
                        AND w.document_type = 'user_information'
                    WHERE
                        -- Add your WHERE condition for the issued date comparison here
                        DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') <='{end_time_regular}' and  YEAR(l.updated_at)  = YEAR(NOW())
                    ) t
                    )

                    SELECT  (_count/cards_count)*100 FROM cards_cout,cards_23_24
                '''  ,
                'is_epoch':False
    },
    # endregion

    # region POS total_current_date
    'pos_total_current_date':{
        'cell_reference':'D5',
        'query':f''' 
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END ) - 
                SUM( CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END ))/100000,2)  
                FROM cards.scapia_unbilled_card_txn_details
                WHERE  txn_time_epoch >= '{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}'
            ''',
        'is_epoch':True
    },
    # endregion
    
    # region cards_count_current_date
    'cards_count_current_date':{
        'cell_reference':'C9',
        'query':f''' 
                    select COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END )+
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END )
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE  txn_time_epoch >='{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}'
                ''',
          'is_epoch':True
    },
    # endregion

     # region cards_count_MTD
    'cards_count_MTD':{
        'cell_reference':'F9',
        'query':f''' 
                    select COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END )+
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END )
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE  txn_time_epoch >='{start_time_epoch}' AND  txn_time_epoch <= '{end_time_epoch}'
                ''',
          'is_epoch':True
    },
    # endregion
    
     # region cards_count_YTD
    'cards_count_YTD':{
        'cell_reference':'I9',
        'query':f''' 
                    select COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code = 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='POS'  AND iso_num_currency_code <> 356 Then card_id END ) +
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code <> 356 Then card_id END )+
                    COUNT( CASE WHEN txn_type='ECOM'  AND iso_num_currency_code = 356 Then card_id END )
                    FROM cards.scapia_unbilled_card_txn_details
                        WHERE  txn_time_epoch <= '{end_time_epoch}' and YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
                ''',
          'is_epoch':True
    },
    # endregion

    # region ECOM_TOTAL_YTD
    'pos_total_YTD':{
        'cell_reference':'J5',
        'query':f'''  
                SELECT 
                ROUND((SUM( CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END ) -
                (SUM( CASE WHEN txn_type='REFUND' Then txn_amount ELSE 0 END )+
                SUM( CASE WHEN txn_type='ECOM_REVERSAL' THEN txn_amount ELSE 0 END )))/100000,2)  AS POS_TOTAL_DOMESTIC
                FROM cards.scapia_unbilled_card_txn_details
                WHERE   txn_time_epoch <= '{end_time_epoch}' AND  YEAR(FROM_UNIXTIME(txn_time_epoch / 1000))  = YEAR(NOW())
            ''',
        'is_epoch':True
    },
    # endregion
    
    # ----------------- from inception-------------------
    
    # region avg_card_limit_MTD
       'average_credit_card_limit_MTD':{
        'cell_reference':'F18',
        'query':f''' 
                   SELECT AVG(t2.card_limit) FROM cards.user_cards t1
                    JOIN cards.card_details t2 ON t1.scapia_customer_id = t2.scapia_customer_id
                    WHERE t1.card_status='ACTIVE' AND DATE(t1.created_at) >='{start_time_regular}' AND DATE(t1.created_at) <='{end_time_regular}'
                ''',
        'is_epoch':False
    },
    # endregion
    
    # region caluclating the ENR FROM THE INCEPTION
    'calculating the ENR':{
        'cell_reference':'C23',
        'query':f'''
                    SELECT enr FROM (
                    SELECT 
                        ROUND((SUM(CASE WHEN txn_type='POS' THEN txn_amount ELSE 0 END) + 
                        SUM(CASE WHEN txn_type='ECOM' THEN txn_amount ELSE 0 END) - 
                        (
                            SUM(CASE WHEN txn_type='POS_REVERSAL' THEN txn_amount ELSE 0 END) +
                            SUM(CASE WHEN txn_type= 'ECOM_REVERSAL' THEN txn_amount ELSE 0 END) +
                            SUM(CASE WHEN txn_type='REFUND' THEN txn_amount ELSE 0 END) +
                            SUM(CASE WHEN txn_type='REPAYMENT' THEN txn_amount ELSE 0 END) 
                        ))/100000,2) AS enr
                    FROM cards.scapia_unbilled_card_txn_details
                    WHERE txn_time_epoch <='{end_time_epoch}'
                ) AS subquery;
            ''',
         'is_epoch':True
    },
    # endregion
 
    # region calculating the CIF we always calculate from the inception
    'CIF_from_incpetion':{
        'cell_reference':'C22',
        'query':f'''
            WITH active_cards AS (	
            SELECT  COUNT(t2.page_id) AS cards_count FROM card_customer_details t1
            JOIN 
            cards.loan_approval_workflow t2 ON
            t1.scapia_customer_id = t2.internal_user_id 
            WHERE DATE(t1.updated_at) <='{end_time_regular}' AND 
            page_id IN ('ONBOARDING_COMPLETED','CIF_POLLING','VIRTUAL_CARD_ACTV','SIM_BINDING','PHYSICAL_CARD_ACTV')
            ), closed_cards AS (
            SELECT COUNT(*) AS closed FROM cards.close_card_request
            ) SELECT (cards_count- closed) AS active_cards_count FROM active_cards, closed_cards
        ''',
         'is_epoch':False
    },
    # endregion

    # region percentage of age2324_MTD
    'age_avg_23_24_MTD':{
        'cell_reference':'F20',
        'query':f'''
                    WITH cards_cout AS (
                    SELECT COUNT(t2.page_id) AS cards_count 
                        FROM card_customer_details t1
                        JOIN cards.loan_approval_workflow t2 ON t1.scapia_customer_id = t2.internal_user_id 
                        WHERE (DATE(t1.updated_at) >='{start_time_regular}' AND DATE(t1.updated_at) <='{end_time_regular}') and
                        (page_id = 'ONBOARDING_COMPLETED' OR page_id = 'CIF_POLLING' OR page_id = 'SIM_BINDING' OR page_id = 'VIRTUAL_CARD_ACTV' OR page_id = 'PHYSICAL_CARD_ACTV')
                    ),
                    cards_23_24 AS (
                    SELECT
                    SUM(
                        IF(
                        CASE 
                        WHEN date_format(t.issued_date,'%m%d') >= date_format(t.dob,'%m%d') THEN YEAR(issued_date)-YEAR(dob)
                        ELSE YEAR(issued_date)-YEAR(dob)-1
                        END in (23,24),1,0)) AS _count
                    FROM
                    (
                    SELECT
                        DATE_FORMAT(JSON_UNQUOTE(JSON_EXTRACT(w.document_details,'$.userPersonalInfo.customerDob')),'%Y-%m-%d') as dob,
                        l.status, DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') as issued_date
                    FROM workflow_docs as w 
                    JOIN loan_approval_workflow as l 
                    ON  l.workflow_type = 'card' AND 
                        l.status = 'completed' AND 
                        l.loan_approval_workflow_id = w.workflow_id 
                        AND w.document_type = 'user_information'
                    WHERE
                        -- Add your WHERE condition for the issued date comparison here
                        DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') >= '{start_time_regular}' and DATE_FORMAT(convert_tz(l.updated_at,'+00:00','+05:30'),'%Y-%m-%d') <='{end_time_regular}'
                    ) t
                    )

                    SELECT  (_count/cards_count)*100 FROM cards_cout,cards_23_24
                '''  ,
                'is_epoch':False
    },
    # endregion

# region Active_cards_YTD
'active_cards_YTD':{
    'cell_reference': 'I21',
    'query':f'''
           SELECT COUNT(card_status) FROM cards.user_cards 
                WHERE card_status='ACTIVE' AND (DATE(created_at)<='{end_time_regular}' and YEAR(created_at)  = YEAR(NOW()))
            ''',
     'is_epoch':False
}
# endregion

}
   
