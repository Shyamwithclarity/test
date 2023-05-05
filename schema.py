 def resolve_live_sold_new_diamond(root, info, diamond_id=None, order_id=None ):
        activeapiObj = """select * from `{0}api_details` where api_name = 'Find diamond by id' and is_active = 1""".format(
             table_prefix)
        cursor = connections['primary'].cursor()
        enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            diamond_details = []
            try:
                status = ""
                code = ""
                message = ""
                diamo_list = list(str(diamond_id).strip().replace(', ', ',').split(","))
                diam_data = [string for string in diamo_list if string != ""]
                ord_list = list(str(order_id).strip().replace(', ', ',').split(","))
                ord_data = [string for string in ord_list if string != ""]

                diamond_sold_list = []

                # fillter diamond which already sold
                update_only_is_sold = []
                sold_diamond_is_not_sold_list = SoldDiamonds.objects.using('primary').filter(
                    diamond_id__in=diam_data, is_sold=1)
                for diam in sold_diamond_is_not_sold_list:
                    update_only_is_sold.append(diam.diamond_id)

                # fillter diamond which already sold table but not sold
                update_only_is_not_sold = []
                sold_diamond_is_not_sold_list = SoldDiamonds.objects.using('primary').filter(
                    diamond_id__in=diam_data, is_sold=0)
                for diam in sold_diamond_is_not_sold_list:
                    update_only_is_not_sold.append(diam.diamond_id)

                sold_diamond_name = SoldDiamonds.objects.using('primary').filter(diamond_id__in=diam_data,
                                                                                      is_sold=1).values_list('diamond_id', flat=True)
                # print(sold_diamond_name.values_list('diamond_id', flat=True))


                sold_diamond_count = SoldDiamonds.objects.using('primary').filter(diamond_id__in=diam_data,
                                                                                      is_sold=1).count()

                # fillter diamond for sold
                list_of_diamond_for_sold = set(diam_data) - set(update_only_is_sold)

                # fillter diamond to insert in sold table
                list_of_diamond_create = list_of_diamond_for_sold - set(update_only_is_not_sold)

                if len(diam_data) > 0 and len(ord_data) > 0:
                    # condition to check diamond alredy sold or need to sold
                    if len(diam_data) == 1 and sold_diamond_count == 1:
                        status = "success"
                        code = 200
                        message = "Diamond already sold"
                    if len(diam_data) >= 1 and sold_diamond_count >= 1:
                        status = "success"
                        code = 200
                        message = str(list(sold_diamond_name))+" Diamond already sold from given diamond range"
                    elif len(diam_data) == sold_diamond_count and sold_diamond_count > 1:
                        status = "success"
                        code = 200
                        message = " {0} Diamonds are already sold".format(', '.join([str(elem) for elem in diam_data]))
                    elif len(diam_data) != sold_diamond_count and sold_diamond_count >= 0:
                        diamond_data_count_query = DiamondDetails_primary.objects.using('primary').filter(diamond_id__in=diam_data, diamond_quantity=1).count()


                        if diamond_data_count_query > 0 and len(update_only_is_not_sold) > 0:
                            SoldDiamonds.objects.using('primary').filter(diamond_id__in=update_only_is_not_sold,
                                                                             is_sold=0).update(
                                order_id=str(order_id),
                                created_at=datetime.datetime.now(),
                                updated_at=datetime.datetime.now(), is_sold=1)

                            diamond_data_query = DiamondDetails_primary.objects.using('primary').filter(
                                diamond_id__in=update_only_is_not_sold,
                                diamond_quantity=1)
                            diamond_data_list = list(diamond_data_query.values())
                            for info in diamond_data_list:
                                DiamondDetails_primary.objects.using('primary').filter(
                                    diamond_id=info['diamond_id']).update(diamond_quantity=0, is_show=0)

                                # update diamond quantity in pair diamond data
                                pair_d1_diamond_data_count_query = PairDiamonds.objects.using('primary').filter(
                                    d1_diamond_id=info['diamond_id'], combined_Quantity=1).count()
                                pair_d2_diamond_data_count_query = PairDiamonds.objects.using('primary').filter(
                                    d2_diamond_id=info['diamond_id'], combined_Quantity=1).count()

                                if pair_d1_diamond_data_count_query > 0:
                                    PairDiamonds.objects.using('primary').filter(
                                        d1_diamond_id=info['diamond_id']).update(d1_diamond_quantity=0, combined_Quantity=0, d1_is_show=0)
                                elif pair_d2_diamond_data_count_query > 0:
                                    PairDiamonds.objects.using('primary').filter(
                                        d2_diamond_id=info['diamond_id']).update(d2_diamond_quantity=0, combined_Quantity=0, d2_is_show=0)


                            status = "success"
                            code = 200
                            if len(diam_data) >= 2 and len(update_only_is_not_sold) > 1:
                                diamond_sold_list.extend(update_only_is_not_sold)
                                update_only_is_not_soldToStr = ', '.join(
                                    [str(elem) for elem in list(set(diamond_sold_list))])
                                message = "{0} Diamonds are sold".format(update_only_is_not_soldToStr)
                            elif len(diam_data) >= 1 and len(update_only_is_not_sold) == 1:
                                diamond_sold_list.extend(update_only_is_not_sold)
                                update_only_is_not_soldToStr = ', '.join(
                                    [str(elem) for elem in list(set(diamond_sold_list))])
                                message = "{0} Diamond are sold".format(update_only_is_not_soldToStr)

                        if diamond_data_count_query > 0 and len(list(list_of_diamond_create)) > 0:
                            a_list = list(list_of_diamond_create)
                            # diamond_data_query_find = DiamondDetails.objects.using('primary').filter(diamond_id__in=a_list,
                            #                                                         diamond_quantity=1)
                            # diamond_data_list = list(diamond_data_query_find.values())
                            if len(a_list) > 1:
                                diamond_data_query_find = "select * from `websr_diamond_details_view` where diamond_id IN {0}".format(
                                    tuple(a_list))
                            elif len(a_list) == 1:
                                diamond_data_query_find = "select * from `websr_diamond_details_view` where diamond_id = '{0}'".format(
                                    a_list[0])
                            cursor.execute(diamond_data_query_find)
                            columns = [column[0] for column in cursor.description]
                            diamond_data_list = []
                            for row in cursor.fetchall():
                                diamond_data_list.append(dict(zip(columns, row)))
                            new = []

                            # print(diamond_data_list)

                            objs = [SoldDiamonds(
                                diamond_id=str(data['diamond_id']).strip(),
                                shape=data['shape'],
                                color=data['color'],
                                clarity=data['clarity'],
                                carat_weight=data['carat_weight'],
                                lab=data['lab'],
                                cut=data['cut'],
                                polish=data['polish'],
                                symmetry=data['symmetry'],
                                flour_intensity=data['flour_intensity'],
                                rapaport_price=data['rapaport_price'],
                                perc_off_rap=data['perc_off_rap'],
                                certificate_number=str(data['certificate_number']).strip(),
                                measurement=data['measurement'],
                                length=data['length'],
                                width=data['width'],
                                depth=data['depth'],
                                ratio=data['ratio'],
                                dept_perc=data['dept_perc'],
                                table_perc=data['table_perc'],
                                fancy_color=data['fancy_color'],
                                fancy_color_intensity=data['fancy_color_intensity'],
                                fancy_color_overtone=data['fancy_color_overtone'],
                                desc_comments=data['desc_comments'],
                                memo_status=data['memo_status'],
                                inscription=data['inscription'],
                                location=data['location'],
                                certificate_file=data['certificate_file'],
                                diamond_image=data['diamond_image'],
                                diamond_video=data['diamond_video'],
                                price_per_ct=data['price_per_ct'],
                                original_total_price=data['original_total_price'],
                                exchange_rate=data['exchange_rate'],
                                convert_price=data['convert_price'],
                                plus_markup_price_ct=data['plus_markup_price_ct'],
                                plus_markup_price=data['plus_markup_price'],
                                final_price=data['final_price'],
                                final_discount_price=data['final_discount_price'],
                                exchange_rate_pound=data['exchange_rate_pound'],
                                price_per_ct_pound=data['price_per_ct_pound'],
                                plus_markup_price_ct_pound=data['plus_markup_price_ct_pound'],
                                original_total_price_pound=data['original_total_price_pound'],
                                final_price_pound=data['final_price_pound'],
                                exchange_rate_cad=data['exchange_rate_cad'],
                                price_per_ct_cad=data['price_per_ct_cad'],
                                plus_markup_price_ct_cad=data['plus_markup_price_ct_cad'],
                                original_total_price_cad=data['original_total_price_cad'],
                                final_price_cad=data['final_price_cad'],
                                availability=data['availability'],
                                girdle=data['girdle'],
                                girdle_min=data['girdle_min'],
                                girdle_max=data['girdle_max'],
                                girdle_perc=data['girdle_perc'],
                                girdle_condition=data['girdle_condition'],
                                culet=data['culet'],
                                culet_condition=data['culet_condition'],
                                crown_angle=data['crown_angle'],
                                crown_height=data['crown_height'],
                                pavilion_depth=data['pavilion_depth'],
                                pavilion_angle=data['pavilion_angle'],
                                origin=data['origin'],
                                seller_name=data['seller_name'],
                                city=data['city'],
                                state=data['state'],
                                country=data['country'],
                                is_match_pair_separable=data['is_match_pair_separable'],
                                member_comments=data['member_comments'],
                                supplier_country=data['supplier_country'],
                                milky=data['milky'],
                                diamond_quantity=data['diamond_quantity'],
                                diamond_type=data['diamond_type'],
                                supplier_id=data['supplier_id'],
                                data_entry_point=data['data_entry_point'],
                                created_at=data['created_at'],
                                updated_at=datetime.datetime.now(),
                                stock_number=data['stock_number'],
                                fluorescence_color=data['fluorescence_color'],
                                shade=data['shade'],
                                eye_clean=data['eye_clean'],
                                treatment=data['treatment'],
                                cert_comment=data['cert_comment'],
                                key_to_symbols=data['key_to_symbols'],
                                white_inclusion=data['white_inclusion'],
                                black_inclusion=data['black_inclusion'],
                                open_inclusion=data['open_inclusion'],
                                quickship=data['quick_ship'],
                                appointment=data['appointment'],
                                order_id=str(order_id),
                                is_sold=1)
                                for data in diamond_data_list]
                            msg = SoldDiamonds.objects.using('primary').bulk_create(objs)

                            # update diamond quantity in diamond data
                            for info in diamond_data_list:
                                DiamondDetails_primary.objects.using('primary').filter(
                                    diamond_id=info['diamond_id']).update(diamond_quantity=0, is_show=0)

                                # update diamond quantity in pair diamond data
                                pair_d1_diamond_data_count_query = PairDiamonds.objects.using('primary').filter(
                                    d1_diamond_id=info['diamond_id'], combined_Quantity=1).count()
                                pair_d2_diamond_data_count_query = PairDiamonds.objects.using('primary').filter(
                                    d2_diamond_id=info['diamond_id'], combined_Quantity=1).count()

                                if pair_d1_diamond_data_count_query > 0:
                                    PairDiamonds.objects.using('primary').filter(
                                        d1_diamond_id=info['diamond_id']).update(d1_diamond_quantity=0, combined_Quantity=0, d1_is_show=0)
                                elif pair_d2_diamond_data_count_query > 0:
                                    PairDiamonds.objects.using('primary').filter(
                                        d2_diamond_id=info['diamond_id']).update(d2_diamond_quantity=0, combined_Quantity=0, d2_is_show=0)

                            status = "success"
                            code = 200
                            if len(diam_data) >= 2 and len(diamond_data_list) >= 1:
                                diamond_sold_list.extend([(elem['diamond_id']) for elem in diamond_data_list])
                                update_only_is_not_soldToStr = ', '.join(
                                    [str(elem) for elem in list(set(diamond_sold_list))])
                                message = "{0} Diamonds are sold".format(update_only_is_not_soldToStr)
                            elif len(diam_data) >= 1 and len(diamond_data_list) == 1:
                                diamond_sold_list.extend([(elem['diamond_id']) for elem in diamond_data_list])
                                update_only_is_not_soldToStr = ', '.join(
                                    [str(elem) for elem in list(set(diamond_sold_list))])
                                message = "{0} Diamonds are sold".format(update_only_is_not_soldToStr)

                    else:
                        status = "success"
                        code = 200
                        message = "Please Insert valid data"
                else:
                    status = "success"
                    code = 200
                    message = "Please don't provide blank value"
            except Exception as ex:
                status = "Fail"
                code = 400
                message = "{0}".format(ex)

            # return Solddiam(status=status, code=code, message=message)


            return {"status": status, 'code': code, 'message': message}
            # except:
            #     return None
        else:
            return None
