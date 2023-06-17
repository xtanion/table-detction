import cv2
from PIL import Image
import pytesseract
import numpy as np
from scipy import ndimage
import math
import pandas as pd

# filename = 'samples/sample1.png'

def ocr_image(filename):
    img = np.array(Image.open(filename))
    img = ~img

    if len(img.shape)>=3:
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_grey = img 
    img = cv2.resize(img, None, fx=2, fy=2)

    img_edges = cv2.Canny(img_grey, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, np.pi / 180.0,
                            100, minLineLength=100, maxLineGap=5)

    angles = []

    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img_grey, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    median_angle = np.median(angles)
    img_rotated = ndimage.rotate(img, median_angle)
    # text extraction
    df = pytesseract.image_to_data(img_rotated, lang='eng', config='--psm 6',
                                   output_type=pytesseract.Output.DATAFRAME)

    df.to_csv('initial.csv', encoding='utf-8')
    filter_dataframe(df)
    return df


def filter_dataframe(df=None):
    if df is None:
        df = pd.read_csv('initial.csv')
    #  Remove values with confidence = -1
    locs = df.loc[df['conf'] == -1]
    df = df.drop(list(locs.index))

    # removing unnessesasy columns
    t = ['level', 'page_num', 'block_num', 'par_num', 'top', 'height']
    df = df.drop(t, axis=1)

    df['nearest'] = df.left.diff()
    csum = (df.nearest < df.width+20).cumsum()
    df['csum'] = csum
    df.to_csv('filtered.csv', encoding='utf-8')

    # df_final = df.groupby((df.left.diff() < df.width+20).cumsum(), as_index=False).sum()
    # df_final.to_csv('final.csv', encoding='utf-8')

    out_list = []
    in_list = []
    index = 0
    len_max = 0
    len_min = 0
    for i, rows in df.iterrows():
        len_max = len_min if len_min > len_max else len_max
        if rows['line_num'] == index:
            in_list.append(rows['text'])
        else:
            out_list.append(in_list)
            index += 1
            in_list = []
            in_list.append(rows['text'])
            len_min = 0
        len_min += 1
    
    buff = 3
    for i, row in enumerate(out_list):
        if len(row) < len_max-buff:
            out_list.pop(i)

    df_final = pd.DataFrame(out_list)
    df_final.to_csv('web/static/js/final.csv', encoding='utf-8')
    modify_html(df_final)


def modify_html(df):
    html_string = '''
    <html>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <link rel="stylesheet" href="{link}">
        <body>
            <h1>Table from Image/Pdf</h1>
            {table}
        </body>
    </html>.
    '''

    # OUTPUT AN HTML FILE
    table=df.to_html(na_rep='huh', classes='mystyle')
    with open('web/templates/table.html', 'w') as f:
        f.write(html_string.format(table=table, link="{{ url_for('static', filename='css/style.css') }}"))

filter_dataframe()