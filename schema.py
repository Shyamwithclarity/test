import datetime
import decimal
import json
from functools import reduce

import django_filters
import graphene
import graphql
import pickle
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers import serialize
from django.db import connection, connections
from django.db.migrations.operations.base import Operation
from graphql import GraphQLError
from graphene import relay, String
from graphene_django import DjangoObjectType

# from .diamand import DiamondClass


from webapp_live.models import DiamondDetails, SoldDiamonds, SupplierDetails, DiamondDetails_primary, \
    PairDiamonds
# from webapp_easydiam.models import DiamondDetails, SoldDiamonds
from webservice.settings import TABLE_PREFIX as table_prefix
# from billing_webservice.settings import TABLE_PREFIX as table_prefix
from django.db.models import Q
import operator

from django.contrib.auth import get_user_model


class DimondType(DjangoObjectType):
    class Meta:
        model = DiamondDetails
        fields = "__all__"
        diacount = String()


class Diamond(graphene.ObjectType):
    id = graphene.String()
    diamond_id = graphene.String()
    shape = graphene.String()
    color = graphene.String()
    clarity = graphene.String()
    size = graphene.String()
    lab = graphene.String()
    cut = graphene.String()
    polish = graphene.String()
    symmetry = graphene.String()
    fluor_intensity = graphene.String()
    cert_num = graphene.String()
    measurement = graphene.String()
    meas_length = graphene.String()
    meas_width = graphene.String()
    meas_depth = graphene.String()
    ratio = graphene.String()
    depth_percent = graphene.String()
    table_percent = graphene.String()
    fancy_color = graphene.String()
    fancy_color_intensity = graphene.String()
    fancy_color_overtone = graphene.String()
    desc_comments = graphene.String()
    memo_status = graphene.String()
    inscription = graphene.String()
    location = graphene.String()
    certificate_file = graphene.String()
    image_url = graphene.String()
    video_url = graphene.String()
    image_file_url = graphene.String()
    video_file_url = graphene.String()
    price_per_ct = graphene.String()
    original_total_price = graphene.String()
    exchange_rate = graphene.String()
    convert_price = graphene.String()
    plus_markup_price_ct = graphene.String()
    plus_markup_price = graphene.String()
    total_sales_price = graphene.String()
    total_sales_price_in_currency = graphene.String()
    price_per_ct_eur = graphene.String()
    plus_markup_price_ct_eur = graphene.String()
    original_total_price_eur = graphene.String()
    final_price_eur = graphene.String()
    exchange_rate_pound = graphene.String()
    price_per_ct_pound = graphene.String()
    plus_markup_price_ct_pound = graphene.String()
    original_total_price_pound = graphene.String()
    final_price_pound = graphene.String()
    exchange_rate_cad = graphene.String()
    price_per_ct_cad = graphene.String()
    plus_markup_price_ct_cad = graphene.String()
    original_total_price_cad = graphene.String()
    final_price_cad = graphene.String()
    availability = graphene.String()
    girdle = graphene.String()
    girdle_min = graphene.String()
    girdle_max = graphene.String()
    girdle_perc = graphene.String()
    girdle_condition = graphene.String()
    culet = graphene.String()
    culet_condition = graphene.String()
    crown_angle = graphene.String()
    crown_height = graphene.String()
    pavilion_depth = graphene.String()
    pavilion_angle = graphene.String()
    origin = graphene.String()
    seller_name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    is_match_pair_separable = graphene.String()
    member_comments = graphene.String()
    supplier_country = graphene.String()
    milky = graphene.String()
    diamond_quantity = graphene.String()
    diamond_type = graphene.String()
    supplier_id = graphene.String()
    data_entry_point = graphene.String()
    inserted_on = graphene.String()
    updated_at = graphene.String()
    stock_number = graphene.String()
    is_show = graphene.String()
    currency_code = graphene.String()
    currency_symbol = graphene.String()
    special_price = graphene.String()
    diamond_feed = graphene.String()
    QuickShip = graphene.String()
    Appointment = graphene.String()
    final_discount_price = graphene.String()
    vault_discount = graphene.String()


class Searchresults(graphene.ObjectType):
    count_diam = graphene.String()
    diamonds_returned = graphene.String()
    page_no = graphene.String()


class Fillterdiamond(graphene.ObjectType):
    diamond = graphene.List(Diamond)
    searchresults = graphene.List(Searchresults)
    data_count = graphene.String()
    diamonds_returned = graphene.String()
    page_no = graphene.String()
    status = graphene.String()


class Pairdiamond(graphene.ObjectType):
    d1_diamond_id = graphene.String()
    d1_shape = graphene.String()
    d1_color = graphene.String()
    d1_clarity = graphene.String()
    d1_size = graphene.String()
    d1_lab = graphene.String()
    d1_cut = graphene.String()
    d1_polish = graphene.String()
    d1_symmetry = graphene.String()
    d1_flour_intensity = graphene.String()
    d1_cert_num = graphene.String()
    d1_measurement = graphene.String()
    d1_meas_length = graphene.String()
    d1_meas_width = graphene.String()
    d1_meas_depth = graphene.String()
    d1_ratio = graphene.String()
    d1_depth_percent = graphene.String()
    d1_table_percent = graphene.String()
    d1_rapaport_price = graphene.String()
    d1_perc_off_rap = graphene.String()
    d1_fancy_color = graphene.String()
    d1_fancy_color_intensity = graphene.String()
    d1_fancy_color_overtone = graphene.String()
    d1_price_per_ct = graphene.String()
    d1_original_total_price = graphene.String()
    d1_exchange_rate = graphene.String()
    d1_convert_price = graphene.String()
    d1_plus_markup_price_ct = graphene.String()
    d1_plus_markup_price = graphene.String()
    d1_total_sales_price = graphene.String()
    d1_total_sales_price_in_currency = graphene.String()
    d1_price_per_ct_eur = graphene.String()
    d1_plus_markup_price_ct_eur = graphene.String()
    d1_original_total_price_eur = graphene.String()
    d1_final_price_eur = graphene.String()
    d1_exchange_rate_pound = graphene.String()
    d1_price_per_ct_pound = graphene.String()
    d1_plus_markup_price_ct_pound = graphene.String()
    d1_original_total_price_pound = graphene.String()
    d1_final_price_pound = graphene.String()
    d1_exchange_rate_cad = graphene.String()
    d1_price_per_ct_cad = graphene.String()
    d1_plus_markup_price_ct_cad = graphene.String()
    d1_original_total_price_cad = graphene.String()
    d1_final_price_cad = graphene.String()
    d2_exchange_rate_cad = graphene.String()
    d2_price_per_ct_cad = graphene.String()
    d2_plus_markup_price_ct_cad = graphene.String()
    d2_original_total_price_cad = graphene.String()
    d2_final_price_cad = graphene.String()
    d1_certificate_file = graphene.String()
    d1_image_url = graphene.String()
    d1_video_url = graphene.String()
    d1_image_file_url = graphene.String()
    d1_video_file_url = graphene.String()
    d1_availability = graphene.String()
    d1_diamond_quantity = graphene.String()
    d1_diamond_type = graphene.String()
    d1_supplier_id = graphene.String()
    d1_data_entry_point = graphene.String()
    d1_created_at = graphene.String()
    d1_updated_at = graphene.String()
    d1_stock_number = graphene.String()
    d1_is_show = graphene.String()
    d1_desc_comments = graphene.String()
    d1_memo_status = graphene.String()
    d1_inscription = graphene.String()
    d1_location = graphene.String()
    d1_girdle = graphene.String()
    d1_girdle_min = graphene.String()
    d1_girdle_max = graphene.String()
    d1_girdle_perc = graphene.String()
    d1_girdle_condition = graphene.String()
    d1_culet = graphene.String()
    d1_culet_condition = graphene.String()
    d1_crown_angle = graphene.String()
    d1_crown_height = graphene.String()
    d1_pavilion_depth = graphene.String()
    d1_pavilion_angle = graphene.String()
    d1_origin = graphene.String()
    d1_seller_name = graphene.String()
    d1_city = graphene.String()
    d1_state = graphene.String()
    d1_country = graphene.String()
    d1_is_match_pair_separable = graphene.String()
    d1_member_comments = graphene.String()
    d1_supplier_country = graphene.String()
    d1_milky = graphene.String()
    d1_fluorescence_color = graphene.String()
    d1_shade = graphene.String()
    d1_eye_clean = graphene.String()
    d1_treatment = graphene.String()
    d1_cert_comment = graphene.String()
    d1_key_to_symbols = graphene.String()
    d1_white_inclusion = graphene.String()
    d1_black_inclusion = graphene.String()
    d1_open_inclusion = graphene.String()
    d1_quick_ship = graphene.String()
    d1_appointment = graphene.String()
    d2_diamond_id = graphene.String()
    d2_shape = graphene.String()
    d2_color = graphene.String()
    d2_clarity = graphene.String()
    d2_size = graphene.String()
    d2_lab = graphene.String()
    d2_cut = graphene.String()
    d2_polish = graphene.String()
    d2_symmetry = graphene.String()
    d2_flour_intensity = graphene.String()
    d2_cert_num = graphene.String()
    d2_measurement = graphene.String()
    d2_meas_length = graphene.String()
    d2_meas_width = graphene.String()
    d2_meas_depth = graphene.String()
    d2_ratio = graphene.String()
    d2_depth_percent = graphene.String()
    d2_table_percent = graphene.String()
    d2_rapaport_price = graphene.String()
    d2_perc_off_rap = graphene.String()
    d2_fancy_color = graphene.String()
    d2_fancy_color_intensity = graphene.String()
    d2_fancy_color_overtone = graphene.String()
    d2_price_per_ct = graphene.String()
    d2_original_total_price = graphene.String()
    d2_exchange_rate = graphene.String()
    d2_convert_price = graphene.String()
    d2_plus_markup_price_ct = graphene.String()
    d2_plus_markup_price = graphene.String()
    d2_total_sales_price = graphene.String()
    d2_total_sales_price_in_currency= graphene.String()
    d2_price_per_ct_eur = graphene.String()
    d2_plus_markup_price_ct_eur = graphene.String()
    d2_original_total_price_eur = graphene.String()
    d2_final_price_eur = graphene.String()
    d2_exchange_rate_pound = graphene.String()
    d2_price_per_ct_pound = graphene.String()
    d2_plus_markup_price_ct_pound = graphene.String()
    d2_original_total_price_pound = graphene.String()
    d2_final_price_pound = graphene.String()
    d2_certificate_file = graphene.String()
    d2_image_url = graphene.String()
    d2_video_url = graphene.String()
    d2_image_file_url = graphene.String()
    d2_video_file_url = graphene.String()
    d2_availability = graphene.String()
    d2_diamond_quantity = graphene.String()
    d2_diamond_type = graphene.String()
    d2_supplier_id = graphene.String()
    d2_data_entry_point = graphene.String()
    d2_created_at = graphene.String()
    d2_updated_at = graphene.String()
    d2_stock_number = graphene.String()
    d2_is_show = graphene.String()
    d2_desc_comments = graphene.String()
    d2_memo_status = graphene.String()
    d2_inscription = graphene.String()
    d2_location = graphene.String()
    d2_girdle = graphene.String()
    d2_girdle_min = graphene.String()
    d2_girdle_max = graphene.String()
    d2_girdle_perc = graphene.String()
    d2_girdle_condition = graphene.String()
    d2_culet = graphene.String()
    d2_culet_condition = graphene.String()
    d2_crown_angle = graphene.String()
    d2_crown_height = graphene.String()
    d2_pavilion_depth = graphene.String()
    d2_pavilion_angle = graphene.String()
    d2_origin = graphene.String()
    d2_seller_name = graphene.String()
    d2_city = graphene.String()
    d2_state = graphene.String()
    d2_country = graphene.String()
    d2_is_match_pair_separable = graphene.String()
    d2_member_comments = graphene.String()
    d2_supplier_country = graphene.String()
    d2_milky = graphene.String()
    d2_fluorescence_color = graphene.String()
    d2_shade = graphene.String()
    d2_eye_clean = graphene.String()
    d2_treatment = graphene.String()
    d2_cert_comment = graphene.String()
    d2_key_to_symbols = graphene.String()
    d2_white_inclusion = graphene.String()
    d2_black_inclusion = graphene.String()
    d2_open_inclusion = graphene.String()
    d2_quick_ship = graphene.String()
    d2_appointment = graphene.String()
    combined_price = graphene.String()
    combined_price_pound = graphene.String()
    combined_price_cad = graphene.String()
    combined_QuickShip = graphene.String()
    combined_SKU = graphene.String()
    combined_Quantity = graphene.String()
    combined_Carat = graphene.String()
    combined_Diamond_ID = graphene.String()
    combined_Cut = graphene.String()
    d1_diamond_feed = graphene.String()
    d2_diamond_feed = graphene.String()
    inserted_on = graphene.String()
    final_discount_price = graphene.String()


class Fillterpairdiamond(graphene.ObjectType):
    diamond = graphene.List(Pairdiamond)
    data_count = graphene.String()
    diamonds_returned = graphene.String()
    page_no = graphene.String()
    status = graphene.String()


class diamondbyid(graphene.ObjectType):
    diamond = graphene.List(Diamond)
    status = graphene.String()


class diamondbystockorcert(graphene.ObjectType):
    diamond = graphene.List(Diamond)
    status = graphene.String()

class sold_the_diamond(graphene.ObjectType):
    status = graphene.String()
    code = graphene.String()
    message = graphene.String()


class Query(graphene.ObjectType):
    live_alldiamond = graphene.List(DimondType, page=graphene.String())
    live_diamond_by_id = graphene.Field(diamondbyid, diamond_id=graphene.String(), only_not_sold_quantity=graphene.String(), diamond_type=graphene.String())
    live_diamond_by_stockorcert = graphene.Field(diamondbystockorcert, input_id=graphene.String(), only_not_sold_quantity=graphene.String(), diamond_type=graphene.String())
    live_diamond_data = graphene.Field(Fillterdiamond, shapes=graphene.String(),
                                      carat=graphene.String(),
                                      clarity=graphene.String(), color=graphene.String(), polish=graphene.String(),
                                      symmetry=graphene.String(), fluoroscence=graphene.String(),
                                      price=graphene.String(),
                                      depth_per=graphene.String(), table=graphene.String(), ratio=graphene.String(),
                                      cut=graphene.String(), lab=graphene.String(), diamond_type=graphene.String(),
                                      length=graphene.String(), width=graphene.String(), depth=graphene.String(),
                                      final_price=graphene.String(), order_by=graphene.String(),
                                      sort_by=graphene.String(), diamond_id=graphene.String(), quickship=graphene.String(),
                                      appointment=graphene.String(), supplier_name=graphene.String(), both_quantity=graphene.String(), vault_discount=graphene.String(), diamond_img=graphene.String())

    live_pair_diamond_data = graphene.Field(Fillterpairdiamond, page=graphene.String(), shapes=graphene.String(),
                                           carat=graphene.String(),
                                           clarity=graphene.String(), color=graphene.String(), polish=graphene.String(),
                                           symmetry=graphene.String(), fluoroscence=graphene.String(),
                                           price=graphene.String(),
                                           depth_per=graphene.String(), table=graphene.String(),
                                           ratio=graphene.String(),
                                           cut=graphene.String(), lab=graphene.String(), diamond_type=graphene.String(),
                                           length=graphene.String(), width=graphene.String(), depth=graphene.String(),
                                           final_price=graphene.String(), order_by=graphene.String(),
                                           sort_by=graphene.String(), diamond_id=graphene.String(), quickship=graphene.String(),
                                           appointment=graphene.String())
    live_pair_diamond_by_id = graphene.Field(Fillterpairdiamond, diamond_id=graphene.String())
    # live_sold_new_diamond = graphene.Field(sold_the_diamond, diamond_id=graphene.String(),
    #                                         order_id=graphene.String(),
    #                                         customer_name=graphene.String(),
    #                                         date=graphene.String(),
    #                                         dia_sku=graphene.String(),
    #                                         gemstone_type=graphene.String(),
    #                                         measurements=graphene.String(),
    #                                         gemstone_cost=graphene.String(),
    #                                         certificate_number=graphene.String(),
    #                                         engraving=graphene.String(),
    #                                         fm_setting_sku=graphene.String(),
    #                                         setting_supplier_sku=graphene.String(),
    #                                         product_name=graphene.String(),
    #                                         head_price=graphene.String(),
    #                                         shank_setting_price=graphene.String(),
    #                                         setting_metal=graphene.String(),
    #                                         setting_size=graphene.String(),
    #                                         setting_tcw=graphene.String(),
    #                                         side_diamond_tcw=graphene.String(),
    #                                         tcw_cost=graphene.String(),
    #                                         labor=graphene.String(),
    #                                         total_price=graphene.String(),
    #                                         supplier_paid=graphene.String(),
    #                                         setting_supplier=graphene.String(),
    #                                         net_cost_price=graphene.String(),
    #                                         retail_price=graphene.String(),
    #                                         where_is_setting=graphene.String(),
    #                                         pay_date=graphene.String(),
    #                                         check_number=graphene.String(),
    #                                         notes_order_status=graphene.String(),
    #                                         delivery_deadline=graphene.String(),
    #                                         order_comment=graphene.String(),
    #                                         lab_natural=graphene.String(),
    #                                         sku_order_quantity=graphene.String(),
    #                                         diamond_lab=graphene.String(),
    #                                         discount_amount=graphene.String(),
    #                                         tax_amount=graphene.String(),
    #                                         billing_city=graphene.String(),
    #                                         billing_country_id=graphene.String(),
    #                                         billing_email=graphene.String(),
    #                                         billing_firstname=graphene.String(),
    #                                         billing_lastname=graphene.String(),
    #                                         billing_postcode=graphene.String(),
    #                                         billing_region=graphene.String(),
    #                                         billing_street=graphene.String(),
    #                                         billing_telephone=graphene.String(),
    #                                         shipping_city=graphene.String(),
    #                                         shipping_country_id=graphene.String(),
    #                                         shipping_email=graphene.String(),
    #                                         shipping_firstname=graphene.String(),
    #                                         shipping_lastname=graphene.String(),
    #                                         shipping_postcode=graphene.String(),
    #                                         shipping_region=graphene.String(),
    #                                         shipping_street=graphene.String(),
    #                                         shipping_telephone=graphene.String(),
    #                                         ships_by=graphene.String(),
    #                                         order_status=graphene.String())
                                            
    live_sold_new_diamond = graphene.Field(sold_the_diamond, diamond_id=graphene.String(), order_id=graphene.String())

    def resolve_live_diamond_data(self, info, page=None, shapes=None, carat=None, clarity=None, color=None, polish=None,
                                 symmetry=None, fluoroscence=None, price=None, depth_per=None, table=None, ratio=None,
                                 cut=None, lab=None, diamond_type=None, final_price=None,
                                 order_by=None, sort_by=None, diamond_id=None, quickship=None, appointment=None,
                                 supplier_name=None, both_quantity=None, vault_discount=None, diamond_img=None):

        # activeapiObj = """select * from `{0}api_details` where api_name = 'Filter diamond data' and is_active = 1""".format(
        #     table_prefix)
        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:

            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')

            og_shapes_list = ['Round', 'Princess', 'Cushion', 'Radiant', 'Asscher', 'Emerald', 'Oval', 'Pear',
                              'Marquise', ]

            regular_color_codes_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                                        'L']  # Only White Diamonds in this project

            diamond_cuts_list = ['Excellent', 'Very Good', 'Good']

            labgrown_diamond_cuts_list = ['Ideal', 'Excellent', 'Very Good', 'Good']

            diamond_clarity_list = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF', 'FL']

            diamond_fluoroscence_list = ['None', 'Faint', 'Medium', 'Strong']

            diamond_polish_list = ['Fair', 'Good', 'Very Good', 'Excellent']

            diamond_symmetry_list = ['Fair', 'Good', 'Very Good', 'Excellent']

            diamond_labs_list = ['GIA', 'IGI']

            diamond_carat_min = 0.25
            diamond_carat_max = 20.00 #5.25
            diamond_price_min = 100
            diamond_price_max = 1000000

            diamond_depth_min = 40
            diamond_depth_max = 90

            diamond_table_min = 40
            diamond_table_max = 90

            diamond_min_ratio = 0.9
            diamond_max_ratio = 2.75

            diamond_diff_labs_list = ['white', 'lab']
            order_by_price = 'final_price'

            shape_list = list(str(shapes).title().strip().replace(', ', ',').split(","))
            clarity_list = list(str(clarity).upper().strip().replace(', ', ',').split(","))
            color_list = list(str(color).upper().strip().replace(', ', ',').split(","))
            cut_list = list(str(cut).title().strip().replace(', ', ',').split(","))
            polish_list = list(str(polish).title().strip().replace(', ', ',').split(","))
            symmetry_list = list(str(symmetry).title().strip().replace(', ', ',').split(","))
            lab_list = list(str(lab).upper().strip().replace(', ', ',').split(","))
            fluoroscence_list = list(str(fluoroscence).title().strip().replace(', ', ',').split(","))
            carat_tuple = tuple(str(carat).strip().replace(', ', ',').split(","))
            price_tuple = tuple(str(price).strip().replace(', ', ',').split(","))
            depth_per_tuple = tuple(str(depth_per).strip().replace(', ', ',').split(","))
            table_tuple = tuple(str(table).strip().replace(', ', ',').split(","))
            ratio_tuple = tuple(str(ratio).strip().replace(', ', ',').split(","))
            diamond_type_list = list(str(diamond_type).lower().strip().replace(', ', ',').split(","))
            final_price_range = tuple(str(final_price).strip().replace(', ', ',').split(","))
            diamond_id_send = str(diamond_id).strip().replace(', ', ',').replace(' ', '')
            quickship_add = str(quickship).strip().replace(', ', ',').replace(' ', '')
            appointment_add = str(appointment).strip().replace(', ', ',').replace(' ', '')
            supplier_get_name = str(supplier_name).strip().replace(', ', ',')
            quantity_name = str(both_quantity).strip().replace(', ', ',').title()
            vault_get_discount = str(vault_discount).strip().replace(', ', ',').title()
            # print(supplier_get_name)

            if page == None:
                page = 1

            diamond_query = None
            output = []

            show_diamond_count = 500
            if page == None:
                print("Please define Page no.")
                # diamond_query = DiamondDetails.objects.all().order_by(order_by_price)[0:20]
            else:
                vault_discount_id = None
                if vault_get_discount == "Yes" and str(vault_get_discount).strip() != "" and vault_get_discount is not None:
                    vault_discount_query = """SELECT `id` FROM `websr_supplier_details` where `is_vault_discount` = 1""".format(
                        vault_get_discount)
                    cursor.execute(vault_discount_query)
                    vault_discount_id = cursor.fetchall()
                    # print(vault_discount_id)

                # supplier_name_query = """SELECT `id` FROM `websr_supplier_details` where `supplier_name` = '{0}'""".format(supplier_get_name)
                # cursor.execute(supplier_name_query)
                # suplier_get_id = cursor.fetchone()
                # print(suplier_get_id)

                constant_get_isenable = [0]
                constant_get_vault_isenable = [0]
                if  (str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown"):
                    constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'""".format(
                        supplier_get_name)
                    cursor.execute(constant_isenable_query)
                    constant_get_isenable = cursor.fetchone()

                    constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'""".format(
                        supplier_get_name)
                    cursor.execute(constant_isenable_vault_query)
                    constant_get_vault_isenable = cursor.fetchone()

                # supplier filter
                if vault_get_discount == "Yes" and str(vault_get_discount).strip() != "" and vault_get_discount is not None:
                    if quantity_name == "Yes" and str(quantity_name).strip() != "" and quantity_name is not None:
                        quantity_query = "dd.diamond_quantity IN (1, 0)"
                        # quantity_query = "dd.diamond_quantity IN (1)"
                    else:
                        quantity_query = "dd.diamond_quantity = 1"
                else:
                    quantity_query = "dd.diamond_quantity = 1"

                if (shapes!=None or shapes!='') and (carat!=None or carat!='') and (clarity!=None or clarity!='') and (color!=None or color!='') and (polish!=None or polish!='') and (symmetry!=None or symmetry!='') and (fluoroscence!=None or fluoroscence!='') and (price!=None or price!='') and (depth_per!=None or depth_per!='') and (table!=None or table!='') and (ratio!=None or ratio!='') and (cut!=None or cut!='') and (lab!=None or lab!='') and (final_price!=None or final_price!='') and (quickship!=None or quickship!='') and (appointment!=None or appointment!=''):
                    # Shape filter
                    if shapes and str(shapes).strip() != "" and shapes is not None:
                        if len(shapes) > 0:
                            shape_list_new = ", ".join("'{0}'".format(w) for w in shape_list)
                            shape_query = "dd.`shape` in (" + str(shape_list_new) + ")"
                    else:
                        shape_list_new = ", ".join("'{0}'".format(w) for w in og_shapes_list)
                        shape_query = "dd.`shape` in (" + str(shape_list_new) + ")"

                    # carat filter
                    if carat and str(carat).strip() != "" and carat is not None:
                        carat_query = "(dd.`carat_weight` >=" + str(carat_tuple[0]) + " && dd.`carat_weight` <=" + str(
                            carat_tuple[1]) + ")"
                    else:
                        carat_query = "(dd.`carat_weight` >=" + str(diamond_carat_min) + " && dd.`carat_weight` <=" + str(
                            diamond_carat_max) + ")"

                    # clarity filter
                    if clarity and str(clarity).strip() != "" and clarity is not None:
                        if len(clarity) > 0:
                            clarity_list_new = ", ".join("'{0}'".format(c) for c in clarity_list)
                            clarity_query = "dd.`clarity` in (" + str(clarity_list_new) + ")"
                    else:
                        clarity_list_new = ", ".join("'{0}'".format(c) for c in diamond_clarity_list)
                        clarity_query = "dd.`clarity` in (" + str(clarity_list_new) + ")"

                    # print(clarity_query)
                    # color filter
                    if color and str(color).strip() != "" and color is not None:
                        if len(color) > 0:
                            colors_list_new = ", ".join("'{0}'".format(c) for c in color_list)
                            color_query = "dd.`color` in (" + str(colors_list_new) + ")"
                    else:
                        colors_list_new = ", ".join("'{0}'".format(c) for c in regular_color_codes_list)
                        color_query = "dd.`color` in (" + str(colors_list_new) + ")"

                    # polish filter
                    if polish and str(polish).strip() != "" and polish is not None:
                        if len(polish) > 0:
                            polish_list_new = ", ".join("'{0}'".format(c) for c in polish_list)
                            polish_query = "dd.`polish` in (" + str(polish_list_new).replace("_", " ") + ")"
                    else:
                        polish_list_new = ", ".join("'{0}'".format(c) for c in diamond_polish_list)
                        polish_query = "dd.`polish` in (" + str(polish_list_new).replace("_", " ") + ")"

                    # symmetry filter
                    if symmetry and str(symmetry).strip() != "" and symmetry is not None:
                        if len(symmetry) > 0:
                            symmetry_list_new = ", ".join("'{0}'".format(c) for c in symmetry_list)
                            symmetry_query = "dd.`symmetry` in (" + str(symmetry_list_new).replace("_", " ") + ")"
                    else:
                        symmetry_list_new = ", ".join("'{0}'".format(c) for c in diamond_symmetry_list)
                        symmetry_query = "dd.`symmetry` in (" + str(symmetry_list_new).replace("_", " ") + ")"

                    # fluoroscence filter
                    if fluoroscence and str(fluoroscence).strip() != "" and fluoroscence is not None:
                        fluor_list_new = ", ".join("'{0}'".format(w) for w in fluoroscence_list)
                        fluorescence_query = "dd.`flour_intensity` in (" + str(fluor_list_new) + ")"
                    else:
                        fluor_list_new = ", ".join("'{0}'".format(w) for w in diamond_fluoroscence_list)
                        fluorescence_query = "dd.`flour_intensity` in (" + str(fluor_list_new) + ")"

                    # depth perc filter
                    if depth_per and str(depth_per).strip() != "" and depth_per is not None:
                        depth_perc_query = "(dd.`dept_perc` BETWEEN " + str(depth_per_tuple[0]) + " AND " + str(
                            depth_per_tuple[1]) + ")"
                    else:
                        depth_perc_query = "(dd.`dept_perc` BETWEEN " + str(diamond_depth_min) + " AND " + str(
                            diamond_depth_max) + ")"

                    # table filter
                    if table and str(table).strip() != "" and table is not None:
                        table_perc_query = "(dd.`table_perc` BETWEEN " + str(table_tuple[0]) + " AND " + str(
                            table_tuple[1]) + ")"
                    else:
                        table_perc_query = "(dd.`table_perc` BETWEEN " + str(diamond_table_min) + " AND " + str(
                            diamond_table_max) + ")"

                    # ratio filter
                    if ratio and str(ratio).strip() != "" and ratio is not None:
                        ratio_query = "(dd.`ratio` BETWEEN " + str(ratio_tuple[0]) + " AND " + str(ratio_tuple[1]) + ")"
                    else:
                        ratio_query = "(dd.`ratio` BETWEEN " + str(diamond_min_ratio) + " AND " + str(
                            diamond_max_ratio) + ")"

                    # lab filter
                    if lab and str(lab).strip() != "" and lab is not None:
                        lab_list_new = ", ".join("'{0}'".format(c) for c in lab_list)
                        lab_query = "dd.`lab` in (" + str(lab_list_new).replace("_", " ") + ")"
                    else:
                        lab_list_new = ", ".join("'{0}'".format(c) for c in diamond_labs_list)
                        lab_query = "dd.`lab` in (" + str(lab_list_new).replace("_", " ") + ")"

                    # cut filter
                    cut_query = ""
                    if cut and str(cut).strip() != "" and cut is not None:
                        if len(cut) > 0:
                            if str(diamond_type).strip().lower() == "white" or str(
                                    diamond_type).strip().lower() == "natural":
                                cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
                                cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
                            elif str(diamond_type).strip().lower() == "lab" or str(
                                    diamond_type).strip().lower() == "lab-grown":
                                cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
                                cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
                    else:
                        if str(diamond_type).strip().lower() == "white" or str(
                                diamond_type).strip().lower() == "natural":
                            cuts_list_new = ", ".join("'{0}'".format(c) for c in diamond_cuts_list)
                            cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
                        elif str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown":
                            cuts_list_new = ", ".join("'{0}'".format(c) for c in labgrown_diamond_cuts_list)
                            cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"

                    # diamond type filter



                    # print(diamond_type_query)
                    # quickship filter
                    quickship_query = ""
                    if quickship and str(quickship).strip() != "" and quickship is not None:
                        if str(quickship).strip().lower() == 'y' or str(quickship).strip().lower() == 'yes':
                            quickship_query = "AND dd.`quick_ship`= 'Y'"
                        if str(quickship).strip().lower() == 'n' or str(quickship).strip().lower() == 'No':
                            quickship_query = "AND dd.`quick_ship`= 'N' or dd.`quick_ship`= ''"

                    # appointment filter
                    appointment_query = ""
                    if appointment and str(appointment).strip() != "" and appointment is not None:
                        if str(appointment).strip().lower() == 'y' or str(appointment).strip().lower() == 'yes':
                            appointment_query = "AND dd.`appointment`= 'Y'"
                        if str(appointment).strip().lower() == 'n' or str(appointment).strip().lower() == 'No':
                            appointment_query = "AND dd.`appointment`= 'N' or dd.`appointment`= ''"

                    diamond_img_query = ""
                    if diamond_img == 'yes':
                        # diamond_img_query = "AND dd.`diamond_image` NOT IN ('', '-', 'IMAGE', 'IMG', 'Img Link', 'nan', 'VIEW Image')"
                        diamond_img_query = "AND (dd.`diamond_image` LIKE '%jpg' OR dd.`diamond_image` LIKE '%jpeg' OR dd.`diamond_image` LIKE '%png')"

                    # # price per carat
                    # if final_price and str(final_price).strip() != "" and final_price is not None:
                    #     price_query = "(dd.`final_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
                    #         final_price_range[1]) + ")"
                    # else:
                    #     price_query = "(dd.`final_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
                    #         diamond_price_max) + ")"

                    # sort_direct_query = "ORDER BY dd.`final_price` ASC"
                    # if sort_by and str(sort_by).strip() != "":
                    #     if str(order_by).lower() == "price":
                    #         sort_order_by = "dd.`final_price`"
                    #         sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    # price per carat


                    price_query = ""

                    if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown"):
                        if final_price and str(final_price).strip() != "" and final_price is not None:
                            price_query = "(dd.`final_discount_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
                                final_price_range[1]) + ")"
                        else:
                            price_query = "(dd.`final_discount_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
                                diamond_price_max) + ")"
                    else:
                        if final_price and str(final_price).strip() != "" and final_price is not None:
                            price_query = "(dd.`final_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
                                final_price_range[1]) + ")"
                        else:
                            price_query = "(dd.`final_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
                                diamond_price_max) + ")"

                if diamond_type and str(diamond_type).strip() != "" and diamond_type is not None:
                    if str(diamond_type).strip().lower() == "white" or str(
                            diamond_type).strip().lower() == "natural":
                        diamond_type_query = "dd.`diamond_type`='white'"
                    elif str(diamond_type).strip().lower() == "lab" or str(
                            diamond_type).strip().lower() == "lab-grown":
                        diamond_type_query = "dd.`diamond_type`='lab'"
                else:
                    diamond_type_query = "dd.`diamond_type` in ('white', 'lab')"

                sort_direct_query = "ORDER BY dd.`final_price` ASC"
                if sort_by and str(sort_by).strip() != "":
                    if str(order_by).lower() == "price":
                        sort_order_by = ""
                        if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown"):
                            sort_order_by = "dd.`final_discount_price`"
                        else:
                            sort_order_by = "dd.`final_price`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "carat":
                        sort_order_by = "dd.`carat_weight`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "color":
                        sort_order_by = "dd.`color`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "clarity_index":
                        if str(sort_by).strip().lower() == "desc":
                            clarity_org_list = diamond_clarity_list
                            comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`clarity`," + str(comma_sep_clarity) + ")"
                        else:
                            clarity_asc_list = diamond_clarity_list
                            clarity_org_list = clarity_asc_list[::-1]
                            comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`clarity`," + str(comma_sep_clarity) + ")"
                    elif str(order_by).lower() == "cut_index":
                        if str(sort_by).strip().lower() == "desc":
                            cut_org_list = diamond_cuts_list + ['NA']
                            if str(diamond_type).strip().lower() == "lab" or str(
                                    diamond_type).strip().lower() == "lab-grown":
                                cut_org_list = labgrown_diamond_cuts_list
                            comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`cut`," + str(comma_sep_cut) + ")"
                        else:
                            cut_asc_list = diamond_cuts_list
                            if str(diamond_type).strip().lower() == "lab" or str(
                                    diamond_type).strip().lower() == "lab-grown":
                                cut_asc_list = labgrown_diamond_cuts_list
                            cut_org_list = cut_asc_list[::-1]
                            comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`cut`," + str(comma_sep_cut) + ")"
                        # sort_by = "dd.`cut`"
                        # sort_direct_query = "ORDER BY "+str(sort_by)+" "+str(sort_direction).strip()
                    elif str(order_by).lower() == "shape":
                        sort_order_by = "dd.`shape`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "polish":
                        sort_order_by = "dd.`polish`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "symmetry":
                        sort_order_by = "dd.`symmetry`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "flour":
                        sort_order_by = "dd.`flour_intensity`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "table":
                        sort_order_by = "dd.`table_perc`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "depth":
                        sort_order_by = "dd.`dept_perc`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "ratio":
                        sort_order_by = "dd.`ratio`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "quickship":
                        if str(sort_by).strip().lower() == "desc":
                            quickship_org_list = ['Y', 'N']
                            comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`quick_ship`," + str(comma_sep_quickship) + ")"
                        else:
                            quickship_org_list = ['N', 'Y']
                            comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`quick_ship`," + str(comma_sep_quickship) + ")"
                    elif str(order_by).lower() == "appointment":
                        if str(sort_by).strip().lower() == "desc":
                            appointment_org_list = ['Y', 'N']
                            comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`appointment`," + str(comma_sep_appointment) + ")"
                        else:
                            appointment_org_list = ['N', 'Y']
                            comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`appointment`," + str(comma_sep_appointment) + ")"
                    elif str(order_by).lower() == "diamond_quantity":
                        sort_order_by = "dd.`diamond_quantity`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()

                # PAGE NUMBER
                page_num_query = True
                records_limit = 500

                if records_limit and str(records_limit).strip() != "":
                    if page and str(page).strip() != "":
                        start_pos_value = (int(page) - 1) * records_limit
                    else:
                        page_number = 1
                        start_pos_value = (int(page_number) - 1) * records_limit
                    page_num_query = "LIMIT " + str(start_pos_value) + ", " + str(records_limit)

                supplier_query = """SELECT `id`, `supplier_name` FROM `websr_supplier_details` WHERE `is_allow`=1 AND `is_enabled`=1"""
                cursor.execute(supplier_query)
                columns = [column[0] for column in cursor.description]
                suppliers_dict = {}
                supp_ids = ""
                for row in cursor.fetchall():
                    suppliers_dict['supp_' + str(row[0])] = str(row[1])
                    supp_ids += str(row[0]) + ","

                # supp_ids = str(supp_ids).rstrip(",")
                #if supplier_name == "RFMI LAB LAB" and str(supplier_name).strip() != "" and supplier_name is not None:
                if vault_get_discount == "Yes" and str(vault_get_discount).strip() != "" and vault_get_discount is not None:
                    # supplier_list_new = ", ".join("'{0}'".format(w) for w in fluoroscence_list)
                    j = [item[0] for item in vault_discount_id]
                    supp_ids = str(",".join(list(map(str, j))))
                    if supp_ids is "":
                        supp_ids = 0
                else:
                    # fluor_list_new = ", ".join("'{0}'".format(w) for w in diamond_fluoroscence_list)
                    # supplier_id_query = ""
                    supp_ids = str(supp_ids).rstrip(",")

                if diamond_id == None or diamond_id == "" or diamond_id != "":
                    diamond_query = ''  # "dd.diamond_id NOT IN('')"
                else:
                    diamond_query = "dd.diamond_id NOT IN('{0}') AND".format(diamond_id_send)


                if (shapes!=None or shapes!='') and (carat!=None or carat!='') and (clarity!=None or clarity!='') and (color!=None or color!='') and (polish!=None or polish!='') and (symmetry!=None or symmetry!='') and (fluoroscence!=None or fluoroscence!='') and (price!=None or price!='') and (depth_per!=None or depth_per!='') and (table!=None or table!='') and (ratio!=None or ratio!='') and (cut!=None or cut!='') and (lab!=None or lab!='') and (final_price!=None or final_price!='') and (quickship!=None or quickship!='') and (appointment!=None or appointment!=''):
                    # select_query = """SELECT * FROM websr_diamond_details_primary as dd
                    #              JOIN websr_diamond_details_secondary t2
                    #              ON dd.diamond_id = t2.diamond_id
                    #             WHERE {17} {20} AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4} AND {5}
                    #             AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14}  {18} {19} {21} {15} {16}""".format(
                    #     "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
                    #     color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
                    #     table_perc_query, ratio_query, diamond_type_query,
                    #     sort_direct_query, page_num_query, diamond_query, quickship_query, appointment_query, quantity_query, diamond_img_query)

                    select_query = """SELECT * FROM websr_diamond_details_primary as dd
                                    WHERE {17} {20}  AND {2} AND {3} AND {4} AND {5}
                                    AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} 
                                    AND {14}  {18} {19} {21} AND dd.`supplier_id` IN ({1}) {15} {16}""".format(
                        "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
                        color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
                        table_perc_query, ratio_query, diamond_type_query,
                        sort_direct_query, page_num_query, diamond_query, quickship_query, appointment_query,
                        quantity_query, diamond_img_query)

                else:
                    # select_query = """SELECT * FROM websr_diamond_details_primary as dd
                    #                                  JOIN websr_diamond_details_secondary t2
                    #                                  ON dd.diamond_id = t2.diamond_id
                    #                                 WHERE {5} {6} AND dd.`supplier_id` IN ({1}) AND {2} {7} {3} {4}""".format(
                    #     "websr_", supp_ids, diamond_type_query, sort_direct_query, page_num_query, diamond_query, quantity_query, diamond_img_query)

                    select_query = """SELECT * FROM websr_diamond_details_primary as dd
                                WHERE {5} {6} AND {2} {7} AND dd.`supplier_id` IN ({1}) {3} {4}""".format(
                        "websr_", supp_ids, diamond_type_query, sort_direct_query, page_num_query, diamond_query,
                        quantity_query, diamond_img_query)

                cursor.execute(select_query)
                columns = [column[0] for column in cursor.description]
                diamond_list = []
                for row in cursor.fetchall():
                    diamond_list.append(dict(zip(columns, row)))

                if (shapes!=None or shapes!='') and (carat!=None or carat!='') and (clarity!=None or clarity!='') and (color!=None or color!='') and (polish!=None or polish!='') and (symmetry!=None or symmetry!='') and (fluoroscence!=None or fluoroscence!='') and (price!=None or price!='') and (depth_per!=None or depth_per!='') and (table!=None or table!='') and (ratio!=None or ratio!='') and (cut!=None or cut!='') and (lab!=None or lab!='') and (final_price!=None or final_price!='') and (quickship!=None or quickship!='') and (appointment!=None or appointment!=''):
                    # count_select_query = """SELECT count(*) FROM websr_diamond_details_primary as dd
                    #              JOIN websr_diamond_details_secondary t2
                    #              ON dd.diamond_id = t2.diamond_id
                    #             WHERE {17} {20} AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4} AND {5}
                    #             AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14}  {18} {19} {21} {15}""".format(
                    #     "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
                    #     color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
                    #     table_perc_query, ratio_query, diamond_type_query,
                    #     sort_direct_query, page_num_query, diamond_query, quickship_query, appointment_query, quantity_query, diamond_img_query)

                    count_select_query = """SELECT count(*) FROM websr_diamond_details_primary as dd
                        WHERE {17} {20} AND {2} AND {3} AND {4} AND {5}
                        AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14}  {18} {19} {21} AND dd.`supplier_id` IN ({1}) {15}""".format(
                        "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
                        color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
                        table_perc_query, ratio_query, diamond_type_query,
                        sort_direct_query, page_num_query, diamond_query, quickship_query, appointment_query,
                        quantity_query, diamond_img_query)
                else:
                    # count_select_query = """SELECT count(*) FROM websr_diamond_details_primary as dd
                    #                                  JOIN websr_diamond_details_secondary t2
                    #                                  ON dd.diamond_id = t2.diamond_id
                    #                                 WHERE {5} {6} AND dd.`supplier_id` IN ({1}) AND {2} {7} {3}""".format(
                    #     "websr_", supp_ids, diamond_type_query, sort_direct_query, page_num_query, diamond_query, quantity_query, diamond_img_query)
                    count_select_query = """SELECT count(*) FROM websr_diamond_details_primary as dd
                        WHERE {5} {6} AND {2} {7} AND dd.`supplier_id` IN ({1}) {3}""".format(
                        "websr_", supp_ids, diamond_type_query, sort_direct_query, page_num_query, diamond_query,
                        quantity_query, diamond_img_query)

                cursor.execute(count_select_query)
                rows_count_result = cursor.fetchone()

                total_found_diamonds = rows_count_result[0]

                if len(diamond_list) < records_limit:
                    records_limit = len(diamond_list)

                for i, res in enumerate(diamond_list):
                    supplierObj = SupplierDetails.objects.using('primary').get(id=res['supplier_id'])
                    if str(res['diamond_type']).strip().lower() == "white":
                        diamond_type_name = "White"
                    elif str(res['diamond_type']).strip().lower() == "lab":
                        diamond_type_name = "lab-grown"
                    # else:
                    #     diamond_type_name = res['diamond_type']
                    video_file_url=""
                    if res['diamond_video'] != "" or res['diamond_video'] != "nan":
                        if "#VALUE!" not in res['diamond_video']:
                            video_file_url = res['diamond_video']
                    else:
                        video_file_url = ""

                    discount_price = ""
                    if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
                            diamond_type).strip().lower() == "lab-grown"):
                        discount_price = res['final_discount_price']
                    else:
                        discount_price = res['final_price']

                    output.append(Diamond(diamond_id=res['diamond_id'],
                                              shape=res['shape'],
                                              color=res['color'],
                                              clarity=res['clarity'],
                                              size=res['carat_weight'],
                                              lab=res['lab'],
                                              cut=res['cut'],
                                              polish=res['polish'],
                                              symmetry=res['symmetry'],
                                              fluor_intensity=res['flour_intensity'],
                                              cert_num=res['certificate_number'],
                                              measurement=res['measurement'],
                                              meas_length=res['length'],
                                              meas_width=res['width'],
                                              meas_depth=res['depth'],
                                              ratio=res['ratio'],
                                              depth_percent=res['dept_perc'],
                                              table_percent=res['table_perc'],
                                              # fancy_color=res['fancy_color'],
                                              # fancy_color_intensity=res['fancy_color_intensity'],
                                              # fancy_color_overtone=res['fancy_color_overtone'],
                                              # desc_comments=res['desc_comments'],
                                              # memo_status=res['memo_status'],
                                              # inscription=res['inscription'],
                                              # location=res['location'],
                                              certificate_file=res['certificate_file'],
                                              image_url=res['diamond_image'] if res['diamond_image'] != "" or res[
                                                  'diamond_image'] != "nan" else "",
                                              video_url=video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
                                              image_file_url=res['diamond_image'] if res['diamond_image'] != "" or res[
                                                  'diamond_image'] != "nan" else "",
                                              video_file_url=video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
                                              price_per_ct=res['price_per_ct'],
                                              original_total_price=res['original_total_price'],
                                              exchange_rate=res['exchange_rate'],
                                              convert_price=res['convert_price'],
                                              plus_markup_price_ct=res['plus_markup_price_ct'],
                                              plus_markup_price=res['plus_markup_price'],
                                              total_sales_price=res['final_price'],
                                              total_sales_price_in_currency=res['final_price'],
                                              price_per_ct_pound=res['price_per_ct_pound'],
                                              plus_markup_price_ct_pound=res['plus_markup_price_ct_pound'],
                                              original_total_price_pound=res['original_total_price_pound'],
                                              final_price_pound=res['final_price_pound'],
                                              price_per_ct_cad=res['price_per_ct_cad'],
                                              plus_markup_price_ct_cad=res['plus_markup_price_ct_cad'],
                                              original_total_price_cad=res['original_total_price_cad'],
                                              final_price_cad=res['final_price_cad'],
                                              availability=res['availability'],
                                              # girdle=res['girdle'],
                                              # girdle_min=res['girdle_min'],
                                              # girdle_max=res['girdle_max'],
                                              # girdle_perc=res['girdle_perc'],
                                              # girdle_condition=res['girdle_condition'],
                                              # culet=res['culet'],
                                              # culet_condition=res['culet_condition'],
                                              # crown_angle=res['crown_angle'],
                                              # crown_height=res['crown_height'],
                                              # pavilion_depth=res['pavilion_depth'],
                                              # pavilion_angle=res['pavilion_angle'],
                                              # origin=res['origin'],
                                              # seller_name=res['seller_name'],
                                              # city=res['city'],
                                              # state=res['state'],
                                              # country=res['country'],
                                              # is_match_pair_separable=res['is_match_pair_separable'],
                                              # member_comments=res['member_comments'],
                                              # supplier_country=res['supplier_country'],
                                              # milky=res['milky'],
                                              diamond_quantity=res['diamond_quantity'],
                                              diamond_type=diamond_type_name,
                                              supplier_id=res['supplier_id'],
                                              data_entry_point=res['data_entry_point'],
                                              inserted_on=res['created_at'],
                                              updated_at=res['updated_at'],
                                              stock_number=res['stock_number'],
                                              is_show=res['is_show'],
                                              currency_code="USD",
                                              currency_symbol="$",
                                              diamond_feed=supplierObj.vendor_name,
                                              special_price="",
                                              QuickShip=res['quick_ship'] if res['quick_ship'] != "" else "N",
                                              Appointment=res['appointment'] if res['appointment'] != "" else "N",
                                              final_discount_price= discount_price, #res['final_discount_price'],
                                              vault_discount=str(supplierObj.is_vault_discount)
                                              ))

                # counting_per_page_record = diamond_query.count()

                return {"status": 200, 'diamond': output, 'data_count': total_found_diamonds,
                        'diamonds_returned': records_limit,
                        'page_no': page}

        # except Exception as ex:
        #     raise GraphQLError(('Error! Code: {c}, Message, {m}'.format(c = type(ex).__name__, m = str(ex))))
        # return {'error': ex}

        # else:
        return None

    # Fillter diamond

    # def resolve_live_diamond_data(self, info, page=None, shapes=None, carat=None, clarity=None, color=None, polish=None,
    #                              symmetry=None, fluoroscence=None, price=None, depth_per=None, table=None, ratio=None,
    #                              cut=None, lab=None, diamond_type=None, final_price=None,
    #                              order_by=None, sort_by=None, diamond_id=None, quickship=None, appointment=None, supplier_name=None, both_quantity=None, vault_discount=None):

    #     # activeapiObj = """select * from `{0}api_details` where api_name = 'Filter diamond data' and is_active = 1""".format(
    #     #     table_prefix)
    #     cursor = connections['primary'].cursor()
    #     # enable = cursor.execute(activeapiObj)
    #     enable = 1
    #     if enable == 1:

    #         user = info.context.user
    #         if user.is_anonymous:
    #             raise Exception('Authentication Failure!')

    #         og_shapes_list = ['Round', 'Princess', 'Cushion', 'Radiant', 'Asscher', 'Emerald', 'Oval', 'Pear',
    #                           'Marquise', ]

    #         regular_color_codes_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    #                                     'L']  # Only White Diamonds in this project

    #         diamond_cuts_list = ['Excellent','Very Good','Good']

    #         labgrown_diamond_cuts_list = ['Ideal','Excellent','Very Good','Good']

    #         diamond_clarity_list = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF', 'FL']

    #         diamond_fluoroscence_list = ['None', 'Faint', 'Medium', 'Strong']

    #         diamond_polish_list = ['Fair', 'Good', 'Very Good', 'Excellent']

    #         diamond_symmetry_list = ['Fair', 'Good', 'Very Good', 'Excellent']

    #         diamond_labs_list = ['GIA', 'IGI']

    #         diamond_carat_min = 0.25
    #         diamond_carat_max = 5.25
    #         diamond_price_min = 100
    #         diamond_price_max = 1000000

    #         diamond_depth_min = 40
    #         diamond_depth_max = 90

    #         diamond_table_min = 40
    #         diamond_table_max = 90

    #         diamond_min_ratio = 0.9
    #         diamond_max_ratio = 2.75

    #         diamond_diff_labs_list = ['white', 'lab']
    #         order_by_price = 'final_price'

    #         shape_list = list(str(shapes).title().strip().replace(', ', ',').split(","))
    #         clarity_list = list(str(clarity).upper().strip().replace(', ', ',').split(","))
    #         color_list = list(str(color).upper().strip().replace(', ', ',').split(","))
    #         cut_list = list(str(cut).title().strip().replace(', ', ',').split(","))
    #         polish_list = list(str(polish).title().strip().replace(', ', ',').split(","))
    #         symmetry_list = list(str(symmetry).title().strip().replace(', ', ',').split(","))
    #         lab_list = list(str(lab).upper().strip().replace(', ', ',').split(","))
    #         fluoroscence_list = list(str(fluoroscence).title().strip().replace(', ', ',').split(","))
    #         carat_tuple = tuple(str(carat).strip().replace(', ', ',').split(","))
    #         price_tuple = tuple(str(price).strip().replace(', ', ',').split(","))
    #         depth_per_tuple = tuple(str(depth_per).strip().replace(', ', ',').split(","))
    #         table_tuple = tuple(str(table).strip().replace(', ', ',').split(","))
    #         ratio_tuple = tuple(str(ratio).strip().replace(', ', ',').split(","))
    #         diamond_type_list = list(str(diamond_type).lower().strip().replace(', ', ',').split(","))
    #         final_price_range = tuple(str(final_price).strip().replace(', ', ',').split(","))
    #         diamond_id_send = str(diamond_id).strip().replace(', ', ',').replace(' ', '')
    #         quickship_add = str(quickship).strip().replace(', ', ',').replace(' ', '')
    #         appointment_add = str(appointment).strip().replace(', ', ',').replace(' ', '')
    #         supplier_get_name = str(supplier_name).strip().replace(', ', ',')
    #         quantity_name = str(both_quantity).strip().replace(', ', ',').title()
    #         vault_get_discount = str(vault_discount).strip().replace(', ', ',').title()

    #         if page == None:
    #             page = 1

    #         diamond_query = None
    #         output = []

    #         constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'"""
    #         cursor.execute(constant_isenable_query)
    #         constant_get_isenable = cursor.fetchone()

    #         constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'"""
    #         cursor.execute(constant_isenable_vault_query)
    #         constant_get_vault_isenable = cursor.fetchone()

    #         show_diamond_count = 20
    #         if page == None:
    #             print("Please define Page no.")
    #             # diamond_query = DiamondDetails.objects.all().order_by(order_by_price)[0:20]
    #         else:
    #             vault_discount_query = """SELECT `id` FROM `websr_supplier_details` where `is_vault_discount` = 1""".format(
    #                 vault_get_discount)
    #             cursor.execute(vault_discount_query)
    #             vault_discount_id = cursor.fetchall()

    #             supplier_name_query = """SELECT `id` FROM `websr_supplier_details` where `supplier_name` = '{0}'""".format(supplier_get_name)
    #             cursor.execute(supplier_name_query)
    #             suplier_get_id = cursor.fetchone()

    #             if vault_get_discount == "Yes" and str(vault_get_discount).strip() != "" and vault_get_discount is not None:
    #                 if quantity_name == "Yes" and str(quantity_name).strip() != "" and quantity_name is not None:
    #                     quantity_query = "dd.diamond_quantity IN (1, 0)"
    #                     # quantity_query = "dd.diamond_quantity IN (1)"
    #                 else:
    #                     quantity_query = "dd.diamond_quantity = 1"
    #             else:
    #                 quantity_query = "dd.diamond_quantity = 1"


    #             # Shape filter
    #             if shapes and str(shapes).strip() != "" and shapes is not None:
    #                 if len(shapes) > 0:
    #                     shape_list_new = ", ".join("'{0}'".format(w) for w in shape_list)
    #                     shape_query = "dd.`shape` in (" + str(shape_list_new) + ")"
    #             else:
    #                 shape_list_new = ", ".join("'{0}'".format(w) for w in og_shapes_list)
    #                 shape_query = "dd.`shape` in (" + str(shape_list_new) + ")"

    #             # carat filter
    #             if carat and str(carat).strip() != "" and carat is not None:
    #                 carat_query = "(dd.`carat_weight` >=" + str(carat_tuple[0]) + " && dd.`carat_weight` <=" + str(
    #                     carat_tuple[1]) + ")"
    #             else:
    #                 carat_query = "(dd.`carat_weight` >=" + str(diamond_carat_min) + " && dd.`carat_weight` <=" + str(
    #                     diamond_carat_max) + ")"

    #             # clarity filter
    #             if clarity and str(clarity).strip() != "" and clarity is not None:
    #                 if len(clarity) > 0:
    #                     clarity_list_new = ", ".join("'{0}'".format(c) for c in clarity_list)
    #                     clarity_query = "dd.`clarity` in (" + str(clarity_list_new) + ")"
    #             else:
    #                 clarity_list_new = ", ".join("'{0}'".format(c) for c in diamond_clarity_list)
    #                 clarity_query = "dd.`clarity` in (" + str(clarity_list_new) + ")"

    #             # print(clarity_query)
    #             # color filter
    #             if color and str(color).strip() != "" and color is not None:
    #                 if len(color) > 0:
    #                     colors_list_new = ", ".join("'{0}'".format(c) for c in color_list)
    #                     color_query = "dd.`color` in (" + str(colors_list_new) + ")"
    #             else:
    #                 colors_list_new = ", ".join("'{0}'".format(c) for c in regular_color_codes_list)
    #                 color_query = "dd.`color` in (" + str(colors_list_new) + ")"

    #             # polish filter
    #             if polish and str(polish).strip() != "" and polish is not None:
    #                 if len(polish) > 0:
    #                     polish_list_new = ", ".join("'{0}'".format(c) for c in polish_list)
    #                     polish_query = "dd.`polish` in (" + str(polish_list_new).replace("_", " ") + ")"
    #             else:
    #                 polish_list_new = ", ".join("'{0}'".format(c) for c in diamond_polish_list)
    #                 polish_query = "dd.`polish` in (" + str(polish_list_new).replace("_", " ") + ")"

    #             # symmetry filter
    #             if symmetry and str(symmetry).strip() != "" and symmetry is not None:
    #                 if len(symmetry) > 0:
    #                     symmetry_list_new = ", ".join("'{0}'".format(c) for c in symmetry_list)
    #                     symmetry_query = "dd.`symmetry` in (" + str(symmetry_list_new).replace("_", " ") + ")"
    #             else:
    #                 symmetry_list_new = ", ".join("'{0}'".format(c) for c in diamond_symmetry_list)
    #                 symmetry_query = "dd.`symmetry` in (" + str(symmetry_list_new).replace("_", " ") + ")"

    #             # fluoroscence filter
    #             if fluoroscence and str(fluoroscence).strip() != "" and fluoroscence is not None:
    #                 fluor_list_new = ", ".join("'{0}'".format(w) for w in fluoroscence_list)
    #                 fluorescence_query = "dd.`flour_intensity` in (" + str(fluor_list_new) + ")"
    #             else:
    #                 fluor_list_new = ", ".join("'{0}'".format(w) for w in diamond_fluoroscence_list)
    #                 fluorescence_query = "dd.`flour_intensity` in (" + str(fluor_list_new) + ")"

    #             # depth perc filter
    #             if depth_per and str(depth_per).strip() != "" and depth_per is not None:
    #                 depth_perc_query = "(dd.`dept_perc` BETWEEN " + str(depth_per_tuple[0]) + " AND " + str(
    #                     depth_per_tuple[1]) + ")"
    #             else:
    #                 depth_perc_query = "(dd.`dept_perc` BETWEEN " + str(diamond_depth_min) + " AND " + str(
    #                     diamond_depth_max) + ")"

    #             # table filter
    #             if table and str(table).strip() != "" and table is not None:
    #                 table_perc_query = "(dd.`table_perc` BETWEEN " + str(table_tuple[0]) + " AND " + str(
    #                     table_tuple[1]) + ")"
    #             else:
    #                 table_perc_query = "(dd.`table_perc` BETWEEN " + str(diamond_table_min) + " AND " + str(
    #                     diamond_table_max) + ")"

    #             # ratio filter
    #             if ratio and str(ratio).strip() != "" and ratio is not None:
    #                 ratio_query = "(dd.`ratio` BETWEEN " + str(ratio_tuple[0]) + " AND " + str(ratio_tuple[1]) + ")"
    #             else:
    #                 ratio_query = "(dd.`ratio` BETWEEN " + str(diamond_min_ratio) + " AND " + str(
    #                     diamond_max_ratio) + ")"

    #             # lab filter
    #             if lab and str(lab).strip() != "" and lab is not None:
    #                 lab_list_new = ", ".join("'{0}'".format(c) for c in lab_list)
    #                 lab_query = "dd.`lab` in (" + str(lab_list_new).replace("_", " ") + ")"
    #             else:
    #                 lab_list_new = ", ".join("'{0}'".format(c) for c in diamond_labs_list)
    #                 lab_query = "dd.`lab` in (" + str(lab_list_new).replace("_", " ") + ")"

    #             # cut filter
    #             cut_query = ""
    #             if cut and str(cut).strip() != "" and cut is not None:
    #                 if len(cut) > 0:
    #                     if str(diamond_type).strip().lower() == "white" or str(
    #                             diamond_type).strip().lower() == "natural":
    #                         cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
    #                         cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
    #                     elif str(diamond_type).strip().lower() == "lab" or str(
    #                             diamond_type).strip().lower() == "lab-grown":
    #                         cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
    #                         cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
    #             else:
    #                 if str(diamond_type).strip().lower() == "white" or str(
    #                         diamond_type).strip().lower() == "natural":
    #                     cuts_list_new = ", ".join("'{0}'".format(c) for c in diamond_cuts_list)
    #                     cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"
    #                 elif str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown":
    #                     cuts_list_new = ", ".join("'{0}'".format(c) for c in labgrown_diamond_cuts_list)
    #                     cut_query = "dd.`cut` in (" + str(cuts_list_new).replace("_", " ") + ")"

    #             # diamond type filter

    #             if diamond_type and str(diamond_type).strip() != "" and diamond_type is not None:
    #                 if str(diamond_type).strip().lower() == "white" or str(diamond_type).strip().lower() == "natural":
    #                     diamond_type_query = "dd.`diamond_type`='white'"
    #                 elif str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown":
    #                     diamond_type_query = "dd.`diamond_type`='lab'"
    #             else:
    #                 diamond_type_query = "dd.`diamond_type` in ('white', 'lab')"

    #             # print(diamond_type_query)
    #             # quickship filter
    #             quickship_query = ""
    #             if quickship and str(quickship).strip() != "" and quickship is not None:
    #                 if str(quickship).strip().lower() == 'y' or str(quickship).strip().lower() == 'yes':
    #                     quickship_query = "AND t2.`quick_ship`= 'Y'"
    #                 if str(quickship).strip().lower() == 'n' or str(quickship).strip().lower() == 'No':
    #                     quickship_query = "AND t2.`quick_ship`= 'N' or t2.`quick_ship`= ''"

    #             # appointment filter
    #             appointment_query = ""
    #             if appointment and str(appointment).strip() != "" and appointment is not None:
    #                 if str(appointment).strip().lower() == 'y' or str(appointment).strip().lower() == 'yes':
    #                     appointment_query = "AND t2.`appointment`= 'Y'"
    #                 if str(appointment).strip().lower() == 'n' or str(appointment).strip().lower() == 'No':
    #                     appointment_query = "AND t2.`appointment`= 'N' or t2.`appointment`= ''"


    #             # # price per carat
    #             # if final_price and str(final_price).strip() != "" and final_price is not None:
    #             #     price_query = "(dd.`final_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
    #             #         final_price_range[1]) + ")"
    #             # else:
    #             #     price_query = "(dd.`final_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
    #             #         diamond_price_max) + ")"

    #             # sort_direct_query = "ORDER BY dd.`final_price` ASC"
    #             # if sort_by and str(sort_by).strip() != "":
    #             #     if str(order_by).lower() == "price":
    #             #         sort_order_by = "dd.`final_price`"
    #             #         sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #             # price per carat
    #             price_query = ""

    #             if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
    #                     diamond_type).strip().lower() == "lab-grown"):
    #                 if final_price and str(final_price).strip() != "" and final_price is not None:
    #                     price_query = "(dd.`final_discount_price` BETWEEN " + str(
    #                         final_price_range[0]) + " AND " + str(
    #                         final_price_range[1]) + ")"
    #                 else:
    #                     price_query = "(dd.`final_discount_price` BETWEEN " + str(
    #                         diamond_price_min) + " AND " + str(
    #                         diamond_price_max) + ")"
    #             else:
    #                 if final_price and str(final_price).strip() != "" and final_price is not None:
    #                     price_query = "(dd.`final_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(final_price_range[1]) + ")"
    #                 else:
    #                     price_query = "(dd.`final_price` BETWEEN " + str(diamond_price_min) + " AND " + str(diamond_price_max) + ")"

    #             sort_direct_query = "ORDER BY dd.`final_price` ASC"
    #             if sort_by and str(sort_by).strip() != "":
    #                 if str(order_by).lower() == "price":
    #                     sort_order_by = ""
    #                     if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
    #                             diamond_type).strip().lower() == "lab-grown"):
    #                         sort_order_by = "dd.`final_discount_price`"
    #                     else:
    #                         sort_order_by = "dd.`final_price`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "carat":
    #                     sort_order_by = "dd.`carat_weight`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "color":
    #                     sort_order_by = "dd.`color`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "clarity_index":
    #                     if str(sort_by).strip().lower() == "desc":
    #                         clarity_org_list = diamond_clarity_list
    #                         comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(dd.`clarity`,"+str(comma_sep_clarity) + ")"
    #                     else:
    #                         clarity_asc_list = diamond_clarity_list
    #                         clarity_org_list = clarity_asc_list[::-1]
    #                         comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(dd.`clarity`,"+str(comma_sep_clarity) + ")"
    #                 elif str(order_by).lower() == "cut_index":
    #                     if str(sort_by).strip().lower() == "desc":
    #                         cut_org_list = diamond_cuts_list + ['NA']
    #                         if str(diamond_type).strip().lower() == "lab" or str(
    #                                 diamond_type).strip().lower() == "lab-grown":
    #                             cut_org_list = labgrown_diamond_cuts_list
    #                         comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(dd.`cut`,"+str(comma_sep_cut)+")"
    #                     else:
    #                         cut_asc_list = diamond_cuts_list
    #                         if str(diamond_type).strip().lower() == "lab" or str(
    #                                 diamond_type).strip().lower() == "lab-grown":
    #                             cut_asc_list = labgrown_diamond_cuts_list
    #                         cut_org_list = cut_asc_list[::-1]
    #                         comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(dd.`cut`,"+str(comma_sep_cut) + ")"
    #                     # sort_by = "dd.`cut`"
    #                     # sort_direct_query = "ORDER BY "+str(sort_by)+" "+str(sort_direction).strip()
    #                 elif str(order_by).lower() == "shape":
    #                     sort_order_by = "dd.`shape`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "polish":
    #                     sort_order_by = "dd.`polish`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "symmetry":
    #                     sort_order_by = "dd.`symmetry`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "flour":
    #                     sort_order_by = "dd.`flour_intensity`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "table":
    #                     sort_order_by = "dd.`table_perc`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "depth":
    #                     sort_order_by = "dd.`dept_perc`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "ratio":
    #                     sort_order_by = "dd.`ratio`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
    #                 elif str(order_by).lower() == "quickship":
    #                     if str(sort_by).strip().lower() == "desc":
    #                         quickship_org_list = ['Y', 'N']
    #                         comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(t2.`quick_ship`,"+str(comma_sep_quickship) + ")"
    #                     else:
    #                         quickship_org_list = ['N', 'Y']
    #                         comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(t2.`quick_ship`," + str(comma_sep_quickship) + ")"
    #                 elif str(order_by).lower() == "appointment":
    #                     if str(sort_by).strip().lower() == "desc":
    #                         appointment_org_list = ['Y', 'N']
    #                         comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(t2.`appointment`,"+str(comma_sep_appointment) + ")"
    #                     else:
    #                         appointment_org_list = ['N', 'Y']
    #                         comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
    #                         sort_direct_query = "ORDER BY FIELD(t2.`appointment`," + str(comma_sep_appointment) + ")"
    #                 elif str(order_by).lower() == "diamond_quantity":
    #                     sort_order_by = "dd.`diamond_quantity`"
    #                     sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()



    #             # PAGE NUMBER
    #             page_num_query = True
    #             records_limit = 20

    #             if records_limit and str(records_limit).strip() != "":
    #                 if page and str(page).strip() != "":
    #                     start_pos_value = (int(page) - 1) * records_limit
    #                 else:
    #                     page_number = 1
    #                     start_pos_value = (int(page_number) - 1) * records_limit
    #                 page_num_query = "LIMIT " + str(start_pos_value) + ", " + str(records_limit)

    #             supplier_query = """SELECT `id`, `supplier_name` FROM `websr_supplier_details` WHERE `is_allow`=1 AND `is_enabled`=1"""
    #             cursor.execute(supplier_query)
    #             columns = [column[0] for column in cursor.description]
    #             suppliers_dict = {}
    #             supp_ids = ""
    #             for row in cursor.fetchall():
    #                 suppliers_dict['supp_' + str(row[0])] = str(row[1])
    #                 supp_ids += str(row[0]) + ","

    #             # supp_ids = str(supp_ids).rstrip(",")
    #             if vault_get_discount == "Yes" and str(vault_get_discount).strip() != "" and vault_get_discount is not None:
    #                 # supplier_list_new = ", ".join("'{0}'".format(w) for w in fluoroscence_list)
    #                 j = [item[0] for item in vault_discount_id]
    #                 supp_ids = str(",".join(list(map(str, j))))
    #             else:
    #                 # fluor_list_new = ", ".join("'{0}'".format(w) for w in diamond_fluoroscence_list)
    #                 # supplier_id_query = ""
    #                 supp_ids = str(supp_ids).rstrip(",")

    #             # count_query = """SELECT  count(*) FROM websr_diamond_details_primary as dd
    #             #              JOIN websr_diamond_details_secondary t2
    #             #              ON dd.diamond_id = t2.diamond_id WHERE dd.`diamond_quantity`='1' AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4} AND {5}
    #             #             AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14} {15};""".format(
    #             #             "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
    #             #             color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
    #             #             table_perc_query, ratio_query, diamond_type_query,sort_direct_query)
    #             #
    #             # print(count_query)

    #             # count_query = """SELECT count(*) FROM `{0}diamond_details_view` as dd
    #             #                             WHERE dd.`diamond_quantity`='1' AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4}
    #             #                             AND {5} AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14} {15} """.format(
    #             #     "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
    #             #     color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
    #             #     table_perc_query, ratio_query, diamond_type_query,sort_direct_query)
    #             # # print(count_query)
    #             # cursor.execute(count_query)
    #             # diamond_count = cursor.fetchall()
    #             if diamond_id != None or diamond_id != "" or diamond_id != "":
    #                 diamond_query = "dd.diamond_id NOT IN('{0}') AND".format(diamond_id_send)
    #             else:
    #                 diamond_query = "dd.diamond_id NOT IN('')"

    #             select_query = """SELECT  SQL_CALC_FOUND_ROWS * FROM websr_diamond_details_primary as dd
    #                          JOIN websr_diamond_details_secondary t2
    #                          ON dd.diamond_id = t2.diamond_id
    #                         WHERE {17} {20} AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4} AND {5}
    #                         AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14} {18} {19} {15} {16}""".format(
    #                 "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
    #                 color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
    #                 table_perc_query, ratio_query, diamond_type_query,
    #                 sort_direct_query, page_num_query, diamond_query, quickship_query, appointment_query, quantity_query)
    #             # print(select_query)
    #             # select_query = """SELECT SQL_CALC_FOUND_ROWS * FROM `{0}diamond_details_view` as dd
    #             #             WHERE dd.`diamond_quantity`='1' AND dd.`supplier_id` IN ({1}) AND {2} AND {3} AND {4} AND {5}
    #             #             AND {6} AND {7} AND {8} AND {9} AND {10} AND {11} AND {12} AND {13} AND {14} {15} {16}""".format(
    #             #     "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
    #             #     color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
    #             #     table_perc_query, ratio_query, diamond_type_query,
    #             #     sort_direct_query, page_num_query)

    #             # print(select_query)

    #             cursor.execute(select_query)
    #             columns = [column[0] for column in cursor.description]
    #             diamond_list = []
    #             for row in cursor.fetchall():
    #                 diamond_list.append(dict(zip(columns, row)))

    #             cursor.execute("SELECT FOUND_ROWS()")
    #             rows_count_result = cursor.fetchone()
    #             total_found_diamonds = rows_count_result[0]

    #             if len(diamond_list) < records_limit:
    #                 records_limit = len(diamond_list)

    #             for i, res in enumerate(diamond_list):
    #                 supplierObj = SupplierDetails.objects.using('primary').get(id=res['supplier_id'])
    #                 if str(res['diamond_type']).strip().lower() == "white":
    #                     diamond_type_name = "White"
    #                 elif str(res['diamond_type']).strip().lower() == "lab":
    #                     diamond_type_name = "lab-grown"
    #                 # else:
    #                 #     diamond_type_name = res['diamond_type']
    #                 video_file_url = ''
    #                 if res['diamond_video'] != "" or res['diamond_video'] != "nan":
    #                     if "#VALUE!" not in res['diamond_video']:
    #                         video_file_url = res['diamond_video']
    #                 else:
    #                     video_file_url = ""

    #                 discount_price = ""
    #                 if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
    #                         diamond_type).strip().lower() == "lab-grown"):
    #                     discount_price = res['final_discount_price']
    #                 else:
    #                     discount_price = res['final_price']
    #                 output.append(Diamond(diamond_id=res['diamond_id'],
    #                                           shape=res['shape'],
    #                                           color=res['color'],
    #                                           clarity=res['clarity'],
    #                                           size=res['carat_weight'],
    #                                           lab=res['lab'],
    #                                           cut=res['cut'],
    #                                           polish=res['polish'],
    #                                           symmetry=res['symmetry'],
    #                                           fluor_intensity=res['flour_intensity'],
    #                                           cert_num=res['certificate_number'],
    #                                           measurement=res['measurement'],
    #                                           meas_length=res['length'],
    #                                           meas_width=res['width'],
    #                                           meas_depth=res['depth'],
    #                                           ratio=res['ratio'],
    #                                           depth_percent=res['dept_perc'],
    #                                           table_percent=res['table_perc'],
    #                                           fancy_color=res['fancy_color'],
    #                                           fancy_color_intensity=res['fancy_color_intensity'],
    #                                           fancy_color_overtone=res['fancy_color_overtone'],
    #                                           desc_comments=res['desc_comments'],
    #                                           memo_status=res['memo_status'],
    #                                           inscription=res['inscription'],
    #                                           location=res['location'],
    #                                           certificate_file=res['certificate_file'],
    #                                           image_url=res['diamond_image'] if res['diamond_image'] != "" or res['diamond_image'] != "nan" else "",
    #                                           video_url=video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
    #                                           image_file_url=res['diamond_image'] if res['diamond_image'] != "" or res['diamond_image'] != "nan" else "",
    #                                           video_file_url=video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
    #                                           price_per_ct=res['price_per_ct'],
    #                                           original_total_price=res['original_total_price'],
    #                                           exchange_rate=res['exchange_rate'],
    #                                           convert_price=res['convert_price'],
    #                                           plus_markup_price_ct=res['plus_markup_price_ct'],
    #                                           plus_markup_price=res['plus_markup_price'],
    #                                           total_sales_price=res['final_price'],
    #                                           total_sales_price_in_currency=res['final_price'],
    #                                           price_per_ct_pound=res['price_per_ct_pound'],
    #                                           plus_markup_price_ct_pound=res['plus_markup_price_ct_pound'],
    #                                           original_total_price_pound=res['original_total_price_pound'],
    #                                           final_price_pound=res['final_price_pound'],
    #                                           price_per_ct_cad=res['price_per_ct_cad'],
    #                                           plus_markup_price_ct_cad=res['plus_markup_price_ct_cad'],
    #                                           original_total_price_cad=res['original_total_price_cad'],
    #                                           final_price_cad=res['final_price_cad'],
    #                                           availability=res['availability'],
    #                                           girdle=res['girdle'],
    #                                           girdle_min=res['girdle_min'],
    #                                           girdle_max=res['girdle_max'],
    #                                           girdle_perc=res['girdle_perc'],
    #                                           girdle_condition=res['girdle_condition'],
    #                                           culet=res['culet'],
    #                                           culet_condition=res['culet_condition'],
    #                                           crown_angle=res['crown_angle'],
    #                                           crown_height=res['crown_height'],
    #                                           pavilion_depth=res['pavilion_depth'],
    #                                           pavilion_angle=res['pavilion_angle'],
    #                                           origin=res['origin'],
    #                                           seller_name=res['seller_name'],
    #                                           city=res['city'],
    #                                           state=res['state'],
    #                                           country=res['country'],
    #                                           is_match_pair_separable=res['is_match_pair_separable'],
    #                                           member_comments=res['member_comments'],
    #                                           supplier_country=res['supplier_country'],
    #                                           milky=res['milky'],
    #                                           diamond_quantity=res['diamond_quantity'],
    #                                           diamond_type=diamond_type_name,
    #                                           supplier_id=res['supplier_id'],
    #                                           data_entry_point=res['data_entry_point'],
    #                                           inserted_on=res['created_at'],
    #                                           updated_at=res['updated_at'],
    #                                           stock_number=res['stock_number'],
    #                                           is_show=res['is_show'],
    #                                           currency_code="USD",
    #                                           currency_symbol="$",
    #                                           diamond_feed=supplierObj.vendor_name,
    #                                           special_price="",
    #                                           QuickShip=res['quick_ship'] if res['quick_ship'] != "" else "N",
    #                                           Appointment=res['appointment'] if res['appointment'] != "" else "N",
    #                                           final_discount_price=discount_price,
    #                                           vault_discount=str(supplierObj.is_vault_discount)
    #                                           ))

    #             # counting_per_page_record = diamond_query.count()

    #             return {"status": 200,'diamond': output, 'data_count': total_found_diamonds, 'diamonds_returned': records_limit,
    #                     'page_no': page}

    #     # except Exception as ex:
    #     #     raise GraphQLError(('Error! Code: {c}, Message, {m}'.format(c = type(ex).__name__, m = str(ex))))
    #         # return {'error': ex}

    #         # else:
    #     return None

    def resolve_live_alldiamond(root, info, page=None, **kwargs):
        activeapiObj = """select * from `{0}api_details` where api_name = 'All diamond' and is_active = 1""".format(
            table_prefix)
        cursor = connections['primary'].cursor()
        enable = cursor.execute(activeapiObj)
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            # Querying a list
            if page:
                diamond_query = None
                show_diamond_count = 500
                if page == None or str(page).strip() == "":
                    diamond_query = DiamondDetails.objects.using('primary').all()[0:20]
                else:
                    pg_num = (int(page) - 1) * show_diamond_count
                    add = pg_num + show_diamond_count
                    diamond_query = DiamondDetails.objects.using('primary').all()[pg_num:add]
                return diamond_query
            return DiamondDetails.objects.using('primary').all()[0:20]
        else:
            return None

    def resolve_live_diamond_by_id(root, info, diamond_id=None, only_not_sold_quantity=None, diamond_type=None):
        # activeapiObj = """select * from `{0}api_details` where api_name = 'Find diamond by id' and is_active = 1""".format(
        #     table_prefix)
        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            diamond_details = []
            try:
                diamond_id_list = tuple(str(diamond_id).strip().replace(', ', ',').split(","))
                quantity_name = str(only_not_sold_quantity).strip().replace(', ', ',').title()

                if quantity_name == "Yes" and str(quantity_name).strip() != "" and quantity_name is not None:
                    quantity_query = "dd.diamond_quantity = 1"
                else:
                    quantity_query = "(dd.`diamond_quantity`='1' or (sd.is_vault_discount=1 and dd.`diamond_quantity` IN ('1', '0')))"

                output = []
                results = None
                diamond_list = []
                diamond_typ = None
                if diamond_type == None:
                    diamond_typ = ""
                elif diamond_type != None:
                    diamond_typ = """AND dd.`diamond_type` = '{0}'""".format(diamond_type)
                if diamond_id:
                    if len(diamond_id_list) > 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                    LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                    WHERE {2} AND sd.`is_enabled`=1 AND dd.`diamond_id`in {1}""".format(
                            "websr_", diamond_id_list, quantity_query) + diamond_typ
                        cursor.execute(select_query)

                    elif len(diamond_id_list) == 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                       LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                        WHERE {2} AND sd.`is_enabled`=1 AND dd.`diamond_id`='{1}'""".format(
                            "websr_", diamond_id_list[0], quantity_query) + diamond_typ
                        cursor.execute(select_query)
                    columns = [column[0] for column in cursor.description]

                    for row in cursor.fetchall():
                        diamond_list.append(dict(zip(columns, row)))

                constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'"""
                cursor.execute(constant_isenable_query)
                constant_get_isenable = cursor.fetchone()

                constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'"""
                cursor.execute(constant_isenable_vault_query)
                constant_get_vault_isenable = cursor.fetchone()

                for i, res in enumerate(diamond_list):
                    supplierObj = SupplierDetails.objects.using('primary').get(id=res['supplier_id'])
                    if str(res['diamond_type']).strip().lower() == "white":
                        diamond_type_name = "White"
                    elif str(res['diamond_type']).strip().lower() == "lab":
                        diamond_type_name = "lab-grown"
                    # else:
                    #     diamond_type_name = res['diamond_type']
                    video_file_url = ''
                    if res['diamond_video'] != "" or res['diamond_video'] != "nan":
                        if "#VALUE!" not in res['diamond_video']:
                            video_file_url = res['diamond_video']
                    else:
                        video_file_url = ""

                    discount_price = ""
                    if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(res['diamond_type']).strip().lower() == "lab" or str(
                            res['diamond_type']).strip().lower() == "lab-grown"):
                        discount_price = res['final_discount_price']
                    else:
                        discount_price = res['final_price']
                    output.append(Diamond(diamond_id=res['diamond_id'],
                                              shape=res['shape'],
                                              color=res['color'],
                                              clarity=res['clarity'],
                                              size=res['carat_weight'],
                                              lab=res['lab'],
                                              cut=res['cut'],
                                              polish=res['polish'],
                                              symmetry=res['symmetry'],
                                              fluor_intensity=res['flour_intensity'],
                                              cert_num=res['certificate_number'],
                                              measurement=res['measurement'],
                                              meas_length=res['length'],
                                              meas_width=res['width'],
                                              meas_depth=res['depth'],
                                              ratio=res['ratio'],
                                              depth_percent=res['dept_perc'],
                                              table_percent=res['table_perc'],
                                              fancy_color=res['fancy_color'],
                                              fancy_color_intensity=res['fancy_color_intensity'],
                                              fancy_color_overtone=res['fancy_color_overtone'],
                                              desc_comments=res['desc_comments'],
                                              memo_status=res['memo_status'],
                                              inscription=res['inscription'],
                                              location=res['location'],
                                              certificate_file=res['certificate_file'],
                                              image_url=res['diamond_image'] if res['diamond_image'] != "" or res['diamond_image'] != "nan" else "",
                                              video_url= video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
                                              image_file_url=res['diamond_image'] if res['diamond_image'] != "" or res['diamond_image'] != "nan" else "",
                                              video_file_url= video_file_url, #res['diamond_video'] if res['diamond_video'] != "" or res['diamond_video'] != "nan" else "",
                                              price_per_ct=res['price_per_ct'],
                                              original_total_price=res['original_total_price'],
                                              exchange_rate=res['exchange_rate'],
                                              convert_price=res['convert_price'],
                                              plus_markup_price_ct=res['plus_markup_price_ct'],
                                              plus_markup_price=res['plus_markup_price'],
                                              total_sales_price=res['final_price'],
                                              total_sales_price_in_currency=res['final_price'],
                                              price_per_ct_pound=res['price_per_ct_pound'],
                                              plus_markup_price_ct_pound=res['plus_markup_price_ct_pound'],
                                              original_total_price_pound=res['original_total_price_pound'],
                                              final_price_pound=res['final_price_pound'],
                                              price_per_ct_cad=res['price_per_ct_cad'],
                                              plus_markup_price_ct_cad=res['plus_markup_price_ct_cad'],
                                              original_total_price_cad=res['original_total_price_cad'],
                                              final_price_cad=res['final_price_cad'],
                                              availability=res['availability'],
                                              girdle=res['girdle'],
                                              girdle_min=res['girdle_min'],
                                              girdle_max=res['girdle_max'],
                                              girdle_perc=res['girdle_perc'],
                                              girdle_condition=res['girdle_condition'],
                                              culet=res['culet'],
                                              culet_condition=res['culet_condition'],
                                              crown_angle=res['crown_angle'],
                                              crown_height=res['crown_height'],
                                              pavilion_depth=res['pavilion_depth'],
                                              pavilion_angle=res['pavilion_angle'],
                                              origin=res['origin'],
                                              seller_name=res['seller_name'],
                                              city=res['city'],
                                              state=res['state'],
                                              country=res['country'],
                                              is_match_pair_separable=res['is_match_pair_separable'],
                                              member_comments=res['member_comments'],
                                              supplier_country=res['supplier_country'],
                                              milky=res['milky'],
                                              diamond_quantity=res['diamond_quantity'],
                                              diamond_type=diamond_type_name,
                                              supplier_id=res['supplier_id'],
                                              data_entry_point=res['data_entry_point'],
                                              inserted_on=res['created_at'],
                                              updated_at=res['updated_at'],
                                              stock_number=res['stock_number'],
                                              is_show=res['is_show'],
                                              currency_code="USD",
                                              currency_symbol="$",
                                              diamond_feed=supplierObj.vendor_name,
                                              special_price="",
                                              QuickShip=res['quick_ship'] if res['quick_ship'] != "" else "N",
                                              Appointment=res['appointment'] if res['appointment'] != "" else "N",
                                              final_discount_price=discount_price,
                                              vault_discount=str(supplierObj.is_vault_discount)
                                              ))
                return {"status": 200, 'diamond': output}
            except:
                return None
        else:
            return None

    def resolve_live_diamond_by_stockorcert(root, info, input_id=None, only_not_sold_quantity=None, diamond_type=None):

        # activeapiObj = """select * from `{0}api_details` where api_name = 'Find diamond by stock or certificate' and is_active = 1""".format(
        #     table_prefix)
        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:

            try:
                stock_list = tuple(str(input_id).strip().replace(', ', ',').split(","))
                quantity_name = str(only_not_sold_quantity).strip().replace(', ', ',').title()

                if quantity_name == "Yes" and str(quantity_name).strip() != "" and quantity_name is not None:
                    quantity_query = "dd.diamond_quantity = 1"
                    # quantity_query = "dd.diamond_quantity IN (1)"
                else:
                    quantity_query = "(dd.`diamond_quantity`='1' or (sd.is_vault_discount=1 and dd.`diamond_quantity` IN ('1', '0')))"
                # certificate_list = list(str(certificate_number).strip().replace(', ', ',').split(","))
                # print(diamond_list)
                output = []
                results = None

                diamond_list = []
                diamond_typ = None
                if diamond_type == None:
                    diamond_typ = ""
                elif diamond_type != None:
                    diamond_typ = """AND dd.`diamond_type` = '{0}'""".format(diamond_type)
                if input_id:
                    if len(stock_list) > 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                    LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                    WHERE {2} AND sd.`is_enabled`=1 AND dd.`stock_number`in {1}""".format(
                            "websr_", stock_list, quantity_query) + diamond_typ
                        cursor.execute(select_query)

                    elif len(stock_list) == 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                       LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                        WHERE {2} AND sd.`is_enabled`=1 AND dd.`stock_number`='{1}'""".format(
                            "websr_", stock_list[0], quantity_query) + diamond_typ
                        cursor.execute(select_query)
                    columns = [column[0] for column in cursor.description]

                    for row in cursor.fetchall():
                        diamond_list.append(dict(zip(columns, row)))

                if len(diamond_list) == 0:
                    if len(stock_list) > 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                    LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                    WHERE {2} AND sd.`is_enabled`=1 AND dd.`certificate_number`in {1}""".format(
                            "websr_", stock_list, quantity_query) + diamond_typ
                        cursor.execute(select_query)

                    elif len(stock_list) == 1:
                        select_query = """SELECT * FROM `{0}diamond_details_view` as dd
                                       LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`supplier_id`
                                        WHERE {2} AND sd.`is_enabled`=1 AND dd.`certificate_number`='{1}'""".format(
                            "websr_", stock_list[0], quantity_query) + diamond_typ

                        cursor.execute(select_query)
                    columns = [column[0] for column in cursor.description]

                    for row in cursor.fetchall():
                        diamond_list.append(dict(zip(columns, row)))

                constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'"""
                cursor.execute(constant_isenable_query)
                constant_get_isenable = cursor.fetchone()

                constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'"""
                cursor.execute(constant_isenable_vault_query)
                constant_get_vault_isenable = cursor.fetchone()

                for i, res in enumerate(diamond_list):
                    supplierObj = SupplierDetails.objects.using('primary').get(id=res['supplier_id'])
                    if str(res['diamond_type']).strip().lower() == "white":
                        diamond_type_name = "White"
                    elif str(res['diamond_type']).strip().lower() == "lab":
                        diamond_type_name = "lab-grown"
                    # else:
                    #     diamond_type_name = res['diamond_type']
                    video_file_url = ''
                    if res['diamond_video'] != "" or res['diamond_video'] != "nan":
                        if "#VALUE!" not in res['diamond_video']:
                            video_file_url = res['diamond_video']
                    else:
                        video_file_url = ""

                    discount_price = ""
                    if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(res['diamond_type']).strip().lower() == "lab" or str(
                            res['diamond_type']).strip().lower() == "lab-grown"):
                        discount_price = res['final_discount_price']
                    else:
                        discount_price = res['final_price']
                    output.append(Diamond(diamond_id=res['diamond_id'],
                                              shape=res['shape'],
                                              color=res['color'],
                                              clarity=res['clarity'],
                                              size=res['carat_weight'],
                                              lab=res['lab'],
                                              cut=res['cut'],
                                              polish=res['polish'],
                                              symmetry=res['symmetry'],
                                              fluor_intensity=res['flour_intensity'],
                                              cert_num=res['certificate_number'],
                                              measurement=res['measurement'],
                                              meas_length=res['length'],
                                              meas_width=res['width'],
                                              meas_depth=res['depth'],
                                              ratio=res['ratio'],
                                              depth_percent=res['dept_perc'],
                                              table_percent=res['table_perc'],
                                              fancy_color=res['fancy_color'],
                                              fancy_color_intensity=res['fancy_color_intensity'],
                                              fancy_color_overtone=res['fancy_color_overtone'],
                                              desc_comments=res['desc_comments'],
                                              memo_status=res['memo_status'],
                                              inscription=res['inscription'],
                                              location=res['location'],
                                              certificate_file=res['certificate_file'],
                                              image_url=res['diamond_image'] if res['diamond_image'] != "" else "",
                                              video_url= video_file_url, #res['diamond_video'] if res['diamond_video'] != "" else "",
                                              image_file_url=res['diamond_image'] if res['diamond_image'] != "" else "",
                                              video_file_url= video_file_url, #res['diamond_video'] if res['diamond_video'] != "" else "",
                                              price_per_ct=res['price_per_ct'],
                                              original_total_price=res['original_total_price'],
                                              exchange_rate=res['exchange_rate'],
                                              convert_price=res['convert_price'],
                                              plus_markup_price_ct=res['plus_markup_price_ct'],
                                              plus_markup_price=res['plus_markup_price'],
                                              total_sales_price=res['final_price'],
                                              total_sales_price_in_currency=res['final_price'],
                                              price_per_ct_pound=res['price_per_ct_pound'],
                                              plus_markup_price_ct_pound=res['plus_markup_price_ct_pound'],
                                              original_total_price_pound=res['original_total_price_pound'],
                                              final_price_pound=res['final_price_pound'],
                                              price_per_ct_cad=res['price_per_ct_cad'],
                                              plus_markup_price_ct_cad=res['plus_markup_price_ct_cad'],
                                              original_total_price_cad=res['original_total_price_cad'],
                                              final_price_cad=res['final_price_cad'],
                                              availability=res['availability'],
                                              girdle=res['girdle'],
                                              girdle_min=res['girdle_min'],
                                              girdle_max=res['girdle_max'],
                                              girdle_perc=res['girdle_perc'],
                                              girdle_condition=res['girdle_condition'],
                                              culet=res['culet'],
                                              culet_condition=res['culet_condition'],
                                              crown_angle=res['crown_angle'],
                                              crown_height=res['crown_height'],
                                              pavilion_depth=res['pavilion_depth'],
                                              pavilion_angle=res['pavilion_angle'],
                                              origin=res['origin'],
                                              seller_name=res['seller_name'],
                                              city=res['city'],
                                              state=res['state'],
                                              country=res['country'],
                                              is_match_pair_separable=res['is_match_pair_separable'],
                                              member_comments=res['member_comments'],
                                              supplier_country=res['supplier_country'],
                                              milky=res['milky'],
                                              diamond_quantity=res['diamond_quantity'],
                                              diamond_type=diamond_type_name,
                                              supplier_id=res['supplier_id'],
                                              data_entry_point=res['data_entry_point'],
                                              inserted_on=res['created_at'],
                                              updated_at=res['updated_at'],
                                              stock_number=res['stock_number'],
                                              is_show=res['is_show'],
                                              currency_code="USD",
                                              currency_symbol="$",
                                              diamond_feed=supplierObj.vendor_name,
                                              special_price="",
                                              QuickShip=res['quick_ship'] if res['quick_ship'] != "" else "N",
                                              Appointment=res['appointment'] if res['appointment'] != "" else "N",
                                              final_discount_price=discount_price,
                                              vault_discount=str(supplierObj.is_vault_discount)
                                              ))
                return {"status": 200, 'diamond': output}
            except:
                return None
        else:
            return None


    def resolve_live_pair_diamond_data(self, info, page=None, shapes=None, carat=None, clarity=None, color=None,
                                      polish=None,
                                      symmetry=None, fluoroscence=None, price=None, depth_per=None, table=None,
                                      ratio=None,
                                      cut=None, lab=None, diamond_type=None, final_price=None,
                                      order_by=None, sort_by=None, quickship=None, diamond_id=None):

        # activeapiObj = """select * from `{0}api_details` where api_name = 'Filter diamond data' and is_active = 1""".format(
        #     table_prefix)

        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:

            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')

            og_shapes_list = ['Round', 'Princess', 'Cushion', 'Radiant', 'Asscher', 'Emerald', 'Oval', 'Pear',
                              'Marquise', ]

            regular_color_codes_list = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                                        'L']  # Only White Diamonds in this project

            diamond_cuts_list = ['Excellent','Very Good','Good']

            labgrown_diamond_cuts_list = ['Ideal','Excellent','Very Good','Good']

            diamond_clarity_list = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF', 'FL']

            diamond_fluoroscence_list = ['None', 'Faint', 'Medium', 'Strong']

            diamond_polish_list = ['Fair', 'Good', 'Very Good', 'Excellent']

            diamond_symmetry_list = ['Fair', 'Excellent', 'Very Good', 'Good']

            diamond_labs_list = ['GIA', 'IGI']

            diamond_carat_min = 0.25
            diamond_carat_max = 20.50
            diamond_price_min = 100
            diamond_price_max = 1000000

            diamond_depth_min = 40
            diamond_depth_max = 90

            diamond_table_min = 40
            diamond_table_max = 90

            diamond_min_ratio = 0.9
            diamond_max_ratio = 2.75

            diamond_diff_labs_list = ['white', 'lab']
            order_by_price = 'final_price'

            shape_list = list(str(shapes).title().strip().replace(', ', ',').split(","))
            clarity_list = list(str(clarity).upper().strip().replace(', ', ',').split(","))
            color_list = list(str(color).upper().strip().replace(', ', ',').split(","))
            cut_list = list(str(cut).title().strip().replace(', ', ',').split(","))
            polish_list = list(str(polish).title().strip().replace(', ', ',').split(","))
            symmetry_list = list(str(symmetry).title().strip().replace(', ', ',').split(","))
            lab_list = list(str(lab).upper().strip().replace(', ', ',').split(","))
            fluoroscence_list = list(str(fluoroscence).title().strip().replace(', ', ',').split(","))
            carat_tuple = tuple(str(carat).strip().replace(', ', ',').split(","))
            price_tuple = tuple(str(price).strip().replace(', ', ',').split(","))
            depth_per_tuple = tuple(str(depth_per).strip().replace(', ', ',').split(","))
            table_tuple = tuple(str(table).strip().replace(', ', ',').split(","))
            ratio_tuple = tuple(str(ratio).strip().replace(', ', ',').split(","))
            diamond_type_list = list(str(diamond_type).lower().strip().replace(', ', ',').split(","))
            final_price_range = tuple(str(final_price).strip().replace(', ', ',').split(","))
            diamond_id_send = str(diamond_id).strip().replace(', ', ',').replace(' ', '')

            if page == None:
                page = 1

            diamond_query = None
            output = []

            constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'"""
            cursor.execute(constant_isenable_query)
            constant_get_isenable = cursor.fetchone()

            constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'"""
            cursor.execute(constant_isenable_vault_query)
            constant_get_vault_isenable = cursor.fetchone()

            show_diamond_count = 20
            if page == None:
                print("Please define Page no.")
                # diamond_query = DiamondDetails.objects.all().order_by(order_by_price)[0:20]
            else:
                # Shape filter
                if shapes and str(shapes).strip() != "" and shapes is not None:
                    if len(shapes) > 0:
                        shape_list_new = ", ".join("'{0}'".format(w) for w in shape_list)
                        shape_query = "dd.`d1_shape` in (" + str(
                            shape_list_new) + ")" + " and" + " dd.`d2_shape` in (" + str(shape_list_new) + ")" + " and "
                else:
                    shape_list_new = ", ".join("'{0}'".format(w) for w in og_shapes_list)
                    shape_query = "dd.`d1_shape` in (" + str(
                        shape_list_new) + ")" + " and" + " dd.`d2_shape` in (" + str(shape_list_new) + ")" + " and "

                # carat filter
                if carat and str(carat).strip() != "" and carat is not None:
                    carat_query = "(dd.`combined_Carat` >=" + str(carat_tuple[0]) + " && dd.`combined_Carat` <=" + str(
                        carat_tuple[1]) + ")" + " and "
                else:
                    carat_query = "(dd.`combined_Carat` >=" + str(
                        diamond_carat_min) + " && dd.`combined_Carat` <=" + str(diamond_carat_max) + ")" + " and "

                # clarity filter
                if clarity and str(clarity).strip() != "" and clarity is not None:
                    if len(clarity) > 0:
                        clarity_list_new = ", ".join("'{0}'".format(c) for c in clarity_list)
                        clarity_query = "dd.`d1_clarity` in (" + str(
                            clarity_list_new) + ")" + " and" + " dd.`d2_clarity` in (" + str(
                            clarity_list_new) + ") " + " and "
                else:
                    clarity_list_new = ", ".join("'{0}'".format(c) for c in diamond_clarity_list)
                    clarity_query = "dd.`d1_clarity` in (" + str(
                        clarity_list_new) + ")" + " and" + " dd.`d2_clarity` in (" + str(
                        clarity_list_new) + ") " + " and "

                # print(clarity_query)
                # color filter
                if color and str(color).strip() != "" and color is not None:
                    if len(color) > 0:
                        colors_list_new = ", ".join("'{0}'".format(c) for c in color_list)
                        color_query = "dd.`d1_color` in (" + str(
                            colors_list_new) + ")" + " and " + " dd.`d2_color` in (" + str(
                            colors_list_new) + ")" + " and "
                else:
                    colors_list_new = ", ".join("'{0}'".format(c) for c in regular_color_codes_list)
                    color_query = "dd.`d1_color` in (" + str(
                        colors_list_new) + ")" + " and " + " dd.`d2_color` in (" + str(colors_list_new) + ")" + " and "

                # polish filter
                if polish and str(polish).strip() != "" and polish is not None:
                    if len(polish) > 0:
                        polish_list_new = ", ".join("'{0}'".format(c) for c in polish_list)
                        polish_query = "dd.`d1_polish` in (" + str(polish_list_new).replace("_",
                                                                                            " ") + ")" + " and " + " dd.`d2_polish` in (" + str(
                            polish_list_new).replace("_", " ") + ")" + " and "
                else:
                    polish_list_new = ", ".join("'{0}'".format(c) for c in diamond_polish_list)
                    polish_query = "dd.`d1_polish` in (" + str(polish_list_new).replace("_",
                                                                                        " ") + ")" + " and " + " dd.`d2_polish` in (" + str(
                        polish_list_new).replace("_", " ") + ")" + " and "

                # symmetry filter
                if symmetry and str(symmetry).strip() != "" and symmetry is not None:
                    if len(symmetry) > 0:
                        symmetry_list_new = ", ".join("'{0}'".format(c) for c in symmetry_list)
                        symmetry_query = "dd.`d1_symmetry` in (" + str(symmetry_list_new).replace("_",
                                                                                                  " ") + ")" + " and " + "dd.`d2_symmetry` in (" + str(
                            symmetry_list_new).replace("_", " ") + ")" + " and "
                else:
                    symmetry_list_new = ", ".join("'{0}'".format(c) for c in diamond_symmetry_list)
                    symmetry_query = "dd.`d1_symmetry` in (" + str(symmetry_list_new).replace("_",
                                                                                              " ") + ")" + " and " + "dd.`d2_symmetry` in (" + str(
                        symmetry_list_new).replace("_", " ") + ")" + " and "

                # fluoroscence filter
                if fluoroscence and str(fluoroscence).strip() != "" and fluoroscence is not None:
                    fluor_list_new = ", ".join("'{0}'".format(w) for w in fluoroscence_list)
                    fluorescence_query = "dd.`d1_flour_intensity` in (" + str(
                        fluor_list_new) + ")" + " and " + "dd.`d2_flour_intensity` in (" + str(
                        fluor_list_new) + ")" + " and "
                else:
                    fluor_list_new = ", ".join("'{0}'".format(w) for w in diamond_fluoroscence_list)
                    fluorescence_query = "dd.`d1_flour_intensity` in (" + str(
                        fluor_list_new) + ")" + " and " + "dd.`d2_flour_intensity` in (" + str(
                        fluor_list_new) + ")" + " and "

                # depth perc filter
                if depth_per and str(depth_per).strip() != "" and depth_per is not None:
                    depth_perc_query = "(dd.`d1_dept_perc` BETWEEN " + str(depth_per_tuple[0]) + " AND " + str(
                        depth_per_tuple[1]) + ")" + " and " + " (dd.`d2_dept_perc` BETWEEN " + str(
                        depth_per_tuple[0]) + " AND " + str(depth_per_tuple[1]) + ")" + " and "
                else:
                    depth_perc_query = "(dd.`d1_dept_perc` BETWEEN " + str(diamond_depth_min) + " AND " + str(
                        diamond_depth_max) + ")" + " and " + " (dd.`d2_dept_perc` BETWEEN " + str(
                        diamond_depth_min) + " AND " + str(diamond_depth_max) + ")" + " and "

                # table filter
                if table and str(table).strip() != "" and table is not None:
                    table_perc_query = "(dd.`d1_table_perc` BETWEEN " + str(table_tuple[0]) + " AND " + str(
                        table_tuple[1]) + ")" + " and " + " (dd.`d2_table_perc` BETWEEN " + str(
                        table_tuple[0]) + " AND " + str(table_tuple[1]) + ")" + " and "
                else:
                    table_perc_query = "(dd.`d1_table_perc` BETWEEN " + str(diamond_table_min) + " AND " + str(
                        diamond_table_max) + ")" + " and " + " (dd.`d2_table_perc` BETWEEN " + str(
                        diamond_table_min) + " AND " + str(diamond_table_max) + ")" + " and "

                # ratio filter
                if ratio and str(ratio).strip() != "" and ratio is not None:
                    ratio_query = "(dd.`d1_ratio` BETWEEN " + str(ratio_tuple[0]) + " AND " + str(
                        ratio_tuple[1]) + ")" + " and " + " (dd.`d2_ratio` BETWEEN " + str(
                        ratio_tuple[0]) + " AND " + str(ratio_tuple[1]) + ")" + " and "
                else:
                    ratio_query = "(dd.`d1_ratio` BETWEEN " + str(diamond_min_ratio) + " AND " + str(
                        diamond_max_ratio) + ")" + " and " + " (dd.`d2_ratio` BETWEEN " + str(
                        diamond_min_ratio) + " AND " + str(diamond_max_ratio) + ")" + " and "

                # lab filter
                if lab and str(lab).strip() != "" and lab is not None:
                    lab_list_new = ", ".join("'{0}'".format(c) for c in lab_list)
                    lab_query = "dd.`d1_lab` in (" + str(lab_list_new).replace("_",
                                                                               " ") + ")" + " and" + " dd.`d2_lab` in (" + str(
                        lab_list_new).replace("_", " ") + ")" + " and "
                else:
                    lab_list_new = ", ".join("'{0}'".format(c) for c in diamond_labs_list)
                    lab_query = "dd.`d1_lab` in (" + str(lab_list_new).replace("_",
                                                                               " ") + ")" + " and" + " dd.`d2_lab` in (" + str(
                        lab_list_new).replace("_", " ") + ")" + " and "

                # cut filter
                cut_query = ""
                if cut and str(cut).strip() != "" and cut is not None:
                    if len(cut) > 0:
                        if str(diamond_type).strip().lower() == "white" or str(
                                diamond_type).strip().lower() == "natural":
                            cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
                            cut_query = "dd.`d1_cut` in (" + str(cuts_list_new).replace("_",
                                                                                        " ") + ")" + " and" + " dd.`d2_cut` in (" + str(
                                cuts_list_new).replace("_", " ") + ")" + " and "
                        elif str(diamond_type).strip().lower() == "lab" or str(
                                diamond_type).strip().lower() == "lab-grown":
                            cuts_list_new = ", ".join("'{0}'".format(c) for c in cut_list)
                            cut_query = "dd.`d1_cut` in (" + str(cuts_list_new).replace("_",
                                                                                        " ") + ")" + " and" + " dd.`d2_cut` in (" + str(
                                cuts_list_new).replace("_", " ") + ")" + " and "
                else:
                    if str(diamond_type).strip().lower() == "white" or str(
                            diamond_type).strip().lower() == "natural":
                        cuts_list_new = ", ".join("'{0}'".format(c) for c in diamond_cuts_list)
                        cut_query = "dd.`d1_cut` in (" + str(cuts_list_new).replace("_",
                                                                                    " ") + ")" + " and" + " dd.`d2_cut` in (" + str(
                            cuts_list_new).replace("_", " ") + ")" + " and "
                    elif str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown":
                        cuts_list_new = ", ".join("'{0}'".format(c) for c in labgrown_diamond_cuts_list)
                        cut_query = "dd.`d1_cut` in (" + str(cuts_list_new).replace("_",
                                                                                    " ") + ")" + " and" + " dd.`d2_cut` in (" + str(
                            cuts_list_new).replace("_", " ") + ")" + " and "

                # diamond type filter

                if diamond_type and str(diamond_type).strip() != "" and diamond_type is not None:
                    if str(diamond_type).strip().lower() == "white" or str(diamond_type).strip().lower() == "natural":
                        diamond_type_query = "dd.`d1_diamond_type`='white'" + " and" + " dd.`d2_diamond_type`='white'"
                    elif str(diamond_type).strip().lower() == "lab" or str(diamond_type).strip().lower() == "lab-grown":
                        diamond_type_query = "dd.`d1_diamond_type`='lab'" + " and" + " dd.`d2_diamond_type`='lab'"
                else:
                    diamond_type_query = "dd.`d1_diamond_type` in ('white', 'lab')" + " and" + " dd.`d2_diamond_type` in ('white', 'lab')"

                # print(diamond_type_query)

                # quickship filter
                quickship_query = ""
                if quickship and str(quickship).strip() != "" and quickship is not None:
                    if str(quickship).strip().lower() == 'y' or str(quickship).strip().lower() == 'yes':
                        quickship_query = "AND dd.`combined_QuickShip`= 'Y'"
                    if str(quickship).strip().lower() == 'n' or str(quickship).strip().lower() == 'No':
                        quickship_query = "AND dd.`combined_QuickShip`= 'N' or dd.`combined_QuickShip`= ''"

                #diamond id not need in range
                if diamond_id != None or diamond_id != "" or diamond_id != "":
                    diamond_query = "AND dd.combined_Diamond_ID NOT IN('{0}')".format(diamond_id_send)
                else:
                    diamond_query = "AND dd.combined_Diamond_ID NOT IN('')"

                # # price per carat
                # if final_price and str(final_price).strip() != "" and final_price is not None:
                #     price_query = "(dd.`combined_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
                #         final_price_range[1]) + ")" + " and "
                # else:
                #     price_query = "(dd.`combined_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
                #         diamond_price_max) + ")" + " and "

                # sort_direct_query = "ORDER BY dd.`combined_price` ASC"
                # if sort_by and str(sort_by).strip() != "":
                #     if str(order_by).lower() == "price":
                #         sort_order_by = "dd.`combined_price`"
                #         sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()

                # price per carat
                price_query = ""

                if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
                        diamond_type).strip().lower() == "lab-grown"):
                    if final_price and str(final_price).strip() != "" and final_price is not None:
                        price_query = "(dd.`final_discount_price` BETWEEN " + str(
                            final_price_range[0]) + " AND " + str(
                            final_price_range[1]) + ")" + " and "
                    else:
                        price_query = "(dd.`final_discount_price` BETWEEN " + str(
                            diamond_price_min) + " AND " + str(
                            diamond_price_max) + ")" + " and "
                else:
                    if final_price and str(final_price).strip() != "" and final_price is not None:
                        price_query = "(dd.`combined_price` BETWEEN " + str(final_price_range[0]) + " AND " + str(
                            final_price_range[1]) + ")" + " and "
                    else:
                        price_query = "(dd.`combined_price` BETWEEN " + str(diamond_price_min) + " AND " + str(
                            diamond_price_max) + ")" + " and "

                sort_direct_query = "ORDER BY dd.`combined_price` ASC"
                if sort_by and str(sort_by).strip() != "":
                    if str(order_by).lower() == "price":
                        sort_order_by = ""
                        if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
                                diamond_type).strip().lower() == "lab-grown"):
                            sort_order_by = "dd.`final_discount_price`"
                        else:
                            sort_order_by = "dd.`combined_price`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "carat":
                        sort_order_by = "dd.`combined_Carat`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "color":
                        sort_order_by = "dd.`d1_color`"
                        sort_order_by2 = "dd.`d2_color`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "clarity_index":
                        if str(sort_by).strip().lower() == "desc":
                            clarity_org_list = diamond_clarity_list
                            comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
                            sort_direct_query = "ORDER BY  FIELD(dd.`d1_clarity`,"+str(comma_sep_clarity)+ ")," + "FIELD(dd.`d2_clarity`,"+str(comma_sep_clarity)+")"
                        else:
                            clarity_asc_list = diamond_clarity_list
                            clarity_org_list = clarity_asc_list[::-1]
                            comma_sep_clarity = ",".join("'" + str(c) + "'" for c in clarity_org_list)
                            sort_direct_query = "ORDER BY  FIELD(dd.`d1_clarity`,"+str(comma_sep_clarity)+ ")," + "FIELD(dd.`d2_clarity`,"+str(comma_sep_clarity)+ ")"
                    elif str(order_by).lower() == "cut_index":
                        if str(sort_by).strip().lower() == "desc":
                            cut_org_list = diamond_cuts_list + ['NA']
                            if str(diamond_type).strip().lower() == "lab" or str(
                                    diamond_type).strip().lower() == "lab-grown":
                                cut_org_list = labgrown_diamond_cuts_list + ['NA']
                            comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
                            sort_direct_query = "ORDER BY  FIELD(dd.`d1_cut`,"+str(comma_sep_cut)+ ")," + "FIELD(dd.`d2_cut`,"+str(comma_sep_cut)+ ")"
                        else:
                            cut_asc_list = diamond_cuts_list
                            if str(diamond_type).strip().lower() == "lab" or str(
                                    diamond_type).strip().lower() == "lab-grown":
                                cut_asc_list = labgrown_diamond_cuts_list
                            cut_org_list = cut_asc_list[::-1] + ['NA']
                            comma_sep_cut = ",".join("'" + str(c) + "'" for c in cut_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`d1_cut`,"+str(comma_sep_cut)+ ")," + "FIELD(dd.`d2_cut`,"+str(comma_sep_cut)+ ")"
                        # sort_by = "dd.`cut`"
                        # sort_direct_query = "ORDER BY "+str(sort_by)+" "+str(sort_direction).strip()
                    elif str(order_by).lower() == "shape":
                        sort_order_by = "dd.`d1_shape`"
                        sort_order_by2 = "dd.`d2_shape`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "polish":
                        sort_order_by = "dd.`d1_polish`"
                        sort_order_by2 = "dd.`d2_polish`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "symmetry":
                        sort_order_by = "dd.`d1_symmetry`"
                        sort_order_by2 = "dd.`d2_symmetry`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "flour":
                        sort_order_by = "dd.`d1_flour_intensity`"
                        sort_order_by2 = "dd.`d2_flour_intensity`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "table":
                        sort_order_by = "dd.`d1_table_perc`"
                        sort_order_by2 = "dd.`d2_table_perc`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "depth":
                        sort_order_by = "dd.`d1_dept_perc`"
                        sort_order_by2 = "dd.`d2_dept_perc`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "ratio":
                        sort_order_by = "dd.`d1_ratio`"
                        sort_order_by2 = "dd.`d2_ratio`"
                        sort_direct_query = "ORDER BY " + str(sort_order_by) + " " + str(sort_by).strip() + "," + str(
                            sort_order_by2) + " " + str(sort_by).strip()
                    elif str(order_by).lower() == "quickship":
                        if str(sort_by).strip().lower() == "desc":
                            quickship_org_list = ['Y', 'N']
                            comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`combined_QuickShip`,"+str(comma_sep_quickship) +")"
                        else:
                            quickship_org_list = ['N', 'Y']
                            comma_sep_quickship = ",".join("'" + str(c) + "'" for c in quickship_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`combined_QuickShip`," + str(comma_sep_quickship) + ")"
                    elif str(order_by).lower() == "appointment":
                        if str(sort_by).strip().lower() == "desc":
                            appointment_org_list = ['Y', 'N']
                            comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`d1_appointment`,"+str(comma_sep_appointment) + ")," + "FIELD(dd.`d2_appointment`,"+str(comma_sep_appointment)+ ")"
                        else:
                            appointment_org_list = ['Y', 'N']
                            comma_sep_appointment = ",".join("'" + str(c) + "'" for c in appointment_org_list)
                            sort_direct_query = "ORDER BY FIELD(dd.`d1_appointment`," + str(
                                comma_sep_appointment) + ")," + "FIELD(dd.`d2_appointment`," + str(
                                comma_sep_appointment) + ")"

                # PAGE NUMBER
                page_num_query = True
                records_limit = 500

                if records_limit and str(records_limit).strip() != "":
                    if page and str(page).strip() != "":
                        start_pos_value = (int(page) - 1) * records_limit
                    else:
                        page_number = 1
                        start_pos_value = (int(page_number) - 1) * records_limit
                    page_num_query = "LIMIT " + str(start_pos_value) + ", " + str(records_limit)

                supplier_query = """SELECT `id`, `supplier_name` FROM `websr_supplier_details` WHERE `is_allow`=1 AND `is_enabled`=1"""
                cursor.execute(supplier_query)
                columns = [column[0] for column in cursor.description]
                suppliers_dict = {}
                supp_ids = ""
                for row in cursor.fetchall():
                    suppliers_dict['supp_' + str(row[0])] = str(row[1])
                    supp_ids += str(row[0]) + ","

                supp_ids = str(supp_ids).rstrip(",")

                diamond_list_sigle_diamond_table = DiamondDetails_primary.objects.using('primary').all().values_list('diamond_id', flat=True)

                select_query = """SELECT SQL_CALC_FOUND_ROWS dd.* FROM `{0}pair_diamond_details` as dd
                    JOIN {0}diamond_details_primary AS t2
                    JOIN {0}diamond_details_primary AS t3
                    ON dd.`d1_diamond_id` =  t2.`diamond_id` AND dd.`d2_diamond_id` = t3.`diamond_id`
                   WHERE dd.`combined_Quantity`='1' AND dd.`d1_supplier_id` IN ({1}) AND 
                   dd.`d2_supplier_id` IN ({1}) AND {2}  {3}  {4}  {5}
                   {6}  {7}  {8}  {9}  {10}  {11}  {12}  {13}  {14} {15} {16} {17} {18}""".format(
                    "websr_", supp_ids, shape_query, price_query, carat_query, cut_query,
                    color_query, clarity_query, polish_query, symmetry_query, fluorescence_query, depth_perc_query,
                    table_perc_query, ratio_query, diamond_type_query, quickship_query, diamond_query,
                    sort_direct_query, page_num_query)
                print(select_query)
                cursor.execute(select_query)
                columns = [column[0] for column in cursor.description]
                diamond_list = []
                for row in cursor.fetchall():
                    diamond_list.append(dict(zip(columns, row)))

                cursor.execute("SELECT FOUND_ROWS()")
                rows_count_result = cursor.fetchone()
                total_found_diamonds = rows_count_result[0]

                if len(diamond_list) < records_limit:
                    records_limit = len(diamond_list)

                for i, res in enumerate(diamond_list):
                    if str(res['d1_diamond_id']).strip() in diamond_list_sigle_diamond_table and str(res['d2_diamond_id']).strip() in diamond_list_sigle_diamond_table :
                        supplierObj1 = SupplierDetails.objects.using('primary').get(id=res['d1_supplier_id'])
                        supplierObj2 = SupplierDetails.objects.using('primary').get(id=res['d2_supplier_id'])
                        if str(res['d1_diamond_type']).strip().lower() == "white" and str(
                                res['d2_diamond_type']).strip().lower() == "white":
                            diamond_type_name1 = 'White'
                            diamond_type_name2 = 'White'
                        elif str(res['d1_diamond_type']).strip().lower() == "lab" and str(
                                res['d2_diamond_type']).strip().lower() == "lab":
                            diamond_type_name1 = "lab-grown"
                            diamond_type_name2 = "lab-grown"
                        # else:
                        #     diamond_type_name1 = res['d1_diamond_type']
                        #     diamond_type_name2 = res['d2_diamond_type']

                        discount_price = ""
                        if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (str(diamond_type).strip().lower() == "lab" or str(
                                diamond_type).strip().lower() == "lab-grown"):
                            discount_price = res['final_discount_price']
                        else:
                            discount_price = res['combined_price']

                        output.append(Pairdiamond(d1_diamond_id=res['d1_diamond_id'],
                                                      d1_shape=res['d1_shape'],
                                                      d1_color=res['d1_color'],
                                                      d1_clarity=res['d1_clarity'],
                                                      d1_size=res['d1_carat_weight'],
                                                      d1_lab=res['d1_lab'],
                                                      d1_cut=res['d1_cut'],
                                                      d1_polish=res['d1_polish'],
                                                      d1_symmetry=res['d1_symmetry'],
                                                      d1_flour_intensity=res['d1_flour_intensity'],
                                                      d1_cert_num=res['d1_certificate_number'],
                                                      d1_measurement=res['d1_measurement'],
                                                      d1_meas_length=res['d1_length'],
                                                      d1_meas_width=res['d1_width'],
                                                      d1_meas_depth=res['d1_depth'],
                                                      d1_ratio=res['d1_ratio'],
                                                      d1_depth_percent=res['d1_dept_perc'],
                                                      d1_table_percent=res['d1_table_perc'],
                                                      d1_rapaport_price=res['d1_rapaport_price'],
                                                      d1_perc_off_rap=res['d1_perc_off_rap'],
                                                      d1_fancy_color=res['d1_fancy_color'],
                                                      d1_fancy_color_intensity=res['d1_fancy_color_intensity'],
                                                      d1_fancy_color_overtone=res['d1_fancy_color_overtone'],
                                                      d1_price_per_ct=res['d1_price_per_ct'],
                                                      d1_original_total_price=res['d1_original_total_price'],
                                                      d1_exchange_rate=res['d1_exchange_rate'],
                                                      d1_convert_price=res['d1_convert_price'],
                                                      d1_plus_markup_price_ct=res['d1_plus_markup_price_ct'],
                                                      d1_plus_markup_price=res['d1_plus_markup_price'],
                                                      d1_total_sales_price=res['d1_final_price'],
                                                      d1_total_sales_price_in_currency=res['d1_final_price'],
                                                      d1_price_per_ct_eur=res['d1_price_per_ct_eur'],
                                                      d1_plus_markup_price_ct_eur=res['d1_plus_markup_price_ct_eur'],
                                                      d1_original_total_price_eur=res['d1_original_total_price_eur'],
                                                      d1_final_price_eur=res['d1_final_price_eur'],
                                                      d1_exchange_rate_pound=res['d1_exchange_rate_pound'],
                                                      d1_price_per_ct_pound=res['d1_price_per_ct_pound'],
                                                      d1_plus_markup_price_ct_pound=res['d1_plus_markup_price_ct_pound'],
                                                      d1_original_total_price_pound=res['d1_original_total_price_pound'],
                                                      d1_final_price_pound=res['d1_final_price_pound'],
                                                      d1_exchange_rate_cad=res['d1_exchange_rate_cad'],
                                                      d1_price_per_ct_cad=res['d1_price_per_ct_cad'],
                                                      d1_plus_markup_price_ct_cad=res['d1_plus_markup_price_ct_cad'],
                                                      d1_original_total_price_cad=res['d1_original_total_price_cad'],
                                                      d1_final_price_cad=res['d1_final_price_cad'],
                                                      d2_exchange_rate_cad=res['d2_exchange_rate_cad'],
                                                      d2_price_per_ct_cad=res['d2_price_per_ct_cad'],
                                                      d2_plus_markup_price_ct_cad=res['d2_plus_markup_price_ct_cad'],
                                                      d2_original_total_price_cad=res['d2_original_total_price_cad'],
                                                      d2_final_price_cad=res['d2_final_price_cad'],
                                                      d1_certificate_file=res['d1_certificate_file'] if res['d1_certificate_file'] != "nan" else "",
                                                      d1_image_url=res['d1_diamond_image'] if res['d1_diamond_image'] != "nan" else "",
                                                      d1_video_url=res['d1_diamond_video'] if res['d1_diamond_video'] != "nan" else "",
                                                      d1_image_file_url=res['d1_diamond_image'] if res['d1_diamond_image'] != "nan" else "",
                                                      d1_video_file_url=res['d1_diamond_video'] if res['d1_diamond_video'] != "nan" else "",
                                                      d1_availability=res['d1_availability'],
                                                      d1_diamond_quantity=res['d1_diamond_quantity'],
                                                      d1_diamond_type=diamond_type_name1,
                                                      d1_supplier_id=res['d1_supplier_id'],
                                                      d1_data_entry_point=res['d1_data_entry_point'],
                                                      d1_created_at=res['d1_created_at'],
                                                      d1_updated_at=res['d1_updated_at'],
                                                      d1_stock_number=res['d1_stock_number'],
                                                      d1_is_show=res['d1_is_show'],
                                                      d1_desc_comments=res['d1_desc_comments'],
                                                      d1_memo_status=res['d1_memo_status'],
                                                      d1_inscription=res['d1_inscription'],
                                                      d1_location=res['d1_location'],
                                                      d1_girdle=res['d1_girdle'],
                                                      d1_girdle_min=res['d1_girdle_min'],
                                                      d1_girdle_max=res['d1_girdle_max'],
                                                      d1_girdle_perc=res['d1_girdle_perc'],
                                                      d1_girdle_condition=res['d1_girdle_condition'],
                                                      d1_culet=res['d1_culet'],
                                                      d1_culet_condition=res['d1_culet_condition'],
                                                      d1_crown_angle=res['d1_crown_angle'],
                                                      d1_crown_height=res['d1_crown_height'],
                                                      d1_pavilion_depth=res['d1_pavilion_depth'],
                                                      d1_pavilion_angle=res['d1_pavilion_angle'],
                                                      d1_origin=res['d1_origin'],
                                                      d1_seller_name=res['d1_seller_name'],
                                                      d1_city=res['d1_city'],
                                                      d1_state=res['d1_state'],
                                                      d1_country=res['d1_country'],
                                                      d1_is_match_pair_separable=res['d1_is_match_pair_separable'],
                                                      d1_member_comments=res['d1_member_comments'],
                                                      d1_supplier_country=res['d1_supplier_country'],
                                                      d1_milky=res['d1_milky'],
                                                      d1_fluorescence_color=res['d1_fluorescence_color'],
                                                      d1_shade=res['d1_shade'],
                                                      d1_eye_clean=res['d1_eye_clean'],
                                                      d1_treatment=res['d1_treatment'],
                                                      d1_cert_comment=res['d1_cert_comment'],
                                                      d1_key_to_symbols=res['d1_key_to_symbols'],
                                                      d1_white_inclusion=res['d1_white_inclusion'],
                                                      d1_black_inclusion=res['d1_black_inclusion'],
                                                      d1_open_inclusion=res['d1_open_inclusion'],
                                                      d1_quick_ship=res['d1_quick_ship'],
                                                      d1_appointment=res['d1_appointment'],
                                                      d2_diamond_id=res['d2_diamond_id'],
                                                      d2_shape=res['d2_shape'],
                                                      d2_color=res['d2_color'],
                                                      d2_clarity=res['d2_clarity'],
                                                      d2_size=res['d2_carat_weight'],
                                                      d2_lab=res['d2_lab'],
                                                      d2_cut=res['d2_cut'],
                                                      d2_polish=res['d2_polish'],
                                                      d2_symmetry=res['d2_symmetry'],
                                                      d2_flour_intensity=res['d2_flour_intensity'],
                                                      d2_cert_num=res['d2_certificate_number'],
                                                      d2_measurement=res['d2_measurement'],
                                                      d2_meas_length=res['d2_length'],
                                                      d2_meas_width=res['d2_width'],
                                                      d2_meas_depth=res['d2_depth'],
                                                      d2_ratio=res['d2_ratio'],
                                                      d2_depth_percent=res['d2_dept_perc'],
                                                      d2_table_percent=res['d2_table_perc'],
                                                      d2_rapaport_price=res['d2_rapaport_price'],
                                                      d2_perc_off_rap=res['d2_perc_off_rap'],
                                                      d2_fancy_color=res['d2_fancy_color'],
                                                      d2_fancy_color_intensity=res['d2_fancy_color_intensity'],
                                                      d2_fancy_color_overtone=res['d2_fancy_color_overtone'],
                                                      d2_price_per_ct=res['d2_price_per_ct'],
                                                      d2_original_total_price=res['d2_original_total_price'],
                                                      d2_exchange_rate=res['d2_exchange_rate'],
                                                      d2_convert_price=res['d2_convert_price'],
                                                      d2_plus_markup_price_ct=res['d2_plus_markup_price_ct'],
                                                      d2_plus_markup_price=res['d2_plus_markup_price'],
                                                      d2_total_sales_price=res['d2_final_price'],
                                                      d2_total_sales_price_in_currency=res['d2_final_price'],
                                                      d2_price_per_ct_eur=res['d2_price_per_ct_eur'],
                                                      d2_plus_markup_price_ct_eur=res['d2_plus_markup_price_ct_eur'],
                                                      d2_original_total_price_eur=res['d2_original_total_price_eur'],
                                                      d2_final_price_eur=res['d2_final_price_eur'],
                                                      d2_exchange_rate_pound=res['d2_exchange_rate_pound'],
                                                      d2_price_per_ct_pound=res['d2_price_per_ct_pound'],
                                                      d2_plus_markup_price_ct_pound=res['d2_plus_markup_price_ct_pound'],
                                                      d2_original_total_price_pound=res['d2_original_total_price_pound'],
                                                      d2_final_price_pound=res['d2_final_price_pound'],
                                                      d2_certificate_file=res['d2_certificate_file']  if res['d2_certificate_file'] != "nan" else "",
                                                      d2_image_url=res['d2_diamond_image'] if res['d2_diamond_image'] != "nan" else "",
                                                      d2_video_url=res['d2_diamond_video'] if res['d2_diamond_video'] != "nan" else "",
                                                      d2_image_file_url=res['d2_diamond_image'] if res['d2_diamond_image'] != "nan" else "",
                                                      d2_video_file_url=res['d2_diamond_video'] if res['d2_diamond_video'] != "nan" else "",
                                                      d2_availability=res['d2_availability'],
                                                      d2_diamond_quantity=res['d2_diamond_quantity'],
                                                      d2_diamond_type=diamond_type_name2,
                                                      d2_supplier_id=res['d2_supplier_id'],
                                                      d2_data_entry_point=res['d2_data_entry_point'],
                                                      d2_created_at=res['d2_created_at'],
                                                      d2_updated_at=res['d2_updated_at'],
                                                      d2_stock_number=res['d2_stock_number'],
                                                      d2_is_show=res['d2_is_show'],
                                                      d2_desc_comments=res['d2_desc_comments'],
                                                      d2_memo_status=res['d2_memo_status'],
                                                      d2_inscription=res['d2_inscription'],
                                                      d2_location=res['d2_location'],
                                                      d2_girdle=res['d2_girdle'],
                                                      d2_girdle_min=res['d2_girdle_min'],
                                                      d2_girdle_max=res['d2_girdle_max'],
                                                      d2_girdle_perc=res['d2_girdle_perc'],
                                                      d2_girdle_condition=res['d2_girdle_condition'],
                                                      d2_culet=res['d2_culet'],
                                                      d2_culet_condition=res['d2_culet_condition'],
                                                      d2_crown_angle=res['d2_crown_angle'],
                                                      d2_crown_height=res['d2_crown_height'],
                                                      d2_pavilion_depth=res['d2_pavilion_depth'],
                                                      d2_pavilion_angle=res['d2_pavilion_angle'],
                                                      d2_origin=res['d2_origin'],
                                                      d2_seller_name=res['d2_seller_name'],
                                                      d2_city=res['d2_city'],
                                                      d2_state=res['d2_state'],
                                                      d2_country=res['d2_country'],
                                                      d2_is_match_pair_separable=res['d2_is_match_pair_separable'],
                                                      d2_member_comments=res['d2_member_comments'],
                                                      d2_supplier_country=res['d2_supplier_country'],
                                                      d2_milky=res['d2_milky'],
                                                      d2_fluorescence_color=res['d2_fluorescence_color'],
                                                      d2_shade=res['d2_shade'],
                                                      d2_eye_clean=res['d2_eye_clean'],
                                                      d2_treatment=res['d2_treatment'],
                                                      d2_cert_comment=res['d2_cert_comment'],
                                                      d2_key_to_symbols=res['d2_key_to_symbols'],
                                                      d2_white_inclusion=res['d2_white_inclusion'],
                                                      d2_black_inclusion=res['d2_black_inclusion'],
                                                      d2_open_inclusion=res['d2_open_inclusion'],
                                                      d2_quick_ship=res['d2_quick_ship'],
                                                      d2_appointment=res['d2_appointment'],
                                                      combined_price=res['combined_price'],
                                                      combined_price_pound=res['combined_price_pound'],
                                                      combined_price_cad=res['combined_price_cad'],
                                                      combined_QuickShip=res['combined_QuickShip'] if res['combined_QuickShip'] != "" else "N",
                                                      combined_SKU=res['combined_SKU'],
                                                      combined_Quantity=res['combined_Quantity'],
                                                      combined_Carat=res['combined_Carat'],
                                                      combined_Diamond_ID=res['combined_Diamond_ID'],
                                                      combined_Cut=res['combined_Cut'],
                                                      d1_diamond_feed=supplierObj1.vendor_name,
                                                      d2_diamond_feed=supplierObj2.vendor_name,
                                                      inserted_on=res['Inserted_on'],
                                                      final_discount_price=discount_price
                                                      ))
                    # output.append(Diamond("a"))

                # counting_per_page_record = diamond_query.count()

                return {"status": 200, 'diamond': output, 'data_count': total_found_diamonds, 'diamonds_returned': records_limit,
                        'page_no': page}

            # else:
            return None

    def resolve_live_pair_diamond_by_id(root, info, diamond_id=None):
        # activeapiObj = """select * from `{0}api_details` where api_name = 'Find diamond by id' and is_active = 1""".format(
        #     table_prefix)
        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            diamond_details = []
            try:
                diamond_id_list = tuple(str(diamond_id).strip().replace(', ', ',').split(","))
                output = []
                results = None
                diamond_list = []
                diamond_list_sigle_diamond_table = DiamondDetails_primary.objects.using('primary').all().values_list('diamond_id', flat=True)
                if diamond_id:
                    if len(diamond_id_list) > 1:
                        select_query = """SELECT * FROM `{0}pair_diamond_details` as dd
                                    LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`d1_supplier_id`
                                    LEFT JOIN `websr_supplier_details` AS sk ON  sk.`id`= dd.`d2_supplier_id`
                                    WHERE dd.`combined_Quantity`='1' AND sd.`is_enabled`=1 AND sk.`is_enabled`=1 
                                    AND dd.`combined_Diamond_ID`in {1}""".format(
                            "websr_", diamond_id_list)
                        # print(select_query)
                        cursor.execute(select_query)

                    elif len(diamond_id_list) == 1:
                        select_query = """SELECT * FROM `{0}pair_diamond_details` as dd
                                       LEFT JOIN `{0}supplier_details` as sd ON sd.`id`=dd.`d1_supplier_id`
                                       LEFT JOIN `websr_supplier_details` AS sk ON  sk.`id`= dd.`d2_supplier_id`
                                        WHERE dd.`combined_Quantity`='1' AND sd.`is_enabled`=1 AND sk.`is_enabled`=1 
                                        AND dd.`combined_Diamond_ID`='{1}'""".format(
                            "websr_", diamond_id_list[0])
                        # print(select_query)
                        cursor.execute(select_query)
                    columns = [column[0] for column in cursor.description]

                    for row in cursor.fetchall():
                        diamond_list.append(dict(zip(columns, row)))

                constant_isenable_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'discount'"""
                cursor.execute(constant_isenable_query)
                constant_get_isenable = cursor.fetchone()

                constant_isenable_vault_query = """SELECT `is_enable` FROM `websr_constant_settings` where `constant_name` = 'vault_discount'"""
                cursor.execute(constant_isenable_vault_query)
                constant_get_vault_isenable = cursor.fetchone()

                for i, res in enumerate(diamond_list):
                    if str(res['d1_diamond_id']).strip() in diamond_list_sigle_diamond_table and str(
                            res['d2_diamond_id']).strip() in diamond_list_sigle_diamond_table:
                        supplierObj1 = SupplierDetails.objects.using('primary').get(id=res['d1_supplier_id'])
                        supplierObj2 = SupplierDetails.objects.using('primary').get(id=res['d2_supplier_id'])
                        if str(res['d1_diamond_type']).strip().lower() == "white" and str(
                                res['d2_diamond_type']).strip().lower() == "white":
                            diamond_type_name1 = 'White'
                            diamond_type_name2 = 'White'
                        elif str(res['d1_diamond_type']).strip().lower() == "lab" and str(
                                res['d2_diamond_type']).strip().lower() == "lab":
                            diamond_type_name1 = "lab-grown"
                            diamond_type_name2 = "lab-grown"

                        discount_price = ""
                        if (constant_get_isenable[0] == 1 or constant_get_vault_isenable[0] == 1) and (
                                str(res['d1_diamond_type']).strip().lower() == "lab" or str(
                                res['d2_diamond_type']).strip().lower() == "lab" or str(
                                res['d1_diamond_type']).strip().lower() == "lab-grown" or str(
                                res['d2_diamond_type']).strip().lower() == "lab-grown"):
                            discount_price = res['final_discount_price']
                        else:
                            discount_price = res['combined_price']


                        output.append(Pairdiamond(d1_diamond_id=res['d1_diamond_id'],
                                                      d1_shape=res['d1_shape'],
                                                      d1_color=res['d1_color'],
                                                      d1_clarity=res['d1_clarity'],
                                                      d1_size=res['d1_carat_weight'],
                                                      d1_lab=res['d1_lab'],
                                                      d1_cut=res['d1_cut'],
                                                      d1_polish=res['d1_polish'],
                                                      d1_symmetry=res['d1_symmetry'],
                                                      d1_flour_intensity=res['d1_flour_intensity'],
                                                      d1_cert_num=res['d1_certificate_number'],
                                                      d1_measurement=res['d1_measurement'],
                                                      d1_meas_length=res['d1_length'],
                                                      d1_meas_width=res['d1_width'],
                                                      d1_meas_depth=res['d1_depth'],
                                                      d1_ratio=res['d1_ratio'],
                                                      d1_depth_percent=res['d1_dept_perc'],
                                                      d1_table_percent=res['d1_table_perc'],
                                                      d1_rapaport_price=res['d1_rapaport_price'],
                                                      d1_perc_off_rap=res['d1_perc_off_rap'],
                                                      d1_fancy_color=res['d1_fancy_color'],
                                                      d1_fancy_color_intensity=res['d1_fancy_color_intensity'],
                                                      d1_fancy_color_overtone=res['d1_fancy_color_overtone'],
                                                      d1_price_per_ct=res['d1_price_per_ct'],
                                                      d1_original_total_price=res['d1_original_total_price'],
                                                      d1_exchange_rate=res['d1_exchange_rate'],
                                                      d1_convert_price=res['d1_convert_price'],
                                                      d1_plus_markup_price_ct=res['d1_plus_markup_price_ct'],
                                                      d1_plus_markup_price=res['d1_plus_markup_price'],
                                                      d1_total_sales_price=res['d1_final_price'],
                                                      d1_total_sales_price_in_currency=res['d1_final_price'],
                                                      d1_price_per_ct_eur=res['d1_price_per_ct_eur'],
                                                      d1_plus_markup_price_ct_eur=res['d1_plus_markup_price_ct_eur'],
                                                      d1_original_total_price_eur=res['d1_original_total_price_eur'],
                                                      d1_final_price_eur=res['d1_final_price_eur'],
                                                      d1_exchange_rate_pound=res['d1_exchange_rate_pound'],
                                                      d1_price_per_ct_pound=res['d1_price_per_ct_pound'],
                                                      d1_plus_markup_price_ct_pound=res['d1_plus_markup_price_ct_pound'],
                                                      d1_original_total_price_pound=res['d1_original_total_price_pound'],
                                                      d1_final_price_pound=res['d1_final_price_pound'],
                                                      d1_exchange_rate_cad=res['d1_exchange_rate_cad'],
                                                      d1_price_per_ct_cad=res['d1_price_per_ct_cad'],
                                                      d1_plus_markup_price_ct_cad=res['d1_plus_markup_price_ct_cad'],
                                                      d1_original_total_price_cad=res['d1_original_total_price_cad'],
                                                      d1_final_price_cad=res['d1_final_price_cad'],
                                                      d2_exchange_rate_cad=res['d2_exchange_rate_cad'],
                                                      d2_price_per_ct_cad=res['d2_price_per_ct_cad'],
                                                      d2_plus_markup_price_ct_cad=res['d2_plus_markup_price_ct_cad'],
                                                      d2_original_total_price_cad=res['d2_original_total_price_cad'],
                                                      d2_final_price_cad=res['d2_final_price_cad'],
                                                      d1_certificate_file=res['d1_certificate_file'] if res['d1_certificate_file'] != "nan" else "",
                                                      d1_image_url=res['d1_diamond_image'] if res['d1_diamond_image'] != "nan" else "",
                                                      d1_video_url=res['d1_diamond_video'] if res['d1_diamond_video'] != "nan" else "",
                                                      d1_image_file_url=res['d1_diamond_image'] if res['d1_diamond_image'] != "nan" else "",
                                                      d1_video_file_url=res['d1_diamond_video'] if res['d1_diamond_video'] != "nan" else "",
                                                      d1_availability=res['d1_availability'],
                                                      d1_diamond_quantity=res['d1_diamond_quantity'],
                                                      d1_diamond_type=diamond_type_name1,
                                                      d1_supplier_id=res['d1_supplier_id'],
                                                      d1_data_entry_point=res['d1_data_entry_point'],
                                                      d1_created_at=res['d1_created_at'],
                                                      d1_updated_at=res['d1_updated_at'],
                                                      d1_stock_number=res['d1_stock_number'],
                                                      d1_is_show=res['d1_is_show'],
                                                      d1_desc_comments=res['d1_desc_comments'],
                                                      d1_memo_status=res['d1_memo_status'],
                                                      d1_inscription=res['d1_inscription'],
                                                      d1_location=res['d1_location'],
                                                      d1_girdle=res['d1_girdle'],
                                                      d1_girdle_min=res['d1_girdle_min'],
                                                      d1_girdle_max=res['d1_girdle_max'],
                                                      d1_girdle_perc=res['d1_girdle_perc'],
                                                      d1_girdle_condition=res['d1_girdle_condition'],
                                                      d1_culet=res['d1_culet'],
                                                      d1_culet_condition=res['d1_culet_condition'],
                                                      d1_crown_angle=res['d1_crown_angle'],
                                                      d1_crown_height=res['d1_crown_height'],
                                                      d1_pavilion_depth=res['d1_pavilion_depth'],
                                                      d1_pavilion_angle=res['d1_pavilion_angle'],
                                                      d1_origin=res['d1_origin'],
                                                      d1_seller_name=res['d1_seller_name'],
                                                      d1_city=res['d1_city'],
                                                      d1_state=res['d1_state'],
                                                      d1_country=res['d1_country'],
                                                      d1_is_match_pair_separable=res['d1_is_match_pair_separable'],
                                                      d1_member_comments=res['d1_member_comments'],
                                                      d1_supplier_country=res['d1_supplier_country'],
                                                      d1_milky=res['d1_milky'],
                                                      d1_fluorescence_color=res['d1_fluorescence_color'],
                                                      d1_shade=res['d1_shade'],
                                                      d1_eye_clean=res['d1_eye_clean'],
                                                      d1_treatment=res['d1_treatment'],
                                                      d1_cert_comment=res['d1_cert_comment'],
                                                      d1_key_to_symbols=res['d1_key_to_symbols'],
                                                      d1_white_inclusion=res['d1_white_inclusion'],
                                                      d1_black_inclusion=res['d1_black_inclusion'],
                                                      d1_open_inclusion=res['d1_open_inclusion'],
                                                      d1_quick_ship=res['d1_quick_ship'],
                                                      d1_appointment=res['d1_appointment'],
                                                      d2_diamond_id=res['d2_diamond_id'],
                                                      d2_shape=res['d2_shape'],
                                                      d2_color=res['d2_color'],
                                                      d2_clarity=res['d2_clarity'],
                                                      d2_size=res['d2_carat_weight'],
                                                      d2_lab=res['d2_lab'],
                                                      d2_cut=res['d2_cut'],
                                                      d2_polish=res['d2_polish'],
                                                      d2_symmetry=res['d2_symmetry'],
                                                      d2_flour_intensity=res['d2_flour_intensity'],
                                                      d2_cert_num=res['d2_certificate_number'],
                                                      d2_measurement=res['d2_measurement'],
                                                      d2_meas_length=res['d2_length'],
                                                      d2_meas_width=res['d2_width'],
                                                      d2_meas_depth=res['d2_depth'],
                                                      d2_ratio=res['d2_ratio'],
                                                      d2_depth_percent=res['d2_dept_perc'],
                                                      d2_table_percent=res['d2_table_perc'],
                                                      d2_rapaport_price=res['d2_rapaport_price'],
                                                      d2_perc_off_rap=res['d2_perc_off_rap'],
                                                      d2_fancy_color=res['d2_fancy_color'],
                                                      d2_fancy_color_intensity=res['d2_fancy_color_intensity'],
                                                      d2_fancy_color_overtone=res['d2_fancy_color_overtone'],
                                                      d2_price_per_ct=res['d2_price_per_ct'],
                                                      d2_original_total_price=res['d2_original_total_price'],
                                                      d2_exchange_rate=res['d2_exchange_rate'],
                                                      d2_convert_price=res['d2_convert_price'],
                                                      d2_plus_markup_price_ct=res['d2_plus_markup_price_ct'],
                                                      d2_plus_markup_price=res['d2_plus_markup_price'],
                                                      d2_total_sales_price=res['d2_final_price'],
                                                      d2_total_sales_price_in_currency=res['d2_final_price'],
                                                      d2_price_per_ct_eur=res['d2_price_per_ct_eur'],
                                                      d2_plus_markup_price_ct_eur=res['d2_plus_markup_price_ct_eur'],
                                                      d2_original_total_price_eur=res['d2_original_total_price_eur'],
                                                      d2_final_price_eur=res['d2_final_price_eur'],
                                                      d2_exchange_rate_pound=res['d2_exchange_rate_pound'],
                                                      d2_price_per_ct_pound=res['d2_price_per_ct_pound'],
                                                      d2_plus_markup_price_ct_pound=res['d2_plus_markup_price_ct_pound'],
                                                      d2_original_total_price_pound=res['d2_original_total_price_pound'],
                                                      d2_final_price_pound=res['d2_final_price_pound'],
                                                      d2_certificate_file=res['d2_certificate_file']  if res['d2_certificate_file'] != "nan" else "",
                                                      d2_image_url=res['d2_diamond_image'] if res['d2_diamond_image'] != "nan" else "",
                                                      d2_video_url=res['d2_diamond_video'] if res['d2_diamond_video'] != "nan" else "",
                                                      d2_image_file_url=res['d2_diamond_image'] if res['d2_diamond_image'] != "nan" else "",
                                                      d2_video_file_url=res['d2_diamond_video'] if res['d2_diamond_video'] != "nan" else "",
                                                      d2_availability=res['d2_availability'],
                                                      d2_diamond_quantity=res['d2_diamond_quantity'],
                                                      d2_diamond_type=diamond_type_name2,
                                                      d2_supplier_id=res['d2_supplier_id'],
                                                      d2_data_entry_point=res['d2_data_entry_point'],
                                                      d2_created_at=res['d2_created_at'],
                                                      d2_updated_at=res['d2_updated_at'],
                                                      d2_stock_number=res['d2_stock_number'],
                                                      d2_is_show=res['d2_is_show'],
                                                      d2_desc_comments=res['d2_desc_comments'],
                                                      d2_memo_status=res['d2_memo_status'],
                                                      d2_inscription=res['d2_inscription'],
                                                      d2_location=res['d2_location'],
                                                      d2_girdle=res['d2_girdle'],
                                                      d2_girdle_min=res['d2_girdle_min'],
                                                      d2_girdle_max=res['d2_girdle_max'],
                                                      d2_girdle_perc=res['d2_girdle_perc'],
                                                      d2_girdle_condition=res['d2_girdle_condition'],
                                                      d2_culet=res['d2_culet'],
                                                      d2_culet_condition=res['d2_culet_condition'],
                                                      d2_crown_angle=res['d2_crown_angle'],
                                                      d2_crown_height=res['d2_crown_height'],
                                                      d2_pavilion_depth=res['d2_pavilion_depth'],
                                                      d2_pavilion_angle=res['d2_pavilion_angle'],
                                                      d2_origin=res['d2_origin'],
                                                      d2_seller_name=res['d2_seller_name'],
                                                      d2_city=res['d2_city'],
                                                      d2_state=res['d2_state'],
                                                      d2_country=res['d2_country'],
                                                      d2_is_match_pair_separable=res['d2_is_match_pair_separable'],
                                                      d2_member_comments=res['d2_member_comments'],
                                                      d2_supplier_country=res['d2_supplier_country'],
                                                      d2_milky=res['d2_milky'],
                                                      d2_fluorescence_color=res['d2_fluorescence_color'],
                                                      d2_shade=res['d2_shade'],
                                                      d2_eye_clean=res['d2_eye_clean'],
                                                      d2_treatment=res['d2_treatment'],
                                                      d2_cert_comment=res['d2_cert_comment'],
                                                      d2_key_to_symbols=res['d2_key_to_symbols'],
                                                      d2_white_inclusion=res['d2_white_inclusion'],
                                                      d2_black_inclusion=res['d2_black_inclusion'],
                                                      d2_open_inclusion=res['d2_open_inclusion'],
                                                      d2_quick_ship=res['d2_quick_ship'],
                                                      d2_appointment=res['d2_appointment'],
                                                      combined_price=res['combined_price'],
                                                      combined_price_pound=res['combined_price_pound'],
                                                      combined_price_cad=res['combined_price_cad'],
                                                      combined_QuickShip=res['combined_QuickShip'],
                                                      combined_SKU=res['combined_SKU'],
                                                      combined_Quantity=res['combined_Quantity'],
                                                      combined_Carat=res['combined_Carat'],
                                                      combined_Diamond_ID=res['combined_Diamond_ID'],
                                                      combined_Cut=res['combined_Cut'],
                                                      d1_diamond_feed=supplierObj1.vendor_name,
                                                      d2_diamond_feed=supplierObj2.vendor_name,
                                                      inserted_on = res['Inserted_on'],
                                                      final_discount_price=discount_price
                                                  ))
                return {"status": 200, 'diamond': output}
            except:
                return None
        else:
            return None
            
    #def resolve_live_sold_new_diamond(root, info, diamond_id=None, order_id=None, customer_name=None, date=None, dia_sku=None, gemstone_type=None, measurements=None, gemstone_cost=None, certificate_number=None, engraving=None, fm_setting_sku=None, setting_supplier_sku=None, product_name=None, head_price=None, shank_setting_price=None, setting_metal=None, setting_size=None, setting_tcw=None, side_diamond_tcw=None, tcw_cost=None, labor=None, total_price=None, supplier_paid=None, setting_supplier=None, net_cost_price=None, retail_price=None, where_is_setting=None, pay_date=None, check_number=None, notes_order_status=None, delivery_deadline=None, order_comment=None, lab_natural=None, sku_order_quantity=None, diamond_lab=None, discount_amount=None, tax_amount=None, billing_city=None, billing_country_id=None, billing_email=None, billing_firstname=None, billing_lastname=None, billing_postcode=None, billing_region=None, billing_street=None, billing_telephone=None, shipping_city=None, shipping_country_id=None, shipping_email=None, shipping_firstname=None, shipping_lastname=None, shipping_postcode=None, shipping_region=None, shipping_street=None, shipping_telephone=None, ships_by=None, order_status=None):
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


# Mutation logic


class soldDimondType(DjangoObjectType):
    class Meta:
        model = SoldDiamonds


class Solddiam(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        diamond_id = graphene.String(required=True)
        order_id = graphene.String(required=True)
        customer_name = graphene.String()
    # The class attributes define the response of the mutation
    # sold_diamond_list = graphene.Field(soldDimondType)
    status = graphene.String()
    code = graphene.String()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, diamond_id, order_id):
        # activeapiObj = """select * from `{0}api_details` where api_name = 'Sold diamond' and is_active = 1""".format(
        #     table_prefix)
        cursor = connections['primary'].cursor()
        # enable = cursor.execute(activeapiObj)
        enable = 1
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            try:
                status = ""
                code = ""
                message = ""
                diam_data = list(str(diamond_id).strip().replace(', ', ',').split(","))

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

                sold_diamond_count = SoldDiamonds.objects.using('primary').filter(diamond_id__in=diam_data,
                                                                                      is_sold=1).count()

                # fillter diamond for sold
                list_of_diamond_for_sold = set(diam_data) - set(update_only_is_sold)

                # fillter diamond to insert in sold table
                list_of_diamond_create = list_of_diamond_for_sold - set(update_only_is_not_sold)

                if len(diam_data) > 0:
                    # condition to check diamond alredy sold or need to sold
                    if len(diam_data) == 1 and sold_diamond_count == 1:
                        status = "success"
                        code = 200
                        message = "Diamond already sold"
                    elif len(diam_data) == sold_diamond_count and sold_diamond_count > 1:
                        status = "success"
                        code = 200
                        message = " {0} Diamonds are already sold".format(', '.join([str(elem) for elem in diam_data]))
                    elif len(diam_data) != sold_diamond_count and sold_diamond_count >= 0:
                        diamond_data_count_query = DiamondDetails_primary.objects.using('primary').filter(
                            diamond_id__in=diam_data,
                            diamond_quantity=1).count()

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
                                        diamond_id=data['diamondId'],
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
                                        certificate_number=data['certificate_number'],
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
                                        created_at=datetime.datetime.now(),
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
                                        order_id=str(orderId),
                                        customer_name=str(customer_name),
                                        dia_sku=str(dia_sku),
                                        gemstone_type=str(gemstone_type),
                                        engraving=str(engraving),
                                        fm_setting_sku=str(fm_setting_sku),
                                        setting_supplier_sku=str(setting_supplier_sku),
                                        product_name=str(product_name),
                                        head_price=str(head_price),
                                        shank_setting_price=str(shank_setting_price),
                                        setting_metal=str(setting_metal),
                                        setting_size=str(setting_size),
                                        setting_tcw=str(setting_tcw),
                                        side_diamond_tcw=str(side_diamond_tcw),
                                        tcw_cost=str(tcw_cost),
                                        labor=str(labor),
                                        total_price=str(total_price),
                                        supplier_paid=str(supplier_paid),
                                        setting_supplier=str(setting_supplier),
                                        net_cost_price=str(net_cost_price),
                                        retail_price=str(retail_price),
                                        where_is_setting=str(where_is_setting),
                                        pay_date=str(pay_date),
                                        check_number=str(check_number),
                                        notes_order_status=str(notes_order_status),
                                        delivery_deadline=str(delivery_deadline),
                                        order_comment=str(order_comment),
                                        lab_natural=str(lab_natural),
                                        sku_order_quantity=str(sku_order_quantity),
                                        diamond_lab=str(diamond_lab),
                                        discount_amount=str(discount_amount),
                                        tax_amount=str(tax_amount),
                                        billing_city=str(billing_city),
                                        billing_country_id=str(billing_country_id),
                                        billing_email=str(billing_email),
                                        billing_firstname=str(billing_firstname),
                                        billing_lastname=str(billing_lastname),
                                        billing_postcode=str(billing_postcode),
                                        billing_region=str(billing_region),
                                        billing_street=str(billing_street),
                                        billing_telephone=str(billing_telephone),
                                        shipping_city=str(shipping_city),
                                        shipping_country_id=str(shipping_country_id),
                                        shipping_email=str(shipping_email),
                                        shipping_firstname=str(shipping_firstname),
                                        shipping_lastname=str(shipping_lastname),
                                        shipping_postcode=str(shipping_postcode),
                                        shipping_region=str(shipping_region),
                                        shipping_street=str(shipping_street),
                                        shipping_telephone=str(shipping_telephone),
                                        ships_by=str(ships_by),
                                        order_status=str(order_status),
                                        is_sold=1)
                                for data in diamond_data_list]
                            msg = SoldDiamonds.objects.using('primary').bulk_create(objs)

                            # update diamond quantity in diamond data
                            for info in diamond_data_list:
                                DiamondDetails_primary.objects.using('primary').filter(
                                    diamond_id=info['diamond_id']).update(diamond_quantity=0, is_show=0)
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
            except Exception as ex:
                status = "Fail"
                code = 200
                message = "{0}".format(ex)

            return Solddiam(status=status, code=code, message=message)
        else:
            return None


class DiamondInput(graphene.InputObjectType):
    diamond_id = graphene.String()
    stock_number = graphene.String()
    shape = graphene.String()
    carat_weight = graphene.String()
    clarity = graphene.String()
    lab = graphene.String()
    cut = graphene.String()
    polish = graphene.String()
    symmetry = graphene.String()
    certificate_number = graphene.String()
    color = graphene.String()
    time_created = graphene.DateTime()


class Diamond_kt(graphene.InputObjectType):
    diamond_id = graphene.String()


class UpdateDiamond(graphene.Mutation):
    class Arguments:
        diamond_id = graphene.String(required=True)
        input = DiamondInput(required=True)

    diamond = graphene.Field(DimondType)

    @staticmethod
    def mutate(root, info, diamond_id, input=None):
        activeapiObj = """select * from `{0}api_details` where api_name = 'Update_diamond' and is_active = 1""".format(
            table_prefix)
        cursor = connections['primary'].cursor()
        enable = cursor.execute(activeapiObj)
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            diamond_instance = DiamondDetails.objects.using('primary').get(diamond_id=diamond_id)
            diamond_instance_new = DiamondDetails.objects.using('primary').filter(diamond_id=diamond_id)
            diamond_dic = list(diamond_instance_new.values())

            stock_number = None
            shape = None
            carat_weight = None
            clarity = None

            if input.stock_number == None:
                stock_number = diamond_dic[0]['stock_number']
            else:
                stock_number = input.stock_number

            if input.shape == None:
                shape = diamond_dic[0]['shape']
            else:
                shape = input.shape

            if input.carat_weight == None:
                carat_weight = diamond_dic[0]['carat_weight']
            else:
                carat_weight = input.carat_weight

            if input.clarity == None:
                clarity = diamond_dic[0]['clarity']
            else:
                clarity = input.clarity

            if input.lab == None:
                lab = diamond_dic[0]['lab']
            else:
                lab = input.lab

            if input.cut == None:
                cut = diamond_dic[0]['cut']
            else:
                if str(input.cut).strip() == "" or str(input.cut).strip().title() == 'Na':
                    cut = 'NA'
                else:
                    cut = str(input.cut).strip().title()

            if input.polish == None:
                polish = diamond_dic[0]['polish']
            else:
                polish = input.polish

            if input.symmetry == None:
                symmetry = diamond_dic[0]['symmetry']
            else:
                symmetry = input.symmetry

            if input.certificate_number == None:
                certificate_number = diamond_dic[0]['certificate_number']
            else:
                certificate_number = input.certificate_number

            if input.color == None:
                color = diamond_dic[0]['color']
            else:
                color = input.color

            if diamond_instance:
                DiamondDetails.objects.using('primary').filter(diamond_id=diamond_id).update(
                    stock_number=stock_number,
                    shape=str(shape).strip().title(),
                    carat_weight=carat_weight,
                    clarity=str(clarity).strip().upper(),
                    lab=str(lab).strip().upper(), cut=cut,
                    polish=str(polish).strip().title(),
                    symmetry=str(symmetry).strip().title(),
                    certificate_number=certificate_number,
                    color=str(color).strip().upper())

                diamond_instance = DiamondDetails.objects.using('primary').get(diamond_id=diamond_id)
                return UpdateDiamond(diamond=diamond_instance)
            return UpdateDiamond(diamond=None)
        else:
            return None


# usercreate
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


import graphql_jwt


class deletebyid(graphene.InputObjectType):
    diamondID = graphene.String()
    stockNumber = graphene.String()
    certificateNumber = graphene.String()


class DeleteDiamond(graphene.Mutation):
    class Arguments:
        diamond_id = graphene.List(deletebyid)

    diamond = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, diamond_id):
        activeapiObj = """select * from `{0}api_details` where api_name = 'Delete diamond' and is_active = 1""".format(
            table_prefix)
        cursor = connections['primary'].cursor()
        enable = cursor.execute(activeapiObj)
        if enable == 1:
            user = info.context.user
            if user.is_anonymous:
                raise Exception('Authentication Failure!')
            # else:
            diamond_response = []
            res = ''
            message = ''
            # diamond_count = DiamondDetails.objects.filter(diamond_id__in=diamond_id).count()
            # print(type(diamond_count))
            # if diamond_count > 0:
            for dia in diamond_id:
                # print(dia)
                diamond_instance = DiamondDetails.objects.using('primary').filter(diamond_id=dia['diamondID'])
                # print(diamond_instance)
                for di in diamond_instance:
                    if di:
                        DiamondDetails.objects.using('primary').filter(diamond_id=dia['diamondID']).delete()
                        diamond_response.append(diamond_instance)
                        # res = {message":"diamond deleted"}
                        message = "diamond deleted"

                    else:
                        message = "diamond not available"
            return DeleteDiamond(diamond=message, message=message)
        else:
            return None


class Mutation(graphene.ObjectType):
    sold_diamond = Solddiam.Field()
    update_diamond = UpdateDiamond.Field()
    create_user = CreateUser.Field()
    delete_diamond = DeleteDiamond.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
