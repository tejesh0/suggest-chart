import gramex
import operator
import numpy as np
import pandas as pd
from functools import reduce  # forward compatibility for Python 3


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


type_recognizer = {
    'numerical': {
        'categorical': 'num_and_cat',
        'time_series': 'several_series'
    },
    'categorical': {
        'numerical': 'num_and_cat',
    },
    'num_and_cat': {
        'time_series': 'time_series',
    },
    'time_series': {
        'time_series': 'several_series'
    }
}

chart_possible = {
    'coltype_combination':
    {
        'num_and_cat': {
            'one_num_one_cat': {
                'one_obs_per_group': ['lollipop', 'bar_plot', 'circular_bar_plot', 'treemap', 'circlepack'],
                'several_obs_per_group': ['box_plot', 'violin_plot', 'circular_bar_plot', 'treemap', 'circlepack']
            },
            'one_cat_several_num': { # NOTE: Could not understand rationale behind no_order, a_num_is_ordered in data-to-viz.com
                'one_value_per_group': ['multi_line', 'parallel_plot', 'stacked_bar_plot', 'grouped_bar_plot'],
                'multiple_values_per_group': ['grouped_scatterplot']
            },
            'several_cat_one_num': {
                'subgroup': {

                },
                'nested': {

                },
                'adjacency': {

                }
            }
        },
        'numerical': {
            'one_num': ['histogram', 'density_plot'],
            'two_num': {
                'not_ordered': {
                    'few_points': ['facet_box_plot', 'scatterplot'],
                    'many_points': ['facet_violin_plot', 'facet_densityplot', ]
                },
                'ordered': ['line_chart', 'area_chart', 'connected_scatterplot']
            },
            'three_num': {
                'not_ordered': [],
                'ordered': []
            },
            'several_num': {
                'not_ordered': [],
                'ordered': []
            }
        },
        'categorical': {
            'one_cat': ['barplot', 'lollipop', 'donut', 'treemap', 'circlepack'],
            'several_cat': {

            }
        }
    }
}


def initiate(handler):
    df = gramex.cache.open('flags.xlsx')
    print(df.head())

    # BFS but will go further down only if certain condition is possible
    # So, a node is pushed to the BFS
    queue = []
    charts_recommended = []
    visited_nodes_path = []

    for key in chart_possible:
        queue.append(key)

    while len(queue) > 0:
        if type(getFromDict(chart_possible, visited_nodes_path)) == 'list':   # headsup: you are at leaf node
            charts_recommended.append(getFromDict(chart_possible, visited_nodes_path))
        else:
            visited_node = queue.pop(0)
            next_node = exec(visited_node)
            queue.append(next_node)
            visited_nodes_path.append(next_node)


def coltype_combination(df):
    """returns combination for column types
        https://stackoverflow.com/a/29803297

    Arguments:
        fields_names {list} -- Field names and
        type_map {dict} -- dictionary of field names and its corresponding dtypes

    Returns:
        [string] -- [categorical, numerical and num_and_cat]
    """
    number_df = df.select_dtypes(exclude=['number'])
    if len(number_df.columns) == 0:
        return 'categorical'
    elif len(number_df.columns) == len(df.columns):
        return 'numerical'
    else:
        return 'num_and_cat'


def num_and_cat(df):
    return 'one_num_one_cat'


def one_num_one_cat(df):

    return 'one_obs_per_group' if one_obs_per_group(df) else 'several_obs_per_group'


def one_obs_per_group(df):
    return one_value_per_group(df)


def one_cat_several_num(df):

    return 'one_value_per_group' if one_value_per_group(df) else 'multiple_values_per_group'


def one_value_per_group(df):
    one_cat = df.select_dtypes(exclude=['number'])[0]
    return df[one_cat].unique().count() == df[one_cat].count()


def multiple_values_per_group(df, one_cat):
    return not one_value_per_group


# A dataframe is ORDERED if one column is ordered
def ordered(df):
    """check if any column in dataframe is ordered

    # Alternate solution?: https://stackoverflow.com/a/17705498

    Arguments:
        df {dataframe} -- Expects a dataframe which contains **only numerical columns**

    Returns:
        [boolean] -- [description]
    """
    return any((np.diff(df[colname]) > 0).all() for colname in df.columns)


def not_ordered(df):
    return not ordered(df)


def subgroup(df):

    return ''


def nested(df):

    return ''


def group_type(categorical_cols):
    """if multiple categorical cols chosen, this function is called.

    Arguments:
        categorical_cols {[type]} -- [description]
    """
    return "t1"


def group_item_type(categorical_col):
    """[summary]

    Arguments:
        categorical_col {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    return "h11"
