# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Ingrammicro
# All rights reserved.
from connect.client import R


def __process_line(product, item):
    return [
        product['owner']['id'],
        product['owner']['name'],
        product['id'],
        product['name'],
        product['status'],
        item['id'],
        item['mpn'],
        item['status'],
        item['name'],
        item['description'],
        item['type'],
        item['unit']['id'] if 'unit' in item else '',
        item['period'] if 'period' in item else '',
        item['precision'] if 'precision' in item else '',
        f"{item['commitment']['count']} {item['commitment']['multiplier']}"
        if 'commitment' in item else '',
        item['dynamic'] if 'dynamic' in item else '',
    ]

def generate(
    client=None,
    input_data=None,
    progress_callback=None,
    renderer_type='xlsx',
    extra_context_callback=None,
):
    """
    Extracts data from Connect using the ConnectClient instance
    and input data provided as arguments, applies
    required transformations (if any) and returns the data rendered
    by the given renderer on the arguments list.
    Some renderers may require extra context data to generate the report
    output, for example in the case of the Jinja2 renderer...

    :param client: An instance of the CloudBlue Connect
                    client.
    :type client: cnct.ConnectClient
    :param input_data: Input data used to calculate the
                        resulting dataset.
    :type input_data: dict
    :param progress_callback: A function that accepts t
                                argument of type int that must
                                be invoked to notify the progress
                                of the report generation.
    :type progress_callback: func
    :param renderer_type: Renderer required for generating report
                            output.
    :type renderer_type: string
    :param extra_context_callback: Extra content required by some
                            renderers.
    :type extra_context_callback: func
    """

    products = client.products.filter(
        R().visibility.listing.eq(True) or R().visibility.syndication.eq(True),
    ).all()
    total = products.count()

    counter = 0
    if total == 0:
        yield 'EMPTY PRODUCTS'

    for product in products:
        items = client.products[product['id']].items.all()

        for item in items:
            yield __process_line(product, item)

        counter += 1
        progress_callback(counter, total)
