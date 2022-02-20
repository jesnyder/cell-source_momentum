from bs4 import BeautifulSoup
import datetime
import json
import lxml
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from serpapi import GoogleSearch
import re
import requests
import time


from a0001_admin import clean_dataframe
from a0001_admin import name_paths
from a0001_admin import retrieve_format
from a0001_admin import retrieve_list
from a0001_admin import retrieve_path
from a0001_admin import write_paths
from find_color import find_color


def targeted_word_count():
    """

    """
    print('began targeted_word_count')

    # List task numbers to complete
    tasks = [0]
    write_paths()
    if  0 in tasks: tasks = np.arange(1, 101, 1)
    if  1 in tasks: count_targeted_words()
    if  2 in tasks: annual_count_targeted()
    if  3 in tasks: per_annual_count_targeted()
    if  4 in tasks: plot_annual_count()

    print('completed targeted_word_count')


# completed programs

def plot_annual_count():
    """

    """
    # for each article type
    for name_article in retrieve_list('type_article'):

        for file in os.listdir(retrieve_path('term_compare')):

            path = os.path.join(retrieve_path('term_compare'), file)
            term_list = retrieve_list(path)
            print('term_list = ')
            print(term_list)

            # save dataframe with percent
            file_src = str(name_article + '_compare_terms_annual_count_df')
            compare_file_term = file.split('.')
            compare_file_term = compare_file_term[0]
            compare_file_term = str(compare_file_term + '_percent')
            path_src = os.path.join(retrieve_path(file_src), compare_file_term  + '.csv')
            df = clean_dataframe(pd.read_csv(path_src))

            df =  df[(df['cdf_total'] > 0)]
            df = clean_dataframe(df)
            print('df = ')
            print(df)

            # begin figure
            plt.close('all')
            figure, axes = plt.subplots()
            plot_row, plot_col, plot_num = 3, 1, 0
            plt.figure(figsize=(plot_col*retrieve_format('fig_wid'), plot_row*retrieve_format('fig_hei')))

            plot_num = plot_num +1
            plt.subplot(plot_row, plot_col, plot_num)
            for term in term_list:
                xx = list(df['years'])
                yy = list(df[term])
                color_index = term_list.index(term)
                colorMarker, colorEdge, colorTransparency = find_color(color_index)
                plt.scatter(xx,yy, color=colorMarker, edgecolor=colorEdge, alpha=colorTransparency, label=term)

            plt.title(name_article + ' Annual ' + str(int(sum(list(df['annual_total'])))))
            plt.xlabel('year')
            plt.ylabel('count')
            plt.yscale('log')
            plt.legend(bbox_to_anchor=(1, 0.9), loc ="upper left")


            plot_num = plot_num +1
            plt.subplot(plot_row, plot_col, plot_num)
            for term in term_list:
                term_cdf = str(term + '_cdf')
                xx = list(df['years'])
                yy = list(df[term_cdf])
                color_index = term_list.index(term)
                colorMarker, colorEdge, colorTransparency = find_color(color_index)
                plt.scatter(xx,yy, color=colorMarker, edgecolor=colorEdge, alpha=colorTransparency, label=term)

            plt.title(name_article + ' Cumulative ' + str(int(sum(list(df['annual_total'])))))
            plt.xlabel('year')
            plt.ylabel(term_cdf)
            plt.yscale('log')
            plt.legend(bbox_to_anchor=(1, 0.9), loc ="upper left")


            plot_num = plot_num +1
            plt.subplot(plot_row, plot_col, plot_num)
            for term in term_list:

                term_per = str(term + '_percent')
                xx = list(df['years'])
                yy = list(df[term_per])

                offsets = [0] * len(list(xx))

                if term_list.index(term) > 0:
                    i = term_list.index(term)
                    offsets = []
                    for k in range(len(list(df['years']))):
                        offset = 0
                        for j in range(i):
                            #term = term_list[j]
                            offset = offset + df.loc[k][term_list[j] + '_percent']
                        offsets.append(offset)

                assert len(offsets) == len(xx)
                assert len(offsets) == len(yy)

                plt.bar(xx, yy, width=1.0, bottom=offsets, align='center', label = term)


            plt.title(name_article + ' Percent' + str(int(sum(list(df['annual_total'])))))
            plt.xlabel('year')
            plt.ylabel(term_per)
            # plt.yscale('log')
            plt.legend(bbox_to_anchor=(1, 0.9), loc ="upper left")


            plot_count_annual = str(name_article + '_compare_terms_plot')
            plot_dst = os.path.join(retrieve_path(plot_count_annual), compare_file_term + '.png')
            plt.savefig(plot_dst, dpi = retrieve_format('plot_dpi'), edgecolor = 'w')
            print('saved plot: ' + plot_dst)
            plt.close('all')


def per_annual_count_targeted():
    """

    """

    # for each article type
    for name_article in retrieve_list('type_article'):
        print('article = ' + str(name_article))

        # all search terms together
        # for each term to compare
        for file in os.listdir(retrieve_path('term_compare')):

            path = os.path.join(retrieve_path('term_compare'), file)
            term_list = retrieve_list(path)
            #print('term_list = ')
            #print(term_list)

            # retrieve dataframe with counts
            compare_file_term = file.split('.')
            compare_file_term = compare_file_term[0]
            file_src = str(name_article + '_compare_terms_annual_count_df')
            path_src = os.path.join(retrieve_path(file_src), compare_file_term  + '.csv')
            df = clean_dataframe(pd.read_csv(path_src))

            # add a total column
            df['annual_total'] = [0]* len(list(df['years']))
            for i in range(len(list(df['years']))):

                df_annual = df[(df['years'] == df.loc[i,'years'])]

                count_year = 0
                for name in df_annual.columns:
                    if name in term_list:
                        count_year = count_year + list(df_annual[name])[0]
                df.loc[i,'annual_total'] = count_year
                #print('count_year = ' + str(count_year))


            for term in term_list:
                print('term = ' + term)

                term_per = str(term + '_percent')
                df[term_per] = [0]* len(list(df['years']))

                for i in range(len(list(df['years']))):

                    if df.loc[i,'annual_total'] == 0: continue

                    percent = df.loc[i,term]
                    total = df.loc[i,'annual_total']
                    df.loc[i,term_per] = percent/total

            # add a cdf column
            df['cdf_total'] = [0]* len(list(df['years']))
            for term in term_list:

                print('term = ' + term)
                term_cdf = str(term + '_cdf')
                df[term_cdf] = [0]* len(list(df['years']))

                for i in range(len(list(df['years']))):

                    df_annual = df[(df['years'] <= df.loc[i,'years'])]
                    df.loc[i,term_cdf] = sum(df_annual[term])
                    df.loc[i,'cdf_total'] = df.loc[i,'cdf_total'] + df.loc[i,term_cdf]

            print('df = ')
            print(df)

            # save dataframe with percent
            file_src = str(name_article + '_compare_terms_annual_count_df')
            compare_file_term = str(compare_file_term + '_percent')
            path_src = os.path.join(retrieve_path(file_src), compare_file_term  + '.csv')
            df.to_csv(path_src)


def annual_count_targeted():
    """

    """

    # list search terms
    search_terms = retrieve_list('term_search')

    # list compare terms
    compare_terms = os.path.join(retrieve_path('term_compare'))

    for file in os.listdir(compare_terms):

        path = os.path.join(retrieve_path('term_compare'), file)
        term_list = retrieve_list(path)
        print('term_list = ')
        print(term_list)

        for name_article in retrieve_list('type_article'):

            print('article = ' + str(name_article))

            file_dst = str(name_article + '_compare_terms_df')
            compare_file_term = file.split('.')
            compare_file_term = str(compare_file_term[0])
            path_dst = os.path.join(retrieve_path(file_dst), compare_file_term  + '.csv')
            df = clean_dataframe(pd.read_csv(path_dst))
            print('df = ')
            print(df)

            print('df.columns = ')
            print(df.columns)

            df_yearly_count = pd.DataFrame()

            try:
                years = np.arange(min(list(df['ref_year'])), max(list(df['ref_year'])), 1)
                df_yearly_count['years'] = years
            except:
                years = np.arange(min(list(df['years'])), max(list(df['years'])), 1)
                df_yearly_count['years'] = years

            #for term in search_terms:
            for compare_term in term_list:

                #print('compare_term = ' + str(compare_term))
                counts = []
                for year in years:

                    df_annual = df[(df['ref_year'] == year)]
                    target_list = list(df_annual[compare_term])
                    count = sum(list(df_annual[compare_term]))
                    counts.append(count)

                df_yearly_count[compare_term] = counts

            compare_file_term = file.split('.')
            compare_file_term = compare_file_term[0]
            file_dst = str(name_article + '_compare_terms_annual_count_df')
            path_dst = retrieve_path(file_dst)
            #print('path_dst = ' + str(path_dst))
            path_dst = os.path.join(path_dst, compare_file_term  + '.csv')
            #print('path_dst = ' + str(path_dst))
            df_yearly_count.to_csv(path_dst)


def count_targeted_words():
    """
    for all articles types
    count all words
    """

    # list compare terms
    compare_terms = os.path.join(retrieve_path('term_compare'))
    for file in os.listdir(compare_terms):

        path = os.path.join(retrieve_path('term_compare'), file)
        term_list = retrieve_list(path)
        print('term_list = ')
        print(term_list)

        # search each article type
        for name_article in retrieve_list('type_article'):

            try:
                print('article = ' + str(name_article))
                f = os.path.join(retrieve_path(name_article + '_aggregate_df'),  name_article + '_with_address' + '.csv' )
                print('f = ' + str(f))
                df = clean_dataframe(pd.read_csv(f))

            except:
                print('article = ' + str(name_article))
                f = os.path.join(retrieve_path(name_article + '_aggregate_df'),  name_article + '.csv' )
                print('f = ' + str(f))
                df = clean_dataframe(pd.read_csv(f))


            for compare_term in term_list:
                df[compare_term] = [0] * len(list(df.iloc[:,0]))

            col_name = df.columns

            for i in range(len(list(df.iloc[:,0]))):

                str_all = ''
                for name in col_name:
                    str_all = str_all + str(df.loc[i,name])
                    str_all = str_all + ' '

                # print(str_all)
                for compare_term in term_list:

                    if str(compare_term) in str(str_all):

                        df.loc[i,compare_term] = 1
                        #print('found :' + compare_term)

            compare_file_term = file.split('.')
            compare_file_term = str(compare_file_term[0])
            file_dst = str(name_article + '_compare_terms_df')
            path_dst = os.path.join(retrieve_path(file_dst), compare_file_term  + '.csv')
            df.to_csv(path_dst)


if __name__ == "__main__":
    main()