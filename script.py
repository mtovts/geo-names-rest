import json
import logging
from datetime import datetime
from typing import Dict

import pandas as pd
from django.core.paginator import Paginator
from flask import Flask, jsonify, abort, make_response, request
from pytz import timezone
from unidecode import unidecode

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

names = [
    'geonameid', 'name', 'asciiname',
    'alternatenames', 'latitude', 'longitude',
    'feature class', 'feature code', 'country code',
    'cc2', 'admin1 code', 'admin2 code',
    'admin3 code', 'admin4 code', 'population',
    'elevation', 'dem', 'timezone',
    'modification date'
]

geo_data = pd.read_csv('RU.txt',
                       sep='\t',
                       header=None,
                       names=names,
                       dtype=object,  # fixme
                       )
geo_data.fillna('', inplace=True)


def get_city_info_by(value, by: str, sort_by: str = None) -> Dict:
    """
    :param value: value for search
    :param by: name of parameter
    :param sort_by: sorting by
    :return: Information about city
    """
    if sort_by:
        info = geo_data[geo_data[by] == value].sort_values(
            by=sort_by).iloc[0].to_dict()
    else:
        info = geo_data[geo_data[by] == value].iloc[0].to_dict()

    # delete unfilled values
    info_filled = {key: val for key, val in info.items() if val}
    return info_filled


def get_tz_difference(tz1_name: str, tz2_name: str) -> float:
    """
    :param tz1_name: Name of 1-st timezone
    :param tz2_name: Name of 2-nd timezone
    :return: Difference between timezones in hours
    """
    tz1 = timezone(tz1_name)
    tz2 = timezone(tz2_name)

    utc_offset1 = tz1.localize(datetime.now()).utcoffset().seconds
    utc_offset2 = tz2.localize(datetime.now()).utcoffset().seconds

    if (utc_offset1 >= 0 and utc_offset2 >= 0) or (utc_offset1 < 0 and utc_offset2 < 0):
        tz_diff = abs(utc_offset1 - utc_offset2)
    else:
        tz_diff = abs(utc_offset1) + abs(utc_offset2)
    tz_diff /= 60 * 60

    return tz_diff


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/info', methods=['GET'])
def get_city_info():
    geonameid = request.args.get('geonameid')

    try:
        city_info = get_city_info_by(value=geonameid, by='geonameid')
    except KeyError:
        logger.error(f'Error sending information by geonameid={geonameid}')
        abort(404)

    logger.info(f'Information was sent by geonameid={geonameid}.')
    return jsonify(city_info)


@app.route('/page', methods=['GET'])
@app.route('/page/<int:page>', methods=['GET'])
def get_page(page=1):
    cities_per_page = request.args.get('per_page')

    paginator = Paginator(object_list=geo_data, per_page=cities_per_page)
    cities_page = paginator.page(number=page).object_list
    cities_dict = json.loads(s=cities_page.to_json())

    # delete unfilled values
    cities_dict = {key: {key2: val2 for key2, val2 in val.items() if val2} for key, val in
                   cities_dict.items()}
    cities_dict = {key: val for key, val in cities_dict.items() if val}

    logger.info(f'Page {page} with {cities_per_page} cities per page was sent.')
    return jsonify(cities_dict)


@app.route('/cities', methods=['GET'])
def get_two_cities():
    city_1_ru = request.args.get('city1')
    city_2_ru = request.args.get('city2')

    # trantsliteration into english
    city_1 = unidecode(city_1_ru)
    city_2 = unidecode(city_2_ru)

    try:
        city_1_info = get_city_info_by(value=city_1, by='name', sort_by='population')
        city_2_info = get_city_info_by(value=city_2, by='name', sort_by='population')

        tz_diff = get_tz_difference(city_1_info['timezone'], city_2_info['timezone'])
    except LookupError:
        logger.error(
            f"Error sending information about cities '{city_1_ru}' and '{city_2_ru}'")
        abort(404)

    additional_info = {
        'northernmost_geonameid': city_1_info['geonameid'] if city_1_info['latitude'] >= \
                                                              city_2_info['latitude'] else
        city_2_info['geonameid'],
        'same_tz': not tz_diff,
        'tz_difference': tz_diff
    }

    logger.info(f"Information about cities '{city_1_ru}' and '{city_2_ru}' was sent.")
    return jsonify(city_1_info, city_2_info, additional_info)


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=8000,
            debug=False
            )
