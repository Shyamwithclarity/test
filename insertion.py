def updatediamondNivoda():
    timezone.activate('Asia/Calcutta')
    now = timezone.now()
    diamondObj = DiamondClass()
    csv_filename = ""
    # remaing code
    file_list = ["withclarity-nivoda.csv", "withclarity-2-nivoda.csv"]
    
                    # ftp.cwd('/Test')
                    # CSVlist = ftp.nlst()
                    # if len(CSVlist) > 0:
                    #     for fs in CSVlist:
                    #         if "withclarity-nivoda.csv" in str(fs).strip().lower():
                    #             csv_filename = str(fs).strip()
                    #             break
    file_list = ["withclarity-natural-2-nivoda", "withclarity-natural-nivoda.csv"]
                    
    for x in file_list:
        file = open(str(diamondObj.getBaseDirPath()) + "/static/diamond_files/nivoda_diamond_csv/"+str(x), 'wb')
        file.write
        file.close()

        
    fold_file_list = [str(diamondObj.getBaseDirPath()) + "/static/withclarity_server_uploaded_file/withclarity-natural-nivoda.csv",
                                 str(diamondObj.getBaseDirPath()) + "/static/withclarity_server_uploaded_file/withclarity-natural-2-nivoda.csv"]

    df = pd.concat(map(pd.read_csv, fold_file_list), axis=0, ignore_index=True)
    df.to_csv(str(diamondObj.getBaseDirPath()) + "/static/withclarity_server_uploaded_file/nivoda.csv")
        
    err_msg = ""
    start_time = datetime.now()
    try:
        db_connection = sql.connect(host='127.0.0.1', database='wwwvportal_vendor_live', user='wwwvportal_vlive', password='Vlive@2023')
    except:
        return False
    cursor = db_connection.cursor()
    shape_dict = {"ASSCHER": "Asscher", "AS": "Asscher", "SQEM": "Asscher", "SEM": "Asscher",
                                      "CUSHION B": "Cushion", "CUSHION": "Cushion", "CU": "Cushion", "CUBR": "Cushion", "CUMBR": "Cushion","CMB": "Cushion","CMB-N": "Cushion",
                                      "CB": "Cushion", "CM": "Cushion", "CMB": "Cushion",
                                       "Cushion BRI": "Cushion", "CUSHION MB": "Cushion","SQ.CMB": "Cushion", "Cushion MLG": "Cushion",
                                      "HEART": "Heart","EMERALD": "Emerald","SQ EMERALD": "Emerald", "EM": "Emerald", "PEAR": "Pear", "PS": "Pear",
                                      "PEARS": "Pear","MQ": "Marquise","MARQUISE": "Marquise",
                                      "PRINCESS": "Princess", "PR": "Princess", "SMB": "Princess",
                                      "SQUARE MODIFIED BRILLIANT": "Princess",
                                      "RADIANT": "Radiant", "RA": "Radiant", "SQ RADIANT": "Radiant", "RMB": "Radiant", "L RADIANT": "Radiant","SQRA": "Radiant",
                                      "RECTANGULAR MODIFIED BRILLIANT": "Radiant",
                                      "OVAL": "Oval", "OV": "Oval", "ROUND": "Round","RD": "Round","RMB": "Round", "RB": "Round", "BR": "Round",
                                      "RBC": "Round", "MARQUISE": "Marquise", "MQ": "Marquise", "PRIN": "Princess", "HE": "Heart"}
    
    flour_dict = {"N": "None", "F": "Faint", "M": "Medium", "S": "Strong","NON": "None", "FNT": "Faint", "MED": "Medium", "STG": "Strong","NONE": "None", "FA": "Faint", "MD-BL": "Medium", "ST-BL": "Strong"}

    regular_color_codes_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

    fancy_diamond_colors_list = []
    fluoroscence_colors_list = ['Blue', 'Yellow', 'Green', 'Red', 'Orange', 'White']
    fancy_diamond_color_intensity_list = []

    diamond_cuts_list = ['Excellent', 'Very Good', 'Good','']
    labgrown_diamond_cuts_list = ['Ideal', 'Excellent', 'Very Good', 'Good']
    diamond_clarity_list = ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1']
    diamond_fluoroscence_list = ['None', 'Faint', 'Medium', 'Strong']
    diamond_polish_list = ['Fair', 'Excellent', 'Very Good', 'Good']
    diamond_symmetry_list = ['Fair', 'Excellent', 'Very Good', 'Good']
    diamond_labs_list = ['GIA', 'IGI']

    diamond_carat_min = 0.25
    diamond_carat_max = 10.00
    diamond_price_min = 100
    diamond_price_max = 1000000

    diamond_depth_min = 40
    diamond_depth_max = 90

    diamond_table_min = 40
    diamond_table_max = 90

    diamond_min_ratio = 0.9
    diamond_max_ratio = 2.75

    polish_dict = {"EX": "Excellent", "GD": "Good", "VG": "Very Good", "G": "Good", "F": "Fair", "FR": "Fair",
                   "E": "Excellent", "Good": "Good", "Excellent": "Excellent", "X": "Excellent",
                   "Very Good": "Very Good"}

    symmetry_dict = {"EX": "Excellent", "GD": "Good", "VG": "Very Good", "G": "Good", "F": "Fair", "FR": "Fair",
                     "E": "Excellent",
                     "Good": "Good", "Excellent": "Excellent", "X": "Excellent", "Very Good": "Very Good"}

    
    mega_query_list = []
    bunch_query = ""
    query_string_count = 0

    tot_insert_diamonds_sec = 0
    mega_query_list_sec = []
    bunch_query_sec = ""
    query_string_count_sec = 0
    total_diamonds_near = 0
    tot_insert_diamonds = 0

    tot_delete_diamonds = 0

    fixed_insert_query = getfixedinsertqueryquery()
    fixed_second_insert_query = getfixedsecondinsertqueryquery()
    csv_file=str(diamondObj.getBaseDirPath() + "/static/withclarity_server_uploaded_file/nivoda.csv")
    # csv_file = "static/diamond_files/natural/natural_custon_diamond.csv"
    # csv_file = csv_file
    used_diamond_list = []
    supplier_id = ""

    usd_gbp_currency = getUsdTOGbpCurrency()
    usd_cad_currency = getUsdTOcanadianCurrency()
    supplierid = 128
    markuptype = "Natural"
    sold_diamonds_ids_list = getSoldDiamondsIdsList()
    saved_diamonds_cert_list = getSavedDiamondsCertListByFeed(supplierid)
    prev_sold_diamonds = []
    already_save_certi_list = []
    invalid_price_list = []
    invalid_ratio_list = []
    csv_markup_list = getMarkupValues(supplierid, markuptype)
    prssess_count = 0
    er_t = ""
    bulk_row_query  = "shyam"
    mega_query_list.append(bulk_row_query)
    
    try:
        mega_query_list = []
        bunch_query = ""
        query_string_count = 0

        tot_insert_diamonds_sec = 0
        mega_query_list_sec = []
        bunch_query_sec = ""
        query_string_count_sec = 0
        total_diamonds_near = 0
        tot_insert_diamonds = 0

        tot_delete_diamonds = 0
        
        for chunk in pd.read_csv(csv_file, chunksize=5000):
            
            f = open('static/logs/nivoda_natural_log.txt', 'a')
            
            dft = chunk.to_dict('records')
            
            
            
            diamond_details_list = []
            for at in dft:
                
                at = {
                    key.replace(' ', ''): value for key, value in at.items()
                }
               
                
                diamond_details_list.append(dict((k.lower(), v) for k, v in at.items()))

            print(len(diamond_details_list), datetime.now().strftime("%X"))
            total_diamonds_near += len(diamond_details_list)
            prssess_count += 1
            f.write("From csv data set "+ str(prssess_count) + ". " + str(len(diamond_details_list))+" Record filter process started "+str(datetime.now().strftime("%X"))+ ".\n")
            ld = [d.get('reportno', None) for d in diamond_details_list]
            jlist = list(set(saved_diamonds_cert_list) & set(ld))
            
            for res in diamond_details_list:
                res['price']=round(Decimal(str(res['price']).strip().replace(",", "")), 0)
                
                is_allow_cut, is_allow_ratio, is_allow_price = True, True, True
                isdigit_price_per_carat = isPureDigits(str(res['price']).strip())
                           
                if(str(res['reportno']) == ""):
                    continue

                diamond_id = str(res['reportno']).strip(".0").replace("LG", "").replace("GIA", "").replace("GIA ", "")
                
                if diamond_id.startswith("GIA"):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                if diamond_id.startswith("0."):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                
                if str(res['shape']).strip().upper() in shape_dict.keys():
                    shape = diamondObj.getDiamondShapeName(shape_dict[str(res['shape'].strip().upper())])
                else:
                    shape = diamondObj.getDiamondShapeName(res['shape']).strip().upper()
                
                color = str(res['col']).strip().replace("+", "").replace("-", "").upper()
                
                if(str(color) == "FANCY" or str(color) == "JMMIX" or str(color) == "LMMIX" or str(color) == "L(DBR)" or str(color) == "L(LBR)" or str(color) == "H(LBR)" or str(color) == "G(FBR)" or str(color) == "F(FBR)"  or str(color) == "E(FBR)"   or str(color) == "H(FBR)"  or str(color) == "I(FBR)" or str(color) == "L(BR)" or str(color) == "EFMIX"  or str(color) == "FFMIX" or str(color) == "KMMIX" or str(color) == "LLMIX" or str(color) == "HMMIX" or str(color) == "E(BR)" or str(color) == "JFMIX" or str(color) == "GFMIX"  or str(color) == "HFMIX" or str(color) == "I(LBR)" or str(color) == "I(LBR)" or str(color) == "IFMIX" or str(color) == "ILMIX" or str(color) == "J(FBR)" or str(color) == "J(LBR)" or str(color) == "JLMIX" or str(color) == "K(FBR)" or str(color) == "K(LBR)" or str(color) == "K(MBR)" or str(color) == "KFMIX" or str(color) == "KLMIX" or str(color) == "L(FBR)" or str(color) == "L(MBR)" or str(color) == "LFMIX" or str(color) == "GMMIX" or str(color) == "HLMIX" or str(color) == "I(MBR)"):
                    continue
                clarity = str(res['clar']).strip().replace("+", "").replace("-", "").upper()
                carat_weight = round(Decimal(str(res['carats']).strip()), 2)
                
                
                if str(res['lab']).strip().upper() != "GIA":
                    continue
                lab = str(res['lab'])  
                if str(res['pol']).strip() != "-" or str(res['pol']).strip() != "NA" or str(
                        res['pol']).strip() != "":
                    polish = polish_dict[str(res['pol']).strip().upper()]
                if str(res['symm']).strip() != "-" or str(res['symm']).strip() != "NA" or str(
                        res['symm']).strip() != "":
                    symmetry = symmetry_dict[str(res['symm']).strip().upper()]
                
                if str(res['flo']).strip().upper() in flour_dict.keys():
                    
                    flour_intensity = diamondObj.getFluorscenceName(flour_dict[str(res['flo'].strip().upper())])
                    
                else:
                    flour_intensity = str(res['flo']).strip().title()
                

                # symmetry = getSymmetryName(res['symmetry'])
                dept_perc = round(Decimal(str(res['depth']).strip().replace("%", "")), 1)
                table_perc = round(Decimal(str(res['table']).strip().replace("%", "")), 1)  
                #cuts_value = getCutsName(res['cut'])
                #portion
                cut_name=res['cut']
                
                #End portion
                cut = "Excellent"
                #catch here
                rapaport_price = ""
                perc_off_rap = ""
                certificate_number = str(res['reportno']).strip("").replace("LG", "").replace("GIA", "").replace(".0", "0")
                if certificate_number.startswith("GIA"):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                if certificate_number.startswith("0."):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                if certificate_number in list(jlist):
                    saved_cert_price_range = getSavedcertpriceRange(certificate_number,
                                                                               original_total_price)
                    if saved_cert_price_range == 0:
                        already_save_certi_list.append(certificate_number)
                        continue
                    elif saved_cert_price_range == 1:
                        cursor.execute(
                            """select `diamond_id` from `{0}diamond_details_primary` where `certificate_number` = '{1}'""".format(
                                table_prefix,
                                str(certificate_number)))
                        diamond_result = cursor.fetchone()
                        cursor.execute(
                            """delete from `{0}diamond_details_primary` where `certificate_number` = '{1}'""".format(
                                table_prefix,
                                str(certificate_number)))
                        cursor.execute(
                            """delete from `{0}diamond_details_secondary` where `diamond_id` = '{1}'""".format(
                                table_prefix,
                                str(diamond_result[0])))
                #Measurement=res['measurement']
                
                # Measurement=Measurement.replace('-', '*')
                # Measurement=Measurement.replace('x', '*')
                # Measurement=Measurement.replace('X', '*')
                # Measurement=Measurement.split('*')
                length=res['length']
                width=res['width']
                depth=res['height']
                measurements=str(length) + "x" + str(width) + "x" + str(depth)
                
                if str(length) != "" and str(width) != "" and str(depth) != "":
                    measurement = str(length).strip() + "x" + str(
                        width).strip() + "x" + str(
                        depth).strip()

                ratio = 0 
                if length != "" and width != "" and str(width) != "0" and str(length).strip() != "nan" and str(
                        width).strip() != "nan" and str(width).strip() != "nan":
                    
                    try:
                        # ratio = round(Decimal(length) / Decimal(width_val), 2)
                        ratio = Decimal(length) / Decimal(width)
                        
                        split_ratio = str(ratio).split(".")
                        if len(split_ratio) == 1:
                            ratio = Decimal(str(split_ratio[0]))
                        else:
                            ratio = Decimal(str(split_ratio[0]) + "." + str(split_ratio[1])[0:2])
                    except:
                        width_val = 0
                
                if str(ratio).strip() != "" or str(ratio).strip().lower() != "nan":
                    if Decimal(str(diamond_min_ratio)) <= Decimal(str(ratio)) <= Decimal(str(diamond_max_ratio)):
                        is_allow_ratio = True
                else:
                    is_allow_ratio = False
                    invalid_ratio_list.append(diamond_id)
                    continue
                
                fancy_color = ""
                fancy_color_intensity = ""
                fancy_color_overtone = ""
                desc_comments = ""  # str(res['description/comments']).strip().replace("\r\n", ",")

                memo_status = ""

                inscription = ""
                location = "USA"
                if str(res['reportno']).startswith("GIA"):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                if str(res['reportno']).startswith("0."):
                    # skip the row if diamond_id starts with "GIA"
                    continue
                CertNo=round(float(res['reportno']))
                certno= CertNo
                stockno=int(certno)+914320
                 
                certificate_file = str(res['pdf'])
                diamond_image = str(res['image'])
                diamond_video = str(res['video'])
                price = round(Decimal(str(res['price']).strip()) / Decimal(carat_weight), 2)
                price_per_ct = round(price, 2)
                original_total_price = str(res['price']).strip()

                exchange_rate = 0
                convert_price = ""
                plus_markup_price = round(
                    Decimal(getTotalPriceWithMarkup(carat_weight, original_total_price, csv_markup_list, markuptype)),
                    2)
                final_price = round(Decimal(plus_markup_price), 2)
                plus_markup_price_ct = round(Decimal(
                    getPricepercaretWithMarkup(carat_weight, original_total_price, round(Decimal(price_per_ct), 2),
                                               csv_markup_list, markuptype)), 2)
                is_allow_price = diamondObj.isAllowDiamondPrice(plus_markup_price)
                
                if is_allow_price == False:
                    invalid_price_list.append(diamond_id)
                    continue

                price_per_ct_eur = 0
                original_total_price_eur = 0
                final_price_eur = 0
                plus_markup_price_ct_eur = 0

                exchange_rate_pound = usd_gbp_currency
                price_per_ct_pound = round(Decimal(price_per_ct) * Decimal(exchange_rate_pound), 2)
                plus_markup_price_ct_pound = round(Decimal(plus_markup_price_ct) * Decimal(exchange_rate_pound), 2)
                original_total_price_pound = round(Decimal(original_total_price) * Decimal(exchange_rate_pound), 2)
                final_price_pound = round(Decimal(final_price) * Decimal(exchange_rate_pound), 2)

                exchange_rate_cad = usd_cad_currency
                price_per_ct_cad = round(Decimal(price_per_ct) * Decimal(exchange_rate_cad), 2)
                plus_markup_price_ct_cad = round(Decimal(plus_markup_price_ct) * Decimal(exchange_rate_cad), 2)
                original_total_price_cad = round(Decimal(original_total_price) * Decimal(exchange_rate_cad), 2)
                final_price_cad = round(Decimal(final_price) * Decimal(exchange_rate_cad), 2)

                availability = "Available"

                girdle = ""

                girdle_min = ""
                girdle_max = ""

                # if girdle != "":
                #     split_girdle = str(girdle).lower().split("to")
                #     girdle_min = str(split_girdle[0]).strip().capitalize()
                #     if len(split_girdle) > 1:
                #         girdle_max = str(split_girdle[1]).strip().capitalize()

                girdle_perc = ""
                girdle_condition = ""
                culet = ""
                culet_condition = ""
                crown_angle = ""
                crown_height = ""

                pavilion_depth = ""
                pavilion_angle = ""

                origin = ""  # str(res['origin']).strip()
                seller_name = 'Nivoda'
                city = 'NewYork'
                state = ""
                country = "USA"
                is_match_pair_separable = ""
                member_comments = ""
                supplier_country = ""
                diamond_quantity = 1
                milky = "NA"  # diamondObj.getmilky(str(res['milky']).strip())

                fluorescence_color = ""
                shade = ""
                eye_clean = "NA"  # diamondObj.geteyeclean(str(res['eye clean']).strip())
                treatment = "NA"  # diamondObj.gettretment(str(res['treatment']).strip())
                cert_comment = ""
                key_to_symbols = ""
                white_inclusion = ''
                black_inclusion = ''
                open_inclusion = ''

                diamond_type = 'white'
                supplier_id = 128
                data_entry_point = "csv"
                created_at = datetime.now()
                updated_at = datetime.now()
                stock_number = certificate_number
                show_diamond = 1
                quick_ship = 'N'
                appointment = 'N'
                
                if is_allow_cut and is_allow_price and is_allow_ratio:
                    insert_query = getinsertquery(diamond_id, shape, color, clarity,
                                                  carat_weight, lab, cut, polish, symmetry, flour_intensity,
                                                  rapaport_price,
                                                  perc_off_rap,
                                                  certificate_number, measurement, length, width, depth, ratio,
                                                  dept_perc,
                                                  table_perc,
                                                  fancy_color, fancy_color_intensity, fancy_color_overtone,
                                                  price_per_ct,
                                                  original_total_price, exchange_rate, convert_price,
                                                  plus_markup_price_ct,
                                                  plus_markup_price, final_price, price_per_ct_eur,
                                                  plus_markup_price_ct_eur,
                                                  original_total_price_eur, final_price_eur, exchange_rate_pound,
                                                  price_per_ct_pound, plus_markup_price_ct_pound,
                                                  original_total_price_pound,
                                                  final_price_pound, exchange_rate_cad, price_per_ct_cad,
                                                  plus_markup_price_ct_cad,
                                                  original_total_price_cad, final_price_cad,
                                                  certificate_file, diamond_image, diamond_video,
                                                  availability, diamond_quantity, diamond_type, supplier_id,
                                                  data_entry_point,
                                                  created_at,
                                                  updated_at, stock_number, show_diamond)

                    insert_sec_query = getinsertsecquery(diamond_id, desc_comments,
                                                         memo_status, inscription, location, girdle, girdle_min,
                                                         girdle_max,
                                                         girdle_perc,
                                                         girdle_condition, culet, culet_condition, crown_angle,
                                                         crown_height,
                                                         pavilion_depth,
                                                         pavilion_angle, origin, seller_name, city, state, country,
                                                         is_match_pair_separable,
                                                         member_comments, supplier_country, milky, fluorescence_color,
                                                         shade,
                                                         eye_clean, treatment,
                                                         cert_comment, key_to_symbols, white_inclusion, black_inclusion,
                                                         open_inclusion, quick_ship,
                                                         appointment, supplier_id)

                bunch_query += insert_query + ",\n"
                
                query_string_count += 1
                tot_insert_diamonds += 1

                bunch_query_sec += insert_sec_query + ",\n"
                
                query_string_count_sec += 1
                tot_insert_diamonds_sec += 1

                used_diamond_list.append(
                    str(diamond_id))  # Appending diamond id, to prevent from duplicates
                
                if query_string_count == 5000:
                    bulk_row_query = str(fixed_insert_query) + bunch_query.strip().rstrip(
                        ",") + ";"  # rstrip(",") this isused to remove last comma from query
                    
                    mega_query_list.append(bulk_row_query)
                    
                    bunch_query = ""
                    query_string_count = 0

                if query_string_count_sec == 5000:
                    bulk_row_query_sec = str(fixed_second_insert_query) + bunch_query_sec.strip().rstrip(
                        ",") + ";"  # rstrip(",") this isused to remove last comma from query

                    mega_query_list_sec.append(bulk_row_query_sec)
                    bunch_query_sec = ""
                    query_string_count_sec = 0
               
            f.close()
        print(mega_query_list)    
        # If querys count not reach to 5000 then generate query
        
        if bulk_row_query != "":
                bulk_row_query = str(fixed_insert_query) + bunch_query.strip().rstrip(
                        ",") + ";"  # rstrip(",") this isused to remove last comma from query
                mega_query_list.append(bulk_row_query)
                bunch_query = ""

                # If querys count not reach to 5000 then generate query
        if bulk_row_query != "":
                bulk_row_query_sec = str(fixed_second_insert_query) + bunch_query_sec.strip().rstrip(
                        ",") + ";"  # rstrip(",") this isused to remove last comma from query
                mega_query_list_sec.append(bulk_row_query_sec)
                bunch_query_sec = ""
            
        
        if len(mega_query_list) > 0 and len(mega_query_list_sec) > 0:
            query = """ select count(*) FROM `{0}diamond_details_primary`AS dd
                        JOIN {0}diamond_details_secondary AS t2
                        ON dd.diamond_id = t2.diamond_id  AND dd.`supplier_id` = t2.`supplier_id` WHERE dd.`supplier_id`='{1}' 
                        AND t2.`supplier_id`= '{1}' """.format(table_prefix, supplier_id)
            cursor.execute(query)
            tot_delete = cursor.fetchone()
            tot_delete_diamonds = int(tot_delete[0])

            query = """ DELETE  dd, t2 FROM `{0}diamond_details_primary`AS dd
            JOIN {0}diamond_details_secondary AS t2
            ON dd.diamond_id = t2.diamond_id  AND dd.`supplier_id` = t2.`supplier_id` WHERE dd.`supplier_id`='{1}'
            AND t2.`supplier_id`= '{1}' """.format(table_prefix, supplier_id)
            cursor.execute(query)
            print(query)
            db_connection.commit()

        
        # Insert Query data to Database
        if len(mega_query_list) > 0:
            for query_res in mega_query_list:
                query = str(query_res)
                
                cursor.execute(query)
                db_connection.commit()

        # Insert Query data to Database
        if len(mega_query_list_sec) > 0:
            for query_res_sec in mega_query_list_sec:
                query_sec = str(query_res_sec)
                cursor.execute(query_sec)
                db_connection.commit()



        print("end time", datetime.now())
        if len(already_save_certi_list) > 0:
            err_msg += str(len(already_save_certi_list)) + "Diamonds Skipped due to certificate no. already available " \

        if len(invalid_price_list) > 0:
            err_msg += str(len(invalid_price_list)) + " Diamonds skipped due to price is not in range\n"

        if len(invalid_ratio_list) > 0:
            err_msg += str(len(invalid_ratio_list)) + " Diamonds skipped due to ratio is not in range\n"

        if len(prev_sold_diamonds) > 0:
            err_msg += str(len(prev_sold_diamonds)) + " Diamonds are already sold\n"
        api_response = "ok"
    except Exception as ex:
        err_msg = ex
        er_t = ex
        api_response = "error"
    end_time = datetime.now()
    details = {'supp_id': supplierid, 'action': "Nivoda Natural CSV", 'api_resp': api_response,
               'total_diamonds': total_diamonds_near,
               'total_insert_diamond': tot_insert_diamonds, 'total_deleted_diamond': str(tot_delete_diamonds),
               'total_updated_diamond': 0,
               'error_msg': err_msg, 'diamond_entry': "custom CSV", 'start_time': start_time, 'end_time': end_time}
    # print(details)
    diamondObj.generateLog(details)
    f = open('static/logs/nivoda_natural_log.txt', 'a')

    f.write("Total CSV diamonds = " + str(total_diamonds_near) + ", Inserted diamonds = " + str(tot_insert_diamonds) + ", total deleted diamond = " + str(tot_delete_diamonds) +"\n")
    f.write("Issues found : " + str(err_msg) + "\n")
    f.close()
    return details
